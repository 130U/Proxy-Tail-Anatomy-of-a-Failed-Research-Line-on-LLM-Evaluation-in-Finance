# Snapshot of the repository's current state (as of 2026-11-15)

**Sources:** `README.md`, `docs/PROJECT_OVERVIEW.md`, `docs/MODEL_CARD.md`, `docs/TRAINING_SYSTEM.md`, `docs/ENGINEERING.md`, `docs/experiment-results.md` on GitHub, and the repository file tree.

**Limitation:** the advisor read only the documents. The code was neither read nor run. Section 8 lists the items you need to verify in the code.

---

## 1. The public 24M Trial

| Item | Value |
|---|---|
| Parameter count | 24,255,744 |
| Layers / hidden / FFN | 6 / 512 / 1,664 |
| Attention | GQA, 8 query heads, 4 KV heads, head dim 64 |
| Other components | RoPE (theta 1e6), RMSNorm, SwiGLU, QK norm, tied input and output weights |
| Vocabulary / context | 8,192 / 512 |
| Backbone source | A fixed version of MiniMind; modifications are recorded in `docs/THIRD_PARTY_NOTICES.md` |
| Training pipeline | Random initialization → next-token pretraining → financial domain adaptation → target-conditioned stance SFT → calibration and acceptance threshold |
| Task | Input an English financial headline + a literal target entity; output bearish / neutral / bullish, three-class probabilities, a direction score `100 × (P(bull) − P(bear))` and a review flag |

---

## 2. Data and results

**SFT data:**

- Training set 705 rows: 491 neutral / 140 bullish / 74 bearish.
- Dev set 101 items: 76 neutral / 15 bullish / 10 bearish.
- Test set 101 items.

**Results:**

| System | Split | Samples | Accuracy | Macro-F1 |
|---|---|---:|---:|---:|
| Initial SFT | Dev set | 101 | 75.25% | 0.2863 |
| Initial SFT | Test set | 101 | 58.42% | 0.2458 |
| Class-weighted TF-IDF + logistic regression | Dev set | 101 | 75.25% | 0.6087 |
| Class-balanced SFT | Dev set | 101 | 78.22% | 0.6549 |

**Per-class results of class-balanced SFT on the dev set:**

| Class | Samples | Precision | Recall | F1 | Correct | Predicted as this class |
|---|---:|---:|---:|---:|---:|---:|
| Bearish | 10 | 0.4545 | 0.5000 | 0.4762 | 5 | 11 |
| Neutral | 76 | 0.9394 | 0.8158 | 0.8732 | 62 | 66 |
| Bullish | 15 | 0.5000 | 0.8000 | 0.6154 | 12 | 24 |

The last two columns were derived by the advisor from precision, recall and sample counts. The predicted counts of the three classes add up to 101, consistent with the total.

**Limitations stated by the documents themselves:**

- The initial SFT labeled every sample neutral on both the dev set and the test set.
- The class-balanced SFT was an exploratory model selection on the same dev set, not an independent test. The test set had already been looked at in the initial run and was not used again to evaluate the class-balanced model.
- The split is not by time, and event-level independence has not been fully audited.
- The metrics of the class-balanced run come from Kaggle logs provided by Theodore; its checkpoint was not independently downloaded and verified.
- Parameters of the class-balanced run: 3 epochs, 139 optimizer updates, 4,419 supervised label tokens, with each class resampled to 491 exposures per epoch. Code version `75a90c3fca66ae08abf77742ccbd4368e50c7e25`.
- The repository contains DPO code and configuration, but no DPO run results at all.

---

## 3. The two "core designs" described in the documents

### 3.1 Financial semantic permissions

For each "original–edited" sample pair and each task axis, one of four relations is hand-annotated:

- label-preserving
- distribution-preserving
- relabel
- no constraint

The loss has three parts:

1. The cross-entropy on the original text and on the edited text, each separately;
2. A consistency constraint on distribution-equivalent pairs;
3. A relative-response margin on relabel pairs. When the label changes from a to b:

```
D = [log q(b|edited) − log q(a|edited)] − [log q(b|orig) − log q(a|orig)]
L_change = max(0, margin − D)
```

