# Path 01: from auditing real content versions to an interval for the clean model's statistic

Date: 2026-11-15. Nature: an independent project analysis, awaiting adversarial review by the senior assistant; the author of this document is not Fable and does not represent Fable's views. Everything is based on the literature checks and local evidence saved in this round; no new outreach was made. This document does not rank the other paths.

## Research question and target quantity

What this path studies is not "can a small financial model beat a large model", but: **when the historical availability times of the training corpus still contain residual errors, can actual audit records give a useful, executable test-statistic interval for a clearly defined clean comparator?**

Fix the historical cutoff date t, the observed training corpus D, and the whole training algorithm and its randomness. Each content version i has a recorded time τ_i and a true availability time τ_i*. The contamination set is C_t={i:τ_i≤t<τ_i*}. The clean comparator F_del is the model retrained after deleting C_t from D, keeping the other rules and randomness unchanged. It is not "the best model on the market at the time", and it is not automatically equal to the model "trained on all information available at the time".

The main target quantity is proposed, for now, to be accuracy on a fixed set of J text tasks frozen in advance, or macro-F1 over a fixed set of classes. The latter uses a contribution of 0 for zero denominators; one cannot reselect which classes to average after contamination changes the predictions. Backtesting here means a prediction statistic under historical information-set constraints; it does not yet include trading returns, Sharpe, or drawdown. The output is an interval [L,U], the source of randomness for coverage, all premises, the audit design, and the file identities, rather than a Boolean "no leakage=true".

Success needs two conditions accepted separately: mathematically, the interval covers S(F_del) with probability ≥1−α; scientifically, the interval is narrow enough for the target question and meaningful compared with simple alternatives. Zero error labels, very high classification accuracy, or all tests passing cannot replace these two conditions.

Two logically different claims must also be kept apart:

| Claim | Evidence needed | Name currently allowed |
|---|---|---|
| The statistic difference between the observed model and the "delete the specified bad records" comparator is enclosed | Fixed dependence graph, local influence, a valid audit of bad records, and a safe envelope | Conditional deletion-robustness certificate |
| This deletion comparator really is a model measurable with respect to the historical information set | In addition, historical evidence on the authenticity of content versions, historical selection/metadata, the shared core, and all training dependencies | Only once these premises are also established may it be called a no-look-ahead certificate |

The first can hold on its own while the second is unresolved. **Success on the first must not be named certified look-ahead freedom**; this is exactly the gap between the complete flagship and the components that can be executed now.

## Existing methods and the increment that might be gained

The saved full-text checks show: temporal non-interference already has a formalization; DPA already has stable sharding, deterministic training, and vote-margin certificates; Finite Aggregation and collective bagging already have structured/collective poisoning certification; auditing without replacement and confidence sequences are also mature statistical methods. [Literature ledger L01–L04, L08–L09](../literature/literature_review.md), [Q03](../answers/Q03.md), [Q29](../answers/Q29.md). Therefore none of the following can be a current contribution: the first definition of no look-ahead, the first conversion of error counts into vote robustness, the first union bound, the first computation of a hypergeometric interval, the first optimization over common contamination.

The increment that might be gained should be narrowed to: **a trustworthy contract for content versions and historical selection rules, the propagation from audit errors to the training dependence graph, computable envelopes for the non-additive statistics that actually matter, and the relation between audit cost and interval width on real sources.** Novelty must be counted per explicit problem that existing methods cannot provide directly, and must be established by a check of differences from the literature. The current CM1–CM5 and the checker make this interface reviewable, but by themselves they are not enough to claim that a new theoretical direction has been established.

An object more worth pursuing than "financial application + known components" is: under the same audit budget, can certificates that use the influence structure of different sources/shards systematically dominate certificates that use only the total contamination count? If the answer is only a constant-factor difference at the implementation level, it should be positioned as a rigorous application or a reproducible negative result, rather than packaged as new learning theory.

## Necessity of training from scratch: conditionally necessary, not universally necessary

P1 requires that every source training depends on be traceable, including the tokenizer, deduplication, selection rules, label generation, hyperparameters, and shared features. General pretrained weights whose sources cannot be audited do not automatically satisfy this premise; building a small model from random initialization is indeed the implementation route that is easier to control under current local conditions.

