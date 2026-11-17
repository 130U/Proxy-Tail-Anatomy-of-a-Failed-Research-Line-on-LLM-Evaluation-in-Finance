# WP0.6: Audit of public claims and evidence

Date: 2026-11-15. Audited version: `8e4dd0b33c95ac2ac1a6015eba6f2dfafe5c1254`. The README, docs and existing code were not modified, and nothing was published externally.

## Charter

Goal: distinguish public code implementations, historical run records, method designs only, and unverifiable effects, and provide a traceable baseline for repositioning the redone research. The scope is this repository's README and all docs, including the text of the PDF and the text inside its figures. The audit object is testable claims of fact, implementation or effect; operating commands, task definitions and suggestions are not automatically treated as claims of completion. Repeated claims are merged as in the table below, but every source file is registered in the coverage table. Research type: direct inspection plus a descriptive audit. It is not an external reproduction of private training, nor a novelty verdict.

This round read all Markdown full text and used local pypdf to extract the full text of the 9-page project PDF; no review of the PDF's layout quality was done. Online verification and data downloads were not used for this audit; the user's latest request is not to contact external parties. External links and historical license judgments in the original text are only registered as historical records and are not re-endorsed. The SHA256 values of the file bytes are in [claims_sources.json](claims_sources.json).

## Canonical sources

1. Code and configuration at the exact commit, used to decide what is publicly implemented.
2. The repository's public `reports/*.json` and `docs/experiment-results.md`, used to decide which historical records exist; their original qualifiers, such as "transcribed from user logs", "checkpoint not downloaded" and "local substitute test", are kept.
3. The README, docs and PDF are the audited claims, not independent evidence of their own truth.
4. The advisor snapshot is used to raise questions. It did not read the code and cannot replace this round's checks.

Categories: **A has public evidence**, **B has only design/code, with no evidence of the claimed run or effect**, **C cannot be verified**. A holds only within the stated scope; for example, "a report exists" does not mean "the model weights were independently verified". B does not mean the design is wrong. C does not mean the fact is false.

## Findings ledger

### Claims related to 2.4B (listed separately)

| ID | Public claim/location | Category and evidence | Suggested wording |
|---|---|---|---|
| C01 | README:11, MODEL_CARD:3, INTRO:3, PDF p1: the project already has a private 2.4B model | C: no checkpoint at that scale, run logs, task predictions or independently verifiable artifacts were found; the public code and reports belong to 24M | "The project has released the 24M Trial and proposed a 2.4B architecture and training plan; there is no public evidence that can verify the execution status of the private 2.4B." |
| C02 | MODEL_CARD's 28 layers, hidden 2560, Q20/KV4, vocabulary 65536, parameters 2,397,459,968 | A (architecture arithmetic)/B (instance run): the arithmetic decomposition from the public parameters holds, but it cannot prove that model training was completed | "The theoretical parameter count of the listed 2.4B configuration is ...; the run status is listed separately." |
| C03 | PROJECT_OVERVIEW:21: the 2.4B weights, vocabulary and calibration have been rebuilt | C: the actual vocabulary hash, weights hash and calibration fit records are missing | "Extending to that scale requires rebuilding the vocabulary, weights and calibration; whether this was completed awaits verification from run materials." |
| C04 | PROJECT_OVERVIEW:34: 2.4B can handle more complex relations with manageable resources | B: design motivation; lacks a matched-budget comparison, task effects and evidence of actual throughput/memory | "The goal of choosing this scale is ...; the gains and resource requirements are yet to be measured." |
| C05 | 32k gold, 12k/4k/4k/4k/8k split | B: the original text already says recipe allocation; no actual 32k set was found; it cannot be counted as an annotated quantity | Keep "planned allocation"; do not rewrite it as "has/trained on 32k gold". |
| C06 | 50B + 5B input tokens, 4B/.75B/.20B/.05B mixture | B: the original text already says recipe; no consumption logs were found; it differs from the actual 24M's 26,115,096 supervised positions | "Recipe budget"; list the actually consumed positions and independent documents separately. |
| C07 | PDF p8: 8k natural test + 3k family probes | B: an additional probe plan in a figure; no corresponding test predictions | "Planned test and derived-probe budget; probes do not count as new independent samples." |
| C08 | ENGINEERING:27, PDF p6: 38.36GB of FP32 main training state | A (arithmetic): 2,397,459,968 × 16 bytes = 38,359,359,488 bytes; not the actual peak | "Static estimate of 38.36 GB for parameters, gradients and the two Adam states; it does not include activations and the like, and it is not a T4 run record." |
| C09 | PROJECT_OVERVIEW:92, PDF p5: output tensor 1GiB→0.5MiB | A (arithmetic)/B (this implementation): 2×2048×65536×4 and 2×65536×4 bytes are correct; the public 24M has no gather before the projection | "Theoretical tensor-size comparison; the public Trial still projects all positions, and this saving has not been measured." |
| C10 | 2.4B serves private workflow / personalized standards learned | C: private use or effects cannot be proven by the 24M records | "The intended use is personal research; the effect of personalized learning has no public independent evaluation yet." |

