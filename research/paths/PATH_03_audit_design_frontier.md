# Path 03: The audit-cost–certificate-width frontier driven by influence structure

**2026-11-16 round 9 addendum:** The [exact solution under arbitrary randomized designs](../theory/randomized_audit.md) removes the fixed-quota restriction. Under homogeneous r-of-d, correct audits, ground truth fixed in advance, and a fixed interval that is always issued when all findings are zero, simple random sampling of whole strata plus one partial stratum attains the minimax lower bound. The total-count gate also uses the same class of randomized designs, and pooled SRS is optimal for it; the [full 32-cell table and review](../reports/2026-11-16-round9.md) keeps all comparisons and the zero added gain of the conjunctive family. The adaptive hard cap and the clean-world expected budget can be extended, but must not be swapped in for the expected cost in a bad world. Outside the applicable family, novelty, historical ground truth, and the necessity of training from scratch are all unresolved; exact conditional mathematics is not treated as passing as an independent flagship.

**2026-11-16 round 8 addendum:** [LV1–LV5 and their boundaries](../theory/localization_value.md) give the strongest fixed total-count gate algorithm, an upper bound on location gain / conditions for no gain, and a sharp construction; [all comparisons and the review](../reports/2026-11-16-round8.md) also include min(Box,TotalK) and out-of-class pooled random sampling. A sharp gain under fixed quotas is not an advantage over all feasible audits; a real-world fixed-quota constraint has not been established, and this is the key gap in the current 03 topic. On the old 20 cells the median gain relative to the strong simple combination is 0; the new construction was not used to retroactively declare a gate passed.

**2026-11-16 round 7 addendum:** The [consolidated draft](../paper/manuscript.md) and the [paper-level adversarial review](../reports/paper_review.md) add stronger simple comparisons. A general non-rectangular safe count region is equivalent to the direct method; the balanced total-contamination gate already achieves 88 vs 114 on the main example and an Ω(r) separation relative to the rectangle, so these cannot be used to show that location modeling is necessary. Three strata of 20 documents each give 38 vs 48, another strict difference relative to the fixed total K≤1 gate, but it does not beat all counting methods, much less count as success of a pre-registered experiment or as evidence of originality. The original research question below is kept; the next step must narrow it against these stronger comparisons.

Date: 2026-11-15. Nature: an independent project-proposal analysis, pending review by the senior assistant; this document does not represent Fable or any other external advisor. Positioning: **a mathematical branch of P1, not another independent flagship**. Fully offline; evidence comes from saved verification of the original papers and from local experiments. This file does not rank paths up front.

## Research question, target quantity, and why it might have independent value

The full P1 requires a certificate for the final true information set; this path extracts only one question from it that can be studied rigorously: **given a frozen training influence structure, observed predictions, and a target statistic, what is the minimum audit cost needed to shrink the certificate interval to a specified width? Can information about different sources, shard locations, and audit order systematically reduce the cost while keeping validity in finite samples or under arbitrary stopping?**

The original "about 3N/n" only describes the scale of the upper bound on total contamination under a uniform fixed sample size, zero findings, and a small sampling fraction. It ignores which shards the contamination is in, which shards affect the target statistic, whether the true vote margins support robustness, and whether one source is more expensive or harder to judge. So the target can be changed from "estimate K as accurately as possible" to "directly bring one specific model conclusion to a pre-set precision".

There are two kinds of candidate target, and they must be kept apart:

1. **Fixed-design conditional frontier.** Choose the audit size n or stratified n_h in advance; find the minimum deterministic cost Σ_h c_h n_h needed to make the interval width W=U−L≤w under a specified observed outcome (most simply, zero findings). This does not guarantee that zero findings will be observed, and it is not an expected cost.
2. **Sequential decision frontier.** The auditor picks the next object based on the records audited so far, using simultaneously valid confidence sets; under real contamination scenarios or an explicit prior, study the distribution of stopping time and cost to reach W≤w. To call anything minimax or optimal, one must state over which contamination configurations the worst case is taken, and the reference class for impossibility.

