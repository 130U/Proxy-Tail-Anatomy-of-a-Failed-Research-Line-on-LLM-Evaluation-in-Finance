---
artifact: audit
scope: dependency_expanded
source_files: [research/theory/impact_audit.md, research/planning/impact_report.md, research/reports/completion_audit.md, research/paths/DECISION_CRITERIA.md, research/paper/manuscript.md, research/paper/manuscript.tex, research/paper/FABLE_DECISION_NOTE.md]
theorem_ids: [IA1, IA2, IA3, IA4, IA5, IA6, IA7, IA8]
assumption_ids: [A1, A2, A3, A4]
issue_ids: [PR01, PR02, PR03, PR04, PR05, PR06]
commit: 8e4dd0b-plus-uncommitted-research
generated: 2026-11-16
generator: internal-paper-reviewer; adapted mathematics-proof-review method
---

# Fixed stratified zero-finding audit: paper-level independent adversarial review

The reviewer is the internal AI sub-agent `paper_reviewer`, not Fable; it does not represent external peer review and does not replace the advisor's decisions. Fully offline throughout: no training, external messages, literature downloads or publication. The assumption, quantifier, counterexample and evidence-layering methods of the local "academic research - mathematical proof review" skill were used; no claim is made that the skill's external multi-round review, Lean, or LaTeX citation-verification procedures were completed. Only this report was modified; the mathematical proofs and optimizer under review were not modified.

**Current verdict: IA1–IA8 can hold within the explicit fixed design and the relaxed threat model, and no counterexample to the core theorems was found; but mathematical correctness is not the same as already forming a sufficiently original, sufficiently useful standalone paper. The most important new finding of this review is that the headline r=6, N=20, 88 vs 114, and the Ω(r) rectangle separation are equally achieved by a total-contamination-count gate that needs no detail about where the contamination is located. The paper must separate "the cost of the rectangle's intermediate commitment" from "the value of the influence-location structure itself".**

At the time of the first review, `research/paper/manuscript.md` did not yet exist; v1, v2 and the corresponding TeX were then read, and the main text, the full table in Appendix C and the Fable note were cross-checked. The initial findings and the item-by-item revision status are recorded separately in the last section.

## 1. Main findings and what the author should respond to

Mathematical issues use S0–S3: S0 means the main conclusion does not hold, S1 a missing key premise or step, S2 a local ambiguity, S3 an editorial issue. Scientific-contribution issues are labelled Major separately, so that "not novel enough" is not miscalled a mathematical error.

