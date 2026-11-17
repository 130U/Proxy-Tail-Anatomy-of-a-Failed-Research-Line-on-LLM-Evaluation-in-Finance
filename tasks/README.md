# Task briefs

The advisor wrote one brief per task: the question, the data, the analysis, a decision rule fixed in
advance (continue, stop, or inconclusive) and a prior-art step. The briefs are kept as issued, so
words like "next", "continue" or "write the short paper" describe plans at the time, not the final
state. The final state of each task is in the table and in the [report](../report/proxy_tail_postmortem.pdf).

Stages A and B ran before this folder existed; their plans are in
[`research/advisor_reference/`](../research/advisor_reference/) and
[`research/tail_screening/methods_protocol.md`](../research/tail_screening/methods_protocol.md).

| Order | Brief | Question | What happened | Records |
|---|---|---|---|---|
| 1 | [absolute_scoring.md](absolute_scoring.md) | How stable is a model's own top list under repeated scoring? | 250 calls, 10,000 scores; formally inconclusive (tie gate) | [absolute_scoring/](../research/absolute_scoring/) |
| 2 | [T1_rounding.md](T1_rounding.md) | How many FinQA answers does the filing's rounding leave undetermined? | 196 / 1,147 test questions; continue | [t1_rounding/](../research/t1_rounding/) |
| 2 | [T2_magnitude.md](T2_magnitude.md) | Does sentiment respond smoothly to the size of a number? | Stopped at the prior-art check; no scoring | [t2_magnitude/](../research/t2_magnitude/) |
| 2 | [T3_combination.md](T3_combination.md) | How does a model combine good and bad news? | 3,360 scores; close to additive; closed | [t3_combination/](../research/t3_combination/) |
| 2 | [T4_cross_model.md](T4_cross_model.md) | Top-list overlap between a cheap and an expensive model | Not run (the tail line was closed) | — |
| 3 | [T1a_law.md](T1a_law.md) | A rule that predicts which questions are affected | Zero-parameter rule; matches the exact classification on 5,337 questions | [t1a_law/](../research/t1a_law/) |
| 3 | [T1b_tighten.md](T1b_tighten.md) | Kill test: does the rest of the document pin the answers down? | Only 1 question rescued; 139 survive review | [t1b_tighten/](../research/t1b_tighten/) |
| 3 | [T1c_models.md](T1c_models.md) | Does this change how models are scored? | No effect found | [t1c_models/](../research/t1c_models/) |
| 4 | [T1d_precision.md](T1d_precision.md) | Do models know how precise their answers are? | Yes, when reminded (98.4% accurate intervals); second review leaves 123 | [t1d_precision/](../research/t1d_precision/) |
| 5 | [T1e_full_test.md](T1e_full_test.md) | Extend to the full test set and a second dataset | Not run as a whole; the second-dataset part moved into T1g | — |
| 5 | [T1f_novelty.md](T1f_novelty.md) | Novelty check of five candidate claims | Four of five already had prior work | [t1f_novelty/](../research/t1f_novelty/) |
| 6 | [T1g_consequence.md](T1g_consequence.md) | Where does rounding precision have consequences? | Almost nowhere; the rule holds on TAT-QA | [t1g_consequence/](../research/t1g_consequence/) |

Tasks with the same order number were issued together and ran in parallel.

Cross-vendor replication and a human spot-check of the AI attributions were planned as optional
parts of T1e and were never done.
