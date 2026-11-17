# Round 8 independent adversarial review: localization structure and the total-contamination-count gate

Reviewer: internal AI subagent `localization_reviewer`, not Fable; this does not represent the opinion of outside peers. Scope: local theory, protocol and finite computations with the standard library. No network access, no training, no outside messages. The local skill "academic research - organize an adversarial research review" was applied. All new constructions and comparisons are exploratory. They cannot be relabeled as pre-confirmed results, and no novelty is claimed.

**Addendum on the unified reproduction status:** The first successful execution of the 48 rows and the independent check described below are real historical results. The subsequent unified reproduction process actually ended with exit code 1, because Windows returned WinError 5 when replacing the results JSON. That failure record is kept separately. After the author added bounded I/O retries, the affected 48-row runner was rerun to completion, with exit code 0 and stable execution-source hashes. This review read the new JSON only after receiving the success notice, and the new JSON again passed the independent full-table check; the final record is in Section 8. The engineering failure is not interpreted as a mathematical counterexample, and the failure is not silently erased either.

## Pre-computation budget (2026-11-16, written before the independent script was first run)

- The independent script is written only to `research/reports/localization_review_checks.py`. It uses the Python standard library, with no model, no data download and no network call.
- Risk check: 1–3 layers, each layer of size 1–3; enumerate all fixed quotas and all valid counts; also check 4 layers with 2 documents each. At most 10,000 risk comparisons and 100,000 count-vector evaluations in total.
- Structure check: two documents per layer, all-layer conjunction threshold, 2–8 layers; enumerate over sorted quotas, with no more than 500,000 additional count-vector evaluations in total. Check the closed-form optimum and the direct optimal cost with rational numbers. This cap was set before the first run, computed as the number of sorted tuples times the size of the count grid.
- Time limit 60 seconds. The script sets its own check budget and exits with failure; it does not report an unfinished enumeration as optimal.
- Once the author's implementation appeared, its protocol, theory and implementation were checked read-only, reusing the frozen small check inputs. Any exploration beyond this budget is registered separately.

This section records the pre-run budget, not a pre-registered research hypothesis. The results below were obtained after the budget was written.

## 1. Current judgment and key issues

**The total-K gate is not in general equivalent to localization structure. The homogeneous `d=2r−1` family of last round's IA7 can only have a cost ratio strictly below 2, but this sharp constant gain also holds relative to `min(Box, Total K)`, with an asymptotic saving of 50%. When the general homogeneous threshold family allows `r=d`, there is indeed a linear separation from the total-K gate in which every document is relevant, but a simple Box already reproduces it.** These are substantive clarifications of the mathematical scope. They do not yet prove originality, how often the structure occurs in real models, or that the research project has reached the standard of an independent strong paper.

| ID | Importance | Independent review conclusion |
|---|---|---|
| LR01 | Key algorithmic boundary; initial judgment corrected | The prefix-greedy risk algorithm is correct. The first-factor product risk of the direct method cannot be used for total K. However, with equal N/equal cost and k≤d, a newly added proof shows that enumerating the first k entries and flattening the tail also apply to total K. The author's current full enumeration of d-tuples is correct, but it is not yet the tightest dimension reduction. |
| LR02 | Key boundary on the contribution | In the original homogeneous `d=2r−1` family, `C_K/C_I<2`, and this constant can be approached asymptotically. The family's original Ω(r) rectangle separation cannot substitute for a comparison with the strongest total-K gate. |
| LR03 | Valid new candidate scope | The all-layer conjunction family with `N=2,r=d` has `C_I=2` and `C_K=Θ(d)`, and every document lies in some minimal bad configuration. The exact realization needs additional trusted fixed heads; this structural assumption cannot be omitted. |
| LR04 | Contribution and realism still open | Ruling out padding with irrelevant documents is stronger than last round, but "every document is relevant" is not by itself the same as a natural model or a new theory. The all-layer conjunction needs high redundancy and trusted fixed heads; the star structure needs a common bottleneck or heterogeneous impact. |
| LR05 | Local implementation robustness; source fix checked | The first version of `_exact` checked the digit count after `Fraction(value)`, so a short string in exponent notation could build a huge integer before the check. The author now applies a whitelist before parsing that allows only integers, p/q and finite decimals. This review checked the pre-parse rejection path without passing dangerous inputs to Fraction. |
| LR06 | Important positive evidence and balance of reporting | The 4 bounds-only rows must not be hidden by the summary of the 44 exact rows. On the `r=N²` path the Box cost is Θ(N³) and the optimal Total K is at most Θ(N²), so the combined baseline eventually chooses Total K, and the cost ratio relative to the combined baseline tends to 2. The proved lower bound on the saving at N=32 is 449/1008. |

