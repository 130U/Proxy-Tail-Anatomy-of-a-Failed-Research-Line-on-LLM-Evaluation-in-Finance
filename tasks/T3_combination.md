# T3: How a model combines one good and one bad piece of news

## Question

When one headline contains both a piece of good news and a piece of bad news, how is the model's score composed from the two separate scores? Is it additive, an average, or does the bad news dominate?

## Method

1. Write 30 short single-fact headlines: 10 positive, 10 negative, 10 neutral, spread across strengths. All use the same fictitious company name.
2. First score these 30 on their own, repeat 8 times and average, to get each one's baseline score s.
3. Combine them in pairs into one headline, joined by `; ` or `as`. Make three kinds of combinations:
   - positive + negative (100 pairs, all combinations)
   - positive + positive, negative + negative (45 pairs each)
   - any one + neutral (200 pairs)
4. Do both orders for each pair. Repeat each combined headline 4 or more times.

## Analysis

Convert scores to the deviation from neutral, d = s − 50. For the deviation of a combined headline d(A,B), compare three models:

- **Additive:** d(A,B) = d(A) + d(B), then truncated to the range of the scale.
- **Averaging:** d(A,B) = w·d(A) + (1 − w)·d(B).
- **Asymmetric:** the weight of the negative item is multiplied by a coefficient λ. λ > 1 means bad news dominates.

Report:

1. Which model fits best, and how large the residuals are.
2. The estimate of λ and its interval.
3. Whether adding a neutral item pulls the score towards 50. The additive model predicts it does not; the averaging model predicts it does. This is the cleanest test to tell the two apart.
4. Order effects: whether the item stated first and the item stated second have different weights.
5. Whether two items in the same direction, once combined, are more extreme than a single item, or fall between the two.

## Decision

- **Continue:** the interval for λ clearly excludes 1, or a clear order effect appears, or the averaging model clearly wins (which would mean "adding an irrelevant piece of news dilutes bad news").
- **Abandon:** the additive model fits well, λ ≈ 1, no order effect.

## Why it is worth a try

If the model averages, then adding an irrelevant neutral sentence after a piece of bad news will make the score recover. For people who use models to read announcements, this is an exploitable loophole, and it can be described with a single coefficient.

## Check first

Search whether information integration theory (Anderson's additive and averaging models) has been used to test LLMs, and for dilution effects, negativity bias and order effects in LLM sentiment scoring.