Only the second kind legitimately allows "stop once there is enough evidence". Recomputing the fixed-n formula of the first kind repeatedly until it passes is a coverage error, not an algorithmic improvement.

## Existing methods and the increment we could aim for

The saved full texts show that Waudby-Smith–Ramdas already constructed hypergeometric confidence sequences for sampling without replacement; Shekhar et al. already studied weighted financial audits, auxiliary information, and test martingales; DPA, Finite Aggregation, and collective bagging already have structured optimization of contamination influence and joint prediction. [Literature ledger L02–L04, L08–L09](../literature/literature_review.md), [Q30](../answers/Q30.md). So current evidence supports none of "the first sequential audit", "the first use of risk weights", or "the first to connect confidence intervals to deterministic bounds".

The exact integer inversion in the existing `minimum_zero_audit` is also just a useful interface to mature hypergeometric inversion. It fixes approximate numerics and boundaries, and does not naturally upgrade into a new statistical theorem. Any research increment we could aim for must be about a more specific object, for example:

- **Audit complexity that depends on the influence graph.** With the same contamination count and the same population size, can the amount that must be audited differ by an explicit order under different document → head → test-point structures? Can we give both an achieving algorithm and a matching lower bound?
- **Audit aimed directly at the final claim.** Compared with first estimating the total K and then doing worst-case propagation, does directly testing "there exists a contamination configuration that is enough to push the target statistic out of the interval" strictly save samples without extra assumptions on the contamination distribution?
- **Valid and computable adaptive stratification.** When stratum allocation changes with known costs/structure or with audited results, how do we keep coverage and avoid enumerating all contamination sets? Existing confidence sequences can provide the statistical basis; the contribution must lie in the specific structure and computational guarantees.

These are currently candidate questions, not original results already obtained. If the existing audit literature solves them completely once "reporting error" is replaced with "influence on a model statistic", we should admit this is a transfer application and put it back in a P1 appendix rather than build a separate mathematical flagship.

## Is training from scratch necessary?

**This path itself does not need training from scratch, or even a neural network.** Its inputs are a fixed influence map, votes/scores, and a definition of the statistic; an already trained and traceable model, a rule system, or a sharded linear classifier can all provide them. So it cannot be used to argue that "training from scratch is necessary for research value".

Its relation to training from scratch is experimental control: to know clearly in P1 where contamination could have influence, small models and stable sharded training make it easier to build a complete dependency graph. But if the theoretical contribution holds, it should hold for a wider class of systems. An opponent might also point out: since we can design the system, we should first keep shared components away from suspect sources and reduce the complexity of the influence graph, which may be more effective than optimizing the audit. This must be included as a co-design baseline, instead of treating a complex influence graph as an unchangeable fact of nature.

## Assumptions, established starting point, and counterexamples

### Exact starting point for fixed n

Fix N suspect versions, audit n of them uniformly without replacement, and find zero mislabels. α is fixed in advance and audit judgments are correct. If the certificate can tolerate at most B contaminated documents, 0≤B<N, then

```math
K_u(0)\le B\iff
\frac{\binom{N-(B+1)}n}{\binom Nn}\le\alpha.
```

The right-hand side is monotone in n, which gives the exact minimum integer sample size. For pointwise vote stability, B can be obtained from order statistics of the per-point vote-margin radii; but the stable-prediction fraction is not accuracy, nor is it the macro-F1 interval width. If the target becomes a width w, the tolerable budget B(w) must be redefined using the actual envelope function.

**Counterexamples and design implications.** If K=1 can fall in the shared backbone's training data, it can affect all heads; the same K=1 confined to one fixed small shard has limited influence. The same total K does not mean the same audit value. Another counterexample is tie-breaking toward the lowest-numbered class: with m=2 and both heads voting 0, the prediction stays robust even if one head is allowed to change; so the gate m≥2K+1 without tie semantics is not a general necessary condition.

