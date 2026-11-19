# Path 04: dependence-robust certificates from uncertain marginals to deployment error budgets

Date: 2026-11-15. Status: a mathematical candidate and adversarial analysis; not a selected flagship, and not external peer review. The basis is limited to the local [T3.1](../theory/notes.md), the [finite grid checks](../checks/results.json), the [literature status ledger](../literature/question_status.md), and the [local corpus inventory](../reports/local_data_inventory.md). The original literature for Q20 has not been checked adequately; no new network requests were made, and none of the constructions below is claimed to have confirmed novelty.

Numbering: the deployment-risk side line of the advisor's old plan is written **old P3 / this round's PATH04**; this round's PATH03 refers to the audit-cost branch. The concrete usefulness gates for later trials are in [DECISION_CRITERIA.md](DECISION_CRITERIA.md). The thresholds there are a research proposal for the next round, not yet executed, and not thresholds Fable has accepted; they do not retroactively serve as ex ante criteria for existing results.

**Judgment: a comonotone calculator for known pointwise marginals + independence across clusters is not by itself enough to be a new theoretical direction. The more valuable question is: when only group risk can be estimated and independence across clusters is also uncertain, what minimal information yields a tail error budget strictly smaller than "the whole batch is wrong"? If identification, statistical coverage, and non-vacuity conditions cannot be stated together, this path should be kept as a side line or a negative result.**

## 1. Target quantity and levels of probability

Fix the trained predictor f, the meaning of the labels, and the sampling scheme for future batches; training data, calibration data, and final evaluation data are kept separate. A future batch of B samples has error indicators E_i=1{f(X_i)≠Y_i}, and total error count S=Σ_i E_i∈{0,…,B}. The main target is the upper-tail Expected Shortfall:

```math
\mathrm{ES}_{\beta,Q}(S)=\inf_{t\in ℝ}
\left[t+\frac{𝔼_Q(S-t)_+}{1-\beta}\right],\qquad 0<\beta<1.
```

For discrete distributions this definition includes splitting the atom mass at the quantile, so it cannot be written directly as "the conditional mean beyond VaR". Q is the joint distribution of the future error vector. The calibration data D produce an upper bound U(D), and the required coverage is

```math
\Pr_D\{\mathrm{ES}_{\beta,Q}(S)\le U(D)\}\ge1-\alpha.
```

This is a statistical certificate for the **risk of the future distribution**; it does not claim that some batch already seen must have at most U errors. If future batches are independent of D by design, the ES upper bound also gives the corresponding quantile upper bound, so one can obtain a statement about the number of errors in a batch with joint failure probability at most alpha+(1−beta); the two layers of randomness and their failure budgets must be written out separately.

This plan first studies future batches drawn at random according to preset group/event compositions. **It does not provide an assumption-free conditional risk certificate for an arbitrary given set of selected features X_1,…,X_B.** The latter requires identifying pointwise conditional error rates, which is much harder than ordinary calibration.

## 2. First keep three counterexamples that can kill a wrong narrative

**Group calibration is not pointwise marginals.** Two equal-size subgroups have true error rates 0 and .2, and everything is predicted as .1; grouped by predicted value, this is perfectly calibrated. If a future batch concentrates on the high-risk subgroup, its error marginal is .2. For an arbitrary future feature point whose label has not been observed, finite calibration data also allow two mechanisms that are both consistent with the observed data but give that point conditional error rates of 0 and 1. Without smoothness, a parametric model, repeatable groups, or other structure, a simultaneous upper bound on the pointwise p_i cannot be derived from the calibration curve.

**Correct marginals also do not identify dependence.** B errors each with marginal .1 can be mutually independent, or all be driven by one common Bernoulli(.1); the average error rate is the same, but the tail error budget is completely different. Writing company, event, or date into metadata does not prove independence across clusters; one systematic macro news item may connect all clusters.

**Arbitrary drift invalidates historical evaluation.** If the future labelling mechanism is not constrained, two worlds with exactly the same historical data and model can make the future all correct or all wrong. Any upper bound claiming to cover both worlds must allow B. Observing that unlabelled future features "look close in distribution" also cannot rule out that Y|X has changed.