This review first independently proposed the positive-segment prefix proof for greedy, the constant bound for the original family, the star candidate and the all-layer conjunction candidate, and then cross-checked them with the internal theory agent. The stronger `<2` bound and the approaching construction given by the theory agent were checked independently. This collaboration does not constitute outside peer review, and all new constructions keep the exploratory label.

## 2. Independent proof of prefix-greedy correctness, and implementation boundaries

Write the miss rate of one layer as `p_h(q)=C(N_h−q,n_h)/C(N_h,n_h)`. On the positive-probability segment, the successive factors are

`f_h(j)=(N_h−n_h−j)/(N_h−j)`, `0≤j<N_h−n_h`.

When `n_h>0` these factors are non-increasing in j; when `n_h=0` they all equal 1. Once `q>N_h−n_h`, the miss rate is 0, and the expression with a negative numerator can no longer be treated as a probability factor. Defining the factors for the remaining valid j as 0 still gives a non-increasing sequence.

Any valid contamination allocation with `Σq_h=k` corresponds to choosing a prefix of length q_h from each layer, k factors in total. Sort all factors from largest to smallest. The product of the first k is an upper bound over any choice of k factors. Because each layer is non-increasing, ties at the boundary can be broken in within-layer order, so that these k factors form a union of per-layer prefixes; hence the upper bound is attained by a valid allocation. Taking, at each step, the largest among the first not-yet-taken factors of the layers realizes exactly this ordering, so greedy is exact.

If only positive factors are stored and zeros are not, and the heap empties before k factors have been taken, then every valid choice of k factors contains a zero, and the maximum product is 0. The author's implementation handles it this way. For `k=0` the risk is 1. For `k>ΣN_h` the excluded region is empty and the risk is 0. These two cases must not be confused.

For a fixed n, the risk can be computed with a heap in `O(d+k log d)` arithmetic operations. **This does not make cost optimization over all n a polynomial problem.** With different populations or different costs, the coordinates cannot be sorted directly. Only with the same population and the same cost can the symmetric reduction to non-decreasing quotas be used.

Why the IA8 risk function cannot be used directly: for `N=20,r=2,d=3`, the direct quota `(0,19,19)` has risk 1/20, but against the total-K gate both contaminated documents can be placed in the first layer, giving risk 1. The localization algorithm only cares about one contamination in each distinct layer. The total-K algorithm must also exclude contamination concentrated repeatedly in the same layer.

**Important correction: tail flattening itself can be kept.** The initial review overstated "the first-factor product cannot be carried over" as "the first-k coordinate reduction cannot be done". After the theory agent proposed the argument below, the reviewer checked it independently and corrected the statement. Suppose all layers have the same N and the same cost, `1≤k≤d`, and n is sorted. The first factor of each of the first k chains is at least `x_k=1−n_k/N`, so the k-th largest factor overall is at least x_k. After lowering the sample sizes of the tail layers `h>k` to n_k, all new factors of these layers are at most x_k. Therefore the values of the global top-k factors and their product are unchanged (this also holds with ties and zeros), while the cost does not increase. So it suffices to enumerate the first k non-decreasing integer quotas and copy the k-th entry to the tail, with cost `Σ_{i<k}n_i+(d−k+1)n_k`. The risk must still be computed from the top-k factors of the prefix chains; it cannot be replaced by the product of the first factors of the first k chains. When `k>d` this argument cannot reduce the d dimensions.