### Methods and implementation

| ID | Claim | Category, public evidence and limits | Suggested wording or conditions for keeping it |
|---|---|---|---|
| C11 | Financial semantic permissions: INV/LBL/relabel, pairwise consistency and log-odds margin | B: defined from TRAINING_SYSTEM:23 onward; the actual stages in `src/finllm/training.py` are pretrain/domain/sft/dpo; no corresponding permission loss or edit-pair pipeline was found anywhere in src or scripts | "Proposed a supervision specification; the public 24M has not implemented/verified this loss." Do not treat DPO as this loss. |
| C12 | The permission loss improves the model's semantic responses | C: no CE control on the same edited samples and no shuffled-permission control | "The effect awaits an ablation with matched data and budget"; this round's synthetic experiment is reported separately and does not retroactively replace the historical results. |
| C13 | stance, metric direction and personal judgment are modeled separately | B: the task definitions are clear; MODEL_CARD:23 explicitly says the public interface supports only stance | "The three tasks are distinguished in the plan; the public Trial implements only stance." |
| C14 | Split by family first, then derive views, to avoid event leakage | A (some components)/B (full plan): `data.py:114–185` splits after joining id/group_id/event_id and lexical dedup; there are no general QA/edit derived views and no family loss weighting; TASK_REVIEW:23 says event_id in the old data is entirely empty | "Grouping by known relations and lexical duplicates is implemented; full semantic event independence has not been audited." |
| C15 | Formula for the global effective denominator across multiple GPUs | B: the formula is reasonable under the gradient-averaging premise; the public trainer has no DDP/all_reduce/world_size path; single-device accumulation has an actual denominator correction | "Multi-GPU method specification"; it cannot be described as multi-GPU-verified in the public Trial. |
| C16 | Supervised hidden states are selected before the vocabulary projection | B: the public `model.py:196` applies lm_head to all positions; `training.py` filters the supervised logits with answer_logits only afterward | "The Trial selects answer positions when computing the loss; sparse computation before the projection is not implemented." |
| C17 | Packing uses segmented causal attention | B: `model.py:170–196` accepts only a 2D padding mask and adds an ordinary causal mask; `TokenBlockDataset` has only input_ids/labels and no segment IDs | "Segmented packing is part of the 2.4B plan; the public Trial does not have this interface." EOS is not attention isolation. |
| C18 | 24M random init, dense GQA/RoPE/RMSNorm/SwiGLU/QK norm, tied embedding | A: `model.py`, `configs/model_24m.json`; the parameter count has a public CPU check report; not retrained this time | Keep the version boundary; do not call the architecture mechanisms themselves original. |
| C19 | Full-vocabulary CE, with the three-label conditional probabilities computed separately | A: answer_logits/sft_loss in `training.py:24–47`; `inference.py` filters the label logits; it is not a three-class CE replacing the vocabulary CE | Can be kept. |
| C20 | Exact resume restores optimizer/RNG/data cursor; a new stage carries over only the weights | A (implementation and historical local tests): `checkpoint.py`, `training.py`; `reports/expanded_continuation_checks_20261011.json` contains a bitwise comparison with tiny CPU dropout in the same environment | "Resume checks within the verified hardware/software/configuration and input contract"; do not extend it to bitwise determinism on arbitrary hardware or to a proof for all sharded training. |
| C21 | The tokenizer is a self-trained 8192 BPE | A: `tokenizer.py:40–88` and `reports/seed_data_preparation.json` record the hash/vocab; the training input is a 455-document sample from seed train, Wikipedia snapshot 20231101 + FOMC 2021–2024 meeting texts | Keep the self-trained claim. Its candidate sources include minutes published in 2025-01, and the latest availability time of the actual 455 documents still needs item-by-item checking, so it cannot be used directly for a certificate with an earlier historical cutoff. |
| C22 | Tokenizer and LM training exclude evaluation text | A (mechanism)/C (no leakage for all events): `preparation.py` freezes the candidate pool and does lexical dedup; SHA proves identity, not complete semantic isolation | "Excluded for the frozen text under the specified near-duplicate rule"; do not call it a complete no-leakage proof. |
| C23 | Inference: three-class probabilities, direction score, review flag, rejection of invalid input | A: `inference.py`, `tokenizer.py`, `evaluation.py`; the formula of the claimed score can be checked directly | Keep. The score is not a return/price prediction and does not represent a calibrated true pointwise error probability. |
| C24 | Temperature/threshold fitted separately and bound to the weights, vocabulary and target_mode | A (code): assert_disjoint_calibration, validate_calibration, run_calibration in `evaluation.py`; the threshold selection is explicitly described as an empirical rule | Keep; do not claim a finite-sample guarantee on future accuracy. |
| C25 | DPO is implemented | A (code/synthetic smoke test)/B (real training): `training.py` and `reports/cpu_smoke_check.json`; the docs explicitly say there are no real financial DPO results | "Has a DPO path and synthetic engineering checks; no real preference experiment was run." |
| C26 | The review workspace saves locally; human confirmation and asset verification are kept separate | A (design and implementation): `scripts/build_review_workspace.py`, `review_import.py` and the corresponding tests; no browser run this round | "Has local tools and historical tests"; label confirmation does not establish event/permission/security identity. |
| C27 | Source/rights fields, hashes and fixed revisions guarantee usable data | A (field checks)/C (legal or temporal truth): `validate_training_row` checks the metadata; historical source review records exist in the repository, but the external terms were not rechecked this round | "Records and validates source claims"; flags/machine timestamps cannot be treated as error-free facts. |
| C28 | MiniMind source and modifications, Apache-2.0 code | A (repository attribution records): the model.py header comment, the fixed revision in THIRD_PARTY_NOTICES, LICENSE; the upstream was not re-diffed online | Keep the attribution. Data/weight rights are recorded separately and cannot be inferred from the code license. |

