# Task brief for Codex: redoing 130U-FinLLM

To: Codex (PhD student)
From: advisor
Cc: Theodore (PI, project owner)
Date: 2026-11-15 · Round 1

---

## 1. In one sentence

Redo 130U-FinLLM from "a 24M financial sentiment classifier trained from scratch" into "a financial language model small enough that things can be proven about it".

The research contribution is **testable certificates** about the model: what it can possibly know (its information set) and how it responds to text and numbers (its sensitivity). Experiments are only minimal T4-level checks.

---

## 2. The problem we want to solve

### 2.1 Why redo it

The current project has four problems. The details and numbers are in `02_PROJECT_SNAPSHOT.md`.

1. **The public evidence cannot support research conclusions.** The only verifiable result is a macro-F1 of 0.655 for the 24M model on 101 dev-set headlines. On the same dev set, TF-IDF + logistic regression gets 0.609. The dev set has only 10 bearish and 15 bullish items, so a single sample can move F1 by several points. This dev set was also used for model selection, and there is no independent test set.
2. **The task is in the most saturated track.** Three-class headline sentiment is the most mature task in FinNLP. Existing results show that an open-source 8B model beats FinBERT using only 5% of the training data.
3. **Two "core designs" have not been tested.** Semantic permissions have no ablation. Objective-preserving scaling is correctness hygiene, not a research contribution.
4. **The fundamental problem: there is no answer to "why train from scratch".** Training a small model from scratch to do what open-source large models do better is the definition of a toy project.

### 2.2 Research questions

**Overall question:** for a small financial language model trained from scratch, what can we prove? What data and architecture designs make these proofs non-vacuous?

It splits into three sub-questions:

- **RQ1 Information set.** Can we give a testable certificate that "the model at time t contains no information from after t"? Under residual timestamp errors, can we give a proven interval for a "leakage-free backtest statistic"?
- **RQ2 Sensitivity.** Can we make the model exactly invariant to entity identity, currency unit and reporting scale, certifiably monotone in specified numbers, and give a proven upper bound on the sensitivity of the output to numbers (we call these "the model's Greeks")?
- **RQ3 Deployment risk.** When a batch of new samples is clustered by event and the within-cluster dependence is unknown, given calibrated per-item error probabilities, what is the worst-case tail risk of the number of errors?

### 2.3 Why choose this problem

- **Only training from scratch makes it possible.** The information set, architectural constraints and numeric representation must all be decided before training and cannot be bolted onto an existing model. Small scale turns from a weakness into a precondition: certificates are only computable on small models.
- **It is the same style as Theodore's other research.** That other work is certified bounds for derivative pricing (proof-based price intervals for arithmetic Asian options, a joint pricing-error certificate for rough Heston) and critical budgets for Expected Shortfall under dependence stress. The new project should be able to reuse this method directly: define a quantity, prove a bound, give an executable certificate, and show on real data that the bound is non-vacuous.
- **The timing is right.** Point-in-time language models are a hot topic in finance research in 2025–2026. Many groups build such models; as far as our searches so far show, none has given proofs. You need to verify this.

### 2.4 Specific problems for this round (round 1)

1. **Is the direction novel?** Use literature questions Q1–Q32 to confirm or overturn the advisor's novelty hypotheses.
2. **What level is the current state really at?** Use the Phase 0 evaluation foundation to re-quantify the existing results, with confidence intervals and baselines.
3. **Are the certificates of the two main lines vacuous under realistic parameters?** Answer this with the derivation questions and the Phase 1 numerical feasibility analysis.

At the end of this round we need enough material to pass decision gate G1 and choose the flagship direction (see section 8 of `01_ADVISOR_MEMO.md`).

### 2.5 Final state of the project (what success looks like)

1. At least one **non-vacuous** certificate, computed on real data, with an executable checker.
2. A technical report (arXiv style) whose core is theorems, certificates and minimal experiments.
3. The repository reorganized into `theory/ certify/ pit/ synth/ models/ experiments/ legacy/`.
4. The old 24M Trial kept: moved to `legacy/` and labeled truthfully, not deleted.

---

## 3. How you work

### 3.1 Three types of tasks

The three types of tasks are independent of each other; you can open several Codex tasks and do them in parallel.

| Type | IDs | Content | Output location |
|---|---|---|---|
| Literature questions | Q1–Q32 | Survey and judge novelty | `research/answers/Qxx.md` |
| Derivation questions | T0–T3 (see `04_THEORY_NOTES.md`) | Make the propositions in the theory draft rigorous; prove or disprove them | `research/theory/Txx.md` (or `.tex`) |
| Work packages | WP0.x–WP3.x (see `06_WORK_PACKAGES.md`) | Code, data pipelines and minimal experiments inside the repository | Code on the branch + `research/reports/` |

### 3.2 Start and end of each task

