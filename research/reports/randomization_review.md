# Independent randomization review

## Frozen review budget (written before execution)

- Date: 2026-11-16.
- Role: internal independent AI mathematical reviewer; not Fable, not an external referee.
- Local only: no network, no outside contact, no new empirical audit data.
- Owned outputs: `research/reports/randomization_review.md`, `research/reports/randomization_review_checks.py`.
- The checker will use Python standard library only; it must not import any author kernel, optimizer, or candidate implementation.
- Exhaustive scope: all positive integer `(d,N)` with `d*N <= 10`; all `r=1,...,d`; all audit budgets `m=0,...,d*N`; every document-level audit subset and every minimal bad set (exactly one bad document in each of exactly r distinct layers).
- Separate constructive check: explicitly enumerate the randomized whole-layer strategy support and compare its maximum payoff over all minimal bad sets with the independently enumerated average-payoff lower bound. The candidate closed-form expression is only a third diagnostic, never either oracle.
- Arithmetic: integer counts and `fractions.Fraction`; no simulation, floating optimization, or tolerance-based equality.
- Hard compute budget: at most 20,000,000 payoff intersections, 120 seconds per run, and 3 checker runs. A cap breach must be recorded as incomplete, never silently truncate scope. One initial execution plus at most two corrections is allowed.
- Theory scope: fixed-size nonadaptive minimax, adaptive zero-only hard cap, and expected-budget contracts; explicitly seek counterexamples to overly broad extensions.
- Expected-budget computation: illustrative small exact distributions only, no general LP solver or unbudgeted expansion.
- Originality scope: no novelty determination is possible from this local check; finite verification cannot replace proof.

## Status

Budget frozen before execution. Review completed locally; two checker runs used, both passed. No execution cap was reached.

## Budget amendment before author-table verification

The parent requested an additional independent check of the frozen 32-row round-9 table after the first exhaustive run completed. This amendment is recorded before that check executes. Add `--verify-results PATH` to verify the exact 20 threshold, 8 conjunction, and 4 sharpness rows; compute both reported risks and preceding-budget risks using a sequential avoidance product for whole-layer selection and an independent binomial ratio for pooled sampling. Check integer minimality at alpha=1/20 and reported summaries. Do not import or call author code. Do not reoptimize the round-8 fixed-quota costs; those remain inherited evidence. This stays inside the original limit of three checker executions and 120 seconds per execution, with at most 128 additional exact risk evaluations and no expanded document enumeration.


## Independent conclusion

**The candidate closed form holds under the exact threat class and under the contract that a certificate must be issued when all findings are zero.** This report gives a complete proof and verifies it independently with a document-level integer enumeration that does not import the author's code. Arbitrary random quotas with a fixed integer budget, sequential audit procedures with a hard cap, and procedures whose expected cost in the clean world is bounded need to be stated separately. The latter two also give the same value function, but by different derivations.

The most important conditions of applicability are:

1. All documents and the layering are fixed in advance. Each layer has exactly N documents, and every document has the same audit cost. The true bad set is fixed before the audit's random seed; it cannot be chosen after observing this draw.
2. The threat class is exactly "at least r layers each contain one bad document". Every minimal bad set of the form "r layers, each with exactly one bad document" must belong to the feasible threat class. If this is an outer envelope of a real model, the conclusion proves only minimax optimality relative to that outer envelope, not optimality relative to the real model.
3. The audit feedback is a correct binary bad/good label, and no additional observation channel leaks the unknown bad set during an "all zero" run.
4. The fixed interval I is chosen before sampling. **When all audited labels are zero, I must be output; when any bad document is found, the full range is output.** "I may be output only when everything is zero" is not enough to define this problem: a zero-cost procedure that never outputs I would have zero risk of a false certificate.
5. Risk means the probability of outputting I in a bad world whose true value is not in I. A minimax result for this risk does not automatically establish real model intervals, real audit labels or a non-empty real-world certificate.

These items are the definition of the mathematical problem and its load-bearing conditions, not practical footnotes that can be dropped. Randomization being cheaper does not mean that a complex optimizer is more necessary; in this case the optimum is attained by the simple strategy of choosing whole layers at random.

## Complete proof: fixed-size random audit

Let the document set be D, divided into d layers of equal size. Fix 1≤r≤d and 0≤m≤dN. Let the family of minimal bad sets M consist of all sets formed by taking one document from each of r different layers, so |M|=C(d,r)N^r. For an audit set A and a bad set B, the payoff (the false-certificate indicator) is 1{A∩B=∅}.