### Historical runs and results

| ID | Claim | Category and evidence | Limits/suggestions |
|---|---|---|---|
| C29 | seed 300 updates, 4,914,941 effective tokens, loss 5.5419 | A (public transcription): `reports/colab_t4_continuation_20261011.json`; source_revision/torch/cuda are empty; the cloud checkpoint was not independently downloaded | Must be described as a record of user logs; not enough to reproduce the experiment fully and independently. |
| C30 | expansion 1220, 19,988,195, loss 3.6929 | A (public report): `reports/colab_t4_expanded_continuation_20261030.json` records the historical notebook SHA and the source commit | 1220 includes the 610 and the two cannot be added; the cloud weights were not read this round. |
| C31 | domain 74, 1,211,960, loss 3.2375, general retention got worse | A (public transcription): the domain report records the source, model hash, runtime and input hash; it states that the raw log was not archived and was not independently downloaded | Keep "observed", not a causal or significance inference; losses on different validation sets cannot be compared directly. |
| C32 | A total of 26,115,096 effective supervised positions | A: the three stages above add up consistently | Not a count of unique tokens or independent documents; do not mix it with the 2.4B 55B budget. |
| C33 | Initial SFT dev all neutral, acc 75.25%, F1 .2863; test acc 58.42%, F1 .2458 | A (public summary): `docs/experiment-results.md`; no public row-level output | Keep as a "historical summary"; it cannot be described as a new holdout re-check. |
| C34 | Balanced SFT dev 79/101 correct, F1 .6549 | A (public summary, not independent verification of the weights): it can be recomputed from the P/R/support in the same report; this round's exact reconstruction is in WP0.1 | State clearly that the dev set was used for model selection; a point result without a confidence interval cannot support a claim of beating the baseline. |
| C35 | TF-IDF dev acc 75.25%, F1 .6087 | A (public summary/implementation): `baselines.py` and the control in the balanced script; no public row-level pairing | The significance of the difference from .6549 cannot be identified; claim neither a positive effect nor a zero effect. |
| C36 | Balanced gained 17 direction-correct and lost 14 neutral-correct | A (arithmetic): diagonal 5+12 and 62 vs. the initial 0+0 and 76 | Sampling, epochs, updates and the LR schedule changed together, so it cannot be attributed to the sampling alone. |
| C37 | 2000 reviewed, 1993 confirmed, 1879 three-class, 1008 pool, 705 training | A (public review summary): the human_headline_review report and the TASK_REVIEW definitions; the human review itself is a user claim and was not double-annotated | Pool ≠ training; contextual AI ≠ human gold; assets/events not verified. |
| C38 | 1473 exposures/epoch, 3 epochs, 4419 label tokens, 139 updates | A (arithmetic and log summary): 491×3×3=4419; script and experiment-results | Resampled exposures are not new independent samples. |
| C39 | Calibration T≈1.50634, threshold≈.57380, and export completed | A (a public statement exists)/C (independent verification of the actual artifacts): the export script can be checked; the original final weights/calibration files were not found | "The run-output report provided by the user says it was completed"; not verified by download this round. |
| C40 | FinBERT, repeated seeds, event bootstrap, an independent new holdout | B/not done: the end of DATA_GUIDE states that these have not been executed, and experiment-results says the same | Report them as not done; do not substitute synthetic or historical dev results. |
| C41 | Local engineering tests 128/205/232/274 etc. passed | A (historical records): the corresponding dated reports record test commands, hashes, environments and the local substitution for cloud; not rerun this round | "Reported as passing at the time"; local fixed cases do not prove all inputs or all run environments. |
| C42 | Real counts from download/preprocessing, tokenizer hash and shard count | A (historical aggregates): the seed/expansion preparation reports and the hashes inside the source review; the corpus text was not read again | Interpret times/dates by each historical stage; do not mistake an early "not trained" for today's state. |
| C43 | Kaggle full/lite migration, original four pools verified | A (code, user output records); lite explicitly does not contain the old pools and cannot be independently re-checked | Explain the difference in verification capability between full and lite; no cloud migration was executed this round. |
| C44 | Wikipedia, FOMC, SEntFiN sources/licenses/sizes | A (historical source check records exist); the current external facts are C | This round does not reconfirm licenses or the latest status; SEntFiN labels are not stance, and the CSV has no reliable per-item dates. |
| C45 | Citations and external performance comparisons for Eva-4B, FinanceParam, FinLCR/ARTS etc. | C (not rechecked online within the scope of this audit); these citations are not evidence of this project's novelty or superiority | Use only as method background; specific conclusions go to an independent literature check and are labeled by the actual access tier. |
| C46 | Completing the whole training pipeline means production-ready, investment returns or financial capability | C: the repository explicitly has no such evidence; on the contrary, it actively narrows its claims in many places | Keep these limits; do not reintroduce overly strong wording in the new positioning. |

