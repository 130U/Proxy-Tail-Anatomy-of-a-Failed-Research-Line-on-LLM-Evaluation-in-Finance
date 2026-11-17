# Decision note for Fable: what is worth continuing, and what may still be a toy

2026-11-16, round seven. This file is for the user to pass on; it has not yet reached Fable, and no comments from Fable have been received. The internal AI adversarial review cannot replace the advisor's decision.

**What most deserves review now is one narrow mathematical question: given a trusted document-influence structure, how much audit information is needed to certify a fixed statistic? But we have not proven that it has paper-level originality, nor that it requires training a language model from scratch.** The new [English technical manuscript](manuscript.md) puts the conditions, proofs, complete construction results and the strongest simple alternatives together; the [PDF](output/pdf/audit_budgets_working_report.pdf) is for reading, and the [independent review](../reports/paper_review.md) is for rebuttal. It is not a finished manuscript or a submission.

## Status of the five paths

| Path | Narrow object that can hold | Most critical rejecting control or gap | Current recommendation |
|---|---|---|---|
| [01 Information-set certificate](../paths/PATH_01_audited_information_set.md) | Statistic envelope for a fixed deletion comparator | Historical bytes, selection rules and a trusted shared core have not been proven | Keep the application goal; first separate out the provenance premises |
| [03 Audit design](../paths/PATH_03_audit_design_frontier.md) | Exact risk and cost within a fixed sampling class | A general non-rectangular count certificate can reproduce the direct method; the current main example can even be reached by a simple total-count gate | Continue narrowing it as a mathematical sub-question of 01; do not treat it as an independent flagship |
| [02 Numeric sensitivity](../paths/PATH_02_numeric_sensitivity.md) | Unit invariance, direction and width given semantic candidates | The labels of sign(x−b) can be solved by a rule; natural semantic coverage has no gold standard | First test whether the task needs learning, then decide the architecture |
| [04 Dependence-robust risk](../paths/PATH_04_dependence_robust_risk.md) | Conditional risk bound given true marginals and a dependence set | Calibration cannot identify true pointwise probabilities; the dependence assumption is not established | Supporting component; do not expand into a flagship for now |
| [05 Verifiable numeric programs](../paths/PATH_05_proof_carrying_numeric_reasoning.md) | Checking computation traces and candidate output envelopes | Correct execution does not guarantee semantic correctness; a rule program is a control that must be kept | Explore as a verification tool for 02 |

The original five in-depth reports are kept. The [comparison document](../paths/COMPARATIVE_ANALYSIS.md) records the full reasoning, compute budgets and rejection gates; this table does not pass off the five reports as five independent research families, and does not make the G1 choice for you.

## What this peer discussion changed

First, the strongest risk for the rectangle control is the **maximum** of the miss probabilities of the out-of-bound strata, not the Bonferroni sum. This was corrected earlier; this manuscript keeps using the stronger control.

Second, a safe non-rectangular count region that is issued only when all findings are zero can fully reproduce the risk of the method aimed directly at the statistic. So "the direct method beats first giving any count confidence set" is a wrong statement. What the existing theorem isolates is the cost of **a single rectangular intermediate commitment**.

Third, under the threshold-family balanced audit, the simple total-contamination-count gate K≤r−1 also reaches the same risk. So neither 88 versus 114 documents nor the asymptotic Ω(r) separation is enough to prove that modelling document positions is irreplaceable.

Fourth, positions may still be useful, but this must be proven separately. A small example derived after the review: three strata, 20 documents per stratum, failure only if two strata are affected, α=.05: the direct method's optimum is 38; the fixed-stratification total-count gate that only certifies K≤1 has optimum 48. The lower bound comes from the miss probability of putting two contaminated documents in any one stratum, and attaining 48 is verified by auditing 16 documents per stratum. This example is an exploratory mathematical comparison, not a pre-registered experimental success, and it does not settle prior work or real-world relevance.

The median saving over the complete 20 cells is still 0, and the original whole-family 20% investment gate was not passed. We have not used the new example to cover up this negative result.

## Please give three judgments first

1. **Is the contribution sufficient?** Is the narrow question above just a combination of standard composite testing, shard-poisoning certificates and audit design? If so, please name the minimum result that further investment would have to supply, for example a structural theorem that beats the strongest total-count gate, a tight lower bound for efficient computation, or an influence structure with real meaning. Without such a difference, we suggest ending it as a flagship.
2. **How should the train-from-scratch gate be handled?** Neither the current audit nor the numeric proofs require training an LM from scratch. Should the original hard gate be kept and these flagship candidates eliminated, or should it be formally revised to "assumptions controllable and simple methods irreplaceable"? We have not rewritten this criterion on our own.
3. **What should the next item prove?** If 01/03 continue, first fix strong baselines and a target class that can reject the method; if 02/05 continue, first give a text task with an exogenous basis for direction that rules cannot solve directly. Please specify one narrow target and a stopping condition, to avoid piling on more components.

The real-source task has trained word/char TF-IDF from scratch, with macro-F1 about 0.7920/0.7548. This shows that simple baselines are strong; it cannot prove that language pretraining is necessary. The old 24M row-level evidence cannot be recovered, same-task FinBERT/small-LLM controls are missing, and G0/G1 are still not passed. Source-date declarations, non-interference code, mathematical measurability and historical provenance evidence each carry different obligations and cannot substitute for one another.

The user asked to keep the research local. This round did no downloading, scraping, sending or public release; judgments about novelty go only as far as the existing local evidence and have not been completed into a full literature check.