Every method must also specify: decidable ground truth for version time; the model/test samples frozen before the audit; fixed IDs or an explicit multi-head influence set H_i; how strata and sampling probabilities are determined; whether audited records are removed from training; and how human misses are handled. Without these, there is no sampling distribution to invert.

## Candidate proposition D1: a fixed stratified zero-finding test that calibrates the final interval directly

This is a fully provable research interface, used to state what we want to compare; its proof is a direct application of finite-population sampling and composite hypothesis testing, and **originality cannot be claimed on the basis of this proposition alone**.

**Setup.** Before the audit, fix disjoint strata W_h of size N_h; in each stratum, independently draw n_h objects uniformly without replacement. Given the head set H_i that each document may influence, fix the observed model and the target statistic S. For any true contamination set C, let B(C)=∪_{i∈C}H_i. Let a reliable outer envelope A(C) denote all possible values of S when the heads in B(C) change arbitrarily. If shared components may change, the corresponding H_i must truthfully cover all affected heads; edges must not be dropped to get a tighter bound.

Before the audit, fix the interval to be reported, I=[ℓ,u], and define the set of bad configurations

```math
ℋ_I=\{C:A(C)\not\subseteq I\}.
```

Each stratum's sample size is a fixed integer 0≤n_h≤N_h. If the bad-configuration set is empty, its maximum miss probability is taken to be 0 by convention; the relaxed model has then already determined that all configurations fall in I, and no audit is needed. All actual contamination influence must still be enclosed by A(C); unmodeled historical selection leakage or changes in shared state cannot be repaired by this test.

If

```math
\sup_{C\in ℋ_I}
\prod_h\frac{\binom{N_h-\left\vert C\cap W_h\right\vert}{n_h}}
{\binom{N_h}{n_h}}\le\alpha,
```

then the following procedure covers S(F_del) with probability at least 1−α: report I when every stratum's audit has zero findings; otherwise report the full range of the statistic or explicitly abstain.

**Proof.** Fix the true contamination set C*. If S(F_del)∉I, the reliability of the outer envelope implies C*∈H_I. A necessary condition for the procedure to fail in this case is that every sample misses C*. Since sampling is uniform without replacement within strata and independent across strata, the probability of this event is exactly the displayed product, which is at most the supremum over bad configurations, α. If S(F_del)∈I, a zero-finding report cannot fail. This holds for every fixed C*, so it is frequentist coverage, not a prior probability over contamination locations. QED.

**Relation to the existing budget gate.** With a single stratum and "bad configurations" being exactly |C|≥B+1, the miss probability decreases with the contamination count, the supremum is attained at B+1, and this reduces to the existing exact gate. If H_I uses shard locations and the test target, direct calibration may be tighter than first giving each stratum α_h and then taking a rectangular confidence set over the per-stratum K_h, but this needs an actual proof/measurement; one cannot assume it always strictly dominates.

**Candidate research optimization.** Given a fixed admissible family of intervals and costs c_h, find the minimum Σ_h c_h n_h such that the inequality above holds and |I|≤w. I, the strata, and n_h must be fixed before sampling. Possible contributions are a computable characterization of this composite bad set, the structure of worst-case configurations, and provable approximate optimization or lower bounds; none of this is implemented yet, and we have not ruled out that existing risk-limiting audits cover it directly.

**Risks.** If, after seeing which records were drawn and that no errors were found, one then picks an I that passes more easily, the proof above is not automatically valid. If the audit misses errors, the zero-finding probability no longer equals the product of binomial coefficients. Drawing "the most suspicious documents" while still using the uniform formula is equally invalid.

## Candidate proposition D2: passing valid confidence sets to certificate width under arbitrary stopping