## 3. Constant upper bound for homogeneous threshold families, and its sharpness

Suppose there are d layers with N documents each and equal costs, and a configuration is bad when at least r layers contain contamination, `1≤r≤d`. `C_I` is the optimal fixed-quota cost of the direct gate. `C_K` is the optimal fixed-quota cost of committing to `K≤r−1` when every finding is zero. Since r documents in different layers are already enough to be bad, `K≤r−1` is the largest safe gate among all gates that commit only to an upper bound on total K.

Take a direct optimal quota and sort it as `n_1≤...≤n_d`. Its feasibility gives

`(1−n_r/N)^r ≤ ∏_{i=1}^r(1−n_i/N) ≤ α`.

The balanced quota `(n_r,...,n_r)` is also feasible for the total-K gate: the miss factors for several contaminated documents in one layer are no larger than the first factor, and the worst configuration for k=r is attained by one document in each of r different layers. Therefore

`C_K ≤ d*n_r`, while `C_I ≥ (d−r+1)*n_r`.

A feasible design has `n_r>0` (otherwise r unaudited layers give risk 1), so

`1 ≤ C_K/C_I ≤ d/(d−r+1)`.

This general upper bound covers the equivalence at `r=1`, and for IA7's `d=2r−1` it gives `C_K/C_I≤(2r−1)/r<2`. The comparison here is between optimal values where both sides allow unequal quotas. The optimum of the balanced class is not passed off as the strongest baseline.

**The constant 2 can be approached asymptotically.** Fix α, let N→∞, r=N², d=2r−1, and let k be the smallest positive integer with `(1−1/N)^k≤α`; then k=O(N), and eventually k≤r. Audit no documents in r−k layers and one document in each of the remaining r+k−1 layers. The direct risk is exactly that k-th power, so `C_I≤r+k−1`. If the total-K gate has u zero-audit layers and `uN≥r`, all r contaminated documents can be hidden in those layers, with risk 1. Therefore `u≤floor((r−1)/N)=N−1`, and hence `C_K≥d−u≥2N²−N`. Squeezing against the upper bound gives `C_K/C_I→2`.

This shows that "no gain in asymptotic order" is not the same as "localization gives no gain at all"; in the worst case this family comes close to a factor of two. But the joint growth of the threshold, the number of layers and N must be stated explicitly.

**A stronger negative result at last round's specific scaling `N=r²`.** Write `a=log(1/α)` and `M=C_I`. If `M<rN`, sorting gives `n_r≤M/r` and `Σ_{i≤r}n_i≤rM/d`. From `−log(1−x)≤x/(1−M/(rN))` (here `x≤M/(rN)<1`), feasibility implies

`a ≤ rM/[dN(1−M/(rN))]`, hence `M ≥ N a d r/(r²+a d)`.

If `M≥rN`, the same lower bound holds automatically. The feasible balanced total-K cost is at most `d(Na/r+1)`, so

`C_K/C_I ≤ (1+r/(Na))*(1+a d/r²)`.

With α fixed and `d=2r−1,N=r²`, this upper bound tends to 1, and together with `C_K≥C_I` the ratio tends to 1. In other words, at the specific scaling where last round showed the Ω(r) rectangle cost, the strongest total-K gate and the direct method are asymptotically equivalent. The scaling above that approaches 2 is the opposite one, `r=N²`. The two cannot be interchanged.

## 4. An order separation with non-vacuous relevance for general threshold families

Take `d=r≥2,N=2,α=1/20`. Each layer has two documents, and both affect only that layer's single variable head. There are also d−1 trusted fixed heads that these documents do not affect, for a total of `m=2d−1` heads. All observed votes are correct, and the target can still be the fixed accuracy interval `[9/10,1]`. At any test point, when fewer than d variable heads are affected, there are still at least d votes fixed at the correct answer; when all d variable heads are affected, they can jointly vote wrong. So a configuration is bad exactly when every layer contains contamination.

