# Next step: review target assets and stance labels

**Current handoff:** the user has delivered the 2000-row CSV and explicitly confirmed 1993 headline labels, with 7 pending investigation. The [intake notes](POST_DOMAIN_NEXT.md) record the verification and the gates before SFT. The zero human confirmations mentioned below are what was recorded at first generation.

Later update, 2026-10-30: at the user's request, an AI first draft of 2000 distinct headlines, including the original 200, and an offline review workspace were generated. Each row has a suggested stance, evidence from the text, a Chinese rationale, historical asset candidates and a priority; there are 20 batches of 100 rows each. All human confirmations are left blank. For the preferred workspace and its keyboard shortcuts, see [Review workspace](REVIEW_WORKSPACE.md); for counts and the limits of the evidence, see the [2000-row preparation record](../reports/task_review_2000_20261030.json). The actual material is in the local `runs/review_packages/review_2000_20261030/`; the original 200-row files are unchanged. The export notes for the first 200 rows are kept below.

2026-10-30. The first batch of 200 review rows was generated on this machine, keeping the original AI first-pass judgments and rationales and adding historical symbol candidates from the original author's entity table. The actual material is stored in the ignored directory `runs/review_packages/review_200_20261030/`; no news text or per-row labels were committed to GitHub.

Local files:

- `review_200_to_complete.csv`: open in Excel or another spreadsheet tool that supports UTF-8 and review row by row.
- `READ_ME_FIRST.md`: review rules and grouping requirements.
- `manifest.json`: input and output hashes, counts and limits of the evidence at generation time.

For the summary, see the [preparation record](../reports/task_review_readiness_20261030.json). Of the 200 rows, 116 match exactly one **source symbol candidate**, 2 have several source symbol candidates, and 82 have no match. These are not 116 verified current security identifiers; the original entity table covers historical names and many kinds of targets, which cannot all be treated as US stocks.

## Fields to fill in

| Field | Human action |
|---|---|
| `asset_identifier` | Fill in after checking the asset identity, market and symbol of the specified target; do not copy the historical source symbol directly |
| `human_stance` | Read the investment direction the text expresses toward the specified target and fill in `bullish`, `bearish`, `neutral` or `exclude` |
| `human_reviewed` | Change to `true` only after actually reviewing the row |
| `notes` | Record exclusions, conditional judgments, the basis of the asset mapping, or remaining ambiguity |
| `event_group_id` | Give news items that certainly belong to the same event a common group number; if unknown, leave empty for investigation |

`source_sentiment` is the author's entity sentiment label; `proposed_stance` and `ai_rationale` are AI drafts. All are kept for comparison and cannot be renamed into human ground truth. `source_symbol_candidates` and `source_symbol_match` are only the results of an exact alias lookup; current listing status, exchange and security identity have not been verified.

At first generation, both the human-confirmed stances and the verified asset identifiers were **0**; the current actual numbers will be counted after the workspace export is taken in. This package created no formal SFT data, DPO preference pairs or sealed test set. The 200 rows are a first sample for rule review, not a label corpus of the originally planned size; review by one person is not a two-person independent agreement check.

A text that only reports a price or earnings change that has already happened does not automatically mean bullish or bearish. Items that only raise a question without a conclusion, regulators, vague targets or unsupported assets need review or exclusion. Multi-target news should be judged separately for each target, and conditional views should keep their conditions.

## Generation and retention

Run in the repository root, with all existing material already in place:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/build_task_review_package.py --report reports/task_review_readiness_20261030.json
```

The script reads only local files and verifies the hashes and per-row identity of the fixed source, the original review table and the AI first-pass file. It does not download data, look up current stock symbols or approve labels. By default it needs:

- `data/raw/sentfin_review_v1/review_200.csv`
- `data/raw/sentfin_review_v1/review_200_ai_proposals.csv` and its two manifests
- `data/raw/candidates/sentfin/entity_list_comprehensive.csv`

After generation you can continue editing the CSV directly. Re-running on an unchanged complete package only reuses it and leaves the files unchanged; if there are manual edits or incomplete files, it stops explicitly and does not overwrite the material. For another initial draft, specify a new `--output` directory and keep the reviewed files.

Import and data splitting after the review must still verify labels, asset mapping, source permissions and duplicate relations. News from the same source, multiple targets of the same text, lexical near-duplicates and the same event must be grouped jointly before splitting into train/dev/calibration/test. The current `source_headline_id` and `text_group_id` are only draft groupings and cannot replace event and semantic duplicate review.
