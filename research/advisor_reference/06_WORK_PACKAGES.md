# Work packages (WP)

Each work package contains: goal, inputs, steps, outputs, acceptance criteria, compute budget, dependencies, and a **Codex task card**. A task card is a prompt that can be pasted directly to Codex.

All work is done on the `research/certifiable` branch or on a branch based on it. One draft PR per work package, **not merged**.

---

## Phase 0: foundation (needed whichever main line is chosen)

### WP0.1 Evaluation foundation

**Goal:** re-quantify the existing results and set up the evaluation protocol that all later comparisons use.

**Inputs:**

- the repository's existing evaluation code (`src/finllm/evaluation.py`, `src/finllm/baselines.py`);
- the numbers in `docs/experiment-results.md`;
- the public SEntFiN data (if it is confirmed that the private data comes from it; see item 5 of section 8 in `02_PROJECT_SNAPSHOT.md`).

**Steps:**

1. Write an evaluation module that supports:
   - bootstrap confidence intervals clustered by sample family or event, covering accuracy, macro-F1 and per-class P / R / F1;
   - splitting by time;
   - event-level dedup.
2. **Rebuild the uncertainty from the published numbers.** For class-balanced SFT, the number correct per class (5 / 62 / 12) and the number predicted per class (11 / 66 / 24) are known. Enumerate all 3×3 confusion matrices consistent with these, compute a bootstrap interval for macro-F1 for each matrix, and report the range of the intervals. This step needs no private data.
3. Build three baselines on public data: TF-IDF + logistic regression, FinBERT, and zero-shot use of a small open-source LLM (4-bit quantized on a T4, for example a model in the Qwen3 series that fits on a T4).
4. Write a script that lets Theodore run the same evaluation on the private data on Kaggle or Colab.

**Outputs:** `research/experiments/wp0_1/`, containing: the evaluation code, a report on the rebuilt intervals, a table of baseline results, and run instructions for Theodore.

**Acceptance criteria:**

- Every metric has a 95% confidence interval.
- The report answers explicitly: "Is the gap between 0.655 and 0.609 within sampling error?"
- Both the baselines and the intervals can be reproduced with one command.

**Compute budget:** mainly CPU; the zero-shot LLM at most 1 hour on a T4.

**Dependencies:** none.

> **Codex task card (WP0.1):**
> Read `00_CODEX_BRIEF.md`, `01_ADVISOR_MEMO.md`, `02_PROJECT_SNAPSHOT.md`. On the `research/certifiable` branch, complete WP0.1 of `06_WORK_PACKAGES.md`. Do step 2 first (rebuilding the macro-F1 uncertainty from the published numbers); it needs no data at all. Put all output in `research/experiments/wp0_1/`. Write the experiment record following section 3 of `07_REPORTING_PROTOCOL.md`. Do not modify the README.

### WP0.2 The missing ablation of the permission loss

**Goal:** answer "is the semantic permission loss better than ordinary cross-entropy on the same batch of edited samples?"

**Steps:**

1. Verify whether the permission loss is implemented in the repository, and whether there is code that generates edited sample pairs.
2. If there are no ready-made edit pairs: on public data, generate three kinds of edit pairs with rules:
   - target replacement (relabel or no constraint);
   - irrelevant rewriting (distribution-preserving);
   - appending evidence in the same direction (label-preserving; confidence may change).
   Or do it in the synthetic world after WP0.5 is complete.
3. Compare four configurations: (a) cross-entropy on original samples only; (b) cross-entropy on original + edited samples; (c) (b) + permission loss; (d) (b) + permission loss, but with the permission types shuffled as a control. Run 3 seeds per configuration.
4. Metrics: task metrics (with confidence intervals), and specification violation rates (for each kind of edit, the fraction that violates the T2.1 specification).

**Acceptance criteria:** a conclusion with confidence intervals, whether the result is positive or negative.

**Compute budget:** for the 24M model on a T4, at most 1 hour per configuration per seed; or use a smaller backbone on CPU.