Every document is relevant in the given outer-relaxation impact model: taking one document from each of the other d−1 layers and adding the given document gives exactly a minimal bad set. There are no empty impact sets, no layers that are always ignored, and no artificially added documents unrelated to failure. This is not a measurement of real retraining sensitivity. The fixed heads here are additional trusted structure. This must not be misdescribed as a homogeneous majority vote in which all heads come from the documents under audit.

**The exact direct cost is 2.** A census of any one layer detects every bad configuration, at cost 2. A design with cost below 2 audits at most one document, so the miss probability for a bad configuration is at least 1/2, which exceeds 1/20. Hence the lower bound is attained.

**Exact cost of the total-K gate.** Let a,b,c be the numbers of layers in which 0, 1 and 2 documents are audited, `a+b+c=d`. The positive greedy factors are 2a ones and b halves. The risk at the boundary k=d is:

- 1 when `d≤2a`;
- `2^{−(d−2a)}` when `2a<d≤2a+b`;
- 0 when `d>2a+b`.

The last case is equivalent to `c>a`, with cost `b+2c=d−a+c≥d+1`, which can be attained. Feasibility with positive probability requires `d−2a≥5`, because `2^-4>1/20≥2^-5`. Its cost is at least `d−a≥ceil((d+5)/2)`, attained by `a=floor((d−5)/2),c=0`. Therefore

`C_K = d+1` when `2≤d<5`; `C_K=ceil((d+5)/2)` when `d≥5`.

So `C_K/C_I~d/4`, a linear order separation. This does not contradict Section 3: here `r=d` and the general upper bound is d, while for last round's family `d=2r−1` the upper bound is below 2.

**A simpler structure-aware control attains the same gain.** Taking a census of any one layer, and reporting zero contamination for that layer and the full range for the other layers, is a safe single-rectangle gate, also with cost 2. So this construction proves the cost of the structure that total-K aggregation loses. It does not prove that a complex direct optimizer is necessary, or that direct beats all simple structure-aware rules. The star candidate has the same limitation: certifying only that the center layer is clean already attains the direct optimum. `Direct=Box=2` should be reported alongside; one cannot show only the unfavorable Total K baseline.

This is an existence construction for a finite combinatorial setting. It still does not prove that real models have enough trusted fixed heads or a nearly conjunctive failure geometry. If the goal is an algorithms/theory paper, one would further need to explain which kinds of testable structure lead to this geometry, when it can be solved efficiently, and exactly how it differs from the existing literature. The internal review does not automatically promote this new construction to a publication-level innovation.

## 5. Independent checks actually run

The independent script does not call the author's optimization or risk functions. It enumerates directly with `Fraction` and binomial coefficients.

- 900 fixed designs, with risk comparisons at 6,788 values of k in total. Greedy matches the exact maximum over all valid counts.
- The risk part actually evaluated 31,820 count vectors, including unequal layer sizes, zero sampling, census, zero probability and k=0.
- The all-layer conjunction for d=2..8 was enumerated exhaustively over the full sorted quotas, evaluating 401,031 count vectors. The direct cost is 2 in every case. The total-K costs are `3,4,5,5,6,6,7` in order, matching the closed form term by term.
- The first run exited with code 0, with internal script timing of about 3.873 seconds. These are only this machine's run times for this round, not statements about complexity or general performance.
- After the tail-flattening proof was added, 688 flattening-invariance checks were added on the same frozen input domain, and all pass. The second full run exited with code 0 in about 4.031 seconds. The sample grid was not enlarged and the existing enumeration caps were not raised.

Script path: `research/reports/localization_review_checks.py`. The general propositions above rely on explicit proofs. The finite checks only serve to find implementation/boundary errors; the number of tests cannot substitute for a proof.

## 6. Review of the author's protocol and the final version

**Additional pre-run budget for the full-table review:** After receiving the final JSON, reuse the first-k-chains risk algorithm that was independently proved and validated on a small domain; independently enumerate all sorted k-prefixes for the original 20 cells; and check only whether designs cheaper than the returned cost are feasible, without calling the author's implementation. At most 500,000 prefixes, 100,000 risk calls and 15 seconds of wall-clock time. In addition, check the 16 Star cells by enumerating a two-variable closed form, the 8 conjunction cells against their closed form, and the 4 bounds rows against the analytic formulas, and check the file hashes and the summary arithmetic. This check is an independent recomputation of results that were already public, not a confirmatory finding. If the budget is exceeded, only "not completed" is reported.

