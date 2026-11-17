# Influence-structure audit and source-date check: independent incremental review

Date: 2026-11-16. Reviewer: internal AI sub-agent `fresh_reviewer`, which did not write the mathematical document, optimizer or source checker reviewed in this round; it is not Fable or an external expert. Fully offline throughout. Only this review report was modified; the author's code, old reports and old corpora were not changed. Problems found were handed back to the author for revision and then reviewed again.

**Conclusion: In the current version of IA1–IA8, the exact threshold optimization and the small-scale general influence-graph checker, no unresolved substantive mathematical or implementation error was found within the stated conditions and program class. One important source-date binding defect and one inconsistency in experiment input identity were found and fixed. The median saving across the full 20 cells is 0, which does not reach the pre-registered investment gate of median saving ≥20%. The source re-check still supports only the date claims on the currently saved pages; the number of historical byte versions proven is still 0.**

What can be accepted this time is the finite mathematical interface, the exact results for the specified design class, and the source check within its declared scope. Real dependency graphs, real historical audit ground truth, actual model utility, independent confirmation and originality have not passed as a result.

## 1. Objects checked and execution boundary

I read [IA1–IA8](../theory/impact_audit.md) in full and checked it formula by formula; statically reviewed [threshold_design.py](../planning/threshold_design.py), [its tests](../planning/test_threshold_design.py), the [20-cell machine results](../planning/threshold_results.json), the [general influence-graph implementation](../planning/impact_audit.py), the [general implementation tests](../planning/test_impact_audit.py), the [pre-execution budget](../planning/impact_budget.md) and the [results report](../planning/impact_report.md). I did a targeted review of the exact zero-finding inversion interface and the collective-statistic interface that are called; the old 36 checks were not re-run.

For the source part I read [fomc_source_audit.py](../data/fomc_source_audit.py), [source_audit.json](../data/source_audit.json), the [source report](../data/source_audit.md) and the [source budget](../data/compute_budget.md). I did a read-only check of the local container metadata corresponding to the fixed 10 samples in the original repository; no body text, titles or full URLs were output. After the fix I called `audit()` directly for a read-only recomputation, without calling the main program that writes the JSON; all returned records and the population metadata agree with the saved JSON.

No training, external access, real contamination judgement or full literature novelty search was performed. Finite tests were not treated as a formal proof, and the existence of raw files, hash agreement and historical availability were not conflated.

## 2. Problems found in this round and fix status

### IR01 — important, fixed: different minutes in the same container could be wrongly bound to a single date

The original function required only that the target link be unique and that the local container contain exactly one Released date. Construct a paragraph that contains both minutes A and B, with the single date belonging to B; a query for A still returns `local_release_label`. During the review this error was actually reproduced with an offline construction; neither the manifest nor a unique target link removes this ambiguity.

The author has added a check of supported minutes identity: only known minutes HTML/PDF paths on the official HTTPS domain are accepted, and the eight-digit meeting date in the URL is verified; all links in a local container must belong to the same minutes identity. Different minutes, unknown paths, external sites, query parameters, duplicate targets or multiple Released dates are all rejected. Both orderings of HTML/PDF for the same minutes are still allowed.

The new counterexamples/examples pass, and the reviewer's re-run of the 10 tests passes. For the original fixed 10 samples I also did a read-only check: each local container has exactly two links, HTML and PDF, with the same meeting-date identity; in the first 7 the HTML comes first, in the last 3 the PDF comes first. After the fix, the date-match conclusions for the original 10 are unchanged. **So the defect did need fixing, but there is no evidence that it changed these 10 existing observations.** The current acceptance is limited to the declared FOMC template and supported paths; it is not a proof of date-semantics parsing for arbitrary web pages.

### IR02 — important, fixed: the identity of the mathematical example and the actual execution input were briefly inconsistent

The mathematical document originally wrote the main family as J=10 with two label classes; the pre-execution budget, script and JSON actually computed an abstract threshold structure with a single point of label 0. When every head votes the true class at every point, the two yield the same risk formula and audit cost, so the numeric conclusions are not affected; but one cannot use this to claim that an unexecuted multi-point voting experiment was run.