But "every information-set certificate must train from scratch" is a false statement. An existing encoder whose sources really all pass the same historical contract can also be used; fixed lexical/character features do not even have a pretraining history. Random initialization by itself also does not prevent training the vocabulary on future text or choosing hyperparameters with future labels. What is really necessary here is **complete control of historical dependencies**.

The strongest opposing explanation is: the model is just an expensive carrier for known poisoning-audit theory, and sharded logistic regression on TF-IDF or fixed hashed features can already demonstrate the whole certificate. If the real text task does not require language representations, this explanation should be accepted, and the certificate completed first with a simple model; there is no evidence that a new transformer must be added. If one wants to keep "a small language model" as the core of the paper, one must show that language representations provide a measurable use on the same task, rather than creating innovation through the model's name.

## Full assumptions and candidate propositions

The following conditions cannot be omitted implicitly:

1. Content versions, record IDs, the population W, and the cutoff date are frozen; the definition of true availability time can be audited, rather than mixing crawl time, meeting date, and publication date into one field.
2. The shared core and all shared components have no future contamination, and the selection/metadata mechanism itself is historically measurable. Deleting future content alone is not enough: future bits can leak through "which old documents are kept"; see the counterexample in [T1.1](../theory/notes.md).
3. Suspect periphery records act only on their fixed shard; there is no cross-shard normalization, global early stopping, global reweighting, or suspect periphery updating the shared backbone. Deleting one document affects at most one head; if a modified ID moves across shards, the budget must be enlarged accordingly.
4. Each head is a deterministic function of its shard's data, fixed exogenous randomness, and the qualified core; the identity of the code/runtime environment is traceable.
5. The audit is carried out on a fixed population using a specified random design without replacement; human error judgments are correct, or there is a separate verifiable misjudgment model. The current exact fixed-n interval cannot continue to be used after arbitrary stopping.
6. Test samples, true labels, the class set, the target quantity, and the denominator are frozen; the historical availability of the inputs at prediction time is checked separately, and test labels do not enter training selection.
7. The computation returns the complete outer envelope; while a combinatorial search has not finished, partial search extremes cannot be used as bounds; rational endpoints or outward rounding cover numerical error.

**Candidate main theorem P1-A (a conditional combination of existing components, not listed as original).** Assume the conditions above hold. Let K*=|C_t∩W|, and let audit inversion give P(K*≤K_u)≥1−α. For every common subset B that can affect at most min(K_u,m) heads, compute a safe envelope of the fixed test-set statistic S and take the outer extremes. Then

```math
\Pr\{S(F_{del})\in[L(K_u),U(K_u)]\}\ge1-\alpha.
```

Proof sketch: on the event K*≤K_u, the whole computation for unaffected shards is the same; the clean prediction vector belongs to the set of vectors allowed by the certificate optimization; the interval holds for each element of that set. Accuracy and macro-F1 are both derived from the same event, so reporting them together does not pay two separate α. The envelope is an outer relaxation that allows arbitrary cross-point outputs for any affected head, so solving that relaxation exactly is not the same as describing the real retraining exactly.

**A destructive control that is required.** Deliberately let the suspect periphery train a shared tokenizer, then delete one document that changes the vocabulary. Now several heads can change together, and the K documents→K shards proof fails. If the experiment still outputs the same kind of "certificate", the checker's premise verification is incomplete. Similarly, there should be attack cases with modified IDs, cross-shard normalization, and screening controlled by future information.

## What the existing code actually supports

- The [theory notes](../theory/notes.md) and the [derivation of collective statistics](../theory/collective_metrics.md) already give conditions, counterexamples, and proofs; the [independent theory review](../theory/independent_review.md) found no substantive error within the listed scope, but it did not prove source authenticity.
- `research/local/audit.py` has an exact hypergeometric upper bound and rational computation; `research/certificates/collective.py` has accuracy and macro-F1 component envelopes for a shared head set, plus a small-scale exact DP; when the search exceeds its limit it refuses to issue a certificate.
- The hand-made four-point example in the [collective experiment](../experiments/collective_metrics/report.md) shrinks the pointwise `[0,1]` to accuracy `[1/4,3/4]` and macro-F1 `[1/5,11/15]`. This is a counterexample showing that the algorithm can tighten the bound, **not a real language-model result**.
- The [independent implementation review](../literature/collective_review.md) reran 7 checks and separately verified 112 direct vote-change examples; the [round 2 report](../reports/2026-11-15-round2.md) summarizes 36 integration tests. Finite checks support the soundness of the implementation; they do not replace a proof over the whole domain or a real audit.
- There is not yet a really trained shard prediction matrix, a sampling audit of real timestamps, a real clean-retraining control, or a non-vacuous certificate on an actual historical corpus. The existing G0/G1 status cannot be skipped because mathematical components were added.