Let the true contamination configuration C* be fixed, and let the audit produce a sequence of simultaneous confidence sets G_t satisfying

```math
\Pr\{\forall t,\ C^*\in G_t\}\ge1-\alpha.
```

At each time compute L_t=inf_{C∈G_t}inf A(C) and U_t=sup_{C∈G_t}sup A(C). If the computations of G_t and A(C) are both reliable, then for any data-dependent stopping time τ, with probability at least 1−α, S(F_del)∈[L_τ,U_τ]; the proof is containment at each time on the same simultaneous coverage event, followed by choosing τ. The stopping rule can be set to U_t−L_t≤w or budget exhaustion.

This passing step is itself straightforward; **the hard part is constructing a G_t that is valid and computable under the actual sampling strategy**. Confidence sequences with a fixed mechanism per stratum can give an initial rectangular set; predictive choice of the next stratum, non-uniform sampling, and ordering based on model influence must each be matched, condition by condition, to the corresponding martingale/confidence-sequence theorem. The existing local code has no confidence sequence for general nonzero findings, and has not shown that adaptive influence-first sampling is valid.

One should not impose the assumption that the truly "most harmful documents" are more likely to be mislabeled; if this association is unknown, it can only serve as auxiliary information to improve efficiency, and must not be smuggled into validity. If an adversary places contamination exactly in an underestimated region, the certificate should still cover.

## Existing implementation and actual numbers

The [audit planning record](../planning/record.md) and `research/planning/audit_frontier.py` implement the exact minimum n for a zero-finding fixed sample size; inputs support integers/Fraction, approximate probabilities are not used to shift boundaries, and the code checks that n passes and n−1 fails. 8 local tests cover exhaustive enumeration for small N, monotonicity, ties, and invalid inputs. This module **is not an anytime-valid tool, and it does not implement general versions of D1/D2**.

In the existing hand-designed example with N=1000 and m=11, target certified fractions of 1/3, 1/2, 2/3, and 1 need zero-finding audit sizes of 393, 527, 777, and 950 respectively. [Full results](../planning/frontier_results.json). These use hand-set vote counts and a hypothetical population, not real FOMC/EDGAR observations. The 950 example shows that a point with zero vote margin requires ruling out K=1, which at 95% confidence requires sampling 95% of the population; this is an explicit design cost, and must not be misread as meaning there must actually be zero errors or that the audit succeeds with probability 95%.

`research/certificates/collective.py` can serve as a width oracle: given a joint head set, it computes the envelope of a fixed statistic; the state explosion of exact mode and its subset-enumeration limits are documented. The [collective theory](../theory/collective_metrics.md) shows that some real target quantities respond to location/joint constraints. The next step is to replace "total budget k" with "the influence sets allowed by the audited evidence"; merely enlarging N in the existing example and drawing more contour lines does not count as deeper research.

## Local data and observability of cost

The 120 FOMC documents in the [inventory report](../reports/local_data_inventory.md) are a real source available offline right away; the source time fields and HTML hashes are enough to build an audit task list and to time "how long it takes to judge whether a version is historical". But they do not automatically provide ground truth for timestamp mislabels: the historical revision status of pages scraped in 2026 is still uncertain. For records that cannot be judged from the local snapshots, the correct output is undecided, which must not be counted as an error-free audit.

The existing Wikipedia data has no per-article `published_at`; it can serve as a real comparison for an "evidence-poor source", but real mislabel labels must not be fabricated for it. The same applies to the SEntFiN sources that lack times. Synthetic contamination can validate the statistical coverage and power of a method, but real audit cost, source missingness rates, and decidable fractions must come from real records.

One practical objection to this path is strong: with only 120 FOMC documents, a census may be cheapest, and stratified/adaptive algorithms cannot save much human effort. The mathematical branch can only be practically necessary under an explicit task scale, heterogeneous judgment costs, or a complex dependency graph. A hypothetical corpus of 100,000 documents must not be used to hide the fact that the current scale is small.