| ID | Severity and status | Evidence and impact | What the author should respond |
|---|---|---|---|
| PR01 | Major; the substantive contribution issue remains open | The balanced scheme of IA7 also exactly certifies the total contamination count K≤r−1. So the most prominent 88 vs 114 and Ω(r) do not require using the location of contaminated documents; see the full derivation in the next section. Comparing only against the rectangle cannot prove that the influence-structure method beats the strongest simple counting method. | Include the total-K gate and its equal cost in the full text; call the main theorem the cost of the fixed single-rectangle intermediate coverage commitment; if the value of location is to be stressed, give a separate strict difference against a total-K gate in the same sampling class. |
| PR02 | Major; the qualifying wording can be fixed, the innovation issue remains open | A single rectangle is a restricted class of confidence regions. Once a non-rectangular safe count region D is allowed, the risk of the count-confidence-set method equals that of the direct method; see Section 3. IA6 already correctly limits the box-coverage commitment, but the full text must avoid the broader suggestion that "the direct method breaks through count confidence sets". | Give the definition of D and the coverage-equivalence proof, with all q restricted to the legal count grid; state precisely that "strongest" is only relative to the class that outputs a single pre-specified safe box on all-zero. |
| PR03 | Major, open | The bulk of the IA1–IA8 proofs is finite counting, monotonicity, minimal elements and sorting reductions; exact enumeration by itself does not prove algorithmic innovation. The existing local review also positions finite auditing as a transfer of mature methods, but this round did not check the original papers needed to judge prior work on this separation family. | Write "originality not verified" into the contribution statement; a theorem-level table of differences from prior work is needed for the current narrow proposition, or the manuscript should be positioned explicitly as a conditional interface / technical note. Publication-level novelty cannot be inferred from finding no counterexample, nor can it be asserted without checking that "someone has already proven the same theorem". |
| PR04 | Major; the existing report discloses honestly, but the scientific limitation is not closed | All heads vote the true label, each stratum influences exactly one head, J=1: this is a hand-made oracle threshold structure; even if changed to multiple points and two classes, the worst case can still make all of them wrong together. Of the 20 cells, 9 improve, 11 have no gain, median 0, failing the recommended full-family median 20% gate. | Keep the full table and the no-gain baselines in the full text or in a directly readable appendix; do not treat multi-point replication as a realism reinforcement. It can serve as an existence example in mathematics, but cannot carry evidence of natural-model non-emptiness, real utility, or expected savings in manual cost. |
| PR05 | Major; the conditional boundary remains open | The G0 overall item in completion_audit.md has not passed; G1 non-emptiness under realistic parameters is missing, and novelty and T4 are only partial. Real influence graphs, historical ground truth and gold-label audits are not closed by the mathematical derivation passing. | Continuing the conditional mathematics and tidying the manuscript is allowed, but the manuscript must not be equated with a flagship choice / project completion. If the original 24M requirement of G0 is later modified, the advisor / research-plan revision should be recorded independently, not silently replaced by this review or by the paper writing. |
| PR06 | S2, needs checking in the full text | "Global optimum" actually excludes random quotas, certification on non-zero findings, sequential designs, non-uniform within-stratum sampling, changing the stratification / influence graph, and cases where real training is more robust than the relaxation. The conditional-sampling quantifier of A1 allows choosing I before the audit based on V/y, but not choosing the interval after seeing the audit results. | Where the word "optimal" is first used in the abstract/theorem, state the fixed-quota class; make the conditioning on training randomness and on pre-audit information explicit. The output interval covers only the actual deletion comparator on the fixed test set, not future population accuracy. |

## 2. PR01: the strongest simple alternative and an independent computation

### 2.1 The total-contamination-count gate of the balanced design exactly reproduces the main separation

Follow IA7: d=2r−1 strata, N documents per stratum, a fixed n audited per stratum, independent across strata. Write K=Σ_h q_h. On zero findings, output the count region

```math
D_K=\{q:K\le r-1\}.
```

This region is safe because when the total contamination count is at most r−1, the number of contaminated strata is also at most r−1. It does not use any judgement about which strata the contamination falls in.

For each stratum, if q≤N−n, then

```math
p_h(q;n)=\prod_{j=0}^{q-1}\frac{N-n-j}{N-j}
\le\left(1-\frac nN\right)^q.
```

If q>N−n, the left side is 0 and the upper bound still holds; for q=0 both sides are 1. So any true configuration with K≥r satisfies

```math
p_n(q)\le\left(1-\frac nN\right)^K
\le\left(1-\frac nN\right)^r.
```

Placing one contamination in each of any r different strata attains the last bound. So the exact worst-case miss risk of the total-K gate is exactly `(1−n/N)^r`, identical to IA7's direct balanced scheme. This is the same fixed stratified sampling mechanism, not a covert switch to uniform sampling over the whole population.

So for r=6, N=20, n=8, the total-K gate likewise gets risk `729/15625` with 88 audits; the Ω(r) rectangle cost-ratio separation at N=r² is also achieved by this simple gate. This result does not refute IA7; what it refutes is the narrative of using IA7's main example to prove that "location structure must be used to obtain these savings".

### 2.2 The total-K gate is not equivalent to location structure everywhere

Allow unequal fixed quotas, and take r=2, N=20, d=3, alpha=1/20. The total K≤1 gate must rule out every true configuration that places two contaminations in a single stratum. So every h must satisfy

```math
\frac{(20-n_h)(19-n_h)}{20\cdot19}\le\frac1{20}.
```

At n_h=15 the probability is `1/19>1/20`, and at n_h=16 it is `3/95<1/20`, so each stratum must audit at least 16 documents and the total cost is at least 48. Under quotas (16,16,16), the risks of the two kinds of K=2 configuration are `3/95` (same stratum) and `1/25` (different strata), both within the target; K>2 is no more dangerous by monotonicity. So 48 is the exact optimal cost of **this specific gate, fixed stratified zero-finding reporting total K≤1**, and the unique minimal quota is (16,16,16). It is not a lower bound for all non-rectangular counting methods.

