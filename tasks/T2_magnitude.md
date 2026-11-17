# T2: The model's response curve to the size of a number

## Question

As the number in a headline goes from small to large, how does the sentiment score the model gives change? Is it monotone? Does it grow logarithmically? Are there jumps at round-number thresholds? If the same quantity is written in a different unit, does the score change?

## Method

Use self-made headlines, not real data. Example templates:

- `{company} quarterly profit rises {x}%`
- `{company} cuts {n} jobs`
- `{company} to pay ${v} fine`

Company names are fictitious; fix 5 of them and rotate.

**Experiment A, response curve.** For each template take 25 values, evenly spaced on a log scale (for example 0.1% to 500%). Do both directions, rises and falls.

**Experiment B, round-number thresholds.** Sample more densely near 10, 50 and 100, for example 9.5, 9.9, 10, 10.1, 10.5.

**Experiment C, units.** Write the same amount as `$1,500 million`, `$1.5 billion` and `$1,500,000,000`. Write the same proportion as `0.5%` and `50 basis points`.

Repeat each condition 4 or more times, and score them mixed in with unrelated filler headlines, so the model cannot see the pattern.

## Analysis

1. Plot the score against log(x), one curve for rises and one for falls. Test monotonicity: the share of adjacent sample points that are out of order.
2. Fit and compare three forms: linear in x, linear in log x, and a saturating curve. Report which fits best and the residuals.
3. Jumps at thresholds: the score difference between 10.1 and 9.9, compared with the same spacing away from thresholds.
4. Unit invariance: the score differences among the three ways of writing the same quantity, compared with the size of the test-retest noise.
5. Whether rises and falls are symmetric: for bad news of the same magnitude, does the score move further from neutral than for good news.

## Decision

- **Continue:** any one of the following appears with a size more than twice the test-retest noise: systematic non-monotonicity; a clear threshold jump; differences caused by how the unit is written; a clear asymmetry between rises and falls.
- **Abandon:** the curve is smooth and monotone, approximately linear in log x, unit-invariant and symmetric on both sides. In that case write one page saying "the model's response to numbers is well behaved", and stop.

## Check first

Search for numeric sensitivity of LLMs, the left-digit effect, unit or dimensional invariance, and numeric perturbation tests on financial text, to see whether the same response-curve measurement already exists.