IA7 now explicitly applies to any J≥1, and the actual execution identity is explicitly J=1; the multi-point two-class version is only a mathematical extension of the same proof. The results report makes the same distinction and takes the frozen budget as the run identity. This description issue is closed; hand-made perfect voting still does not test real task utility.

### IR03 — minor, fixed: the strict-separation test of the general checker originally only verified "not worse"

The test originally named strict separation actually used a two-stratum AND and only asserted that the cost was no higher than the rectangle; for that structure the equal-cost free-quota optimum is the same anyway. The review suggested replacing it with an example of six documents, three strata, two documents per stratum mapping to one head, all three heads correct, alpha=1/4.

The current test independently enumerates all vote changes, actual sampling outcomes, all boxes and quotas: the direct scheme (1,1,1) has cost 3 and risk 1/4; the strongest joint zero-finding rectangle has cost 4. The strict inequality is now genuinely checked. The two-stratum AND is kept as a no-gain baseline and no longer serves as evidence of a strict gain.

### A verdict that must be kept: the main family did not pass the gate

I recomputed from the full JSON: of the 20 cells, 9 improve strictly and 11 have zero improvement; the median saving is 0, and only 3 cells save more than 20%. The current mathematical/results reports already record this honestly. The already-seen r=6 sub-family cannot be picked out after the fact and passed off as the original full family passing the median 20% gate. This negative result does not overturn the theorem that a strict separation exists, but it limits the current empirical support for "worth upgrading the investment".

## 3. Independent check of the mathematical propositions

| Proposition or conclusion | Review verdict and key qualifications |
|---|---|
| IA1 joint-deletion dependency graph | Under a fixed DAG, deterministic nodes, fixed exogenous randomness and complete control dependencies, topological induction holds. H_i must cover arbitrary joint deletions and cannot be inferred from invariance under single-document deletion; the OR counterexample is valid. Whether the real pipeline satisfies the graph contract remains an external obligation. |
| IA2 monotonicity and accuracy | Allowing a variable head to keep its original vote makes the feasible prediction sets nested. The exact reachable classes and accuracy endpoints are correct; an arbitrary reliable but non-nested approximate envelope cannot be plugged directly into upward-closed pruning. |
| IA3 coverage | Under stratified independent uniform sampling without replacement and fixed C, the all-zero probability is a product of binomial coefficients; it controls erroneous certification for each fixed ground truth. It is not the posterior probability of contamination after zero findings, nor the probability of audit success. |
| IA4 two-level antichains | The reductions to minimal bad document sets and to Pareto-minimal counts each hold. The risk reduction needs only finiteness and monotonicity of probability; judging minimality by single-element deletion and upward-closed pruning additionally need the bad sets to be upward closed. Having some bad placement for a count does not mean every placement for that count is bad. |
| IA5 global design | A complete finite grid attains the optimum of the declared class; an incomplete search cannot output an exact optimum or infeasibility. Optimality is relative to fixed stratification, fixed I, all-zero reporting and the relaxed threat set, not to arbitrary training or arbitrary audit methods. |
| IA6 rectangle baseline | When the whole box is reported only on all-zero and the full space otherwise, the exact box-coverage risk is max_h p_h(b_h+1). A single out-of-bound stratum can attain it. If only the final I is guaranteed and not the box, the method belongs to the broader direct-calibration class, and this max-box comparison can no longer be called its strongest baseline. |
| IA7 separation | With h=2r−1 consistent true-class votes, an error is possible only with exactly r variable heads; the exact cost of the strongest box is r·ceil[N(1−alpha)]. The ordinary Bonferroni box costs rN−floor(N alpha); its extra conservatism is not counted as the main gain. |
| IA7 order | For fixed alpha and N=r², the direct feasible upper bound is O(N), the box lower bound is Omega(rN), and the derivation of the Omega(r) ratio is correct. The population also grows, as (2r−1)r²; arbitrary-factor savings on a fixed real corpus, or minimax optimality on general graphs, were not proven. |
| IA8 symmetric reduction | With equal stratum sizes and equal costs, after sorting, the risk is determined by the smallest r quotas. Lowering the other quotas to the r-th does not increase risk and weakly lowers cost, so exhaustive enumeration of non-decreasing r-tuples misses no better solution. This does not carry over to unequal costs / stratum sizes; the code's specialized function does not make that generalization. |