`research/planning/LOCALIZATION_PROTOCOL.md` was checked read-only. It explicitly fixes the original 20 threshold cells, the 8 conjunction cells, the 16 Star cells, and 4 sharp sequences that are checked only against analytic bounds. It also reports `min(Box,TotalK)` and does not pick the weaker baseline case by case. The freeze took place after the old results had been seen and new constructions discussed. The file explicitly calls it a freeze of the execution scope rather than a confirmatory pre-registration made in advance, which is appropriate wording. Budget failure, retention of the original JSON, no outside messages and the no-training restriction are all recorded. The review found no issue that would require blocking this finite execution.

For the sharp sequences with N≥16, the number of layers exceeds the default input limit of the general optimizer. It is reasonable for the protocol to restrict these rows to computing the proved constructions and bounds. The results must not label these rows as global exact optima.

A full-text review of `research/theory/localization_value.md` is complete. No mathematical counterexample or missing quantifier was found in LV1 (largest safe gate), LV2 (greedy), LV3 (tail lowering), the sufficient condition for no localization value, LV4 (ratio bounds / two different asymptotic scalings), LV5 (conjunction closed form), the two-quota formula for Star, or the 10/11/12 examples at the end. The two reported issues, a `\qquad` formatting error and an unstated common cost unit, have been fixed. "Every document is relevant" is now restricted to the outer-relaxation model. The finite sharpness construction now explicitly requires `k_N≤r`, to avoid a negative number of zero-audit layers at small N.

Static review of `total_count_design.py`: the positive-factor heap, the independent binomial-coefficient DP, positive-cost pruning, full sorting of the d coordinates for equal N/equal cost, and raising an error on budget overrun are all consistent with its contract. The implementation keeps all d dimensions and does not claim to implement the new first-k reduction. The overly broad comment in the first version saying "the short-prefix reduction does not apply" has been changed. The fix that forbids exponent syntax in numeric text before Fraction parsing has also been checked. The reviewer did not actually run inputs that could cause an exponential blow-up.

Running `python research/reports/localization_review_checks.py --verify-results` on the final results gave **exit code 0**, with final internal script timing of about 0.585 seconds:

- Without calling the author's functions, all 309,349 non-decreasing k-prefixes of the 20 threshold problems were enumerated, and the exact risk was computed independently for the 20,083 cheaper designs among them. No feasible total-K quota cheaper than the reported one was found. Each returned quota itself also passes the risk recomputation.
- For the 16 Star cells, the optimal total-K cost was checked by an independent enumeration over the two variables a,b. The 8 conjunction cells agree with the closed form. The 4 sharpness rows agree with the analytic upper and lower bounds and the minimal k_N, and all keep the `bounds_only` label and the label that the global exact optimum was not computed.
- The original direct costs and rectangle costs were compared row by row with the old JSON. The optimality of the new total K was reviewed by this independent prefix enumeration, without borrowing the author's search output as its own proof. The optimality of the old direct results still relies on the result reviewed last round. This round only recomputed their risk/control costs independently and did not rerun the old optimizer.
- 48/48 planned rows are complete. The hashes of the final execution sources, the protocol and the old JSON match the run record exactly before and after. The hash of the theory draft recorded at run time is also exactly the same as that of the final draft reviewed here.
- The author's full table records about 1.476 seconds and no timeout; that is the author's run record. This review's own timings and enumeration counts are given above, and the two are not reported together. Peak memory was not measured.

The main implications of the full results are as follows:

| Family | Cells in full | Strict saving vs. optimal Total K | Strict saving vs. min(Box, Total K) | Median saving vs. combined baseline | Largest saving |
|---|---:|---:|---:|---:|---:|
| Original threshold family | 20 | 14 | 5 | 0 | 1/11, about 9.09% |
| All-layer conjunction | 8 | 8 | 0 | 0 | 0 |
| Star | 16 | 16 | 0 | 0 | 0 |