## 3. A boundary to prove first: when is the bound necessarily vacuous with only group means?

Suppose the future batch is divided in advance into G mutually exclusive groups, group g having b_g items, Σ_g b_g=B; all that is known is

```math
𝔼_Q\sum_{i\in g}E_i\le b_g u_g,\qquad 0\le u_g\le1,
```

with arbitrary dependence within and across groups allowed, and with no claim that each p_i≤u_g. Let $`𝒬(u)`$ be the set of all joint laws satisfying these conditions, and write a=1−beta.

**A characterization that can be derived directly here; not a novelty claim:**

```math
\sup_{Q\in 𝒬(u)}\mathrm{ES}_{\beta,Q}(S)
=\sum_g b_g\min\{1,u_g/a\}. \qquad (R1)
```

The proof route is short. The finite-state risk envelope of ES can be written as choosing density weights z/q≤1/a on the original law q, with Σz=1. The weighted error count in group g exceeds neither b_g nor the original expectation b_gu_g/a; summing over groups gives the upper bound. Take one common U~Uniform(0,1), make all errors in group g equal to 1{U≤u_g} simultaneously, and concentrate the tail weight on U≤a; this attains every group's bound at once. So this is a sharp bound, not a conservative relaxation.

This reveals a fact that might reject the path directly: if beta=.95 and every group has u_g≥.05, R1 equals B, even if these group means are **fully known with no estimation error**. Adding calibration samples cannot repair the missing dependence information. If there is only an overall mean upper bound u, it degenerates to B·min(1,u/.05). The .95/.05 here is only a mathematical example, not a measurement of a local model.

R1 can serve as an identification boundary or a short negative result in a paper, but comonotonicity, risk envelopes, and worst-case distributions under moment constraints are all classical frameworks. This few-line corollary cannot be called an original theorem. What really needs a prior-art check and deeper work is: what extra constraints estimable from data can strictly tighten this sharp bound, and the minimal sample size needed to obtain that tightening.

## 4. An executable but explicitly conservative statistical entry point

First freeze the grouping rule and f. The calibration set consists of independent clusters c=1,…,C, with arbitrary dependence within clusters; the basic version takes the within-group sample sizes n_cg, n_g=Σ_c n_cg as fixed by design. If a version conditioned on random cluster sizes is used instead, the conditioning sigma-field H must be stated explicitly, and the clusters must be assumed still mutually independent given H; theta_g below must also be changed to the weighted expectation under the same conditional law. **Unconditional independence does not automatically guarantee independence after conditioning**; one cannot fix counts/selection events from the data on one hand and keep using the original independent concentration bound without proof on the other. If the all-zero event bound below uses a conditioning argument, it obeys the same requirement. Let

```math
\widehat\theta_g=\frac{\sum_c\sum_{i\in(c,g)}E_i}{n_g},\quad
r_g=\sqrt{\frac12\sum_c(n_{cg}/n_g)^2\log(G/\alpha)}.
```

Because each cluster's contribution to this mean lies in the interval [0,n_cg/n_g], the concentration bound for independent bounded blocks plus a union bound gives the simultaneous upper bound $`\theta_g\le\widehat\theta_g+r_g`$, where theta_g is the weighted expected error rate for this calibration sampling design; it is not a pointwise conditional probability. A group with n_g=0 must be set to u_g=1 or rejected, not defaulted to zero risk.

Only with the **additional assumption** that the expected average error rate of group g in the future random batch is at most theta_g+delta_g can one take

```math
u_g=\min\{1,\widehat\theta_g+r_g+\delta_g\}
```

and plug it into R1 to obtain coverage of at least 1−alpha. One sufficient transfer condition is: under fixed f and a consistent within-group sampling design, the total variation distance between the future and calibration group-conditional joint laws of (X,Y) is at most delta_g; because the error loss is bounded, its expected shift is at most that distance. **delta_g is not a quantity that can be estimated from the existing unlabelled text; it cannot be replaced by a seemingly small embedding distance.**