## Three-stage minimal validation and budget estimate

Everything below is **a resource estimate not yet executed**; this path needs no GPU and no new language-model training.

| Stage | Experiment design and acceptance | Estimated budget |
|---|---|---|
| A: Offline structure theorem and small-scale exact comparison | Fix 2–4 source strata and an enumerable document influence graph; compare the total-K gate, the stratified union-bound gate, and the D1 direct bad-configuration gate; cover all contamination configurations, not just a few randomly tested good examples | Capped scan of 30–60 CPU minutes; target ≤2 GB memory. Start with N≤16; beyond the budget, give a verifiable outer bound / stop, and do not report unfinished inner extrema |
| B: General findings and sequential validity | Build a minimal without-replacement confidence sequence from the conditions in the saved original papers; first fix the stratum mechanism, then study stratum selection based only on the audited history. For small N, enumerate random sampling orders exhaustively and check actual simultaneous coverage and all stopping rules | Bounded grid within a few CPU hours; no training. The statistical error upper bound comes from proofs and exhaustive enumeration / exact recursion; zero failures in Monte Carlo alone cannot be used to declare exact validity |
| C: Real audit feasibility and efficiency | Write a version-audit specification for the local FOMC documents with "decidable/contaminated/clean/unknown"; first time 10 documents to estimate the human cost distribution; then freeze one real-source trial, record every undecidable item, and assess whether the method really beats a census / simple stratification | Initial estimate of about 4–8 hours for human timing and the specification; the cost for all 120 documents is corrected from the pilot. CPU cost expected to be far below human cost. If the historical status of most documents cannot be judged locally, report a failure of real auditability and do not fill in fake labels |

Stage A results can go directly into a mathematical appendix of P1; if B only reproduces an off-the-shelf sequential algorithm, it should honestly be filed as a reproduction. Only if we find an explicit new bound/algorithm tied to influence structure, checked against prior work, should a separate submission be considered. C is not accepted on "the model is accurate", but on source-audit ground truth, validity, and actual cost.

## Pre-specified decision rules for the next small trial (proposal, not a frozen run)

This path should first use a fully enumerable mathematical design trial to judge "whether complex audits are worth continuing", and only then discuss real cost; read together with the [shared decision proposal](DECISION_CRITERIA.md). The rules below are not yet bound to a specific input grid, implementation version, or run identity; they are a proposal to be frozen after criticism from the senior assistant, not a retroactive registration for existing results.

### Hard validity gate and comparison contract

1. All methods use the same α=0.05, the same fixed statistic S, the same source strata and influence graph, the same model predictions, the same visible auxiliary information, and the same audit error criterion. The main target is **the interval width of this statistic**; the new method must not optimize accuracy width while the baseline optimizes the harder all-prediction stability rate.
2. The main target is provisionally set to fixed-test-set accuracy width **w=0.10**, keeping the same statistical object and resolution as PATH_01. Full enumeration with four to eight test points can be listed separately as an implementation stress test with w=1/4; this only suits discrete scores on a small domain, **cannot be used in place of the main target to pass the gate, and does not claim that a real model allows an error of one quarter**. The main design must make sure that the number of test points and the vote-margin structure allow a nontrivial comparison at w=0.10; if one can only require full stability at every point, state the discretization reason explicitly. Within one comparison instance, w must be exactly the same.
3. Mathematical validity must hold for all pre-specified small-scale contamination configurations: when sampling-event probabilities are computed directly or by exact recursion, the probability of issuing a wrong certificate is ≤0.05; the deterministic statistic envelope must cover on every admissible influence set. Sequential methods must also be shown to cover their actual next-stratum/next-record selection mechanism, which cannot be replaced by a fixed-n test. Undecided records, solves that exceed limits, and unsupported sampling mechanisms do not output a complete valid certificate.
4. Zero-finding planning compares only **the fixed audit cost conditional on zero findings**. Before the procedure has seen real audit results, this must not be called an "expected saving". If a sequential comparison is done later, the contamination scenarios, random sampling mechanism, maximum budget, and termination rule must be frozen independently, and the full fractions of target not reached, undecidable, and budget exhausted must be reported; average cost must not be computed only over runs that successfully issued a certificate.