**Dependencies:** public data, or WP0.5.

> **Codex task card (WP0.2):**
> Read 00, 01, 02 and T2.1 of `04_THEORY_NOTES.md`. Complete WP0.2. First verify in the code whether the permission loss is implemented, and write the conclusion at the start of the experiment record. If synthetic data is needed and WP0.5 is not yet complete, first implement the rule-based edits of step 2 and do it on SEntFiN. Do not modify the README.

### WP0.3 Formal notes

**Goal:** turn the drafts in `04_THEORY_NOTES.md` into rigorous LaTeX notes.

**Scope:** T0, T1.1–T1.5, T2.1–T2.4, T3.1.

**Outputs:** `research/theory/notes.tex` and the PDF compiled from it. Each proposition is labeled with a status: proven / draft / has counterexample / open.

**Acceptance criteria:**

- Every proposition has a complete list of assumptions.
- Proven propositions have complete proofs.
- When an error is found in the advisor's draft, state clearly where the error is and how it is corrected.

**Compute budget:** none.

**Dependencies:** none. Can run in parallel with the literature questions.

> **Codex task card (WP0.3):**
> Read 00, 01 and `04_THEORY_NOTES.md`. Write T0, T1.1–T1.5, T2.1–T2.4 and T3.1 as rigorous LaTeX notes in `research/theory/notes.tex`. Do T1.4 (the audit resolution limit) and T2.2 (the ordered monotone head) first; they are the shortest and the most critical. The advisor's drafts may contain errors; please check every constant and the direction of every inequality.

### WP0.4 XBRL pipeline prototype

**Goal:** confirm whether SEC XBRL data can provide two things at once: supervision that can be verified exactly, and authoritative machine timestamps.

**Steps:**

1. **Pause first.** Accessing the SEC requires contact information in the User-Agent. Ask Theodore for this value (O3 in `08_DECISION_LOG.md`). Until you have it, write only code and tests, and send no requests.
2. Download one quarter of the Financial Statement Data Sets and (if it exists) the Financial Statement and Notes Data Sets. Verify which files they contain and whether calculation relations are included.
3. Count the following:
   - the fraction of calc relations that can be verified automatically;
   - the fraction and types of verification failures;
   - the format and precision of the `accepted` field;
   - how amended filings (10-K/A etc.) appear in the data.
4. If feasible, take a small number of inline XBRL files and measure the fraction of text that can be aligned with facts.

**Outputs:** `research/experiments/wp0_4/`, containing: pipeline code, a statistics report, a data dictionary.

**Acceptance criteria:** the report answers three questions explicitly: (a) can EDGAR timestamps serve as the "trusted core"? (b) how much verifiable supervision can be provided per year? (c) how much text can text–number alignment cover?

**Compute budget:** CPU, a download of about a few hundred MB.

**Dependencies:** O3.

> **Codex task card (WP0.4):**
> Read 00, 01, 02. Complete WP0.4. **Do not send any request to sec.gov until Theodore provides the SEC User-Agent contact information**; write only code and unit tests (with small local sample files). Do not make up an email address, and do not use any email address you have seen elsewhere.

### WP0.5 Synthetic world v0

**Goal:** a testbed whose ground truth is fully known, for verifying that every certificate "holds and is non-vacuous".

**Design requirements:**

1. **Companies and accounting:** N companies with quarterly financial statements that satisfy accounting identities (assets = liabilities + equity, subtotals equal the sum of their items).
2. **Price process:** a stochastic process with company-specific shocks and announcement effects.
3. **Text generation:** templated news, announcements and commentary. Each document has:
   - a timestamp;
   - an author (holder);
   - a target;
   - a true stance (a latent variable of the author);
   - a metric direction (determined by the numbers);
   - the numbers, units and scales that appear in the text.