When the clusters within a group are equal in size, the radius is controlled by the number of independent clusters; many rewrites of the same event cannot increase the effective independent sample size. Choosing groups or models from the data, or repeatedly adjusting delta and then picking the tightest result, also breaks this guarantee and requires independent design samples or explicit uniform control. This entry point is itself a combination of classical bounded concentration and risk envelopes; its value is to expose the budget, not to manufacture novelty by "coming with a confidence interval".

### Direct rejection of this entry point by 120 FOMC documents: the sample size must be computed first

The independent review pointed out that the budget above must be compared with local quantities. Take the most favourable case G=1, alpha=.05, beta=.95, zero observed errors, zero drift, and assume all C calibration clusters are independent and equally weighted; still

```math
r_C=\sqrt{\log(20)/(2C)},\qquad
r_{120}=0.1117238462>0.05.
```

So the upper bound obtained by plugging into R1 is still B. For this **Hoeffding entry point** to have any chance of being strictly smaller than B, one needs at least

```math
C>\frac{\log(20)}{2(0.05)^2}=599.1464547,
```

that is, **600 independent, equally weighted calibration clusters**, not 120. The radius at C=599 is .0500061121, and only at C=600 does it drop to .0499644230; even the latter result is only slightly smaller than B and cannot yet be called a useful deployment budget. Nonzero observed errors or drift raise the threshold. With unequal cluster sizes one should count $`C_{\rm eff}=1/\sum_c(n_c/n)^2\le C`$, and cannot inflate the sample size by the number of headline rows. Calibration with multiple groups also needs to account for log(G/alpha) and each group's own effective number of clusters.

The numbers above are mathematical design values computed directly in this round with the Python standard library; **they are not measured FOMC error rates or effective sample sizes**. The current 120 documents have no verified error gold labels and have not been shown to be mutually independent; after the training/selection/calibration split, there would certainly not still be 120 unused calibration clusters. So the local FOMC set cannot demonstrate a non-vacuous certificate with the current conservative entry point; this judgment already holds before any training.

### This does not prove that every statistical entry point is impossible

One must distinguish "R1's sharp bound under given true mean constraints" from "what method we use to construct that mean upper bound". The identification limit of the former cannot be changed; Hoeffding can be very loose for zero-error data, and one can switch to a valid method better suited to the observed results, with explicit assumptions.

1. **Truly i.i.d. Bernoulli errors.** If there are C independent Bernoulli(p) calibration units and zero errors are observed, the one-sided exact binomial upper bound is $`u_0=1-\alpha^{1/C}`$. Under the alpha/beta above, u_0<.05 requires $`C>\log(.05)/\log(.95)=58.4039748`$, with smallest integer **59**. At C=58, 59, 120 the upper bounds are about .0503393383, .0495076099, .0246554011; plugging the last into R1 gives .493108022B. These are all design values under the condition "zero findings and the given model holds", not local results. A calibration unit can be a single truly independent error, or the indicator "at least one error" for an i.i.d. cluster; the latter upper bound controls the cluster error probability, and converting it to row-average risk also requires matching cluster weights/sizes and the target sampling scheme.
2. **Bounded cluster means, independent across clusters but with arbitrary dependence within.** One cannot force each cluster's fractional error rate to be Bernoulli. A valid alternative only for the all-zero path is: let the independent X_c∈[0,1] be each cluster's average error rate, mu_c=E X_c, with target the equally weighted cluster mean $`\bar\mu=C^{-1}\sum_c\mu_c`$. Because $`P(X_c=0)\le1-\mu_c`$, independence and AM–GM give

```math
P(X_1=\cdots=X_C=0)
\le\prod_c(1-\mu_c)\le(1-\bar\mu)^C.
```

Therefore "output u_0 when all are zero, otherwise output 1" is a one-sided upper-bound rule with coverage at least 1−alpha; it requires neither independence within clusters nor that all clusters be identically distributed. Its all-zero threshold is also 59, but it is **not** plugging an arbitrary fractional error rate into the full Clopper–Pearson formula; no non-trivial bound is given here for nonzero observations. If the original target is row-weighted and the clusters are unequal, the equally weighted $`\bar\mu`$ differs from row risk, so this threshold cannot be borrowed; the corresponding weighted zero-event extremal problem must be re-solved, or a valid weighted bound used.