### Pre-defined structure families and the scientific gain gate

The minimum design requirement is to define fully in advance three finite parameter families and all their grid members: **a family with roughly uniform influence, a family with influence concentrated on a few heads/sources, and a family in which the auxiliary risk score is unrelated or inversely related to true mislabels**. The first two test whether structure is useful; the last tests whether the method secretly relies on the assumption that the risk score is correct. Instances with equal costs and with stratum-specific costs must also be included. The specific N, stratum sizes, number of heads, all vote matrices/target quantities, and grid weights should be frozen with the experiment record; "picking an advantageous subfamily after running" does not count as a complete pre-specified family.

The cost of a fixed design is Σ_h c_h n_h. First compare numbers of audited documents with unit cost c_h=1, then run sensitivity analyses with cost vectors specified in advance, and only last replace c_h with time measurements from a real human pilot. The baseline for each instance must be **the minimum qualifying cost over a pre-defined set of simple fixed designs with the same information**, including at least the uniform exact gate, the enumerable optimal quota with pre-set strata, and the census option where applicable; not just one poor uniform allocation. If no design can reach the target width on an instance, mark it unreachable; do not create savings from infinite or missing costs.

As the main rule for "is this mathematical branch worth more investment", we propose: on at least one **complete structure family specified in advance**, the new method's cost on every nontrivial comparable instance is no higher than the strongest fixed design above, and the family's **pre-specified equal-weight median cost saving is ≥20%**; at the same time, publish as-is the per-instance values, worst degradation, no-gain fraction, and unreachable fraction for all the other structure families. One must also give a general structural condition or a matching lower bound explaining why the saving appears in that family; a numeric grid phenomenon alone is not enough. The median is only a summary of a fixed benchmark family, not an expected gain on a natural corpus. Instances with baseline cost 0 are reported separately, the new method must also be 0 on them, and no percentage is computed for them.

Let the saving be r=(C_base−C_new)/C_base. 20% is not a statistical significance gate, nor a universal theoretical constant; it is there to require that the extra algorithmic complexity produce a clearly visible practical difference relative to an existing reliable tool, so that chance savings on a few objects are not dressed up as a new direction. The real human cost is not yet known, so the threshold can only be provisional. The main rule should come with a sensitivity table over the thresholds {10%,20%,30%} and over cost vectors; if the gate is passed only under one cost ratio tailored for it, record that the scope is very narrow and do not treat it as a general advantage.

"No degradation on any instance" is a conservative design requirement: the new planner can include the known fixed designs as fallback candidates. But if the fallback requires an extra expensive search, **two separate accounts, planning time and audit cost,** must be reported; a 20% reduction in audited documents must not hide a compute cost that exceeds the human saving. In the real stage, at least the human timing for 10 records, the unknown/undecidable fraction, and full working-hour measurements must be included in the comparison. If historical versions still cannot be judged after reading all 120 documents, "census completed" must not be recorded as a successful baseline with zero uncertainty.

If the hard validity gate passes but the gain gate is not reached, this only means **not upgrading to a separate research direction**; it does not negate the exact audit-planning tool or its value as a P1 appendix. If the gate is reached on one family, the next step is still to check how well that family corresponds to real systems and to the existing literature, not to announce a mathematical innovation directly. A sequential scheme cannot borrow the gate result from the fixed zero-finding stage to conclude "lower expected cost"; it needs a new, complete comparison with the same definition of success.

## Strongest simple baselines and alternatives that cannot be avoided