## README and docs coverage table

All the files below were read. For the PDF, the 9 pages of extractable text were covered; the visual layout was not checked. The claims of each row map to the table above. For operating procedures, only their wording about "an implementation exists / was completed historically" was audited; the cloud-service actions were not re-enacted one by one.

| File | Corresponding claims / conclusion |
|---|---|
| README.md | C01–C28, C33–C35; the 2.4B completion status on the first screen needs narrowing |
| docs/130U-FinLLM.pdf | C01–C17, C33–C45; the extra 3k probes on p8 are a plan |
| docs/DATA_EXPANSION.md | C20–C22, C27, C30, C41–C42; local and cloud evidence kept separate |
| docs/DATA_GUIDE.md | C14, C21–C27, C40; a specification is not execution |
| docs/DATA_IMPORT.md | C20, C22, C29–C39; stage lineage and the limits of SHA |
| docs/DOMAIN_TRAINING.md | C20, C31–C32, C37, C41 |
| docs/ENGINEERING.md | C08–C17, C20, C24, C33–C36 |
| docs/ENTITY_SFT_PILOT.md | C22–C23, C33–C39, C41–C43 |
| docs/EXPANDED_CONTINUATION.md | C20, C30, C41; cumulative counts / same-environment resume |
| docs/experiment-results.md | C33–C40; point estimates and limits are stated |
| docs/INTRO.zh-CN.md | C01, C03, C10–C17 |
| docs/KAGGLE_LITE.md | C20, C22, C33–C39, C43 |
| docs/KAGGLE_TRANSFER.md | C20, C22, C41, C43; a single T4, not pooled memory across two GPUs |
| docs/MAINTENANCE.md | C20–C25, C29–C43; without the originals, full reproduction is impossible |
| docs/MODEL_CARD.md | C01–C10, C13, C18–C24, C28 |
| docs/NOTEBOOK_RUNTIME.md | C20, C41, C43; local substitute tests do not certify the cloud services |
| docs/PROJECT_OVERVIEW.md | C01–C19, C29–C45 |
| docs/REVIEW_WORKSPACE.md | C26–C27, C37 |
| docs/SEED_DATA.md | C21–C22, C29, C37, C41–C44 |
| docs/STATUS.md | C01, C18–C25, C29–C43 |
| docs/T4_PILOT.md | C20, C29, C41; the peak is the PyTorch allocation, not total GPU usage |
| docs/TASK_REVIEW.md | C14, C26–C27, C37; states that event_id is entirely empty |
| docs/THIRD_PARTY_NOTICES.md | C28; a fixed upstream attribution record exists; not re-diffed online |
| docs/TRAINING_LEDGER.md | C05–C06, C20, C29–C39 |
| docs/TRAINING_SYSTEM.md | C05–C09, C11–C17, C19–C24 |
| docs/TRIAL_GUIDE.md | C18–C25, C28, C33–C43 |
| docs/TRIAL_SPEC.md | C18–C25, C28–C40 |
| docs/research/20261031-posttraining-plan.md | C12, C24–C25, C34–C40, C44–C45 |
| docs/research/corpus_sources_20261009.md | C21–C22, C27, C41–C44 |
| docs/research/DATA_DECISIONS.md | C21–C22, C27, C37, C42–C44; read as of the historical point in time |
| docs/research/expanded_corpus_sources_20261011.md | C20–C22, C27, C41–C44 |
| docs/research/stance_sources_20261009.md | C27, C37, C41, C44; source sentiment must not be turned into stance automatically |