Both entry points still need independent calibration units, a fixed model/design, verifiable error labels, and a transfer condition from calibration risk to future-batch risk; it is not allowed to pick subgroups that "happen to be all zero" after seeing results. This comparison shows that **600 is the minimum threshold for the Hoeffding formula as written, not a universal lower bound for all methods**. When no real errors have been observed and independence is unverified, "we have 120 articles" can neither announce success nor announce that all possible methods fail.

## 5. Where should the increment worth studying be placed?

The candidate main question should be narrowed to one axis: **when group means can be estimated but pointwise marginals are not identifiable, how does partially verifiable dependence structure change the sharp bound and the sample complexity of the worst-case ES?** It is not advisable to promise at the same time to solve arbitrary drift, unknown clusters, arbitrary conditional calibration, and large-scale exact solving.

One explicit starting point is a finite-state set of moment constraints. For e∈{0,1}^B, q_e is the original law and z_e is the tail risk envelope; solve directly

```math
\begin{aligned}
\max_{q,z}\;&\sum_e \left\vert e\right\vert z_e,\\
&q_e\ge0,\quad\sum_eq_e=1,\quad z_e\ge0,\quad\sum_ez_e=1,\\
&z_e\le q_e/(1-\beta),\\
&\sum_e q_e\sum_{i\in g}e_i\le b_gu_g,\\
&\text{other linear moment constraints with simultaneous statistical coverage.}
\end{aligned} \qquad (R2)
```

R2 is an exact LP for the worst-case ES over the given polytope of joint laws. It has 2^B states, so scalability cannot be claimed, and the LP cannot be called an innovation because the problem is named a "risk certificate". More crucially: how would the added cross-cluster joint-error moments be estimated from independent repeated batches? When there is only one batch of non-repeating financial events, the so-called joint-error constraints may not be identifiable at all.

The data unit must be explicit here. To constrain the joint-error moment $`E[S_aS_b]`$ of future clusters a, b, one sufficient design is M mutually independent **complete repeated batches**, each containing pre-matched cluster types a, b, with the model and task fixed, and with a declared transferability relation between the batch composition and the target distribution. Only then is each batch's $`S_aS_b\in[0,b_ab_b]`$ an observation usable for a bounded-mean interval; multiple moments need simultaneous coverage. The independent statistical units are then the M complete batches; the clusters within a batch cannot also be counted as independent repetitions to exaggerate precision.

One batch of C events does not automatically provide C(C−1)/2 independent joint-error observations: pairwise products share events, and both the dependence structure and the estimation target need separate modelling. One-off FOMC events on different dates also do not become repeated batches from the same joint distribution because they are listed next to each other. Exchangeability, stable cluster types, a known dependence graph, temporal mixing, and so on are all extra assumptions that cannot be inferred from file metadata. **The current local inventory has not established such repeated-batch data or verified moment constraints, so for now R2 can only be oracle-verified with synthetic known moments; one cannot fill in point estimates of joint errors in a real demonstration and call it certification.** If qualified data do appear later, the moment intervals, marginal intervals, and transfer error must also be accounted for jointly; the same alpha cannot be spent twice.

There are two classes of candidate theorems worth handing to the senior advisor for judgment. The first is **matching identifiability/sample-size upper and lower bounds**: in a specified repeated-cluster or known-dependence-graph model, prove how much independent information is necessary and sufficient to tighten R1 by epsilon; giving only a Hoeffding upper bound is not enough. The second is **structured computability**: give an exact dual checker and its complexity for R2 under some finite graph width or block structure, and at the same time prove how much tightness is lost by relaxing the structure. If all of this is already covered by classical distributionally robust moment problems, it should be downgraded to an application or a teaching tool.