The direct method's (0,19,19) has risk 1/20 and cost 38, and the existing specialized optimizer also gives 38 as the global optimum. So one can report that influence location has strict value in this example: 38 vs 48. This example arose after this round's review and should be labelled an exploratory supplement; it is not a pre-frozen additional success gate, and cannot be used to rewrite the conclusion that the median over the full 20 cells is 0.

### 2.3 Small checks actually run by this review

Computed independently with the Python standard library, without calling the author's risk or optimization functions:

- For N∈{2,3,5}, r∈{2,3} and each n∈{0,…,N}, all legal K=r count configurations were enumerated one by one; across 26 balanced designs, the maximum exact rational probability always equals `(1−n/N)^r`.
- For r=2, N=20, d=3, all `21³=9261` fixed quotas were enumerated with the six K=2 count configurations, giving the total-K gate optimum 48, quotas (16,16,16), worst-case risk 1/25.
- The r=6, N=20 balanced risk was recomputed exactly as 729/15625.

The full independent algorithm is saved in [paper_review_checks.py](paper_review_checks.py). Run `python research/reports/paper_review_checks.py` from the repository root; it reads no data, does not call the author's implementation, writes no result files, fully traverses the 9261 quotas and the 6 K=2 count configurations for each quota, and outputs exact fractions. The derivation above also covers K>2, so larger contamination counts need not be enumerated.

These three items support the finite inputs and the identification of the newly proposed baseline; the general conclusions rest on the proofs above and are not replaced by tests. No training was re-run, the existing threshold_results.json was not modified, and this review's run time was not counted as the author's experiment time.

## 3. PR02: non-rectangular count regions are equivalent to the direct method

Let the legal count grid be `Qgrid=∏_h{0,…,N_h}`, and define

```math
D=\{q\in Qgrid:\text{there is no }a\in Q_{\min}\text{ with }a\le q\}.
```

**Count-coverage equivalence.** If D is reported on zero findings and the full grid on any other result, the worst-case count miscoverage risk is `max_{q∉D}p_n(q)`. Each q outside the box dominates some a, and monotonicity gives `p_n(q)≤p_n(a)`; each a is itself outside D and is realized by some real document configuration, so the lower bound is also attained. So the risk is exactly `max_a p_n(a)=R_I(n)`. This step uses only the monotonicity of the miss probability and the realizability of a.

**Exact semantics of the maximal safe count region.** To say further that D contains exactly those q for which "every document-location configuration with that count is safe", IA2's upward closure of the bad sets is needed. If a≤q, start from a minimal bad document set M realizing a and fill each stratum up to q_h documents; since q_h≤N_h, this can always be done. The resulting C⊇M is still bad. Conversely, any bad C dominates the minimal count of some minimal bad configuration. So q∉D if and only if there is a bad location configuration with that count.

This does not claim that every location configuration with the same q is bad; it only says that q cannot be inside a count region that requires every location to be safe. Without upward closure, the risk equivalence can still hold, but the statement "maximal safe region" needs a separate proof.

So the direct method can also be described as calibrating this non-rectangular count region and then passing it on to the final I. The paper's separation targets the rectangular shape restriction, not the principle of first building some intermediate count confidence set.

## 4. Review of the core proofs