Let n_h=|A∩layer h| and x_h=1−n_h/N. Under the uniform prior on M, the average risk of a fixed A is

    L(A) = [sum_{|S|=r} product_{h∈S}(N−n_h)]/[C(d,r)N^r]
         = e_r(x_1,...,x_d)/C(d,r).

This does not assume that the audit set is random independently by layer; A is an arbitrary fixed subset of documents. For any audit distribution P,

    max_{B∈M} E_P[1{A∩B=∅}]
      ≥ E_P L(A)
      ≥ min_{|A|=m} L(A).

This is a lower bound given by an explicit prior. It does not require exchanging min and max, and it does not need to cite a general minimax theorem.

With the other coordinates fixed, for any two coordinates x,y,

    e_r(x,y,z) = e_r(z) + (x+y)e_{r−1}(z) + xy e_{r−2}(z),

where e_0=1 and e_k=0 out of range. If 0<x≤y<1, let ε=min(x,1−y)>0 and replace x,y by x−ε, y+ε. The sum is unchanged, and the change in the product is ε(x−y)−ε²≤0; since e_{r−2}(z)≥0, e_r does not increase. At least one coordinate reaches the boundary, so after at most d−1 repetitions at most one coordinate lies in (0,1). The initial coordinates are on the 1/N grid, and each replacement stays on the grid, so the integer quota problem is not relaxed into an unattainable real-valued solution.

Let q=floor(m/N) and t=m−qN. For m<dN the resulting vector consists of q zeros, d−q−1 ones, and 1−t/N; when t=0 the last coordinate is simply 1. Therefore the lowest average risk is

    V(m) = [C(d−q−1,r) + (1−t/N) C(d−q−1,r−1)]/C(d,r).

C(a,b)=0 is used when 0≤a and b<0 or b>a. For m=dN one must define V(dN)=0 separately; the formula above must not be allowed to produce C(−1,r).

To attain this lower bound, choose q layers uniformly and audit them fully; when t>0, choose one more layer uniformly from the remaining layers and choose t documents uniformly within it. This distribution is invariant under permutations of the layers and of the documents within each layer, and these permutations act transitively on M, so every B∈M has the same miss probability. Its average risk is exactly L(A) for the concentrated quota above, so every minimal bad set has risk V(m). For a general bad set B, one can always choose B0⊆B with B0∈M; pointwise 1{A∩B=∅}≤1{A∩B0=∅}, so the risk is at most V(m). The lower bound and the construction coincide, and the theorem is closed.

### Boundary cases and non-uniqueness

- V=1 at m=0, and V=0 at m=dN.
- For r=1, V=1−m/(dN). In the concentration step e_{−1}=0, so the decrease need not be strict, and the concentrated strategy is not the unique optimum. Every distribution with fixed m in which each document has marginal inclusion probability m/(dN) is optimal.
- For d=1, V=1−m/N; for N=1, V=C(d−m,r)/C(d,r).
- For r=d, it suffices to audit any one layer completely; the risk is zero at m=N.
- In general the first zero-risk budget is N(d−r+1). With a smaller budget, every deterministic audit set leaves at least r layers without a census, and some minimal bad set is missed entirely. Randomization can lower this worst-case probability only when the bad set is fixed first.
- If the bad set is chosen after seeing the drawn set, then for every m<N(d−r+1) the bad set can be made of unaudited documents, giving a conditional false-certificate risk of 1. So the quantifiers over the true bad set and the random seed cannot be swapped.

## Adaptive hard cap: the result extends, but must be proved via the all-zero path

Once the whole random seed is fixed, follow the branch on which every query returns zero until the procedure stops. This gives a deterministic audit set A0 without repeats, of size at most m. For any fixed bad set B, the real run has "no finding" if and only if A0∩B=∅: until the first hit, the real run and the all-zero branch make exactly the same queries, and if the all-zero path has no hit, the real run follows it to the end.

The contract that forces a certificate on all-zero findings therefore makes the risk exactly P(A0∩B=∅). Pad A0 arbitrarily to a set A+ of size m; its miss indicator is pointwise no larger than the original one. The fixed-size theorem gives

    sup_B P(A0∩B=∅) ≥ sup_B P(A+∩B=∅) ≥ V(m).