1. **Full audit.** Determines the contamination count and locations completely; at the scale of 120 documents this is a serious baseline, not a deliberately expensive upper limit.
2. **Fixed uniform hypergeometric.** No structure, uses the existing exact n_min; it is simple, interpretable, and makes implementation errors easy to spot.
3. **Pre-set strata + fixed α_h.** Uses fixed strata by source type/cost; compare allocation by size, equal-cost allocation, and the small-scale offline optimal quota together. One must not pick a clearly worse allocation just to show an adaptive advantage.
4. **Known without-replacement confidence sequences.** The statistical baseline that genuinely supports stopping; this path must compare at the same failure probability and the same information visibility.
5. **System design instead of audit.** Drop the periphery, shrink the core, fix lexical features, or adjust the shard influence graph. If these measures make the audit requirement disappear at a smaller utility cost, report that they beat complex auditing, instead of clinging to the existing system.

Model-influence-first sampling is only a design candidate, not a naturally strong baseline: if inclusion probabilities are not handled correctly, it may save samples but lose validity. Experiments should show three contamination-location scenarios, where the correlation is correct, absent, and reversed, to avoid validating only favorable auxiliary information.

## Kill conditions, value of negative results, and the weakest link

Conditions that kill this path as a "new mathematics paper": the change is only a renaming of variables in off-the-shelf risk-limiting audits; there is no general structure-dependent improvement or interpretable lower bound; a census is cheaper at the real scale; saving samples requires assuming an unsupported relation between error rate and influence score; or solving the resulting algorithm is itself more expensive than auditing and cannot give a useful outer bound.

Negative results that still have value include: under some class of influence graphs, every valid zero-finding procedure must come close to a census; shard uniformization makes complex structured auditing yield no gain; with nonzero findings, the rectangular relaxation of the confidence set dominates the width; real time metadata makes most records impossible to judge reliably. They must be reported together with the restricted design class, the real cost, and the certificate target; the rule of three must not be renamed as a general audit lower bound.

The mathematically weakest link of this path is **whether we can pose a problem that the existing audit literature has not directly solved and that has a provable structural gain**; the empirically weakest link is the reliability of audit judgments and the real human cost. The exact binomial-coefficient computation is already solved, and it is not worth spending more main effort on polishing approximate constants.

## Technical review questions for the senior assistant

- Are the "bad contamination configurations" of D1 just the standard composite null hypothesis of existing risk-limiting audits? If so, to which influence graphs/target quantities should the remaining publishable difference be strictly restricted?
- Is the most suitable target the stable-prediction fraction, accuracy width, or macro-F1 width? The three may give different optimal audit allocations; should we first prove that they cannot substitute for one another?
- If unknown core contamination makes one document influence all heads, does the influence-graph method degenerate into a census? Is there a reasonable core audit / architecture design that avoids the degeneration, rather than ruling it out with strong assumptions?
- Do we pursue worst-case width at a fixed budget, or expected stopping cost under contamination scenarios? Once chosen, can we give the corresponding optimality/impossibility statement, and avoid optimizing two incompatible targets at once?
- When the next stratum is chosen adaptively, which saved confidence-sequence theorem, specifically, covers that sampling mechanism? If none does, should we do fixed designs first instead of stitching together invalid formulas?
- For the 120 local documents, is design complexity beyond a census worth it? If not, this line should become a budget-planning and negative-result appendix of P1, without separate flagship resources.

## Feasibility level and explicit uncertainty

**Fixed-design mathematics and local tools: high feasibility; direct influence-graph audit: medium, still needs an algorithm and a prior-work check; general adaptive validity and a publication-level increment: uncertain.** It fits best attached to P1: giving a verifiable budget for the full certificate design and identifying when further training is pointless. It has no independent necessity for training from scratch, and should not be treated as a second flagship split off to fill a Top 5. Whether to upgrade the research investment should be decided by comparing the concrete structural gain against the census baseline.