| Unit | Verification result | Attempted attacks and key boundaries |
|---|---|---|
| IA1 | Holds conditionally | A fixed DAG and complete control dependencies give topological induction; the joint-deletion OR counterexample correctly refutes substituting per-document sensitivity for structural dependence. Whether the real training graph covers all tokenizer/selection/re-sharding dependencies was not verified. |
| IA2 | Holds conditionally | Allowing a variable head to keep its original vote guarantees nesting; the direction of the tie offset in the majority-vote reachable-class formula is correct; independent vote changes across points let the accuracy endpoints be attained jointly. If a narrower real-training reachable set is adopted, the current result is still an outer relaxation. The threshold family needs at least two outputtable classes. |
| IA3 | Holds conditionally | Fixed true C, independence across strata and uniform within-stratum sampling without replacement give an exact product of binomial coefficients. The probability of erroneous certification is controlled; it is not P(ground truth safe ∣ zero findings). After conditioning on pre-audit information the sampling mechanism must still be kept; one may not audit until satisfied. |
| IA4 | Holds | The two steps, minimal elements of sets → Pareto-minimal counts, are correct. The risk reduction does not need the whole bad set to be upward closed; checking only single deletions to judge minimality / prune needs upward closure. The original text already makes this distinction explicit. |
| IA5 | Holds conditionally | Full enumeration of a finite grid and exact risks give the optimum of the specified class; this is optimality by exhaustion of the feasible set, not a polynomial algorithm for general graphs. A smaller threat set from real training is outside the scope of necessity. |
| IA6 | Holds | With a shared all-zero event, the maximum miss probability over out-of-bound strata is the sharp value, not a sum; b_h+1 contaminations in a single stratum attain the bound. Bonferroni is only a weaker additional baseline. |
| IA7 | Holds conditionally | The threshold of r variable heads, at least r zero-budget box coordinates, and the construction attaining the box lower bound are all correct. Fixed alpha and N=r² give Ω(r), while the total corpus grows at the same time. The total-K alternative narrows its scientific interpretation but does not change whether the proof is true. |
| IA8 | Holds | After sorting, the smallest r quotas determine the risk; lowering the tail to the r-th entry leaves the risk unchanged and does not increase cost. The corresponding objective `Σ_{i<r}a_i+r*a_r` is correct; this reduction does not carry over directly to unequal costs / stratum sizes. |

No S0 or S1 mathematical errors were found; no real premises were marked Verified. Boundaries such as the empty bad set, an empty contamination that is already bad, zero sampling, a census, and a full-budget box are compatible with the original conventions. Fixing training randomness only makes the deletion comparator deterministic given the conditioning information; it does not automatically certify historical sources, the correctness of sampled labels, or future performance.

## 5. Paper completeness and G0/G1

This round is enough to produce a self-contained, reviewable conditional mathematical note or candidate paper draft; the current evidence is not enough for an internal review to declare that it has the originality and usefulness of a strong standalone paper. In particular, "exact optimizer" means an exact solution within the locally enumerable range; code and test counts cannot substitute for new complexity bounds, real task evidence, or differences from prior work.

The current mathematical results do not need a model to be trained first in order to be true, so the missing G0 items are not a logical obstacle to continuing the proofs or the writing. But the project's established gates for main-line training and the flagship choice keep their original meaning: the original 24M per-item family evidence cannot be recovered by new mathematical constructions; G1 non-emptiness on a realistic model, the training budget and the novelty of the narrow proposition still lack material. Whether to revise the research goal or increase the investment is for the user and Fable to decide; this report does not approve or veto on their behalf.

The most valuable response from the author is not to add more hand-made correct points or more interfaces, but to make clear whether this manuscript is meant to prove the cost of the rectangle's expressive restriction, or to prove the independent increment of influence structure over a strong simple audit baseline. The two have different evidence and must be evaluated separately.

## 6. Manuscript cross-check and revision re-review

### 6.1 Item-by-item cross-check of the v2 main text

| First-review item | Author response and where it was verified | Verdict after revision |
|---|---|---|
| PR01 simple total-K alternative | The abstract, the total-K proposition and its proof in §7, the three-row 88/114/88 table in §9, and §10 all state explicitly that the main separation does not need location modelling; §7 also gives 38 as feasible and 48 as the exact gate lower bound, labelled as a post-review analytic comparison | **Omission/narrative issue closed.** The upper-bound derivation and the zero-factor boundary are valid; the new analytic example was not counted as a confirmatory gate pass. The real relevance of location value, the general structural increment and originality remain open. |
| PR02 non-rectangular equivalence | §6 gives D on the legal grid, uses upward closure of bad sets to extend and realize q, and proves that the count-coverage error equals the direct risk; the restriction to a single pre-specified safe rectangle is stated explicitly | **Mathematics and qualifying wording closed.** "There is a bad configuration with this count" was not miswritten as "every location with this count is bad"; nor is it claimed to surpass all count confidence sets. The source-format conversion issue in the formula is covered separately in 6.2. |
| PR03 originality / algorithmic contribution | §2, the abstract and §10 all keep novelty as unverified, and position the work as a self-contained interface, proofs and an exact implementation; §8 acknowledges exponential complexity and the computational budget | **Overstated wording closed; scientific Major open.** There is still no full table of differences from prior work for the current narrow theorem, so it cannot be declared that a standalone original paper is established. |
| PR04 toy and negative results | §7 states J=1 hand-made voting explicitly, Appendix C lists the full 20 cells and explains the Balanced gate, §9 keeps the median 0 and the failure of the 20% gate; real SEntFiN serves only as context | **Disclosure issue closed; scientific Major open.** Multi-point replication is not called a new realism validation; influence structure / audit utility on real tasks is still missing. |
| PR05 G0/G1 | §10 states explicitly that the research goal is not complete, G0/G1 have not passed, and nothing has been sent to Fable; the note leaves the judgement to the user and the advisor | **Risk of misreporting status closed; acceptance gaps open.** The internal review is not authorization to change research gates, nor the advisor's opinion. |
| PR06 quantifiers / optimal class | §1 excludes sequential designs, non-uniform within-stratum sampling and random quotas; §3 fixes randomness and pre-audit conditional sampling; §5 states explicitly that this is not a posterior after zero findings; §8 gives exhaustive optimality over a finite class and the handling of incomplete searches | **Qualifying wording closed.** The commitment is still only for the relaxed threat model, a fixed test quantity and a fixed design; the real dependency graph is not certified by the proof. |

