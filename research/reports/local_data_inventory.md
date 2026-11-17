# Inventory of local real corpora: a restart from raw text is possible

Inventory date: 2026-11-15 (America/New_York). Method: fully offline; only the file lists, sizes, source/licence/split metadata and file hashes under `data/`, `reports/` and `runs/` of the old repository designated by the user were checked. No raw titles, per-item labels or text were printed, no checkpoint was loaded, the old repository was not modified, and no raw corpus was copied into the handoff package.

Absolute path of the original repository: `<workspace>/130U-FinLLM`. All relative file identifiers below are relative to that path, **not to the new research workspace**.

## 1. Conclusion

**Readable, non-synthetic raw corpora do exist locally; the absence of old checkpoints or per-sample predictions does not mean there is no real data.** The most direct material for a restart is 120 Federal Reserve FOMC meeting minutes texts and their local HTML snapshots; there are also 28,486 Wikipedia snapshot texts and the raw SEntFiN candidate data. They are enough to start small-scale new training from random initialization and validation of methods on real text.

The FOMC local metadata is the clearest: every record is marked `synthetic=false`, `training_allowed=true`, `license=public-domain-US-government`, and has a source URL, publication date, crawl date, text hash and HTML hash; all 120 HTML snapshots exist and match the manifest hashes. What is confirmed here is **the integrity of the local source and licence records**; the licence web pages were not re-checked online, and the records themselves are not treated as irrefutable legal proof.

This data **cannot yet directly support a final certificate of historical no-leakage**. FOMC consists of content versions crawled in 2026 plus historical publication dates, and it has not been shown that the content was not revised after the historical dates; Wikipedia has no per-article `published_at`; the existing preprocessing and task-set splits are not time splits. Real P2 number-parsing research can start from the FOMC texts, but the current metadata has no gold labels for numbers, units or comparison baselines, and no local XBRL/iXBRL-aligned data was found, so "we have real text" cannot be stated as "parsing ground truth is in place".

## 2. Scope of the inventory and guarding against miscounting

- `data/` actually holds 431 files, 671,700,099 bytes (a file-system observation that includes raw data, derived files, token files and cached duplicates; **it is not 671.7 MB of independent corpus**).
- `reports/` holds 25 files, 224,012 bytes; the metadata and limitation notes of selected preparation reports were read.
- The initial file-name list of `runs/` shows many `test_*`, `pytest_*` and temporary `original-runtime`/`drive` fixtures. They are not treated as evidence of a real training set or real checkpoints. Only the lists and manifests of directories with actual task use, such as `task_pilot` and `review_packages`, were checked further; no claim is made that the contents of all test fixtures were reviewed one by one.
- The source candidates of seed and expansion overlap. The 120 FOMC documents in expansion include the 32 in seed; the Wikipedia expansion source prefix includes the 825 articles in seed. They cannot be added up to 152 and 29,311 independent documents. The existing preparation manifest already records this exclusion.
- `domain_mix` is a mixed reshuffle of existing tokens and cannot be counted again as independent new corpus.

## 3. Available raw files and sources

The row counts below were checked by a JSONL pass that extracted only the licence, source and time fields; text and title fields were not output.

| Local file | Actual bytes | Records | Local source/licence record | Assessment |
|---|---:|---:|---|---|
| `data/raw/seed_v1/corpora/finance_candidate.jsonl` | 1,791,245 | 32 | Federal Reserve FOMC; `public-domain-US-government` | Real text candidates, not a placeholder example file |
| `data/raw/expansion_v1/corpora/finance_candidate.jsonl` | 6,977,681 | 120 | Same as above; all `training_allowed=true` | The preferred local financial text source for training from scratch |
| `data/raw/seed_v1/corpora/general_candidate.jsonl` | 19,985,370 | 825 | `wikimedia/wikipedia`; `CC-BY-SA-3.0`, `GFDL` | Real general-text candidates; attribution and other conditions to be kept |
| `data/raw/expansion_v1/corpora/general_candidate.jsonl` | 199,996,572 | 28,486 | Same as above, config `20231101.en` | Can start larger local retraining; not a random representative sample |
| `data/raw/candidates/sentfin/SEntFiN.csv` | 1,118,162 | manifest records 10,753 rows, 10,686 exactly unique titles | Fixed author repository version; local MIT LICENSE | Raw candidates exist; news publishers' rights and task semantics have separately recorded limitations |
| `data/examples/annotation_template.jsonl` | 785 | not used in research counts | Template file | This file is the small example, and it does not represent all the local data |