Another bound, usable for sensitivity and not as a novelty claim: if the total variation distance between the true joint error law Q and some Q0 that satisfies independence across clusters is ≤rho, and S∈[0,B], then

```math
\mathrm{ES}_{\beta,Q}(S)
\le\min\{B,\mathrm{ES}_{\beta,Q_0}(S)+B\rho/(1-\beta)\}. \qquad (R3)
```

This follows directly from controlling the expected shift of the bounded stop-loss threshold by threshold and then taking the infimum. It shows how the extreme tail amplifies dependence mismatch; at rho=.05, beta=.95 the added term already reaches B. rho requires a structural assumption with an explicit source or an independent estimate, and must not be set small arbitrarily to obtain a non-vacuous bound.

## 6. The strongest baselines must be used, and the estimand aligned first

| Baseline | Question it really answers | Fair comparison |
|---|---|---|
| Within-cluster comonotone + across-cluster convolution with known true p_i | Given the true marginals and the correct independent-cluster structure, the worst-case convex risk of the future total error | As an oracle; our estimated-marginal method should be wider because of uncertainty, and cannot claim to beat this oracle with a narrower interval |
| Global comonotone/group-mean sharp bound R1 | The identification limit when arbitrary global dependence is allowed | If a new method is narrower, it must list item by item the extra information and its cost |
| Complete finite-state LP R2 | Exact worst-case ES under the same constraint set | Small-scale gold standard; approximate algorithms must give a safe outer bound and a gap, and are not compared with a deliberately weakened per-class method |
| Cluster bootstrap | Under conditions such as independent, representative clusters, the sampling uncertainty in estimating a population average metric | Not the dependence-worst-case ES of the total number of errors among B future items; the risk method cannot be judged a winner or loser just because the bootstrap interval is narrow or wide |
| Markov/bounded mean and a simple union bound | An upper bound on the count tail using only low-order information | A basic lower-end comparison; one must face the stronger oracle and sharp bounds above at the same time, not merely beat these loose bounds |

## 7. Three-stage minimal validation and the real role of local data

The following are **planning budgets before any run, not yet executed**; no GPU is assumed, and enlarging the model is not used to sidestep the mathematical problem.

**Stage 1: proofs and exact small instances.** First prove R1, the calibration coverage chain, the risk-envelope equivalence for R2, and R3; independently review zero-sample groups, beta→1, single-cluster/global common shocks, and drift counterexamples. Treat the 120/600 Hoeffding threshold and the 59 threshold for the valid all-zero entry point as mandatory boundary checks, without confusing their respective statistical units. For B≤8 there are only 256 error states; first cross-check with rational constructions and known extremes, and if an LP solver is already available locally, compare R2 as well; a coarse rational grid cannot be treated as the whole feasible region. Estimated 10–30 CPU minutes, RAM<1 GB, GPU memory/training tokens 0; human verification counted separately. Acceptance requires matching upper and lower bounds and an explicit counterexample for every premise violation.

**Stage 2: finite-sample coverage and vacuity rate.** Freeze grids over the number of independent clusters, cluster imbalance, group proportions, latent common-shock strength, and drift radius, then generate D and future batches. The main metrics are coverage, upper bound/B, fraction vacuous, and gap to the oracle; report a separate binomial interval for the coverage simulation itself, and do not require each empirical coverage to be exactly above nominal. Initial budget: 20–40 scenarios, 2,000 independent replications per scenario, 1–2 CPU hours, RAM<2 GB, GPU 0. This is a planning estimate; if over budget, reduce replications and relax simulation precision, without changing the theoretical target. Failures under wrong assumptions must be shown alongside, not only successes when the model is satisfied.

**Stage 3: a limited demonstration on real local material.** Locally there are 120 FOMC source snapshots, SEntFiN candidates, and a private pilot; see the inventory. FOMC has dates/document identities and suits designing event units and future-batch compositions; but there are no ready-made error gold labels, and p_i cannot be estimated directly from source text. SEntFiN has supervised candidates; after checking row-level approval, task semantics, and scope of use, a simple fixed baseline can be retrained and independent calibration/test sets built. The original non-temporal pilot and the unfinished event audit cannot directly serve as a guarantee about financial temporal drift. Private text is processed only in place; anonymized summaries and hashes are delivered.

