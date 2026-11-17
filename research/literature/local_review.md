# Independent review of the local foundation code and reports

Date: 2026-11-15 · Method: read-only review of code/JSON/reports, offline independent small-domain checks · No new network requests.

Under review: `research/local/world.py`, `audit.py`, `ablation.py`, `write_report.py`; also read `research/evaluation/evaluate.py` with the corresponding tests and experiment JSON. The line numbers below refer to the snapshot from the first review round; the main agent then made fixes, and the status is recorded under each item.

## Items that needed correction

### R1: floating-point endpoints of statistic intervals may round inward

**Status after the fix: resolved and independently reviewed.** The current implementation uses Fraction to accumulate the exact binary values of the input floats, saves exact fraction strings, and after converting to float compares with Fraction and moves outward with nextafter when needed. An independent rerun of the counterexample below gives lower≤exact value≤upper, and both exact endpoints equal the true value; the updated JSON includes an arithmetic note. This change is enough to resolve the item and does not rely on adding an arbitrary tolerance.

In the first round, `audit.py:69` used `sum(lo)/len(lo)` and `sum(hi)/len(hi)`, which cannot guarantee that the floating-point result still contains the mathematical interval. Counterexample: three single-class fixed predictions with per-item scores `1.0, 1e-16, 1e-16`; ordinary floating-point summation loses the small terms and outputs the point interval `0.3333333333333333`. If the input floats are taken to be the corresponding exact reals, the true mean is strictly greater than that upper bound.

This does not affect the two demonstrations in this round, which use only 0/1 scores with a mean of exactly 1, but it does affect the claim of a "numeric certificate" for general bounded scores. Recommendation: define the semantics of the input values, accumulate exactly with Fraction, and output the exact fraction together with outward-rounded floating-point endpoints; or explicitly downgrade the current interface to a non-certified numeric approximation. Priority: must be resolved before the interface is used as a certificate.

### R2: the report generator contains hard-coded conclusions detached from the JSON

**Status after the fix: resolved and reviewed.** The parameter count is now read from the JSON; guards cover the number of steps, the number of seeds, zero paired differences and zero intervals, perfect classification for original/edited/permissions, all violation rates being zero for edited/permissions, and shuffle having classification errors. The key static narrative no longer depends only on zero paired differences. The script is still a report renderer for the frozen first-round experiment; refusing to reuse the interpretation when new results appear is an appropriate boundary.

In the first round, `write_report.py:14,25` wrote as constants the parameter count of 13,739, 250 steps, differences of 0 for all three seeds and the paired interval [0,0], plus fixed text such as "shuffling causes about one misclassification". The current JSON does support these values: every parameter count is 13,739; all three paired macro-F1 differences and intervals are 0; all three shuffle runs get 119/120 correct.

The problem is that after rerunning with a different seed/configuration/data, the report would still assert the old results. Recommendation: generate the report dynamically from the JSON; qualified conclusions that cannot be written dynamically must assert that the current results satisfy their premises, and otherwise fail and require review. Priority: resolve before handing it over as a reproducible entry point.

### R3: the shuffled-permission control has dead gradients and needs a clear explanation

**Status after the fix: disclosed; accepted with qualification.** The updated report now states clearly that REL is constant with zero gradient on pairs with the same labels, and that it is not a pure mismatched-pair control of equal strength. There is no need to rerun in pursuit of significance; if the next round studies this mechanism, it must pre-register a control design with discriminating power.

In the first round, `ablation.py:66–68,104` shuffled the permission types but kept the original pair's `ya,yb`. When an INV/LBL pair is assigned to REL, `ya==yb`, the log-odds difference is always 0, so the REL loss is a fixed margin and its gradient is 0. This is a consequence of the actual shuffle design and cannot be read as a pure semantic-label negative control with the same effective constraint strength.

There is no requirement to retune for "fairness" to obtain a desired result; keeping this control is enough, but it should output the cross-type counts, the number of inactive REL pairs and an explanation. The most important comparison is still permissions vs edited_ce under the same edit exposure, where this round observed no additional gain. The report already cautiously rejects the claim of a gain; the point of the fix is to describe the control mechanism completely.

