# T1: For how many questions does the rounding precision of filings fail to determine the answer

## Question

Financial QA benchmarks treat the numbers in tables as exact values. But filing figures are rounded (commonly to millions, with one decimal place). Differences, growth rates and ratios amplify the rounding error of the inputs. For how many questions is the gold answer, within the benchmark's own tolerance, not determined by the document?

## Method

1. Take the public FinQA data; each question comes with a gold solution program (gold program). If feasible, also add the TAT-QA development set.
2. For each input number, give a rounding interval according to the number of decimal places it shows in the document: displayed value ± half a unit of the last digit.
3. Execute the gold solution with interval arithmetic to get an interval for the answer.
4. Compare with two common scoring rules: 1% relative error, and equality after rounding to the number of digits shown in the gold answer.
5. Count: the share of questions whose answer interval exceeds the tolerance; grouped by operation type (difference, growth rate, ratio, sum); grouped by the number of significant digits of the inputs.
6. Count one more thing: how many questions have the same quantity appearing two or more times in the document at different precisions, and whether computing from different occurrences makes the answer cross the scoring boundary.

## Decision

- **Continue:** the share of questions exceeding the tolerance is ≥ 5%, or ≥ 15% within some operation type.
- **Abandon:** the overall share is < 2%.
- In between: write the numbers out clearly, and Theodore decides.

## If continuing, what comes next

Give a closed-form condition number: for a growth rate (b − a)/a, the uncertainty of the answer is about rounding unit ×(|a| + |b|)/a². Then predict how much "changing the reporting unit from millions to thousands" would reduce the number of undetermined questions, and verify it on the data.

## Check first

Search for existing work that has used interval arithmetic or condition numbers to analyse the determinacy of answers in financial QA benchmarks. The community is known to debate whether the tolerance should be 1% or digit-based; that does not count as the same thing.
