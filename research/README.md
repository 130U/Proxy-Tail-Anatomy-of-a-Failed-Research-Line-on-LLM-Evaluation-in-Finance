# Research Records

One folder per stage or task. Folder names are kept from the working repository because the
analysis code refers to them. The table gives the stage each folder belongs to; start with the
"entry point" file of a stage, then follow its links to protocols and raw records.

The stage letters match the [report](../report/Proxy-Tail-Anatomy-of-a-Failed-Research-Line-on-LLM-Evaluation-in-Finance.pdf) and the route on the
[front page](../README.md).

## Stage A — Certifiable Financial Language Models

Nine rounds of theory, implementation and internal review on "certificates" for a small financial
language model, organised as five research paths. Closed because every component was a standard
tool and the strongest simple baselines matched the elaborate designs.

**Entry points:** [FABLE_FULL_REPORT.md](FABLE_FULL_REPORT.md) (integrated report of the nine rounds),
[paths/COMPARATIVE_ANALYSIS.md](paths/COMPARATIVE_ANALYSIS.md) (the five paths compared),
[START_HERE.md](START_HERE.md) and [INDEX.md](INDEX.md) (file-by-file index).

| Folder or file | Contents |
|---|---|
| [advisor_reference/](advisor_reference/) | The advisor's original brief, memo, literature map, research questions, work packages and decision log |
| [paths/](paths/) | The five research paths, their comparison, decision criteria and internal reviews |
| [theory/](theory/) | Proof notes: certificate basics, collective metrics, impact audits, localisation value, randomised audits, point-in-time non-interference, semantic envelopes |
| [reports/](reports/) | Round-by-round reports (rounds 1–9) and topic reviews |
| [literature/](literature/), [answers/](answers/) | Literature ledger, status of the 32 research questions, and written answers to seven of them |
| [planning/](planning/) | Audit-design computations: threshold, localisation and randomisation tables |
| [real_baseline/](real_baseline/), [experiments/](experiments/) | The SEntFiN entity-sentiment baseline (protocol, preparation, reviews) and experiment outputs |
| [local/](local/), [certificates/](certificates/), [checks/](checks/), [evaluation/](evaluation/) | Synthetic foundation experiments, the collective-metric checker, theory checks, reconstruction of the older model's metrics |
| [numeric/](numeric/), [pit/](pit/), [xbrl/](xbrl/), [data/](data/) | Numeric-envelope checks, point-in-time pipeline checks, a restricted local XBRL parser, the FOMC source audit and compute budget |
| [paper/](paper/) | The English working report from round 7 and its build records |
| [claims_audit.md](claims_audit.md), [claims_sources.json](claims_sources.json) | Audit of 46 public claims of the author's earlier financial language-model project |
| [FABLE_HANDOFF.md](FABLE_HANDOFF.md), [REPRODUCE.md](REPRODUCE.md), [reproduce.py](reproduce.py), [reproduction_log.json](reproduction_log.json) | Handoff notes and the offline reproduction runner for Stage A |