In the original threshold family, the 5 cells with a nonzero saving against the combined baseline are `(r,N)=(4,10),(5,5),(5,10),(5,20),(6,2)`, with savings `1/40,2/25,1/22,1/43,1/11` respectively. The original main example `(6,20)` is still `Direct=88, Total K=88, Box=114`; the combined baseline already reproduces the whole gain of the original main example. The 14/20 against Total K, or the large gaps for conjunction/Star, cannot be substituted for the result against the combined baseline.

**Four rows of analytic positive evidence that must be kept separately.** The table above summarizes only the 44 exactly solved points. It does not cover the 4 `bounds_only` points listed separately in the protocol. Let `C_S=min(C_box,C_K)`. On the `r=N²,d=2r−1` path, the exact Box cost is `r*ceil(N(1−α))=Θ(N³)`, while auditing one document in every layer gives the feasible total-K upper bound `C_K≤d=Θ(N²)` (for sufficiently large N the risk is `≤exp(−N)≤α`). So eventually `C_S=C_K`, and the squeeze in Section 3 also gives `C_S/C_I→2` and a saving `1−C_I/C_S→1/2`. For this round's α and the four values of N, Box already exceeds the feasible total-K upper bound in every row, so all of the following combined-baseline bounds hold strictly:

| N | r | Proved interval for the direct optimal cost | Proved interval for the combined-baseline optimal cost | Exact Box cost | Lower bound on the direct method's saving vs. the combined baseline |
|---:|---:|---:|---:|---:|---:|
| 4 | 16 | [16,26] | [28,31] | 64 | 1/14, about 7.14% |
| 8 | 64 | [64,86] | [120,127] | 512 | 17/60, about 28.33% |
| 16 | 256 | [256,302] | [496,511] | 4096 | 97/248, about 39.11% |
| 32 | 1024 | [1024,1118] | [2016,2047] | 31744 | 449/1008, about 44.54% |

The saving lower bound here is computed as `1 − (upper bound on the feasible direct cost)/(lower bound on the necessary combined-baseline cost)`. It compares the global optima of the two sides, but it does not claim that these large problems were solved exactly, and it is not an actual audit saving. In particular, the lower bound at N=32 is much stronger than the 10 vs 11 in the exact small grid. One cannot cite only the latter to deny the method's substantive mathematical advantage over this combined baseline. Conversely, these exploratory analytic constructions still do not retroactively pass the original confirmatory 20% gate, and they say nothing about effects on a real task.

The first version of the full-table review did not spell out separately what these 4 rows mean for the combined baseline. After the author pointed this out, this review independently checked the Box formula, the row-by-row upper-bound comparison and all the saving fractions, and completed this section. The added proof explanation does not change the existing numerical execution inputs. The final hash of the theory draft with the new §8 is `3187fd0cfb9b39e9ff797b295557841fc59b16fd1e09d3f385edb076bea2015f`. The `d403...` hash of the draft that supported the earlier run is kept as a historical record and is not written back to fake the old execution record.

## 7. Conclusion and remaining research obligations

**This round's conditional mathematics and finite implementation passed the local independent review. A non-trivial, sharp constant advantage over the combined baseline has been proved, but the claim that "a complex structural optimizer is necessary / a strong paper-level innovation is established" still has not passed.** The current progress contains both a negative boundary and a positive separation: the advantage disappears on the original `N=r²` path, while the opposite `r=N²` path can approach a 50% saving relative to the same strong combined baseline. All new results should remain exploratory technical supplements. Passing an internal review, having an exact optimizer or adding more constructions must not be used as a proxy for originality and real value.