## Real local data: raw material exists, the certificate ingredients are not yet complete

The [local inventory](../reports/local_data_inventory.md) confirms 120 FOMC texts of about 6.98 MB; 120 local HTML snapshots match the manifest hashes; each has its source, publication date, crawl date, and text and HTML hashes, and the local license record marks it as public domain with training allowed. There are also 28,486 Wikipedia snapshot texts and the SEntFiN raw candidates. So training a new model from scratch does not depend on the old checkpoint, and simulation is not forced by a lack of real source text.

But the local FOMC files are versions crawled in 2026. Showing a 2011 publication date does not prove that the same bytes existed in 2011; the meeting date is also not the publication date. Wikipedia has no per-article historical publication time and should not be added to the historically trusted core without checking revision history. The old derived SEntFiN set is explicitly a private non-temporal pilot, with no proper event audit or historical times; ready-made sentiment cannot be taken as the needed author-stance ground truth.

There is another gap that is easy to miss: FOMC minutes provide real financial language, but do not automatically provide task labels that are independent, large enough, and actually require language understanding. If rate up/down/unchanged can be extracted mechanically from fixed numbers, a symbolic rule may already solve the task. One can study contextual comparison benchmarks, attribution to a subject, or stance across different paragraphs, but that requires a new labelling specification and human review; one cannot switch temporarily to template recognition to get a non-vacuous interval sooner.

If only locally saved files are used, one honestly executable boundary is a real-text certificate prototype "conditional on the existing version-time records being correct"; it must be kept apart from "real historical no-leakage certified". Insufficient evidence on historical versions is one of the weakest links of the current complete flagship.

## Three-stage minimal validation and resource estimates

Everything in the table below is a **forward-looking estimate, not performance or timing already measured**. No GPU is assumed to be available now; any GPU quota is first estimated from short local CPU runs; the current offline boundary is not bypassed.

| Stage | Concrete work and acceptance output | Resource estimate and stopping rule |
|---|---|---|
| A: freeze the object of study | Grade the source/version-time evidence for the 120 local FOMC documents; extract one explicit text task and set up a labelling specification with at least two annotators or independent review; the split unit is a whole set of minutes/an event, and the final test events are held back first | File checks within 15 CPU minutes; manual source evidence and the first batch of labels about 6–12 hours, to be calibrated by timing the first 10 records. Records whose content-version date cannot be determined are listed as unknown and cannot be assumed clean |
| B: minimal complete chain | First train fixed lexical features + sharded linear heads; freeze the corpus, model, and audit design at small scale. Verify coverage with real text and controlled injection; then compute intervals on real time-audit inputs | CPU preferred; m∈{5,11,21}, with head training and small-scale solving limited to 30 minutes at first. If public complete labels are insufficient, first report only a constructive/conditional prototype, not "real certificate completed" |
| C: test language-model necessity and real non-vacuity | A new randomly initialized small encoder of 0.5–3M parameters; train only on the qualified core, then freeze, keep the same task/audit design, and compare with the linear baseline. Finally give a three-way table of audit size–width–task utility | First a 5–15 minute CPU throughput trial; full training is planned to be capped at 2–4 hours on a single T4 with ≤16 GB of GPU memory; these figures are not yet verified. With no usable GPU or throughput over the limit, shrink to the smallest model that still does useful work; do not fill unrun results into the table |

The amount of real labels is not judged sufficient by convenient numbers such as "200 rows": FOMC has only 120 document units, and the number of paragraphs cannot be taken as the number of independent samples. Task difficulty, event coverage, and audit evidence should first decide whether it is worth going to C. If a complex head only improves dev-set performance and cannot improve the valid certificate on the frozen test, stop at the simple method.

## Ex ante decision rules for the next small trial (a proposal, not a frozen run)

These rules are only for deciding whether to keep investing in this path; read them together with the [common decision proposal](DECISION_CRITERIA.md). Because the task labels, the historical cutoff date, and the evidence standard for deciding version times have not yet been chosen, **no new experiment has yet been pre-registered under the thresholds below**. Stage A must be completed first, writing the specific data IDs, source contract, task, simple baseline, code identity, and budget into the experiment record, and then one frozen small trial is run; one cannot pick the easiest target to pass after seeing the results.