The Stage A workspace was created from the author's earlier financial language-model project,
[130U/RESEARCH-Financial-Large-Language-Model](https://github.com/130U/RESEARCH-Financial-Large-Language-Model).
Its material treated the advisor's plan as a
proposal to be checked, not as established results. The student worked offline after the first
round, so no SEC data were downloaded. All scripts run offline and download nothing.

## Stage B — Proxy Tail: Tail Screening with a Cheap Model

How wide must a cheap model's shortlist be to keep a fixed share of a reference model's top items?
Closed because the law was already known and the reference LLM did not agree with itself in the tail.

**Entry points:** [tail_screening/FABLE_ONE_PAGE.md](tail_screening/FABLE_ONE_PAGE.md),
[tail_screening/FABLE_CURRENT_REPORT.md](tail_screening/FABLE_CURRENT_REPORT.md).

| Folder | Contents |
|---|---|
| [tail_screening/](tail_screening/) | Theory and counterexamples, literature check, lexical baselines, the agent pilot, stage 1 (32 items) and stage 2 (128 items) protocols, reports, figures and analysis code |
| [private/agent_tail_pilot/](private/agent_tail_pilot/), [private/agent_tail_methods/](private/agent_tail_methods/) | Raw inputs and outputs of every agent ranking and pairwise run |
| [private/real_baseline/](private/real_baseline/) | SEntFiN entity rows, fixed splits, saved lexical models and per-row predictions (shared with Stages A and C) |

## Stage C — Absolute-Score Stability

Does one model agree with itself on its own top 10%? 1,000 headlines × 8 rounds, 10,000 scores.
Formally inconclusive (tie gate breached).

**Entry point:** [absolute_scoring/FABLE_ONE_PAGE.md](absolute_scoring/FABLE_ONE_PAGE.md). Task brief:
[../tasks/absolute_scoring.md](../tasks/absolute_scoring.md).

## Stage D — Two Behavioural Probes

| Folder | Task | Outcome |
|---|---|---|
| [t2_magnitude/](t2_magnitude/) | T2: does sentiment respond smoothly to the size of a number? | Stopped at the prior-art check; no scoring run. Entry: [FABLE_DECISION.md](t2_magnitude/FABLE_DECISION.md) |
| [t3_combination/](t3_combination/) | T3: how does a model combine a good and a bad fact? | 3,360 scores; close to additive; no mechanism to pursue. Entry: [README.md](t3_combination/README.md) |

## Stage E — Rounding Precision in FinQA

Filings print rounded numbers; benchmarks treat them as exact. How many answers does the displayed
precision fail to determine? Closed because the effect, although real, changes no official score.

| Folder | Task | Outcome | Entry point |
|---|---|---|---|
| [t1_rounding/](t1_rounding/) | T1: count the questions | 196 / 1,147 test questions (17.1%) | [FABLE_ONE_PAGE.md](t1_rounding/FABLE_ONE_PAGE.md) |
| [t1a_law/](t1a_law/) | T1a: a predictive rule | Zero-parameter rule matches exact classification on 5,337 questions | [ONE_PAGE.md](t1a_law/ONE_PAGE.md) |
| [t1b_tighten/](t1b_tighten/) | T1b: try to kill the finding | Survives; 139 questions after review | [FABLE_ONE_PAGE.md](t1b_tighten/FABLE_ONE_PAGE.md) |
| [t1c_models/](t1c_models/) | T1c: effect on model scoring | None found | [ONE_PAGE.md](t1c_models/ONE_PAGE.md) |
| [t1d_precision/](t1d_precision/) | T1d: do models know their precision? | Yes, when asked; second review leaves 123 questions | [ONE_PAGE.md](t1d_precision/ONE_PAGE.md) |
| [t1f_novelty/](t1f_novelty/) | T1f: novelty check of five candidate claims | Four of five had prior work | [README.md](t1f_novelty/README.md) |
| [t1g_consequence/](t1g_consequence/) | T1g: where does precision have consequences? | Almost nowhere; rule holds on TAT-QA | [ONE_PAGE.md](t1g_consequence/ONE_PAGE.md) |

T1e (extending to the full test set) was planned and not run; its brief is in
[../tasks/T1e_full_test.md](../tasks/T1e_full_test.md).

## Conventions in These Records

- "Fable" is the AI advisor and "Theodore" is the author; the student agents wrote most documents
  for them.
- "Pass", "fail", "continue", "stop" and "inconclusive" refer to gates written down before the data
  were seen. Gates were never moved after the fact.
- Numbers marked as AI review or AI adjudication come from AI models, not human annotators.
- Some files record SHA-256 hashes of other files. They refer to the original-language files, kept at
  commit [`e4b7bc0`](https://github.com/130U/RESEARCH-Proxy-Tail-Anatomy-of-a-Failed-Research-Line-on-LLM-Evaluation-in-Finance/tree/e4b7bc061976bcdd2f48c437172b034351ac7e77).