The r, N, Direct, Box, Balanced and exact Saving of the 20 rows in Appendix C were checked row by row against `threshold_results.json` with a read-only script, and all agree. The Balanced column is called optimal only within the balanced class and is not passed off as the optimum of the unequal-quota total-K gate. The review re-checked the current condensed statements in Appendices A/B and saw no obvious new contradiction; their full original proofs, source code and experiment review were not redone in this round.

The four discussion changes in FABLE_DECISION_NOTE.md accurately convey this review: the rectangle max, general non-rectangular equivalence, the total-K reproduction of the main example, and the location-sensitive 38/48 described separately. It states explicitly that it has not been delivered to Fable, that no feedback has been received, and that it is not a flagship choice; I did not decide on Fable's behalf whether to continue or end the direction.

### 6.2 Check of the manuscript's source-format fidelity

For v2, the inline/display math of the MD and the corresponding math segments of the TeX were extracted with regular expressions, keeping the order and normalizing only whitespace before comparing. Of 176 segments in total, 175 agree exactly; it was found that the definition of D in the MD used a single `$` spanning lines, and the TeX converter turned that segment into literal escaped commands such as `\\textbackslash{}left`. This is a real source-conversion defect, not just a typesetting preference. The author changed it to display math in v3 and regenerated the TeX; an independent re-check shows that **the two source drafts still each have 176 math segments, and all agree in order**, and the display definition of D is present. This source-conversion defect has been fixed and closed.

It was also pointed out that the original box budget in §6 was written only as `0≤b_h≤N_h`, while the later binomial coefficients require integers. v3 now states `b_h∈{0,…,N_h}` explicitly, and the comparison of math segments across the two drafts includes this change; this S2 local definitional ambiguity is closed, and it does not change the integer definition in the original IA6 theory.

The PDF has not been included in this report's completion check; the TeX has not passed a real TeX compilation. This report does not infer from the math check of the source files that the PDF has been checked page by page or that LaTeX compiled successfully.

SHA256 of the final reviewed source drafts (v3; later changes must be re-checked):

| File | SHA256 |
|---|---|
| `research/paper/manuscript.md` | `a9cd81ab194e54bb583dab69cbc7f3440745468b2f701ee6146e66c02d844ce0` |
| `research/paper/manuscript.tex` | `f4b423e730e235c38d816d4f50ea61fa2a6cb6b16d0aac94b906e29f144c02f2` |
| `research/paper/FABLE_DECISION_NOTE.md` | `de785c0db986876fba42e187a16e1da9c31bd8f220dd16e73cf6e67fe317be9f` |

### 6.3 Current academic disposition

**Agreed: it can be organized as an internal technical report for the user to review. Not agreed: claiming on this basis that originality is confirmed, that a standalone flagship is established, or that the paper meets submission conditions.** The core mathematics is reviewable within its conditions, and the author has accepted the most important strong-baseline limitation; the user and Fable still need to judge which narrow difference is worth the next round of research. This judgement is an internal evidence assessment, not an external accept/reject decision.