4. **Contamination planting:** a number k can be specified to generate documents "timestamped before t whose content reveals outcomes after t", recording their ids.
5. **Edit-pair generation:** generate edit pairs according to the five permission types of T2.1, each pair with its ground-truth relation.
6. All generation is determined by the seed and is bitwise reproducible.

**Outputs:** a `synth/` directory (code + tests) and a data card.

**Acceptance criteria:**

- Unit tests check that the accounting identities hold in all generated statements.
- The number of planted contaminations is exactly right.
- Data generated from the same seed is bitwise identical.

**Compute budget:** CPU.

**Dependencies:** none.

> **Codex task card (WP0.5):**
> Read 00, 01 and T1.1 and T2.1 of `04_THEORY_NOTES.md`. Complete WP0.5, with the code in `synth/`. The generator must be fully determined by the seed and must be able to plant exactly k documents with mislabeled timestamps. Write the tests before the generator. Make the template language as varied as possible, so that a model does not just learn the templates.

### WP0.6 Claims audit

**Goal:** list all external claims in the repository and compare each one with the public evidence.

**Steps:** read the README and every document under `docs/` sentence by sentence. Put each claim into one of these categories:

- has public evidence (point to a file or number);
- design only, no run evidence;
- cannot be verified.

For the last two categories, give suggested rewording.

**Outputs:** `research/claims_audit.md`.

**Acceptance criteria:** covers the README and all docs files; every claim is categorized; claims related to 2.4B get their own section. **Do not modify any original file.**

**Compute budget:** none.

**Dependencies:** none.

> **Codex task card (WP0.6):**
> Read 00, 02. Complete WP0.6 and output `research/claims_audit.md`. Write only the audit report; do not modify the README or any docs file. Keep the tone objective and avoid evaluative adjectives.

---

## Phase 1: feasibility of the two main lines (experiments start after G0 passes; the theory parts can be done earlier)

### WP1.1 Numerical feasibility map for P1

**Goal:** without training any model, answer "can the P1 certificate be non-vacuous under realistic parameters?"

**Steps:**

1. Implement the following computations:
   - the DP bound of T1.2 (grid over ε and μ);
   - the audit upper bound of T1.4 (exact hypergeometric computation);
   - the shard requirement of T1.3.
2. Fill in the parameters with real counts (from WP0.4 and Q5): the number of EDGAR documents per year; the scheme for splitting the trusted core and the suspect window.
3. Plot the feasible region: the horizontal axis is the suspect window size N, the vertical axis is the audit size n, and the contours are the required number of shards m and documents per shard.

**Outputs:** `certify/feasibility.py` and `research/experiments/wp1_1/report.md`.

**Acceptance criteria:** the report gives an explicit conclusion: "non-vacuous under condition X; necessarily vacuous under condition Y."

**Compute budget:** CPU, minutes.

**Dependencies:** WP0.4 helps to get real numbers, but assumed values can be used first.

> **Codex task card (WP1.1):**
> Read section 5.1 of 01 and T1.2–T1.4 of 04. Complete WP1.1. Compute the audit upper bound exactly with the hypergeometric distribution; do not use only the approximate formula. If WP0.4 is not yet complete, use adjustable assumed values first and mark them in the report.

### WP1.2 Point-in-time corpus pipeline

**Goal:** implement the "measurable by record" pipeline of T1.1, with tests serving as the constructive certificate.

**Steps:**

1. Build a document store: each document has an id, a content hash, a recorded timestamp, a source, and whether it belongs to the trusted core.
2. Every component (tokenizer training, filtering, dedup, data sampling, validation split, hyperparameter selection) explicitly receives the cutoff t and reads only data with τ ≤ t.
3. Write tests: for any t, after adding documents with τ > t to the store, the outputs of all components must be bitwise unchanged. This test is the checker of the constructive certificate.

**Outputs:** a `pit/` directory (code + tests).

**Acceptance criteria:** the invariance tests cover all components.

**Compute budget:** CPU.

**Dependencies:** WP0.4 or WP0.5 provides the data.