## Scope filter

Do not extend engineering runnability to task validity, and do not extend theorem-style design or terminology to theoretical novelty. All descriptions of data licenses/rights are limited to historical records; no new legal judgment was made. Remove the default inference that "the 24M already implements full semantic permission training" (C11–C17); keep its reusable training, metadata and resume components.

## Object filter

The 2.4B plan and the 24M public implementation must be kept separate. "SFT not yet done" in earlier-dated reports describes only the state at that time and cannot override later log summaries; the later summaries also cannot replace the original checkpoint that was missing at that time. The sample source is literal entities in headlines, which cannot be transferred automatically to security tickers, Twitter or investment decisions. Passing tests covers only the tested conditions and is not a proof of F_t-measurability or of absolute determinism.

## Conclusions

1. The public assets have real engineering content, but the research contribution still lacks controls and theorem support. "Engineering hygiene" can become a premise for future certificates, but it cannot be upgraded directly into an established certificate (C11–C28).
2. The architecture arithmetic and recipe of the 2.4B model can be reviewed; training completion and the effects of the private application still cannot be verified from the public materials (C01–C10). This is not a negation of unpublished work.
3. The original balanced SFT score is a model-selection result on a small dev set, and its statistical advantage is undetermined. The user has confirmed not depending on old artifacts, so the next step should freeze a new test protocol and generate evidence from scratch (C33–C40, WP0.1).
4. The original tokenizer/source records cannot directly support a historical no-look-ahead guarantee; cutoff coverage, event identity and verification of per-content version availability times are missing (C14, C21–C22, C37, C44).

## Next steps / Risks

This round produced only rewriting suggestions; the README and docs text stay unchanged. If external repositioning is needed, the PI should first review a concrete diff draft. The research should first carry out the synthetic foundation, complete derivations of the assumptions and failure cases, and then collect real data that may be used locally. The document reading and the merging audit of the main repeated claims for WP0.6 are complete; this does not mean that all historical runs, all external citations or the private assets have been independently certified.