The non-adaptive construction already belongs to the adaptive class, so the minimax value is still V(m). There is no need to enumerate complete decision trees. The argument allows stopping immediately after a positive finding. If refusing to certify after all-zero findings is allowed, the result degenerates again.

This round did not enumerate all adaptive strategy trees; what is given here is a mathematical reduction. Writing it up as "all adaptive strategies were verified numerically" would be false.

## Expected budget: two different problems

For real b∈[0,dN], extend V by linear interpolation between adjacent integer points. It is in fact linear on each segment [qN,(q+1)N], with slope

    −C(d−q−1,r−1)/[N C(d,r)].

These slopes are non-decreasing in q, so V is non-increasing and convex; on the final interval, where V is zero, the slope is zero.

If the size T of a non-adaptive audit set is random with E T≤b, then under the uniform prior on minimal bad sets the average risk is at least E V(T)≥V(E T)≥V(b). For an adaptive procedure, let T0 be the length of its all-zero path. If the budget requires E[T0]≤b, that is, if the expected cost in the completely clean world is bounded, the same reduction and Jensen's inequality give the lower bound V(b). If the budget holds uniformly over all true values, it of course includes the clean world, and the result holds as well.

Conversely, mixing with suitable probabilities the optimal non-adaptive strategies for the two integer budgets floor(b) and ceil(b) gives an expected cost of exactly b, and every minimal bad set has risk V(b). This also satisfies an expected-cost budget that is the same for every true value. Therefore, under a clean-world budget or a budget uniform over all true values, allowing early stopping does not improve this minimax risk.

**This result cannot be extended to a constraint on the expected cost in bad worlds only.** Counterexample: d=1,N=2,r=1. Order the two documents uniformly at random, stop as soon as a bad document is found, and otherwise audit both. In any world with a single bad document the expected cost is 3/2; when both are bad the cost is 1; the false-certificate risk is 0 in every bad world; in the clean world the cost is 2. So an expected budget of b=3/2 imposed only on bad worlds can attain risk 0, while V(3/2)=1/4 above. This counterexample is enumerated exactly in the independent script, permutation by permutation and bad set by bad set.

## Verification scope and execution evidence

The independent script imports only the Python standard library and does not import the author's kernel, optimizer or risk implementation. The two main numerical objects are:

1. For each m, enumerate every document-level A and every minimal bad set B, count A∩B=∅ directly, and take the minimum over fixed A of the average risk under uniform bad sets.
2. Explicitly list the support of the random whole-layer strategy as document sets, count misses for each minimal bad set, and take the maximum.

Only after these two agree is the candidate closed form compared as a third diagnostic value. Two functions that call the same closed form were not used to "verify" each other.

Actual scope of the first run: all positive integers (d,N) with dN≤10, 27 pairs in total; for each pair, all r=1,...,d and m=0,...,dN, giving **87 risk tables and 709 budget problems**. The run generated 7,306 audit masks (counted once per (d,N)), 2,583 minimal-bad-set masks (accumulated over (d,N,r)) and 22,542 construction support actions (accumulated over (d,N,r,m)), and performed a total of **3,239,464 exact payoff intersections**. In all 709 cells, prior lower bound = worst-case risk of the construction = closed form, and the discrete slopes of all 87 independent risk tables are non-decreasing. The budget cap was not reached.

Additional expected-budget example d=3,N=2,r=2: mixing budgets 2 and 3 with equal probability, direct enumeration gives risk 1/4 for every minimal bad set and an expected cost of 5/2. The counterexample with a budget on bad worlds only is also enumerated in the original query order, without calling the candidate formula.

The observed time of the first run was 0.184557 seconds. This is an observation of execution on this machine, not algorithmic complexity or a cross-machine performance guarantee. Peak memory was not measured, and no model training, data audit or real cost measurement was done.

Reproduction command (from the root of this worktree):

    & '..\130U-FinLLM\.venv\Scripts\python.exe' 'research\reports\randomization_review_checks.py'

SHA256 of the canonicalized record of all 709 cells:

    acb8af54ed68e6121e70966d099ff895200258643d7e183139b61dcd1cbc484a

The script prints its own current SHA256, the counts, the boundary examples and the full scope, which helps prevent different versions from being mixed into one piece of execution evidence. The SHA256 of the version used in the first run is 1aacf4eab89e903784d9055c1ba995ff26884bfb8a1120bc923d3b42236d82b1. Afterwards, at the parent agent's request, an interface for checking the author's table was added, so this old hash does not represent the final script.