> **Codex task card (WP1.2):**
> Read T1.1 of 04. Complete WP1.2, with the code in `pit/`. The core deliverable is the invariance test: after adding any documents with τ > t, the outputs of all components must be bitwise unchanged. Implement it first on the synthetic world (WP0.5).

### WP1.3 Shard-aggregation certificate prototype

**Goal:** verify the certificate chain of T1.5 on the synthetic world: the certificate holds, and measure how tight it is.

**Steps:**

1. Train a small backbone on the trusted core (for example 4 layers, d=256), or directly use a scaled-down version of the 24M architecture.
2. Freeze the backbone and train a linear head or small MLP on each of the m shards of the suspect window, with a deterministic algorithm (CPU).
3. Verify determinism: repeated training on the same shard gives bitwise-identical results.
4. Plant k contaminated documents and compute $[S_{\text{low}}, S_{\text{high}}]$; also train a "contamination-free" version as ground truth, and check whether the ground truth falls inside the interval.
5. Scan m ∈ {11, 31, 101, 301} and k ∈ {0, 1, 3, 10, 30}, and report: interval width, the fraction of certified predictions, the accuracy cost.
6. Optional: compute a tighter collective certificate with ILP and compare it with the naive bound.

**Outputs:** `certify/partition.py` and `research/experiments/wp1_3/`.

**Acceptance criteria:**

- In all settings, the ground truth falls inside the certificate interval. If it ever does not, there is a bug or the theorem is wrong, and this must be resolved first.
- Give a complete table of "interval width–m–k".

**Compute budget:** backbone training at most 2 hours on a T4, or train a smaller backbone on CPU; shard heads trained on CPU.

**Dependencies:** WP0.5, WP1.2.

> **Codex task card (WP1.3):**
> Read section 5.1 of 01 and T1.3–T1.5 of 04. Complete WP1.3. The most important check is that the ground-truth statistic must fall inside the certificate interval in all settings. First get the whole chain running at a very small scale (m=11, k=1), then scan the parameters.

### WP2.1 Number parsing and dimensionless features

**Goal:** implement the statistical link of P2 and measure its error rate.

**Steps:**

1. Write a rule-based parser that extracts values, units, scales, periods and comparison baselines from text. Cover the common error types listed in Q32.
2. Evaluate on the synthetic world (ground truth known); if WP0.4 obtained inline XBRL, also evaluate on it (with XBRL facts as ground truth).
3. Build dimensionless groups: ratios of quantities with the same unit, growth rates, shares relative to a reference quantity.
4. Give an exact confidence upper bound on the parsing error rate (this is the certificate of the statistical link).

**Outputs:** `models/numeric/parse.py`, `models/numeric/pi_groups.py` and an evaluation report.

**Acceptance criteria:** report the error rate for each error type, and a confidence upper bound on the overall error rate.

**Compute budget:** CPU.

**Dependencies:** WP0.5; WP0.4 optional.

> **Codex task card (WP2.1):**
> Read section 5.2 of 01 and T2.3 of 04. Complete WP2.1. Use rule-based methods first, not LLM extraction; we need a parser that is auditable and whose error rate can be measured.

### WP2.2 Ordered monotone head

**Goal:** implement T2.2 and verify the certificates.

**Steps:**

1. Implement a Lipschitz monotone network (the weight normalization of Kitouni et al., with ℓ1 / ℓ∞ constraints).
2. Implement a cumulative-link output layer.
3. Attach it to a small transformer: numbers in the text stream are replaced by placeholders; values enter the monotone head only through dimensionless features.
4. Write checkers:
   - (a) architecture level: check layer by layer that the weight norms satisfy the constraints, and compute an upper bound on λ from them;
   - (b) numerical level: verify monotonicity and the derivative bound on a grid, as a sanity check rather than a proof.

**Outputs:** `models/monotone/` and `certify/monotone_check.py`.

**Acceptance criteria:** checker (a) outputs the proven λ and the upper bounds on the Greeks; checker (b) finds no violation on 10⁵ random points.