Stage 3 should first give a table of "which statistical assumptions the local design can support, and which can only be sensitivity analyses", and only then decide whether it is worth running a small-model error analysis. **The current 120 FOMC documents are not enough to make the Hoeffding entry point above non-vacuous, and training longer cannot change that radius threshold; without gold labels, independence, or evidence of repeated batches, one also cannot promise in advance that switching to the all-zero entry point or R2 will succeed.** Budget estimate: if the preliminary judgment passes, CPU baselines and offline statistics take 1–3 hours, RAM<4 GB; gold-label review hours are logged separately, and automatic model labelling cannot pose as true errors. Without enough independent events/repeated batches, the result can only be an empirical example and cannot be turned into a deployment certificate with a verified dependence structure.

## 8. Necessity of training from scratch and rejection conditions

This path is essentially model-agnostic with respect to f: a linear classifier, a frozen off-the-shelf encoder, and an LM trained from scratch can all produce E_i. **Training from scratch is not a mathematical necessity.** So it does not satisfy the advisor's original filter of "keep only questions that can only be answered by training from scratch"; if that filter is kept, old P3 / this round's PATH04 should stay a side line with ≤10% of effort. If one is willing to change the central target to certified bounds for deployment decisions, it can be a candidate for an independent statistics paper, but this change of scope must be recorded; it cannot claim to still fully meet the original screen.

Conditions for early rejection or downgrading:

- The new content only convolves comonotone distributions for known marginals, or treats estimated probabilities directly as the true p_i: this is not new theory, and the latter may also be invalid.
- There are only group means, R1 stays equal to B at the actual target beta, and there is no credible source of dependence information: do not keep training a more accurate model to cover up the identification gap.
- The chosen confidence upper bound is itself necessarily ≥1−beta under the sample-size budget: reject that statistical entry point first. The Hoeffding formula as written, with the current C≤120, falls into this case; this does not automatically reject a valid and tighter all-zero bound, or other methods under different assumptions.
- All "non-vacuous" results depend on an unverifiable delta/rho chosen small after the fact, and the report gives no robustness frontier: the certificate is only an optimistic scenario.
- Simultaneous coverage cannot be given for the candidate moment constraints, or the LP only yields an uncertified numerical interior solution: do not claim a safe risk upper bound.
- The minimal structural problem is already fully covered by classical moment LPs, comonotonicity theory, and the existing distributionally robust literature: keep the tool and the review, and do not claim novelty through financial application vocabulary.

A negative result still has value: it can state clearly at which step the "calibrated pointwise risk" narrative cannot be identified, and prove under what mean/dependence information every method must be vacuous. It can stop the project from packaging a known risk calculator as a financial language-model innovation, and it gives principles for what extra labels or repeated events to collect later.

## 9. Concrete questions for the senior advisor to attack

1. Is R1's mean-identification bound already enough to kill the practically meaningful beta/error-rate combinations? If so, should old P3 / this round's PATH04 immediately stay a side line, instead of continuing to build engineering?
2. Do we really have repeated independent clusters to estimate joint-error moments, or only a string of different macro events? Which dependence-structure assumption can be supported by the research design, rather than asserted from experience?
3. Is the target really random future batches, or is it conditional on specific selected texts? If the latter, what function classes/smoothness/repeated-measurement structure need to be added, and does the cost already exceed the project budget?
4. When unknown marginals and unknown dependence coexist, which minimal sub-question could yield a matching lower bound, a sharp frontier, or a certifiable dual algorithm, rather than just a sum of classical concentration bounds?
5. Is this candidate allowed to break explicitly from the "must train from scratch" filter? If not, we should stop putting it forward to compete for the flagship and keep only T3.1 as a correct appendix tool.

The current recommendation is to finish the identification boundary in stage 1 first and keep a strict right of rejection; until novelty and the source of dependence information are clarified, do not rank it as a definite Top 1, and do not pre-commit to a paper grade.
