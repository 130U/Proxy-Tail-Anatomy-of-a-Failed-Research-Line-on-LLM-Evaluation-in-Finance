# Colab kernel installation and training entry fix

Issue record: [GitHub #1](https://github.com/130U/130U-FinLLM/issues/1). The user's screenshots from 2026-10-09 show that Tesla T4 was selected in 02a, but the training cell raised `ModuleNotFoundError` when importing `finllm.runtime`. In the same set of screenshots, 01a shows a CPU runtime; its disconnect notice alone cannot prove an out-of-memory condition or establish the cause of the disconnect.

Update 2026-10-11: T4 screenshots from the user show that 02a completed 61 updates and 999,424 tokens and was backed up to Drive. The later 02b log and backup output show 300 steps in total, 4,914,941 effective tokens, and a passing check of the final snapshot. The earlier import failure no longer occurred in the user's runs. The actual reported numbers and the limits of the evidence are in the [T4 training record](T4_PILOT.md). This is run evidence provided by the user; the cloud checkpoints were not read independently.

## Root cause and fix

The project uses a `src` layout. The notebook's Python kernel starts before `pip install -e .` runs. The `.pth` file created by an editable install is read by new Python processes started later; a kernel that is already running does not re-read it automatically. So an earlier success of `python -m finllm environment` did not prove that a later in-kernel `from finllm.runtime import ...` would succeed.

The shared install cell now explicitly activates the current repository's `src`, refreshes only the cached modules that belong to `finllm`, and separately checks the actual import paths in the current kernel and in a new Python process, as well as the checkpoint-resume interface. Torch is not reloaded.

When the old project installation metadata still restricts `tokenizers<0.23`, upgrading tokenizers first and updating the project afterwards creates an intermediate dependency conflict. The editable project and a compatible tokenizer are now installed in the same pip transaction, constrained to the full Torch version currently installed. Afterwards the project's base dependencies and the tokenizer constraint of Transformers are checked.

Two problems in the training flow were fixed at the same time:

- Re-running after the training budget has been reached reuses the original result read-only, keeping the checkpoint, the backups and the original throughput / memory records. When resuming only from a checkpoint with the original summary missing, no new throughput or memory figures are invented.
- After a training failure, the final backup cell of 02a stops explicitly, so it does not go on to show completion. During normal training, the update step and loss are shown at each update.

## Verification method and limits

The new `tests/test_notebook_execution.py` uses a real, persistent Jupyter kernel: the kernel is started first, and then the editable install is actually run. The test reproduces the old import failure and executes the generated notebook's install, 01a configuration restore, 02a restore, configuration, training, backup and repeat-run cells. A separate Python environment and kernel then restore the data and checkpoint in a different directory, verify continuation from 2 updates to 3 updates, and check that the checkpoint hashes in the persistent directory and in the working directory match.

In the test, external Git and Drive are local directories, dependency installation reuses existing libraries offline, and the GPU budget is explicitly replaced by a tiny CPU test configuration. Python package installation, kernel imports, model parameter updates and checkpoint restore are actually executed. This verifies the notebook execution chain; it is not acceptance of the cloud Google Drive service or of T4 performance. Earlier tests only checked subprocesses and syntax and did not cover this difference in kernel lifecycle.

The full local test suite passed (120 tests, 73.26 seconds); format / syntax checks of the 9 notebooks passed; `pip check` passed. The machine record is [colab_kernel_fix.json](../reports/colab_kernel_fix.json). CI runs the same full test suite under Python 3.12 and 3.13; for its results, the Actions run of this fix commit is authoritative.

## How the user continues

If a `seed_v1` Drive backup from 01a already exists, reopen [the latest 02a](https://colab.research.google.com/github/130U/130U-FinLLM/blob/main/notebooks/02a_seed_pilot.ipynb) directly and save a copy. Keep T4 and `SEED_VERSION = "seed_v1"`, and run in order from the first cell. The install cell should show "Current notebook kernel import check passed" and "Fresh Python process import check passed"; the later cells restore the existing data, vocabulary and progress.

There is no need to delete files in Drive or to redo 01a. An old-version notebook that was already opened or saved in Drive does not update its cell code automatically; use the new entry above. If it is run again after training has completed, it returns `resumed_no_training: true`; the original `run_summary.json` keeps the measurements from the run that actually trained.