## Independent check of the author's 32-cell results table

Status: the author's table after final integration **passes 32/32**. All 128 exact risks at the current/preceding budget match, and all integer-minimality conditions pass. The second run also reran the complete independent document enumeration of the 709 cells. Total observed time 0.230907 seconds. Actual command:

    & '..\130U-FinLLM\.venv\Scripts\python.exe' 'research\reports\randomization_review_checks.py' --verify-results 'research\planning\randomization_results.json'

The risk of the random strategy uses the avoidance product for drawing whole layers in sequence, multiplied by the conditional miss probability of the partial audit in the remaining layer. The pooled risk uses the raw ratio of binomial coefficients. For each cell, the strict crossing of the alpha=1/20 threshold between the current budget and the budget one document smaller was checked. Since both risks are non-increasing in the budget, feasibility at the current budget together with infeasibility at the preceding budget proves integer minimality. Rounded display decimals play no part in the decision.

The round-8 fixed-quota optimal costs are not re-enumerated here. For the related "gains", only the arithmetic, ranges and summaries of the numbers in the table are checked independently; the evidence for the fixed costs themselves is still the round-8 report and the existing independent review. All 32 cells are exploratory hand-built structures and cannot serve as a new confirmation set.

| Hand-built structure family | Cells | Strict saving vs. pooled | Median saving relative to pooled | Strictly below the inherited fixed-direct lower bound |
|---|---:|---:|---:|---:|
| threshold | 20 | 20 | 64/315 | 18 |
| and | 8 | 8 | 1/2 | 0 |
| sharpness bounds | 4 | 4 | 1069/4324 | 3 |

These summaries were recomputed by an independent program. The comparators must be kept alongside. All 8 and rows beat pooled, but they all tie with the cost 2 of "fixed census of one layer"; reporting only the wins over pooled would hide the fact that a known simple baseline is already optimal. The fixed costs of the 4 sharpness rows are still intervals: the upper bound cannot be called the exact optimum, and the equal lower bound in the N=4 row cannot be taken to mean a real tie. The original 16 star rows do not satisfy the symmetric threshold structure and were not quietly counted under this theorem.

Independent check of the largest row, N=32: the minimum budget of the random scheme is 141, with risk 28239839/570148863; the risk at the preceding budget 140 is 9598421/190049621, strictly greater than 1/20. The construction is a census of 4 layers plus 13 documents sampled from one more layer. The integer minimum budget for pooled is 190; round 8's 192 was only a feasible budget and can no longer be called the optimal value in this round.

The version evidence at execution time is below. All 5 source hashes recorded in the author's results equal the values recomputed from the local files. Equal hashes prove only that the versions correspond, not that the mathematics is correct.

| File or record | SHA256 |
|---|---|
| Final independent check script | 1b6dfed3c880f0eb587327a91a37f173bc932da5deb3ef689a2de0f54e1f5cd3 |
| randomization_results.json | 90c3feb577533f39d69be92b687f0f77db3ff3cd38eb6f617a7785899c690616 |
| run_randomization.py | 702312f54f5defa628458d4c4538143eb9821995771c679d0e212168882b051d |
| randomized_audit.py | bbe16b1637e1cc805c9c81f53aca261bd3a8347076312efa7f8fde77adebfd6d |
| test_randomized_audit.py | 985595a14a716ea284b5bc40520b1704b63b90ca2d23b7a3719208e36aa125cd |
| RANDOMIZATION_PROTOCOL.md | 0dc929118dfbde182c49493201e0c34dff74dc762ac1e246f1ff4740f2e831a8 |
| Inherited localization_results.json | 9b7f81cd51d6724838afa7b08707363c988bb4b361c64e9cac1b20d2a3f2c1d0 |

Reading the author's script that generates the main table also confirmed the following: the set of 32 cell IDs has a complete scope check; failures are not treated as completed; each row keeps the risk at the preceding budget; the sharpness fixed costs are marked as non-exact; and the ranges of the costs on both sides are clearly defined. This semantic reading does not include a line-by-line audit of the author's random-risk kernel. The core correctness is supported by this report's independent mathematical proof and by computational comparisons that import no author code.

## Proof closure and research status