## Review of the mathematical implementation

`audit_upper` uses integer binomial coefficients and a rational α comparison. For fixed N,n, perfect labelling of errors and a uniform sample without replacement, the CDF decreases monotonically in K, and the bisection search domain `[x,N−n+x]` is correct; K=x is always accepted. The boundary of the strict `P(X≤x)>α` agrees with the definition of coverage. A full inspection returns x; zero sampling returns N.

This independent run: all N,n,K with N≤10, and α∈{0.01,0.05,0.2,0.5,0.9}; the under-coverage probability was computed with exact fractions and never exceeds α. The check was run offline with `python -B`, writing no result files or caches. This is an implementation test; it cannot replace a theoretical proof, nor can it guarantee that real audit labels are error-free.

The logic of `reachable` is correct: for a candidate class c, if a outside votes are all changed to c, c reaches count+a; every other class must be cut to no more than that number, and a class with a smaller index must have one fewer. The sum of the minimum cuts over classes is ≤a, and a≤m−count, so this is exactly achievable. Any attack that moves votes away from c can be changed into an attack more favourable to c, so the search loses nothing. Its budget is the number of votes from affected partitions, which is not necessarily the number of document modifications.

Independently enumerated four-class votes with 1≤m≤4 and 0≤k≤m+1, 362 count combinations/budgets in total; the results agree exactly with the winner sets obtained by enumerating all vote-by-vote replacements. Tie counterexamples: `[2,0,0],k=1` can reach only class 0; `[0,2,0],k=1` can reach 0 and 1. No error was found in the hypergeometric upper bound or the core reachable-label algorithm.

## Statistical and data qualifications that must be kept

- These bootstrap intervals are approximate test uncertainty for a given trained model under a given generation setting; they are not finite-sample certificates, and they do not incorporate training-seed uncertainty.
- Under perfect classification, the empirical bootstrap [1,1], the difference [0,0] and the zero violation rate [0,0] cannot prove that the population risk is zero. The current report already explains this correctly, and it must be kept.
- Resampling whole company clusters is more cautious than treating each quarterly sample as IID; it depends on the company clusters being representative and on an applicable independence assumption. The shared holder names are only deterministic words in this generator and contain no random common shock; real data cannot be treated the same way.
- Training and test use the same companies and the same three templates, with only a quarterly split; this does not support transfer to new companies, new templates or natural language. The report already acknowledges that the task is saturated.
- All pattern vocabularies come from the original training text and the training edits. Test vocabulary was not read and no test-set leakage was found; but `original_ce` also knows the edit vocabulary, so it cannot be described as having seen only the original text at every processing step. A shared vocabulary used to isolate the optimization target is an acceptable design and should be disclosed.
- The training quarter cutoff of 16 and the contamination time cutoff=0 are not the same threshold: the current model's training includes rows with relative time >0. This run is a stance smoke test with k=0 and does not claim P1 temporal compliance, so this is not a current training-leakage error; in future, this split cannot be used directly as a look-ahead-free pipeline.
- The ideal ground truth for INV is the same output distribution under deterministic labels, but on the synthetic ground truth it is not distinguished from LBL by any real change in confidence; the current experiment cannot adequately identify the difference in value between the two permission specifications.
- `independent shards` should be written as "the training dependencies of the partitions are functionally isolated". The DPA bound does not require the vote statistics to be independent; it requires the prediction functions of unchanged partitions to stay unchanged.
- The generator's accounting identities and exact contamination implementation match the current definitions; bit-for-bit reproduction with a fixed seed is limited to a locked Python/environment, and the Gaussian price sampling and floating point do not imply a cross-version, cross-platform guarantee.

## Review conclusion

The current foundation has checkable mathematical components and honest negative results. No integer computation error was found that would overturn the two existing demonstrations; the inward rounding of general score endpoints has been fixed, the dead gradients of the shuffled permissions have been disclosed, and the key static narrative of the report is now protected by explicit guards. **All three items raised in this review have been addressed, and the review passes within the qualified scope.** This is still only enough to support the local smoke test and the soundness of the components; it cannot be used to pass G0/G1 on real data, or to claim that a certifiable financial language model has been obtained.
