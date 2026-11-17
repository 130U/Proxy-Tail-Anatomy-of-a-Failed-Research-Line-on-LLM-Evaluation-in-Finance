# After 03a: taking in the real review progress

2026-10-30. The user provided the full 03a output: `domain_v1` completed 74 updates and 1,211,960 effective tokens, the financial validation loss was 3.2375, and the final backup of 7 files / 615,896,468 bytes reported `verified: true`. The loss on the original seed general retention subset went 3.9842→4.0574, an increase of 0.07317. See the [domain training record](../reports/colab_t4_domain_20261030.json). This is cloud evidence posted by the user; the agent did not independently download the Drive weights.

Latest fast path: the [04a entity stance SFT trial](ENTITY_SFT_PILOT.md) is ready. It can use the 1008 confirmed headlines, with the literal entity in the headline as the target, for private exploration, without first claiming that the entities are verified securities. It has not yet been run in the user's Colab; real security mapping and the final task evaluation are still to be done.

This stage is complete and 03a does not need to be retrained. A later probe re-run showed 74→74 and `resumed_no_training: true`; that is a read-only resume after completion, not another 74 training steps. The original 100M general / 25M finance budget has not been completed; what was accepted here is a bounded small domain experiment.

## Current progress: headline review table received

The user has delivered the 2000-row CSV and, in this conversation, explicitly confirmed that every row except 7 pending ones was reviewed one by one. All IDs, headlines and targets were independently checked against the original frozen data and match. The 1,993 confirmed rows comprise 426 bullish, 234 bearish, 1219 neutral and 114 excluded; another 7 are pending. Five records where the judgment from the headline differs from the article context are kept. The confirmation comes from the user's statement in this conversation; the old `human_reviewed` field in the original CSV is still false. An independent derived version updates this field based on the explicit confirmation, and the original table is unchanged. The [summary record](../reports/human_headline_review_20261030.json) and the full private files are kept separately; the news text has not been published.

Asset verification is not complete. The 1,879 three-class candidates were merged into 740 target candidate groups, and a local `runs/review_packages/asset_audit_20261030/` has been prepared for later checking. The next step is to check assets, source permissions and event grouping, then set up fixed SFT data partitions. This CSV is not the original workspace progress JSON; the two versions cannot directly overwrite each other or be merged.

The NSE lists of current securities, historical symbols and company name changes were obtained, and per-group [evidence statistics](../reports/nse_asset_evidence_20261030.json) and a local private candidate table were produced. Of the 740 groups, 347 have a lead from the same current symbol, 30 have a lead from an old symbol change, and the rest are unconfirmed. The same current symbol does not prove the asset identity at the time of the news. Source candidates such as `STOCKEXCHNG` and `GOLDSPC` also include non-equity categories; indices, commodities, currencies, sectors and companies need to be distinguished.

The new read-only `finllm.sft_preflight.audit_domain_parent` can, once the materials are in place, check the actual Drive domain snapshot, the frozen parent checkpoint, the vocabulary, the shards and the before/after retention-set reports. This tool does not build formal data or start training, and it has not actually read the user's Drive. For overall and token-budget statistics, see [project progress](PROJECT_PROGRESS.md).

## Note on the original workspace progress JSON

To keep the original workspace's independent record of operations, click "Back up progress JSON" on the left **in the original browser and the original workspace**. The file contains the full data SHA, the list of row IDs and the human actions, and keeps confirmed, draft, pending and exclusion decisions; it does not contain the news full text.

This time the CSV was taken in on the basis of the user's explicit confirmation; the progress JSON is needed only to recover the original workspace's independent record of operations. Different versions are not merged automatically.

To add assets, filter on "Stance reviewed / asset unverified", fill in the identifier, tick the verification box, and only then press `A`. Changing a field revokes the old confirmation; stance review and asset verification are recorded separately. Assets that have not been resolved can stay pending; export the existing progress first.

## Prepared intake check

Run in the project root, replacing the path with the actual export; review material is kept only in local ignored directories:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/import_review_progress.py `
  --source runs/review_packages/review_2000_20261030/ai_annotations.jsonl `
  --progress <actually-exported-review_progress-file.json> `
  --output runs/review_imports/review_v1
```

The importer checks the exact input SHA, the complete ordered list of row IDs, the per-row status and the boolean flags. Asset identifiers in drafts are not promoted to human-verified. AI suggestions, the original author's sentiment and the human stance are kept separately. If versions differ, row IDs are unknown or duplicated, or statuses contradict each other, it stops and keeps the original file. If the first version of the workspace was used, the matching original input must be found; the SHA cannot be changed to bypass the check.

On success it produces:

| File | Purpose |
|---|---|
| `normalized_decisions.jsonl` | Real progress for all original row IDs; rows with no action are listed separately as unreviewed |
| `reviewed_label_candidates.jsonl` | Human-confirmed, non-excluded label candidates, keeping the text, source and event group |
| `pending_asset_resolution.csv` | Review table for the later standard asset identifiers, aliases, events and sources |
| `manifest.json` | Hashes of inputs and outputs, counts by status / class, remaining gates |

All of these outputs are `formal_training_ready: false` and have no training `label` or `target`; they cannot be used directly as SFT files. A different or incomplete existing directory is not overwritten; when the review has new progress, use a new version directory.

## Order of work after intake

1. Count the actual numbers reviewed, the distribution over the three classes, the exclusions and the pending items; first complete the records whose asset is verified but cannot be mapped to the input rules.
2. Check asset identity and generate valid `target` and `target_aliases`. Historical source symbols are only candidates; free-text identifiers such as `NSE:TCS` cannot be used directly as model targets.
3. Verify source permissions and event / semantic duplicate relations. Same-source headlines, multiple targets, lexical near-duplicates and the same event are first grouped jointly, and only then are train / development / calibration / test fixed. Later, the human `event_group_id` is mapped explicitly to the `event_id` of the existing code. The two calibration halves must also be non-empty and group-isolated.
4. The new SFT entry point first re-reads and verifies `domains/domain_v1/run`, the matching report and the diagnostics, freezes the chosen domain parent weights, keeps using `tokenizer/seed_v1`, and creates a new optimizer. The default paths of the old `04_sft.ipynb` do not apply to this training branch; do not run it directly for now.
5. Build a baseline evaluation for the SFT model selected on the development set, then prepare DPO preference pairs, which need a separate human review. The test set is unsealed only after the final model has been calibrated independently. A confirmed stance is not an approved DPO preference.

2000 rows are better suited than 200 for starting a small real SFT, but the usable amount depends on acceptance of the human review, the assets and the grouping. The original AI draft had 113 exclusion suggestions; this does not determine the final class counts of the human review. The source of this batch is financial news headlines, so it cannot be used to announce a verified effect in the Twitter setting.