- **At the start**, read in this order: `AGENTS.md` → this file → `01_ADVISOR_MEMO.md` → `02_PROJECT_SNAPSHOT.md` → the files related to the task.
- **At the end**, write the output using the templates in `07_REPORTING_PROTOCOL.md`, and add one line to `research/INDEX.md`.

### 3.3 Round 1 deliverables

The four items below can run in parallel. If there is only one Codex session, do them in this order:

1. **The 6 work packages of Phase 0.** This is the foundation; it has to be done whichever main line is chosen in the end.
2. **Derivation questions** T1.2, T1.3, T1.4, T1.5, T2.2, T2.3, T3.1. These do not need internet access.
3. **Literature questions Q1–Q32.** These need internet access.
4. **One round 1 progress report.**

---

## 4. Hard rules

### 4.1 Scope

- Work only in the `github.com/130U/130U-FinLLM` repository.
- Do not modify the `theodoreoy.com` website.
- Do not touch `130U/agent-evaluation-methodology`; it is left for later.

### 4.2 Git

- Work on the `research/certifiable` branch or on a branch based on it.
- Do not push to `main`, do not force push, do not rewrite history, do not delete old files. Old files are only moved, and the move is explained in the move record.
- Merging into `main`, changing the first screen of the README and publishing externally all need Theodore's approval.

### 4.3 Compute

- Assume **there is no GPU**. Every experiment must be smoke-testable on CPU, and a full run must finish within a few hours on a single T4 (16 GB).
- Before starting each experiment, write a compute budget estimate (GPU memory, time, token count) in the experiment record.
- If a direction cannot proceed without adding a GPU, stop and report back the minimal GPU requirement. Do not shrink the problem to force a fit.

### 4.4 Honesty

- Do not fabricate citations, numbers or experimental results.
- **Without internet access, do not answer literature questions.** Do only the derivation questions and work packages, and state in the report that there was no internet access.
- Label every number with its source tier: `full text` / `abstract` / `secondary` / `advisor memory` / `our experiment`.
- Distinguish three kinds of statements: the advisor's hypotheses, conclusions from the literature, and our own results. Do not mix them when writing.

### 4.5 Data and external services

- Do not commit private headlines, labels, checkpoints or weights to the public repository.
- Accessing SEC EDGAR requires contact information in the User-Agent. Use the value Theodore provides; do not make one up, and do not use an email address Theodore has not agreed to. If none is provided, stop at this step and write it into "Needs PI decision".
- Respect the data sources' licenses and rate limits.

### 4.6 Content

- Do not give investment advice. In this project a backtest is only a statistic, not a trading strategy.

---

## 5. Work focus (summary)

The full logic is in `01_ADVISOR_MEMO.md`. Only four principles are listed here:

1. **Foundation first, main lines later.** Until Phase 0 is complete, run no main-line experiments. Literature and derivation questions are not subject to this rule.
2. **Synthetic world first, real data later.** Every certificate is first checked for two things in a synthetic world where the ground truth is known: the certificate really holds, and it is not vacuous.
3. **Look for kill evidence first, invest later.** For each main line, first look for evidence that could kill it: someone has already done it, or the bound is vacuous under realistic parameters.
4. **About 60% theory, about 40% experiments.** Experiments are only used to test the premises of theorems or to show how tight a bound is.

---

## 6. What to do in these situations

| Situation | What you should do |
|---|---|
| You find that a direction has already been done by others | Stop engineering investment in that direction. Write a one-page "prior work vs. our difference" and send it back to the advisor. |
| The computed bound is vacuous | Do not tune parameters to force it. Report which link is weakest and causes it. That is a result in itself. |
| A GPU is needed to continue | Stop, and report back the minimal GPU requirement (memory, hours). |
| Existing claims in the repository do not match the evidence | Record it in `research/claims_audit.md`. Do not edit the README directly. |
| Theodore's private data or a decision is needed | Write it into the "Needs PI decision" section of the progress report, and continue with the parts that do not depend on it. |
| The advisor's hypothesis or formula is wrong | Point it out directly and give a correction. This is what you are expected to do; it is not an offense. |
| The conclusions of two tasks contradict each other | Report both; do not pick one yourself. |

---

## 7. Output directory

```
research/
  INDEX.md                 # one line per output: date, ID, file, one-sentence conclusion
  answers/Q01.md ... Q32.md
  theory/T1_2.md ...
  experiments/<id>/record.md
  reports/2026-MM-DD-round1.md
  claims_audit.md
```

---

## 8. If only one session is open, what to do first

1. Create the branch `research/certifiable` from `main`.
2. Create the `research/` directory and `research/INDEX.md`.
3. Do WP0.6 (claims audit) and WP0.1 (evaluation foundation). WP0.6 lets you understand the whole repository; WP0.1 re-quantifies the current results, and all later comparisons depend on it.
4. Then do derivation question T1.4 (the audit resolution limit). It is the shortest, and it decides whether the P1 main line is worth continuing.
