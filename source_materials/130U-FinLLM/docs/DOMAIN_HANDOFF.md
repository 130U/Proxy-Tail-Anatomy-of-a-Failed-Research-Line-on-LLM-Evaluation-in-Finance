# 03a | From the 1220-step general model to financial-domain training

2026-10-30. Entry point: [03a_domain_pretrain.ipynb](https://colab.research.google.com/github/130U/130U-FinLLM/blob/main/notebooks/03a_domain_pretrain.ipynb).

**Latest acceptance: this stage is complete.** The user later provided the full Colab output: the domain stage ran 74 steps / 1,211,960 effective tokens, the financial validation loss was 3.2375, the general retention subset went 3.9842→4.0574, and the final backup output was `verified: true`. See the [domain record](../reports/colab_t4_domain_20261030.json). The entry design and the recovery notes are kept below. The current next step is to [take in the human-review progress](POST_DOMAIN_NEXT.md); there is no need to redo this stage.

The completed 02d output is saved in [the user's historical commit](https://github.com/130U/130U-FinLLM/blob/e14b85e5660c4bce175341ee4d9da2e3984a12b5/notebooks/02d_expanded_continue.ipynb), and the read-back record is in the [1220-step report](../reports/colab_t4_expanded_continuation_20261030.json). The expansion stage processed 19,988,195 effective tokens in total; including the seed path, the total is 24,903,136. This is not an independent corpus size. The next stage first reads the Drive files back in Colab and verifies the parent checkpoint; the outputs saved on GitHub do not replace this check.

## Run

1. Open 03a, keep T4, run in order from the first cell, and complete the Drive mount. There is no need to redo 01b / 02c / 02d.
2. The preparation cell restores the frozen data and the 8K vocabulary, verifies the complete snapshot manifest, the 1220-step parent checkpoint, the matching measured report and its "after" report on the original seed retention set, and freezes the parent checkpoint. The `parent_audit` output should show the hashes, step count and tokens actually read.
3. Measure the "before" loss on the original seed general retention subset. The first run transfers only the model weights, sets up a new AdamW optimizer and learning-rate schedule for the financial stage, and counts stage steps from 0.
4. Run a 1-step check, then continue to 74 steps in total for this financial stage. A checkpoint is saved and synced every 10 steps; within the new stage, resume restores the optimizer, scaler, random state and data position.
5. Measure the "after" loss on the same original seed retention subset and run the last cell to verify the backup. Keep the financial validation loss, this stage's report, `parent_audit`, and the final `verified: true` output.

The user has posted the T4, Drive mount, parent-checkpoint SHA, training and final backup outputs; these form the evidence of this cloud execution. The agent did not independently download the Drive checkpoints. The first preparation cell carries out the actual cloud verification; if any check fails, keep the output and the existing artifacts.

## Budget for this stage

| Item | Amount |
|---|---:|
| Existing 80/20 finance / general mixed shards | 1,215,545 tokens |
| of which finance-source positions | 972,436 |
| of which general-source positions | 243,109 |
| Financial validation shard | 50,999 tokens |
| batch / gradient accumulation / sequence length | 4 / 8 / 512 |
| Single-step check and cumulative stop target | 1 / 74 |
| Nominal input positions for 74 full-length steps | 1,212,416 |
| Learning rate / warmup / schedule span | 1e-4 / 5 steps / 74 steps |

This is one short no-replay pass over existing data. Actual effective tokens, padding, duration and throughput are those in the new report. A pure arithmetic estimate from the previous 3221 tokens/second gives about 6 minutes of training; cloud verification, measurement and backup take additional time. The mixed shards are a reordering of the source content and cannot be counted again as new independent corpus.

The originally planned 100M general / 25M finance is a longer cumulative processing budget and has not been completed. This stage is explicitly reduced to about 1.21M positions so that the financial stage can be accepted first; extending it later or adding material requires a separate budget decision. Reusing the existing mixed pool for 25M of processing would be about 20.57 passes; that replay would have to be reported explicitly and cannot be called 25M of independent financial corpus. 03a does not extend this way automatically.

The one-pass data limit is enforced both in the preparation check and before every micro-batch. Even if steps skipped by AMP consume data, the run does not quietly enter a second pass to reach 74 successful updates; when the data run out it stops and keeps the last complete checkpoint and the original artifacts.

## Files and recovery

The Drive project root is `MyDrive/130U-FinLLM`:

| Content | Relative path |
|---|---|
| Original 1220-step expansion artifacts | `expansions/expansion_v1/run` |
| Parent checkpoint frozen for this financial stage, and its source reports | `domains/domain_v1/parent` |
| Before/after retention-set measurements for this financial stage | `domains/domain_v1/retention` |
| Measured reports for each run of this financial stage | `domains/domain_v1/report_archive` |
| Final complete snapshot of this financial stage | `domains/domain_v1/run` |
| Automatic checkpoints of this financial stage | `live_checkpoints/domain_v1` |

The local hot training directory is `/content/130U-FinLLM/runs/domain_v1`. The original seed, the 610-step archive and the 1220-step model are kept. The first cross-stage run transfers only the weights, so the parent checkpoint's original PyTorch version may differ from the current version of the new stage; both identities are recorded. Later exact resumes within the same `domain_v1` are bound to the data, vocabulary, model, training semantics and the new runtime identity.

After a disconnect, first confirm the state of the original training, then resume in order from the first cell of 03a. When 74 steps are already complete, the matching original measured report is reused and not rewritten as zero-second throughput; a failed training or measurement cannot show a complete backup. If the environment or input identity does not match, keep the error message and do not bypass the check.

## Material for task post-training

The review material has been expanded to 2000 rows. The user delivered the CSV and explicitly confirmed 1993 headline labels; another 7 are pending investigation. See the [review record](../reports/human_headline_review_20261030.json). Real SFT, later DPO preference review, calibration and sealed testing can begin only after asset mapping, deduplication / event grouping and partitioning have passed. Language-modeling loss cannot be taken as bullish/bearish accuracy on assets.

Runnable notebooks in the repository are kept with no stored outputs. To keep executed content, save it to a personal Drive copy; the full 02d evidence saved this time remains in the historical commit above and in the local archive.

## Engineering verification

The full local suite of 274 tests passed (557.43 seconds); format / syntax / no-output checks of the 14 notebooks and the dependency check passed. This includes 03a execution in two real isolated Jupyter kernels, the optimizer reset for the new domain, a numerical comparison with dropout between direct and segmented continued training, recovery from failure and interruption, and preservation of the original measurements after completion. A source-linkage check was also run on the real local 8K shards. See the [engineering record](../reports/domain_handoff_checks_20261030.json). These local substitute tests are not the same as actual verification on the user's Drive / T4.
