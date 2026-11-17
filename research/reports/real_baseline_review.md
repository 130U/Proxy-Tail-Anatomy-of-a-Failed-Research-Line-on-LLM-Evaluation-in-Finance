# New SEntFiN Phase 0: independent review of implementation and evidence

Date: 2026-11-16. Role: internal AI adversarial reviewer; does not represent Fable, the advisor or outside peers. Fully offline; no outside person was contacted. Conducted according to the local skill "academic research - organize an adversarial research review" and its reviewer template.

**Conclusion: within the reviewed scope, the preparation, training and paired-evaluation design for the source's original task can form new, scope-limited Phase 0 baseline evidence. No critical implementation error was found that would still change this round's model selection. The important model-name interface error that was found has been fixed and retested. This judgment does not mean that the human labels, full event independence, historical availability or the old G0/G1 have passed.** For the final public interval and the archive review, see the incremental record at the end.

## Review scope and evidence boundaries

Files actually read: [PROTOCOL](../real_baseline/PROTOCOL.md), [DESIGN_REVIEW](../real_baseline/DESIGN_REVIEW.md), the three code sets prepare/train/bootstrap and their constructed tests, the [evaluation implementation](../evaluation/evaluate.py) and its tests, the [packaging code](https://github.com/130U/Proxy-Tail-Anatomy-of-a-Failed-Research-Line-on-LLM-Evaluation-in-Finance/blob/closeout-2026-11-17/research/package_handoff.py) and its tests, and the anonymized [preparation manifest](../real_baseline/aggregate_manifest.json) and [training summary](../experiments/real_baseline/baseline_summary.json). The threadpoolctl implementation on this machine was also consulted, to check the behavior of the thread-enumeration fallback.

Not read: the raw CSV, and the news text, per-row labels, splits, predictions or model weights under `research/private/`. No labels were relabeled by hand, no actual semantic event membership was checked, and no real model was retrained. The artificial strings and labels in the constructed tests are not part of the real private corpus. Byte verification and row-level invariants for the real data processing were executed and recorded by the code under review. This review independently checked the code, the internal consistency of the public summaries and the public file hashes. It must not be described as the reviewer having re-checked the real data row by row.

According to the execution record, this round's protocol was written before the real preparation/training. The final main comparison is the pre-run PROTOCOL's **char−word test macro-F1**. The "development-set winner − majority" comparison suggested by DESIGN_REVIEW was not adopted. Keeping the disagreement on record is reasonable, but after the results are in, the two must not be merged into a single pre-specified analysis. The solver `lbfgs` was fixed in the code/config before training, although the original protocol text does not spell out this field. Local file digests and execution records are not externally trusted timestamps.

## Item-by-item verification

| Item | What was verified and conclusion | Conclusions that still cannot be drawn |
|---|---|---|
| Labels and target input | The three classes stay negative/neutral/positive; different labels for multiple entities in the same headline are legitimate. The two main models share the target prefix and a word-boundary literal replacement; raw `input_text` is not used as a feature. | Does not prove the semantic binding of the target entity, the identity of a listed security, or the ground truth of an investment stance. |
| Strict parsing and conflicts | The AST check rejects duplicate raw keys and normalization collisions before literal_eval. The key for cross-row conflicts is canonical headline + canonical entity, and the whole key is quarantined; duplicates with the same label are merged. | Does not prove that the source labels are correct or that the population after quarantine is representative. |
| Near-duplicate completeness | Under one global token order, the prefix length is `|X|−ceil(.8|X|)+1`; a qualifying pair has enough common tokens, so its earliest common token must lie in both prefixes. Integer Jaccard decisions and the full transitive closure are then applied. | Covers only the defined lexical relation; cannot cover all same-event or cross-source dependence. |
| Grouping and splits | The graph is built from valid headlines before label cleaning; quarantined headlines can still act as bridges, so labels do not decide how the graph is split. The component content digest and the seed decide the split, and group identity does not depend on union-find root indices. Headlines with empty tokens were not all merged together. | It is not a time split or an unseen-entity split, and not an outside confirmation set that was never touched. |
| Fitting and selection | The vocabulary, IDF, max-feature truncation and LR are fit on train only. For each system the three C values are chosen only by fixed three-class macro-F1 on dev, with exact ties going to the smaller C. Test prediction happens only after all systems have finished selection. There is no train+dev refit. | Development selection done separately for the three feature types still does not make the bootstrap include the uncertainty of the whole research search process. |
| Input and identity binding | The real CLI requires the manifest. Before any fit it compares the SHA256 of the prepared rows and the class schema. It refuses to overwrite existing real outputs, and the new models did not load the old checkpoint. | Cannot recover the old 24M weights or the old per-row scores. |
| Paired interval | Explicit three-class names; confusion matrix in the correct orientation. Each replicate applies the same multinomial group counts to both models, sums the row counts first and then computes the fixed three-class metrics. Missing, duplicate, wrongly grouped, wrong-ground-truth and wrong-model-set inputs are rejected. | It is not an equal-weight-per-group metric, an exact finite-sample certificate, an interval over the training process or a guarantee against drift. |
| Private boundary | Data preparation/training paths are restricted to private; models, vocabularies and per-row predictions do not enter the aggregate. Packaging excludes private path components in any letter case, and file symlinks. | This check is not a word-by-word privacy forensic review of all old public documents; the final archive was reviewed only against its actual members and the manifest. |

## Issues, fixes and reservations

### I01 — important, closed: model names in the training output and the evaluation entry point did not match

The first version of the trainer's joint predictions used `word_tfidf_lr / char_tfidf_lr / entity_only_tfidf_lr`, while the bootstrap entry point required `word / char / entity_only`. Each module's own tests could pass, but the real evaluation would be rejected by the schema check. The review notified the main agent immediately after finding this.

The fix uses an explicit `PREDICTION_KEYS` mapping: the private input keeps the trainer's long names, and public display uses the short names. Validation requires a complete, unique set of long names. A new test imports the trainer's `SYSTEMS` directly and rejects input with the old short names. The 3 bootstrap tests were rerun independently and pass. This fix did not change the models, C, grouping, features or the frozen main comparison, and it does not amount to selection driven by test scores.

### I02 — important, scientific boundary still open: lexical clusters do not prove independent events or historical availability

Having 1,570 test lexical clusters and zero cross-split near-duplicate edges (as defined) only proves lexical separation under the current algorithm. Different lexical descriptions can still correspond to the same news event. In this round the whole corpus took part in graph construction and conflict cleaning, and the source corpus is not an outside sample touched for the first time. So the nominal 95% interval can only be interpreted approximately, under the stated conditions. The remedy is to keep this limitation on record. If claims of event independence, historical no-look-ahead or deployment risk are made in the future, event/time evidence and a corresponding design must be established separately. The current code tests cannot close this scientific gate.

### I03 — important, scientific boundary still open: labels and comparisons of simple models are not enough to prove that a language model is necessary

The test entity-only macro-F1 is 0.533588, which shows that on this split entity identity and the label prior are predictive. It is a diagnostic for an alternative explanation. Its ratio to the main model's F1 cannot be described as "explaining some percentage of the performance": macro-F1 is not an additive contribution decomposition, and the two are different fitted models. The main model's literal matching of the target is not an audit of semantic parsing.

This round had no human relabeling, no full event review, and no FinBERT or zero-shot LLM control. It cannot be said to complete the original advisor's three-baseline requirement, to prove that some class of models is generally better or worse, or to prove that a language model must be pretrained from scratch. What is closed now is "there is a checkable baseline on a new source task". The old G0/G1, a gold standard for financial investment labels, and research novelty are not closed.

### M01 — minor, documentation gap filled: the denominators in the aggregate ledger must be kept

In the preparation summary, 13 is the number of anomalous source rows, 7 is the number of conflicting headline–entity keys, and 73 is the number of extra entity occurrences that were merged. They cannot be added directly, and 7 cannot be written as the number of conflicting source rows. PREPARE_README now states this explicitly. The current main manifest does not give the fully expanded number of entity occurrences or the number of conflicting entity occurrences, so all cleaning steps cannot be fully reconciled from that table alone. If this is supplemented, the original run identity and hashes should be kept, and the manifest that training is bound to should not be silently rewritten.

The author then added [PREPARATION_ACCOUNTING](../real_baseline/PREPARATION_ACCOUNTING.md). It keeps the original manifest and training inputs unchanged and gives the reconciliations `10,753=13+10,740` for source rows and `14,371=14+73+14,284` for successfully parsed entity occurrences. These equations and the consistency of the split counts were read and checked independently. The supplementary counts come from the author's read-only accounting of the fixed source CSV; this reviewer did not re-read the source rows. The documentation gap is closed. This is not promoted to an independent review of the semantics of the original labels.

### M02 — minor: the two entity-match counts use different definitions

In prepare, the number of raw substring non-matches is 19. Training uses a case-insensitive literal marker with word boundaries, with non-matches of 81 in train, 10 in dev and 21 in test, 112 in total. This is not an arithmetic contradiction. Reports should keep each definition. They cannot say that all semantic entity bindings succeeded, and they cannot use 19 in place of the model's actual number of marker non-matches.

## Thread fix and budget evidence

An exception in the Windows snapshot enumeration path of threadpoolctl on this machine surfaced during the constructed tests. The implementation first tries the normal controller. Only on FileNotFoundError and on Windows does it use a patch inside a context to make the library take its own Unicode module-enumeration fallback. Reading the library source independently confirmed that returning None leads to that fallback. Leaving the context restores the patch, and site-packages was not modified. A failure is not ignored as if it were a success.

Before and after training, three numerical libraries each reported a configured thread count of 2, and the real run recorded how this was found. It means the libraries' self-reported thread configuration. It is not a measured OS peak thread count, nor does it mean the process had only two threads. The environment variables are in-process startup requests. Actual training plus output took 13.809371 seconds in total, and none of the 9 LR candidates had a convergence warning. Peak memory was not measured, so no claim can be made on this basis that RAM≤2GB was verified.

## Independent checks and result arithmetic

Constructed tests run independently: 12 for prepare, 8 for train and 2 for the first-version bootstrap, 22 in total, all passing (0.825 seconds); in addition, 8 for evaluation and 1 for package, 9 in total, all passing (0.348 seconds). After the interface fix, only the 3 affected bootstrap tests were rerun, and all pass. The old full mathematical suite was not repeated, and no real model was retrained.

In addition, three clusters of unequal size were constructed. All 27 group resamplings with replacement were enumerated and repeated four times, and macro-F1, the paired difference between the two models and the quantiles were computed by hand with an independent Fraction confusion-matrix formula. They agree with the evaluator's point estimates and intervals. This oracle checks the group weighting and the pairing implementation; it is not a proof of coverage on the actual corpus.

Accuracy, macro-F1 and support were recomputed independently from all 21 confusion matrices in the public training summary, and all agree with the exact recorded scores. The three selected C values are 10 for word, 1 for char and 0.1 for entity-only; each is the exact best of the three listed dev candidates. The public training source hash, the manifest file hash and the configuration hash were recomputed and agree. The data digests agree between the preparation and training summaries; the actual private bytes were not re-read by this reviewer.

| System | Fixed C | Test macro-F1 | Test accuracy |
|---|---:|---:|---:|
| majority | — | 0.181295 | 0.373517 |
| word TF-IDF LR | 10 | 0.792016 | 0.794020 |
| char TF-IDF LR | 1 | 0.754783 | 0.753678 |
| entity-only TF-IDF LR | 0.1 | 0.533588 | 0.537257 |

The preparation record gives 14,284 retained entity rows. Train/dev/test are 10,041/2,136/2,107, and the test set has 1,570 lexical clusters. The four systems are reported on the same frozen test rows, and the direction of the main comparison was not changed according to the test results. The strong word baseline on this literal task is a reference that later research must explain and beat. It does not automatically produce a theoretical innovation.

## Final incremental review

Read [bootstrap_summary](../experiments/real_baseline/bootstrap_summary.json): 2,107 rows, 1,570 lexical clusters, 10,000 resamples, seed 130. The main paired difference is **−0.0372334174**, with a nominal 95% percentile interval of **[−0.0530594770, −0.0215595431]**, keeping the char−word direction. The point estimates of the four systems all agree with the training summary. The paired CI was not replaced by subtracting the endpoints of two single-model CIs.

Also read: the [experiment report](../experiments/real_baseline/report.md), the [round-4 progress report](2026-11-16-round4.md) and the [review response](../real_baseline/REVIEW_RESPONSE.md). They keep the design disagreement over the main comparison, the different matching definitions, the limits of the identity-shortcut diagnostic, and the old G0's failed status. No claim was found that passes this round's scores off as the old model's scores or as a historical investment certificate.

Independently checked: the file hash of the evaluation source, and three identity bindings across the public summaries (the prepared-rows digest, the preparation-manifest digest and the joint test-prediction digest); all agree. The joint prediction digest is `d18a8a43c8ee10c5ce248ae7d0e96207ce759cbdf238dc36436f911e7f10adab`. The real per-row predictions were not reopened or recomputed here. The real bootstrap took 2.306168 seconds. Its three system summaries reuse the fixed predictions; they are not new model training or re-tuning.

The final interpretation can be written as: "Under this fixed, non-temporal lexical-group split of the source's original task and the pre-specified analysis, word has a higher test macro-F1 than char, and the paired approximate interval points in the same direction." Entity priors, source measurement error, event links across clusters and prior contact by researchers remain explanations that have not been ruled out. The engineering issue I01 is closed; the scientific gates I02/I03 remain open.

Archive boundary: first, `package_handoff.files()` was checked on the actual working tree. At that time, among 115 candidate public files, there were 0 members with private paths and 0 model-weight members, and the constructed test that excludes private directories had passed. Then the round-4 zip, rebuilt for the first time in this round (not reusing the round-3 manifest), was checked independently. It has 123 members in total, of which 122 payloads correspond one-to-one with HANDOFF_MANIFEST; all byte counts and SHA256 values match, and the CRC check passes. There are no private path components, model-weight suffixes, CSV or JSONL members. This round's protocol, response, count reconciliation, review and the two aggregate results are all in the package. The member boundary was checked first, and only then were the public manifest and public members read for hashing; no private output was opened.

The SHA256 of the checked zip snapshot is `bc8fd9825043b11367430affed0dff52bb4ab835afe9dc313533d25b322a9c2b`. The main agent will pack this addendum into the final package, so the digest of the final zip itself will necessarily differ; the final delivery record should be taken as authoritative. A package cannot embed its own final SHA256. The packaging code only updates the round-4 index, the reading order and the status description; its private-exclusion logic is unchanged.

### SHA256 of the reviewed snapshot

Paths are relative to `research/`. These are the public content identities for this review; the digest of the packaging entry point has been updated to the round-4 archive version.

| File | SHA256 |
|---|---|
| `real_baseline/PROTOCOL.md` | `9bc87c797f415c63c2f70cc59d0ae85ca53f58a0280ec57e24d4a15eb36dfda3` |
| `real_baseline/DESIGN_REVIEW.md` | `377f6cd944a2c7777c481041df2fa029df79b778054d7aca8d04b29bd4758954` |
| `real_baseline/prepare.py` | `c7f56b29875b6e76b7d2201cb4de6bea329c97b3582523218424096af53af06c` |
| `real_baseline/test_prepare.py` | `ff856de047249c9062379add77153e11d7138dd80061e414f54b7e6371d922f9` |
| `real_baseline/train_baselines.py` | `4859f8cfd01eb4650285116476c8a61f6b19bbe5790a34b58fe186c40b5e1136` |
| `real_baseline/test_train_baselines.py` | `1f791e588987a496b6d46f71256e59c52c4152b902f047f15fd46f6794e6f84f` |
| `real_baseline/bootstrap_results.py` | `c677b85f551294239a0088d1e12d0c272d3e7a8d1f8675d6d332e2c99e5cc8d6` |
| `real_baseline/test_bootstrap_results.py` | `27b000dc48ff8742a55e0416d0e5c6b0be67c605929448bf7850830ab9eba626` |
| `evaluation/evaluate.py` | `2b1ffc7c03ed92918e3de35e2c4c5269454587017998e0d3416983def7b73d00` |
| `evaluation/test_evaluate.py` | `b396d753af9829dd4f7c0e6e5b49449f13825a0186c71b10b1901b8fe49af5b4` |
| `package_handoff.py` | `1b6b455b8b65943d26f4715ad477979fad678e2f255f9448eaf9b72d75ad8539` |
| `test_package_handoff.py` | `e906a13f5a1e03e457c48015f61452f390cf86f1e836485cf3c948575ceaf81f` |
| `real_baseline/aggregate_manifest.json` | `6a8e8175bbbe391e866528e8b9d1e35fb3292c9d693da61948a4a91a44eac212` |
| `experiments/real_baseline/baseline_summary.json` | `6a4c98bd5dd92c45c747d6d8a123ab0fd5cd4bd8a78ebe63c495fdbd50e2a69a` |
| `experiments/real_baseline/bootstrap_summary.json` | `e9cf9561de7d9469463bc6f2c7ccd5859deabcc736325acedd0657a009267c1b` |