If the next round wants to claim that a complex optimizer is necessary, it still needs either a substantive theoretical increment against a broader, explicitly defined class of simple strategies than `min(Box, Total K)`, or a proof that some class of natural and verifiable impact structures satisfies a meaningful gain condition. The existing sharpness construction itself has a simple analytic feasible quota, so a large saving does not automatically prove that complex optimization is irreplaceable. The 10 vs 11 result and the analytic lower bound of at least 44.54% should each be kept with its correct type of evidence; neither one alone can retroactively pass the original confirmatory investment gate. Historical sources, real audit labels, the utility of trained models and the difference from outside prior work have not been verified. G0/G1 are not changed by this report.

The fixed per-layer quota restriction has a substantive effect here and cannot be left out as a footnote. If one may draw m documents uniformly without replacement from the full population `M=dN` (so that the per-layer audit counts are random), the worst-case miss rate of the total-K gate excluding `s=r` is `C(M−s,m)/C(M,m)≤exp(−ms/M)`. So for sufficiently large N, `m=ceil((M/s)log(1/α))` is enough. On the `r=N²,d=2r−1` path this is O(N), smaller than the Θ(N²) of this round's fixed-quota class. This is a comparison with a **different class of sampling procedures**. It does not enter the frozen 48 rows and does not refute sharp2 within the same-class comparison. It makes clear that the existing 50% asymptotic saving cannot be stated as an advantage over all simple audit methods. If an application must satisfy fixed layer quotas, the source of that requirement needs to be explained.

SHA256 of the key files for the first complete run and the independent recomputation (the theory hash with the new §8 is listed separately above; the old records keep their historical meaning):

| File | SHA256 |
|---|---|
| `research/theory/localization_value.md` | `d403a84db96a18d3ec5e98a1a18116cee0fd83dc7d43b388f8d7dc83a2b2669f` |
| `research/planning/total_count_design.py` | `ac0d7f2b753c5747146aa36f4abd1b920d0d9568ec556f83186d68418c5aa209` |
| `research/planning/localization_results.json` | `6924aa5d879e29b1378484e9c35bbccc6587bf8110cb0723a3159c7687a3a928` |
| `research/reports/localization_review_checks.py` | `1cc5e1a6b5fa81f9ae252374a8ce5b001a97e78d5030562ce5d0c07fdeade70d` |

## 8. Final reproduction fix and freeze record

The failure snapshot of the first unified reproduction, the full exception stack and the 6 case IDs whose persistence did not complete are saved in `research/planning/localization_io_failure.json`. A read-only review shows that `run_localization.py` makes at most 6 attempts, and only for atomic-replacement failures with Windows error codes 5/32/33, with total waiting of at most 0.775 seconds. Other errors and persistent failures are still raised, and the old target file cannot be taken as a newly completed result. The mathematical code and the comparison scope did not change because of this.

The author reports that all 13 tests pass (10 mathematical plus 3 I/O), with unittest timing of about 0.413 seconds. The reviewer statically read the 3 new regression tests. They cover real replacement after a brief lock, keeping the old content under a persistent lock, and no retry for non-whitelisted errors. The actual results were then recorded as 48/48 complete, worker exit code 0, about 1.460 seconds, no wall-clock overrun, with all execution-source hashes identical before and after.

The reviewer ran the independent `--verify-results` again on this new result: exit code 0, about 0.571 seconds. The checks of the 309,349 prefixes and the 20,083 cheaper designs, the 44 exact results, the 4 analytic lower bounds against the combined baseline, the execution sources and the hash of the final theory draft all pass. The new assertions for the 4 rows of positive evidence are verified directly in this final script; they were not only added as text.

Final frozen files:

| File | SHA256 |
|---|---|
| `research/theory/localization_value.md` | `3187fd0cfb9b39e9ff797b295557841fc59b16fd1e09d3f385edb076bea2015f` |
| `research/planning/run_localization.py` | `3ef2500be1cb9cafdd55456a0f83e6a3cfcf6709fc17eddb11ffd35934ddc617` |
| `research/planning/localization_results.json` | `f42b3f74e324422db359d53eee3970d387ae40b16aa81b85ec27bc5cacff0cb5` |
| `research/planning/localization_io_failure.json` | `dd3668f4a005bef1a228a27a1c18d9a958efcc98f5f028f1971551792c21ce6a` |
| `research/reports/localization_review_checks.py` | `522643761737e5f1a92893904b825c59eff418030d1253a8dc6fea3adfdb4ed9` |

