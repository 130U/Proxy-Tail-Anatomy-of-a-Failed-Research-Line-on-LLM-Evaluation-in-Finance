# Local asset stance review workspace

Review the AI first-pass judgments in a self-contained HTML page; no server, account or external scripts are needed. The text, the suggestions and the human actions all stay on this machine; the page sends no network requests. The generated HTML and the per-row data go in Git-ignored directories such as `runs/`.

## Recommended review order

1. First tick "Review 40 annotation-calibration examples first". This set is stratified by AI class with easy items first, takes at most one row per group where possible, and turns on blind review by default. Judge by your own understanding first, then turn off blind review and compare with the AI suggestions. It is a rule-calibration sample, not a final test set.
2. Once the rules are stable, work in batches of 100 rows. First filter on "Priority review" / "Ambiguous / difficult" to handle examples that are easy to misread, or first complete an easy batch to get used to the controls. For each row, look only at the text, the specified target and the basis needed for the judgment.
3. `A` confirms the current stance and moves to the next row; `1/2/3` select bearish / neutral / bullish, followed by `A`; `X` explicitly excludes and confirms; `U` moves the row to pending investigation. `J/K` move forward and back; `Z` withdraws the last confirmation / pending flag and returns to that row. Shortcuts do not fire while you are typing in a note or asset field.
4. Asset identity and stance are confirmed separately. Candidates given by the AI stay as drafts; after human verification, fill in the identifier and tick the verification box. You can confirm the stance first and fill in assets later using the "Stance reviewed / asset unverified" filter. Assets without human verification are not exported as a verified `asset_identifier`.
5. After each batch, export the progress JSON and save it in your own project directory; the browser cache does not replace a backup. The next time the HTML for the same data version is opened, progress is usually restored automatically; when switching browsers, import the JSON.

Only an explicit confirmation writes `human_reviewed=true`. In this workspace the flag means that the stance has been confirmed by a human; **it does not automatically prove that the asset mapping, source permissions, event deduplication or data split have been accepted**. Assets have a separate `asset_verified` flag, and all merged rows keep `formal_training_ready=false`. Importing formal data requires separate gates.

If some rows have a second AI review, the page shows the second suggestion and its reason and provides an "AI suggestions disagree" filter. This only helps you prioritize reviewing the disagreements; a second AI review is not a human review and cannot be used to claim human accuracy or confidence probabilities.

## Files and recovery

- **Progress JSON**: stores only the human actions, the data SHA and the exact list of row IDs; it can restore draft, needs-investigation and confirmed states. Import stops explicitly and keeps the current progress when the data version differs, row IDs are unknown/duplicated, a state is invalid, or it conflicts with existing local actions.
- **Confirmed CSV**: contains only the human fields of rows whose stance is confirmed. Formula prefixes are escaped for Excel; unverified asset fields go only in `asset_identifier_draft`.
- **Confirmed JSONL**: the text, the AI first-pass judgment and the human decision merged, keeping the original text. Used later for source, grouping, mapping and label checks; it is not a final dataset ready for training.
- **All rows JSONL**: also includes unreviewed and pending rows, with their status unchanged. Exporting or opening a file cannot be treated as approval.

Rows with `human_reviewed=false`, `exclude` rows, unverified asset identities and rows that fail later isolation checks cannot enter formal training on the strength of the AI first pass alone. The share of stances confirmed in the browser is also not an AI model accuracy or a two-person agreement score.

## Generation

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/build_review_workspace.py `
  --input runs/review_packages/review_2000_20261030/ai_annotations.jsonl `
  --output runs/review_packages/review_2000_20261030/review_workspace.html
```

Each JSON row must contain a non-empty `id`, English `text`, `source_entity` and `ai_stance` (or `proposed_stance`); suggested fields are `ai_rationale`, verbatim `evidence_quotes`, `ai_asset_candidate`, `mapping_status`, `priority`, `difficulty`, `batch_id` and grouping / source fields. The input accepts only the AI pending-review state and cannot carry human approvals.

Page data and progress are bound to the SHA256 of the input file. The generator does not overwrite an existing HTML with different content; for a new interface version or new data, specify a new file name and keep the exported progress JSON. After an interface upgrade for the same input, progress can be restored from the progress file; progress cannot be imported directly, without verification, after the input bytes have changed.

## Before handing over to the training pipeline

Preferably hand over the `review_progress_*.json` downloaded with "Back up progress JSON"; it contains drafts, pending items, exclusions and explicit confirmations, so the full set of actions is kept. The project adds `scripts/import_review_progress.py`, which checks the exact source file SHA and all ordered IDs and then generates the progress, the label candidates, an asset to-verify table and a manifest. Rows without a decision stay unreviewed, rows whose stance is reviewed but whose asset is unverified are still listed separately, and all outputs remain barred from formal training.

For the full command and the next steps, see the [handoff after 03a](POST_DOMAIN_NEXT.md). The importer accepts only actual progress JSON, not an AI draft renamed as human results. The SHA of the current workspace data is `becc92113c191f807c8a4d73fe8e792cfc7d0ea193f2b2627c4e66f80ac4070c`; other versions must use the matching original data.