The Wikipedia data source version is `b04c8d1ceb2f5cd4588862100d08de323dccfbaa`, config `20231101.en`. The SEntFiN author repository version is `eba43610fe3cb57a3e5773cd6c037da1f8992ad5`. These version numbers come from locally saved manifests; this round made no request to external services to confirm them.

Both candidate corpora keep `candidate_only=true`; this means the source candidates still need the deduplication, splitting and auditing that the research requires. It does not mean the data does not exist or is synthetic, nor does it prove that reusing the old splits directly satisfies the new research.

## 4. Hash and time-field verification

The actual SHA256 of all four raw JSONL files matches the corresponding source manifest:

| Short file name | SHA256 |
|---|---|
| seed/general_candidate | `cee8dfb34401588ca8ecde6ec8d13d1ffa275efb5e0ca1391499da16e6a1b22f` |
| seed/finance_candidate | `f864068487758cdcec3142a526c9abcc5da7e92f14f289f201078f34e424f1c6` |
| expansion/general_candidate | `5b2b8def467868f177afd438c27ba4254fe41d746a5bbabb4bbbf3046769d547` |
| expansion/finance_candidate | `5a9b357c4b979b5e85dc7622e28c5793068baeb67a48abbd218e81e7d8219a0a` |

The actual SHA256 of `SEntFiN.csv` was also checked: `570af7ba58f724f3fcc414dd5ba80da5b1a3b342134d76c6ebdf53a32c54a92f`; the local `LICENSE` is 1,110 bytes, and its opening states explicitly that it is the MIT License.

| Attribute | seed FOMC | expansion FOMC | Wikipedia |
|---|---|---|---|
| `published_at` range | 2021-02-17 to 2025-01-08 | 2011-02-16 to 2025-12-30 | all missing |
| source manifest crawl time | 2026-10-09T13:43:00.227319+00:00 | 2026-10-11T10:39:20.795698+00:00 | the corresponding seed/expansion crawl times |
| `meeting_date` | present on every record | present on every record | not applicable |
| `source_url`, `text_sha256` | present on every record | present on every record | present on every record |
| HTML snapshots | all 32 present and matching SHA256 | all 120 present and matching SHA256 | no per-article HTML hash field saved |

For FOMC, `meeting_date` and `published_at` are two different fields; for example, a late-2024 meeting corresponds to an early-2025 release, so the meeting date cannot stand in for the real availability time. This check only verified that the time metadata exists and its range; **the HTML body was not read to independently reconstruct the release time, time zone or revision history**. Hash agreement proves that the current files agree with the saved manifest; it does not prove that the same content existed on that day in 2011.

## 5. Layers of local licence records

### Candidates with clear sources that can be reused first

Each FOMC `rights_note` records: the text comes from the Federal Reserve Board's original meeting minutes; institutional attribution is kept; it is marked public domain on the basis of the saved disclaimer source; content with explicit copyright marks, third-party images and external-link content is excluded. All records are `training_allowed=true`, `synthetic=false`. This is enough to avoid misdescribing the local material as of unknown source, but whether the full-text filtering was fully carried out is still a pipeline claim and should be kept as an assumption or a check item in the new data card.

Each Wikipedia record notes the article URL attribution, the CC-BY-SA-3.0/GFDL of the snapshot card, and differences with later versions of the Wikimedia terms; `training_allowed=true`. Its local source metadata is traceable; it should not be called data without a source, nor unconditionally called public domain. The attribution and other applicable conditions required by the original should be kept; this round did not re-review the licence web pages.

### Candidates that are explicitly private derivatives / restricted in use

The LICENSE of the original SEntFiN author repository is MIT, but `runs/task_pilot/entity_v1/task_manifest.json` states explicitly:

- `private_research_only=true`;
- the author repository's licence does not independently guarantee the rights of the original news publishers;
- `scope` is the literal entity, not a verified security;
- `semantic_event_audit_complete=false`;
- the existing data is a non-temporal pilot with literal/source-group isolation, not a final independent test.

So it can be confirmed that the raw/derived data for the entity task actually exists, and it cannot be dismissed wholesale as "having no rights record"; but the private research derivative set must not be packaged for publication, or directly relabelled as certificate data whose rights and historical times have both been reviewed.

`data/raw/sentfin_review_v1/ai_review_manifest.json` explicitly marks the items as AI proposals, not human-approved, `not_for_formal_training=true`. A later human review report also limits its scope of confirmation so that it does not include source rights, historical times or a complete event split. Label approval statuses from different stages must not be mixed; this inventory did not read per-item labels to decide which rows may be used for training.

