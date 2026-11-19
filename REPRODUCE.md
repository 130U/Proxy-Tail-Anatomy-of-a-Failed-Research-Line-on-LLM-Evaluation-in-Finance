# Reproducing the Results

Every result can be recomputed from the saved model outputs. Recomputation calls no model, needs no
API key and trains nothing. Calling the models again will not reproduce the outputs byte for byte.

Run commands from the repository root. The analysis was run with Python 3.12.14; the numerical
packages and versions are in [`requirements-analysis.txt`](requirements-analysis.txt) (numpy, scipy,
matplotlib). Some stages need more; each stage's own notes say what.

## Where Each Stage's Instructions Are

| Stage | Instructions |
|---|---|
| A. Certifiable FinLM | [research/REPRODUCE.md](research/REPRODUCE.md); runner `python research/reproduce.py` |
| B. Proxy tail | [research/tail_screening/REPRODUCE_CURRENT.md](research/tail_screening/REPRODUCE_CURRENT.md) |
| C. Absolute scoring | [research/absolute_scoring/REPRODUCE.md](research/absolute_scoring/REPRODUCE.md) |
| D. T3 | [research/t3_combination/execution_notes.md](research/t3_combination/execution_notes.md) |
| E. T1–T1g | Each `research/t1*/` folder; T1g: [research/t1g_consequence/RUN.md](research/t1g_consequence/RUN.md) |

## Stage B Quick Start

```sh
python research/tail_screening/review_measurements.py
python research/tail_screening/analyze_agent_methods.py --method all
python research/tail_screening/analyze_agent_methods_validation.py
```

The first command re-checks the raw outputs against the saved results with an independent
implementation and changes nothing. The other two rewrite the corresponding JSON, PNG and PDF figures
and per-item reports; run times vary, but the statistics and decisions should be identical. To check
the paired batches:

```sh
python research/tail_screening/prepare_agent_methods.py --verify-batches
```

The historical data-preparation script accepts
`--source source_materials/130U-FinLLM/data/raw/candidates/sentfin/SEntFiN.csv` and refuses to
overwrite existing samples or aggregates.

## Stage A Source Audit

```sh
python research/data/fomc_source_audit.py --self-test
python research/data/fomc_source_audit.py --source-root source_materials/source_audit
```

The second command rewrites the derived audit JSON (its time fields will change).

## Known Limits

- **Paths.** Some T1-series scripts default to sibling working directories that existed on the
  student's machine (for example `proxy-tail-t1a/`). Pass the documented `--t1-dir`-style arguments,
  or point them at the matching folder under `research/`. Run records show local paths as
  placeholders such as `<workspace>`.
- **Hashes.** Several records pin other files by SHA-256 (protocols, proof notes, prompts). The
  hashes refer to the original-language files; run those checks on commit
  [`e4b7bc0`](https://github.com/130U/RESEARCH-Proxy-Tail-Anatomy-of-a-Failed-Research-Line-on-LLM-Evaluation-in-Finance/tree/e4b7bc061976bcdd2f48c437172b034351ac7e77).
- **Data.** FinQA and TAT-QA are downloaded by `research/t1_rounding/download_inputs.py` and the T1g
  scripts; they are not stored in the repository.
- **Reports.** The Markdown files are the source of the stage reports.