## 9. Supplementary check after the final unified reproduction

After receiving the notice that the final unified reproduction had finished, only the reviewer's `--verify-results` was rerun; the author's experiments were not rerun. Exit code 0 again, about 0.630 seconds. The 48-row scope, the source hashes, the final theory draft and all mathematical checks remain consistent. The formal rerun updated the run time and the source hash of the old threshold JSON in the main results JSON. Its new hash is recorded in the final table below; the earlier hashes keep their historical meaning.

Budget for an additional single-point check (written before running): check only the existing `N=32,d=2047,M=65504,s=1024,m=192` in `research/planning/pooled_scope_check.json`, computed two ways, as a 192-term rational product and as a ratio of binomial coefficients, with a wall-clock limit of 2 seconds. No search over other sample sizes, no extension of the original 48 cells, and no claim of optimality or of a confirmatory finding.

The actual run of `--verify-pooled` exited with code 0, with internal script timing of about 0.001 seconds. The probability obtained by independent term-by-term multiplication is exactly equal to `C(65504−1024,192)/C(65504,192)` and to the exact fraction in the results file, and rational arithmetic confirms that it is no greater than 1/20. The decimal value for display is about **0.04833363775444638**. 192 is a feasible sample size; no search for the minimum sample size was done. The fixed-quota direct lower bound of 1024 still holds.

The contract of this certificate is as follows. Before sampling, freeze the full population of M documents, the uniform audit cost and the criterion for a correct judgment, and fix the true contamination set. Draw a fixed total of 192 documents from the full population with equal probability and without replacement. Report a total contamination count of at most 1023 only when there are zero findings. For any true configuration with at least 1024 contaminated documents, the probability of issuing a wrong certificate is no greater than the value above; by monotonicity, more contamination can only lower the miss rate. Since fewer than 1024 contaminated documents cannot reach 1024 different layers, this total-count gate is safe for the current threshold-type final statistical target.

Under pooled sampling the per-layer quotas are random, and the allocation across layers is not fixed in advance either. Its coverage guarantee therefore refers to the full random sampling mechanism. It does not mean that the gate still satisfies this round's fixed-quota risk gate after conditioning on an arbitrary realized quota vector. The pooled risk cannot be applied to a fixed stratified design, and the fixed-quota lower bound of 1024 cannot be described as a lower bound for all audit methods. **In applications that allow this kind of pooled sampling at the same cost, the simple 192-document gate is already strictly cheaper than any fixed-quota direct design of this round. Why the layer quotas must be fixed is the main limitation of the research, and passing an internal mathematical review cannot substitute for an explanation.** This single point is an out-of-class scope check. It adds no actual audit, no training, no 48-cell results and no confirmatory investment gate.

After this single-point check entry was added, `--verify-results` of the final script also succeeded again. The original 309,349 prefixes, the 20,083 lower-cost design checks and the 48 rows of results are unchanged. That round did not rerun the author's experiments.

Current file hashes frozen after the final unified reproduction (the old result hashes in Section 8 are kept as the history of an earlier successful run):

| File | SHA256 |
|---|---|
| `research/theory/localization_value.md` | `3187fd0cfb9b39e9ff797b295557841fc59b16fd1e09d3f385edb076bea2015f` |
| `research/planning/localization_results.json` | `0e990e8ef2790e3b6edde983f399efdd5e667c21bea189fe642f925dd84b7c22` |
| `research/planning/pooled_scope_check.json` | `38d4aa7867f4ad665a0425e47e22a4c3286f6111d0d50f9fb833aabf8445b43c` |
| `research/planning/localization_io_failure.json` (historical failure record, unchanged) | `dd3668f4a005bef1a228a27a1c18d9a958efcc98f5f028f1971551792c21ce6a` |
| `research/reports/localization_review_checks.py` | `ff78a96df7eba6841225f734872a4ed294f9d4583cebcb7ed6c9d42ca069f22f` |