The documents themselves say that it needs to be compared with ordinary cross-entropy on the same batch of edited samples. This comparison **has never been done**.

### 3.2 Objective-preserving scaling

It includes the following:

- sample family bookkeeping: all views derived from the same event belong to one family; families are split first and views are derived afterward;
- a global effective denominator across devices and under gradient accumulation: `local_loss_r = W × Σ_j λ_j S_rj / C_j`;
- full-vocabulary projection only at supervised positions, to save output-layer computation;
- segmented causal attention when packing, so that one sample cannot see the answer of an adjacent sample;
- restoring the optimizer state, the random state and the data-consumption position together when resuming from a checkpoint.

---

## 4. Repository structure

| Directory | Count | Notes |
|---|---:|---|
| `src/finllm/` | 27 modules | Most of them, such as `kaggle_*`, `*_runtime`, `expansion*` and `continuation`, relate to run environments and workflows |
| `scripts/` | 26 | Mostly notebook generators, Colab/Kaggle exports and data scraping |
| `notebooks/` | 19 | Stages 00–06 and their variants |
| `tests/` | 40 | Test coverage is fairly good; this is a strength |
| `reports/` | 20 | JSON run records and check results |
| `docs/` | about 25 | Including 5 data and post-training plans under `docs/research/` |
| `configs/` | 6 | model_24m, pretrain, pretrain_pilot, domain, sft, dpo |

---

## 5. The private 2.4B version

Architecture given in the documents: 28 layers, hidden 2,560, FFN 8,320, Q20 / KV4, head dim 128, vocabulary 65,536, context 4,096, total parameters 2,397,459,968.

The documents describe "50B + 5B input tokens" and "32k human gold annotations" as a **recipe allocation**, and state that the actual consumption is recorded separately.

**The public materials cannot tell whether the 2.4B has finished training.** This is an open question for Theodore; see O1 in `08_DECISION_LOG.md`. If it is only a design, the wording on the first screen of the README conflicts with the positioning of "making conclusions verifiable". The WP0.6 claims audit will spell this out.

---

## 6. Diagnosis summary

| Problem | Severity | Notes |
|---|---|---|
| No answer to "why train from scratch" | Fundamental | The starting point of the new direction |
| The evidence is not enough to support "the model is effective" | High | 0.655 vs. 0.609, very few samples, no confidence interval, no independent test |
| Saturated task | High | Three-class headline sentiment |
| Core designs untested | Medium | The permission loss has no ablation |
| Claims go beyond the public evidence | Medium | The 2.4B wording |
| Much engineering, little research | Medium | A large amount of code is run-environment plumbing |

---

## 7. Assets to keep, and their role in the new direction

| Existing asset | Role in the new direction |
|---|---|
| The `as_of` field, source records (provenance) | P1: data precondition for the information-set certificate |
| The tokenizer and the evaluation-set exclusion boundary | P1: part of the F_t-measurable pipeline |
| Deterministic training, resume semantics | P1: the shard-aggregation certificate requires each shard's training to be a deterministic function |
| sample family, split first and derive afterward | P3 and the evaluation foundation: a family is a natural cluster |
| semantic permissions | P2: an early form of the sensitivity specification, and also the "soft" side in the soft-constraint vs. hard-constraint comparison |
| Calibration / threshold / final test partition | P3: the deployment-risk certificate uses calibrated probabilities |
| 40 tests | Test framework for the certificate checkers |
| 24M architecture code | Small backbone for the synthetic-world experiments |

---

## 8. Items you need to verify in the code

1. Is the permission loss (the formula in section 3.1) already implemented in the code? In which file? Is there code that generates edited sample pairs?
2. Are segmented causal attention and "projection only at supervised positions" implemented in the 24M code?
3. Does rerunning with the same seed on CPU produce bitwise-identical weights? The shard-aggregation certificate needs this.
4. What data was the tokenizer trained on? What is the time range of that data?
5. Does the SFT data come from SEntFiN? The repository's `scripts/prepare_sentfin_review.py` suggests it does. If so, we can rebuild a public version from the public SEntFiN for WP0.1 and WP0.2.
6. What reproducibility information do the JSON files in `reports/` record? Is it enough to rebuild the experiments?