Zero risk for an empty bad set, infeasibility when an empty contamination is already bad, a factor of 1 for zero sampling, a factor of 0 for a census of a contaminated stratum, no out-of-box restriction when b_h=N_h, empty influence and an empty population are all distinguished in the implementation/tests. The general API allows empty strata and treats them as neutral strata with factor 1; this is equivalent to the theory first deleting empty strata.

## 4. Implementation and exact optimal values

The threshold optimizer uses `Fraction` and integer-power comparisons; no floating-point roots take part in feasibility decisions. The initial balanced scheme is a valid upper bound, and cost pruning skips only tuples that cannot strictly improve on the incumbent; after full enumeration of all allowed non-decreasing tuples, global optimality can be claimed. The largest domain is C(26,6)=230,230; beyond `max_tuples` the code refuses to return a partial optimum.

So **for r=6, h=11, N=20, alpha=1/20, 88 is the computed exact optimum within this fixed equal-cost stratified uniform design class**, no longer just a hand-computed balanced feasible upper bound. All quotas are 8, and the worst-case miss risk is 729/15625=.046656; the strongest box is 114 and the Bonferroni box 119, so the saving against the stronger main baseline is 13/57≈22.807%. This was not extended to optimality under random quotas, sequential designs, non-uniform within-stratum sampling or unequal costs.

The general implementation independently handles real document influence lists: it enumerates contamination sets, caches exact envelopes for unions of heads, checks single-deletion minimality and performs Pareto reduction on counts. Accuracy uses additive exact endpoints and macro-F1 uses the existing joint-count DP; per-class component bounds are not miscalled exact. Positive rational costs and exact alpha/intervals are kept, and invalid inputs such as bool/float are rejected.

Enumerating only maximal safe boxes in the rectangle optimization is a correct additional reduction: the set of safe boxes is downward closed; increasing a safe budget coordinate does not raise the corresponding minimum zero-finding audit size required, so under positive costs some optimal box can be extended to a maximal box. This part still targets whole-box coverage. Exceeding the configuration, DP-state or search budgets raises `BudgetExceeded`, and no pseudo-exact partial search result is returned. The general code is explicitly limited to small populations and does not prove scalability to arbitrary influence graphs.

The zero-finding risk API allows profiles to be passed in from outside; the documentation explicitly requires them to cover the full bad set or a valid frontier; this low-level function does not itself verify the real dependency graph. The high-level `plan_impact_audit` builds the frontier from the declared graph, votes and labels, so that a hand-written profile list with omissions is not slipped in as a complete certificate.

## 5. Scope of the source-date evidence

The read-only recomputation after the fix confirms: 120 raw candidates, 10 taken at fixed equally spaced date ranks, 8 corresponding index snapshots; for all 10 the current Released claim, the manifest publication date and the current Last Update agree; the source hash and all output records match the saved JSON. The recomputation did not change the source files or saved results.

The supported conclusion goes only as far as: **the currently saved official index declares the same public date within the local container of the same minutes identity, and the related saved objects agree with the list hashes.** The following unknowns were not closed:

- Whether the date claim proves that the same bytes were public at that time, and whether there were unmarked revisions; all `historical_byte_version_proven` are still false.
- The intraday release time and time zone; all `release_time_of_day_proven` are still false, and no arbitrary "2 p.m." in the meeting text was borrowed for this.
- Point-in-time measurability of the 2026 collection, filtering and preprocessing.
- The mislabelling rate over all 120; the sample is not a random sample, and 10/10 cannot be turned into a zero contamination rate or a finite-population confidence bound.
- Full semantic agreement between the extracted text and the HTML. The current dual hash check on text/HTML verifies the link between the records and the saved list; text extraction was not independently re-run to prove there are no omissions/mis-extractions.