The paths of the source/licence review documents are recorded in the manifest, but they are under `docs/`; this task was limited to `data/`, `reports/` and `runs/`, so those documents were not read, and no claim is made that an independent rights verification was completed.

## 6. Existing splits and preprocessing can be consulted, but not inherited as a new certificate

| Evidence file | Recorded size/split | Meaning for the new research |
|---|---|---|
| `data/raw/seed_v1/prepared/preparation_manifest.json` | general 794 train / 31 validation; finance 31/1; seed=130, hash split | The data exists; non-temporal split; finance validation has only one document and cannot support a stable evaluation of the financial population |
| `data/raw/expansion_v1/prepared/preparation_manifest.json` | After removing seed: general 26,267/1,394; finance 84/4 | This is the incremental part; it cannot be double-counted with the source candidates; still a non-temporal hash split |
| `data/processed/seed_v1/seed_summary.json` | general train 4,976,894 tokens; finance train 341,309 tokens | Measured size under the old tokenizer, not guaranteed to be the same under a new tokenizer; token binaries were not read this time |
| `data/processed/expansion_v1/expansion_summary.json` | general train 41,499,364; finance train 972,438 tokens | Incremental tokens under the old tokenizer; `domain_mix` cannot be added again as new data |
| `runs/task_pilot/entity_v1/split_manifest.json` | train 705, development 101, calibration 101, test 101; 1,008 groups | Real task data exists; `grouped_non_temporal`, not a historical test |

Actual sizes of the task files: `train.jsonl` 482,398 bytes, `development.jsonl` 69,978 bytes, `test.jsonl` 68,771 bytes, `calibration.jsonl` 69,882 bytes, plus separate temperature/threshold calibration files. The existence of these files does not mean that the predictions of every old model have been obtained; that is a different evidence question.

The goal this time is to build the research from scratch, so the new training/validation/audit boundaries and tokenizer should be re-established from the raw text, rather than treating old weights or old development-set scores as new results. The old non-temporal splits can be used to check data structure and reproduce the old engineering state, but do not automatically carry over to a P1 information-set certificate.

## 7. Concrete verdicts for the next steps

| Planned action | Is local material enough to start? | Gaps that still need closing |
|---|---|---|
| Train a small real financial-text model from random initialization | **Enough to start**: the 120 FOMC originals and snapshots are readable; a subset can be taken according to budget | New training budget, content checks, training/validation design, a newly built tokenizer; small scale does not mean sufficient language ability |
| Supplement pre-training with real general text | **Enough to start**: 28,486 fixed Wikipedia snapshot candidates | Keeping licence attribution, the gap in time information, a non-representative prefix, an independent split from the financial task |
| Validate P2 number/unit parsing on local real financial text | **Enough to start text extraction and preparation for manual verification** | No verified gold labels for numbers/units/periods/comparison baselines; FOMC is not an XBRL corpus, so complete supervision cannot be promised automatically |
| Use the P1 trusted historical core directly for certification | **Not enough for direct certification, but not because the original text is missing** | The historical-revision issue of versions crawled in 2026, release time zone/precision, historical selection, and contracts for shared components |
| Retrain the three-class headline baseline | Raw candidates and private pilot files exist | Per-row approval status, rights boundaries, task semantics and an independent evaluation set still need to be made explicit; the old development set cannot be reused as final evidence |
| Real XBRL-aligned certificate | **No corresponding material found in `data/`** | A search by file name and extension found no `.xbrl`, `.xhtml`, `companyfacts`, or data named XBRL/financialstatement; no claim is made that the internal tags of all HTML were checked |

**Recommended minimal actionable path:** first use the local FOMC raw text to build a new, hash-reproducible small corpus snapshot, freeze its use and splits, and then train a budget-constrained small model from scratch. P2 parsing gold labels and P1 historical version evidence are each listed independently as items still to be done. This carries on with the next step that real research needs, instead of inflating the loss of old training assets into "no usable raw corpus".

## 8. Evidence levels and things not done

The file sizes, JSONL counts, SHA256 agreement and snapshot existence in this report come from this round's file-system verification; the source licences, old splits and old token counts come from explicitly listed local metadata and were not externally reviewed. No web browsing, SEC access, data downloads, reading/executing of old scripts, loading of weights, or evaluation of raw labels was done.

No raw titles, news bodies, per-item labels or private review sheets were output, and none of the data above was copied into the new repository or the Fable package. This report delivers only a list and evidence boundaries for decision-making.
