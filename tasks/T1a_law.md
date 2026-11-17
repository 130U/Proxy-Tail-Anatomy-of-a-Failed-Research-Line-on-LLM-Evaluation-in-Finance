# T1a: Write the phenomenon as a law and test it with a zero-parameter prediction

Prerequisite: T1 is complete (branch `task/t1`, directory `research/t1_rounding/`). This task is done on branch `task/t1a`, in directory `research/t1a_law/`; it only reads T1's `results/per_question.jsonl` and does not change T1's files.

## The claim to test

A growth rate g = (b − a)/a is computed from two rounded numbers. Convert the difference between the two numbers into a count of "last displayed units", written Δ. Then:

> The relative uncertainty of the growth rate is about 1/Δ. For the answer to be determined within relative tolerance τ, Δ must be at least about 1/τ.

A tolerance of 1% corresponds to Δ ≥ 100. In other words, the two numbers must differ by at least 100 last-digit units before the growth rate can be called exact to 1%.

The advisor has already made a rough check on T1's per-question results: over all 1,425 two-input growth-rate questions, the single sentence "if Δ < 100 then undetermined" agrees with T1's exact interval classification 97.8% of the time; with Δ between 60 and 100, 100% are undetermined, and between 150 and 300 only 4%. Reproduce this number first.

## What to do

1. **Proof.** Give exact upper and lower bounds on the relative uncertainty of the growth rate, stating the first-order term, the remainder and the conditions of validity (the denominator does not cross zero, the two numbers have the same sign, etc.). Give a corresponding one-sentence rule for differences, ratios b/a and sums.
2. **Digit budget.** Rewrite the rule in the language of significant digits: a growth rate of size g computed from numbers with k significant digits has only about k − log10(1/g) meaningful digits. To reach tolerance τ, the inputs need about log10(1/(g·τ)) significant digits. Give an exact statement.
3. **Zero-parameter test.** For all analysable questions in T1, use only the rule above to predict "determined / undetermined", and compare with T1's exact classification. Give confusion tables by operation type. List every question the rule gets wrong, with the reason.
4. **A priori prediction.** Without looking at the specific values of each question, use only "leading digits follow the Benford distribution" plus the actual distributions of growth rates and displayed digits to predict the undetermined share, and compare with the observed share.
5. **Probabilistic version.** T1's witness is taken at a corner of the rounding box, which is the worst case. Assuming the rounding errors of the inputs are independent and uniform within half a last-digit unit, compute for each question the probability that "the true value lies outside the tolerance", then sum to get the expected share. For the growth-rate case, give a closed form if possible.
6. **Tolerance curve.** Replace 1% with 0.1%, 0.5%, 2% and 5%, and plot how the undetermined share changes with the tolerance.

## Deliverables

- One figure: x-axis Δ (log scale), y-axis the undetermined share, with the step at 1/τ marked; alongside it a panel of the digit-budget prediction versus observation.
- A one-page summary.
- Proofs, code, per-question results.

## Decision

- **Holds:** the agreement rate between the rule and the exact classification is at least 95% in every operation type, and the a priori prediction differs from the observed share by no more than 5 percentage points.
- **Needs correction:** some operation type has a clearly lower agreement rate. List it as it is and give the corrected rule.
- Report the expected share from the probabilistic version as it is, whatever it is. If it is far below 17%, the worst-case statement is exaggerated, and the summary must say so.

## Check first

In numerical analysis, "subtracting nearby numbers loses significant digits" is classical material; do not treat it as a new result. What to check is whether anyone has written it as a quantitative rule for financial statement analysis or for financial QA benchmarks, and tested it on a benchmark.