Last Update is kept as an independent update channel, not as proof of the publication date; finding no machine date field applies only to the supported entry points and is not an exhaustive negation over arbitrary web-page scripts. The current report records these limits separately.

The judgement about SEntFiN's use comes from separately reading the local source/approval notes, not from row-by-row verification by this checker; I did not review all the raw labels, the publisher's rights or the new training split. Its source-native sentiment, asset stance, security identity, approval scope and event independence still need separate acceptance and cannot be replaced by this FOMC date check.

## 6. Verification actually run by this review

The following were run by the reviewer and are not mixed with the author's original run times; the old 36 tests were not re-run and nothing was retrained.

| Action | Result |
|---|---|
| `python -m unittest research.planning.test_threshold_design -v` | Currently 5 pass, unittest reports 0.361 seconds; includes uncompressed quotas, full box/sampling baselines and the Bonferroni baseline |
| `python -m unittest research.planning.test_impact_audit -v` | Currently 8 pass, 0.093 seconds; includes actual vote-change and sampling oracles, both metrics, six-document strict separation, two-level antichains and boundary rejections |
| `python research/data/fomc_source_audit.py --self-test` | After the fix 10 pass, 0.003 seconds; includes the mixed-binding counterexample raised by this review |
| Direct call of the source `audit()`, printing only a summary and consistency booleans | 0.328512 seconds; records and population metadata fully agree with the saved JSON; no output file written |
| Recomputing the summary and source hashes after reading the full threshold JSON | 20 cells, 11 with zero gain, median 0, 3 cells above 20%; the source/budget hashes bound in the JSON match |

The author's earlier 20-cell sweep took 0.702440 seconds; the root agent's subsequent integration re-run updated the JSON to 0.680830 seconds. The reviewer did a read-only check of the updated 20-cell summary, the 88/114 for r=6/N=20, and the source/budget hashes; the conclusions are unchanged. The reviewer did not run the result-writing sweep main program again, nor repeat the root agent's full set of 49 tests. All timings are local CPU records; peak memory was not measured, so no claim is made that the RAM budget passed a measurement. Passing tests supports these finite inputs and implementation boundaries; it is not a machine proof for all inputs.

## 7. Reviewed snapshot and final disposition

The SHA256 values below pin the main files at the time this review was completed; later changes need a separate record. The budget, source notes and results report were also read, but the table lists only the core computation and source-evidence files.

| File | SHA256 |
|---|---|
| theory/impact_audit.md | `9ec371e5727d0cd8b9bbae088047c75cee93800ff6ae13e8b0eae515b19c79ec` |
| planning/threshold_design.py | `2eddf0a0d29621ecafedbdb23d31aebfe141f6fa63a2a4bb3a1a144ca508e8f1` |
| planning/test_threshold_design.py | `bc81c0934865b1b6ce2660c9bbc48c61435a221999ed04e914c8e87bbf1aa742` |
| planning/threshold_results.json | `9d1e06131bfc126e5230f31229dbb60bac3b753b4621edb0481cd68799022fb3` |
| planning/impact_audit.py | `b0d7da428676ff658c2d88ac61b2ba29839a1dbe8018f257dbc32aac4509b7c6` |
| planning/test_impact_audit.py | `82e04071647a211bbab8dc8060e2420ce5a673f2e9290128f8e8b494fd1b43f1` |
| data/fomc_source_audit.py | `96577f6b877e02259cd6a138e7359f574fe0da722abec30b6ceb2777c55e2987` |
| data/source_audit.json | `d8649cddcded9d5153bf0e71abde59b4209e22d1a6f0005181da6b06ad5d358d` |
| data/source_audit.md | `c056e06d8d8ada569d52ce124736e58cf83bcb5b0ad6bb4b1d367f62f7931a53` |

**Disposition: the code/description defects identified in this round have been fixed and re-checked; the small-scale mathematical implementation can be kept.** The family-wide 20% investment gate was not passed, and real historical versions, task utility, reliability of manual audits, and differences from prior work remain open. Follow-up work can study which structures reliably produce gains and what real source evidence is needed; this check must not be marked as G0/G1, a complete historical certificate, or a submission-level innovation being complete.