### Hard gates for correctness and sources

1. The first main metric is fixed as **the clean-comparator interval for accuracy**, with an overall audit failure budget α=0.05; if there are also core/auditor misjudgment steps that are treated probabilistically, their budgets count within this 0.05. Sources that are still conditional assumptions are not additionally assumed to have "zero failure probability", and the output keeps the name conditional deletion robustness.
2. For every contamination configuration in the pre-specified small-scale exhaustive check, when the real influence budget is used, the deterministic envelope must contain all allowed clean outputs; a single failure to contain stops the work for debugging. Statistical inversion is tested for coverage ≥0.95 over the complete sampling distribution; **every individual sample is not required to cover, and zero failures in finitely many trials cannot replace a proof of coverage**. Illegal ID migration, changes to shared components, and searches over the limit must refuse certification or explicitly enlarge the threat set.
3. The audit status of real documents must include "undetermined". Records lacking a basis for the historical version cannot be recorded as clean; even if all 120 are examined, a census only removes sampling uncertainty and does not automatically remove the undecidability of the historical truth. Before finally claiming historical no-look-ahead, the evidence gate for historical versions and selection rules must also be passed separately.

### Provisional gates for scientific usefulness

When the task is frozen, one must explain why it is not solved directly by a simple symbolic rule, and keep an event test set never used for model/threshold selection. **At least 40 distinct meeting/event units** is proposed as the operational minimum scale for this scientific-usefulness trial; this is a design constraint that keeps the counting step of accuracy no larger than 2.5 percentage points, **not a guarantee of independence, statistical power, or population generalization, and not a mathematical condition for the certificate to hold**. If only a smaller test set, or one with only a single real class, can be obtained, implementation checks are allowed, but no verdict on whether the language model is useful is drawn from it. The document-ID budgets for training, development, source audit, and testing must be listed together; the 120 local documents cannot be promised repeatedly to each step.

After passing the hard gates above, the proposed main criterion is: under an audit design fixed in advance, the real-text trial has **U−L≤0.10**, and at least one pre-specified complete setting with contamination budget ≥1 meets this condition. The budget ≥1 check is to exclude trivial certificates that only show "no change is allowed"; it cannot be manufactured by reducing the audit size after the fact, modifying the trusted core, or picking the points with the largest vote margins. If this real audit happens to give K_u=0, report its certificate as it is, and leave "usability under a nonzero budget" to the pre-specified stress verification, without changing the identity of the result.

A narrow interval must also exclude a useless constant model. For this, freeze a constant predictor and its label-selection rule in advance using dev data; let its accuracy on the same fixed test set be S_const. To claim an informative task conclusion, require **L>S_const**; this is a fixed-test-set comparison, not a population significance test. Also freeze a strong simple **core-only qualified baseline**, and report its score S_base, [L−S_base,U−S_base], and the total cost; do not compare interval width alone. If the baseline uses the same uncertain periphery, it must be given its own clean envelope; its observed score cannot be treated as the contamination-free truth. A drop of 5 percentage points relative to core-only can be listed as a discussion point for utility cost, but **an arbitrarily pre-set 5 percentage points is not used as a one-vote veto of the mathematical branch**; whether the cost is acceptable depends on the actual use of the frozen task and the new information the certificate provides.

A width of 0.10 allows up to 10 percentage points of uncertainty in the clean statistic, which can serve some coarse-grained judgments of usefulness; it may still be too wide, and cannot identify model gains of a few percentage points. Under class imbalance, the "random level" is not a reliable reference, so the task gate uses the actual score of the frozen constant predictor. 0.10 was chosen to make one constrained small trial convenient; **it is not a threshold supported by data, and not a publication threshold**. If the final scientific question requires distinguishing a 2-percentage-point difference, the target must be tightened in advance; one cannot keep 0.10 and then claim a finer question has been solved.

The same frozen result must show the width gates {0.05,0.10,0.20} together, and place the utility cost relative to core-only at three discussion scales {0.02,0.05,0.10}, without retraining or choosing test points to suit any cell. The main decision is still width 0.10 and L>S_const; the three cost scales are not added veto gates. If the width holds only in the loosest cell, record it as sensitive, not as passing the main gate. The fraction of robust predictions is a separate diagnostic; **no mandatory fraction gate replacing the accuracy width is set**, because a collective statistic can still have a non-trivial interval when there is no pointwise stability.