| Unit or risk | Initial state | Independent review result |
|---|---|---|
| Fixed-size claim | A proof sketch was provided | This report expands the complete lower bound, the integer concentration and the construction that attains the lower bound; holds under the stated conditions |
| Ambiguity of "certificate allowed only on all zero" | S1: admits a degenerate procedure that never certifies | Must be changed to "certificate required on all zero"; this report adopts that definition explicitly |
| Integers and boundaries | r=1, t=0, m=dN need explanation | Handled separately; no claim of a unique optimum |
| Adaptive hard cap | The adaptive set cannot directly be treated as an ex ante distribution | Closed by the all-zero seed path and the padding reduction |
| Expected cost without a stated scope over true values | S1: different budget contracts give different results | Complete convexity proof for clean-world or all-true-value budgets; explicit counterexample for budgets on bad worlds only |
| The real model is only enveloped | S1: could be misstated as optimal for the real model | Optimality holds only on the complete feasible threat class; the outer envelope cannot be promoted |
| Novelty and usefulness | Not verified | No network, no outside review; no judgment of originality or real-world value |

Proof sketches: 1; expanded: 1; not expanded: 0. The review status is "mathematically closed locally, given the explicit contract and threat class". It is not a formal proof or the endorsement of an outside human referee. This report was written by an internal independent AI reviewer and **is not Fable's opinion**.

Finite checks do not rule out errors in the check script itself, and they do not replace a general proof. The reachability of the exact family of minimal bad sets, the real impact graph, reliable audit ground truth and the actual interval semantics still have to be established separately. No outside literature was consulted, so this finite symmetric combinatorial result cannot be judged novel. G0/G1, a real non-empty certificate and the necessity of a complex algorithm have not been proved.


## Final review of the frozen author full text and the round-9 narrative

After the independent enumeration and the main table were complete, the author's final full draft `research/theory/randomized_audit.md` and `research/reports/2026-11-16-round9.md` were also read. This is a review of text and versions. The computations that had already passed were not rerun, and the set of numerical cases was not enlarged.

- Author's theory draft SHA256: `4fd7808a87e1712aaf1ee6f4c1f40fce2dd83f5b7f7c5ea559675cc7b981977d`.
- Round-9 report SHA256: `1add400b39f8a738b8766208315b58c9ac32ef9018f522829b1bf502911e96b3`.

For RA1, RA2 and RA3, the threat family, the mandatory certificate on all-zero findings, the order of the random seed and the true value, the restriction on adaptive feedback and the worlds covered by the expected budget all agree with the propositions reviewed in this report. The author was not found to promote outer-envelope optimality to real-model optimality, or to mix the bad-world-only expected-cost example into the main theorem.

The new RA4 optimality of the total-count gate also holds. Averaging uniformly over all r-element bad document sets, the average miss rate of any fixed m-element audit set is C(dN−m,r)/C(dN,r), and SRS over the whole population attains this value for every such bad set. So calling pooled "optimal for the total-count coverage contract, given the same randomized design capability" is supported by a matching lower bound. The two classes of procedures commit to excluding different bad sets, and the draft distinguishes them. This does not imply an advantage over all simple audits.

The new asymptotic note in Section 6 was checked step by step. With alpha=1/20 fixed, r=N² and d=2r−1, the limiting risks at budgets 4N and 5N are 1/16 and 1/32 respectively; the crossing point on the linear piece satisfies remainder/N → 2/5, so structural budget/N → 22/5. The log product for the total-count gate uses z_max=O(N⁻²); r z_max²/(1−z_max)=O(N⁻²) → 0, and the risk tends to exp(−lambda/2). Squeezing the minimum integer budget with the strict limits on both sides of the threshold and monotonicity then gives budget/N → 2log20. The limiting saving 1−11/(5log20) is a constant difference between different coverage commitments within the same permitted design class; the author did not pass it off as a gain in asymptotic order or as empirical evidence on natural data. The note's proof is complete and does not depend on any new numerical scan.

The round-9 report's 32-cell scope, the counts of strict improvement over fixed direct (18/20 and 0/8), and the values 141/190, 49/190 and 883/1024 for N=32 all agree with the checked records. The limits are kept explicitly: zero additional gain for the conjunction family, the sharp fixed costs still being bounds, the original 192 being only feasible, G0/G1 not reached, no novelty check, and nothing sent to Fable. The 125 tests and 13 reproduction commands mentioned in the text belong to the author's integration run record; this review does not pass them off as its own reruns. No substantive mathematical or scientific-narrative problem requiring changes was found.