**Compute budget:** CPU or T4, at most 2 hours.

**Dependencies:** WP2.1.

> **Codex task card (WP2.2):**
> Read T2.2 of 04. Complete WP2.2. Pay special attention: the text-context representation c must never depend on the value g, otherwise the monotonicity certificate fails. Write a test dedicated to checking this (when g changes, c must be bitwise unchanged).

### WP2.3 Soft constraints vs. hard constraints

**Goal:** compare three configurations on the synthetic world, and along the way answer "is the permission loss useful?"

**Configurations:**

- (a) an unconstrained transformer;
- (b) (a) + the permission soft loss;
- (c) the hard-constrained monotone head.

**Metrics:** task accuracy (with confidence intervals); specification violation rates under numeric perturbation and unit scaling; the empirical maximum of the Greeks and the proven upper bound.

**Acceptance criteria:** a complete comparison table and a paragraph of conclusions.

**Compute budget:** T4, at most 1 hour per configuration, 3 seeds.

**Dependencies:** WP0.2, WP2.2.

> **Codex task card (WP2.3):**
> Complete WP2.3. The three configurations use the same data, the same backbone size and the same number of training steps. The report must include how much accuracy the hard constraints cost.

### WP2.4 Verification of unit invariance

**Goal:** verify that T2.3 holds exactly on an actual model, and show how sensitive an unconstrained model is to unit changes.

**Steps:** apply unit transformations (thousands of yuan ↔ millions of yuan, scaling within the same currency) to the synthetic world and to XBRL-aligned text, and compare two kinds of model:

- P2 model: the output should be unchanged within floating-point error;
- unconstrained baseline: report the distribution of output changes.

**Acceptance criteria:** the maximum output change of the P2 model does not exceed 1e-6; the distribution of the baseline's changes is shown in a figure and a table.

**Compute budget:** CPU.

**Dependencies:** WP2.2.

> **Codex task card (WP2.4):**
> Complete WP2.4. If the output change of the P2 model exceeds floating-point error, some number is bypassing the dimensionless channel. Find that leakage path first, then report.

---

## Side line

### WP3.1 Deployment-risk certificate

**Goal:** implement T3.1.

**Steps:**

1. Input: calibrated per-item error probabilities p_i, and the cluster partition.
2. Compute the exact distribution of the number of errors under "comonotone within clusters, independent across clusters" (cluster-by-cluster convolution).
3. Output: the worst-case variance and ES_β, compared with the case of independence within clusters.
4. Demonstrate on the public-data results of WP0.1.

**Outputs:** `certify/deployment_risk.py` and a demonstration report.

**Acceptance criteria:** for small cases, cross-check with brute-force enumeration of all couplings (or a linear program) that comonotonicity really gives the maximum ES.

**Compute budget:** CPU.

**Dependencies:** WP0.1; the derivation of T3.1.

> **Codex task card (WP3.1):**
> Read T3.1 of 04. Complete WP3.1. First use a linear program to find the worst-case ES at small scale (3 samples per cluster) and verify that it equals the comonotone result. Only after this check passes, write the general implementation.

---

## Overview of dependencies

| Work package | Depends on | Can run in parallel with |
|---|---|---|
| WP0.1 | None | All of Phase 0 |
| WP0.2 | Public data, or WP0.5 | — |
| WP0.3 | None | All |
| WP0.4 | O3 (User-Agent) | — |
| WP0.5 | None | All |
| WP0.6 | None | All |
| WP1.1 | WP0.4 optional | WP1.2, WP2.1 |
| WP1.2 | WP0.5 | WP2.1 |
| WP1.3 | WP0.5, WP1.2 | WP2.x |
| WP2.1 | WP0.5 | WP1.x |
| WP2.2 | WP2.1 | WP1.x |
| WP2.3 | WP0.2, WP2.2 | WP1.3 |
| WP2.4 | WP2.2 | WP1.3 |
| WP3.1 | WP0.1 | All |