Decision outcomes are recorded separately: hard gate fails→stop issuing certificates; hard gates pass but the width/usefulness gate fails→keep a rigorous negative result and do not upgrade to a real-model flagship; all proposed gates pass→continuing to more complete source, novelty, and actual-budget verification is allowed, and this still does not mean G1, population generalization, or submission quality has passed.

## Strongest simple baselines and alternative explanations

1. **Trusted-core-only model.** Give up the suspect periphery entirely and avoid its audit cost. P1 must show that admitting the periphery is worth it in task utility or data cost; otherwise the complex certificate chain has no practical design necessity.
2. **Full audit/direct deletion.** Locally there are only 120 FOMC documents, and reviewing each one may be cheaper than designing a sequential audit. When the data are small enough for a census to be feasible, one cannot inflate N artificially to manufacture a statistics problem.
3. **Fixed character/lexical features + sharded linear heads.** It has the same contaminated-head budget and removes the weak link of a shared language-model history; it should be run first, not treated as an auxiliary weak baseline.
4. **Same-budget implementations of pointwise DPA and collective bagging.** Only width/cost improvements under the same corpus, sharing conditions, and target quantity are valid comparisons. One cannot compare this document's exact DP with a crude formula deliberately used for the competitor and then call the new theory tighter.
5. **Bounded soft-score aggregation.** If the target is changed to the average of each head's bounded loss, arbitrary changes in k heads directly give a shift bound of at most k/m. It evaluates a different pre-defined statistic and must not be confused with voting macro-F1; but if it already answers the scientific question, complex discrete certification may not be needed.

## Rejection conditions, negative results, and the weakest link

The real rejection conditions include: the target ground truth does not depend on language and a symbolic rule is enough; trustworthy conditions cannot be established for historical content versions while the conclusion still requires absolute historicity; a small amount of core uncertainty makes all heads variable; real nonzero audit findings make the interval under every reasonable budget close to the trivial range; prior work covers the same difference; or "drop the suspect periphery" is cheaper at the same utility.

A loose bound need not reject automatically, but one must explain whether it comes from unavoidable audit resolution, small model vote margins, too wide a set relaxation, or insufficient source authenticity. Lumping the four together as "the model is too small" has no scientific value. A valuable negative result is: for an explicit real corpus and budget, prove/reproduce which condition blocks the certificate, and give the minimal condition that could close it, or evidence that it cannot be closed.

The current weakest link is **the pairing of historical-version availability with qualified task data**, followed by the task utility of sharded models on a small corpus. The existing combinatorics, DP, and program unit tests are no longer the main obstacle. Continuing to expand the checker without dealing with these two weak links would turn this back into a project with "many frameworks and no evidence on the core question".

## Concrete review questions for the senior assistant

- Is the deletion comparator F_del exactly the economic/statistical object the paper needs to explain? If what really matters is "the best model available at the time", the current certificate does not answer it.
- Is a conditional certificate on real sources acceptable as an intermediate result, with the external assumption about historical versions made explicit? What kind of result is enough to upgrade to the final information-set conclusion?
- Is there a substantive reason for the original task to center on macro-F1, or is it only inherited from the old sentiment task? Changing the target quantity requires rewriting the research question first, then comparing methods.
- Does using a shared core + small periphery heads weaken the "contaminated language model" question too much? If contamination affects only linear heads, reviewers may think the hardest part has been avoided.
- For the small FOMC set, do full review and the core-only baseline already make complex statistical auditing unnecessary? And if it is extended to unverified sources, would that destroy trustworthiness?
- Which difference is worth a new theorem: tighter statistic envelopes under an influence graph, lower bounds on audit cost, or the propagation of shared-core uncertainty? One cannot pursue all three at once with an engineering plan in place of a research choice.

## Feasibility conclusion and uncertainty

**Feasibility of the mathematics and the local prototype: fairly high; feasibility of a complete real historical certificate: conditional, moderate; publication-grade novelty: undetermined.** This is not a priority ranking. The existing proofs and code are enough to rule out some wrong arguments, and enough to support the next small real experiment; they are not yet enough to confirm that the flagship's scientific question and data conditions both hold. The most reasonable next step is to do the object/source gate in A first, rather than immediately scaling up the model or claiming "a certifiable financial language model is done".
