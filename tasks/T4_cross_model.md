# T4: Top-list overlap between a cheap model and an expensive model (finishing the original question)

## Question

The original question was: if a cheap model is used as a filter, how much of the expensive model's top list will it miss? Earlier rounds could not measure this because the measurement was unstable. The per-item scoring method is now stable, and the expensive model (Sol) already has 8 rounds of scores on 1,000 items, so adding the cheap model is enough to answer it.

## Method

1. Using exactly the same 1,000 items in `research/absolute_scoring/`, the same prompt and the same batching, have the cheaper model tier (Luna, or the cheapest configuration currently available) score 4 rounds. About 100 calls.
2. For the expensive model, use the existing 8 rounds of scores and take their average as the reference.

## Analysis

1. Cross-model correlation (on normal scores). Then apply an attenuation correction using each side's own test-retest reliability, to get the correlation "with scoring noise removed".
2. For p = 20%, 10%, 5%, at both ends: the overlap between the cheap model's top p and the expensive model's top p; the widening factor needed to recover 90% of the expensive model's top list.
3. Compare with the Gaussian benchmark: use the cross-model correlation to predict the overlap rate and widening factor, with no tuning.
4. Look at the cross-model overlap rate side by side with the expensive model's own overlap rate (known, about 90%–92%). The difference between the two is "what the cheap model really misses".
5. List the IDs of the expensive model's top-list headlines that the cheap model missed, look at 20 of them by hand, and write three sentences: do they share any features (multiple entities, negation, numbers, implicit comparison).

## Decision

- **Continue:** the cross-model overlap is clearly below the Gaussian prediction (by more than 10 percentage points), or the two ends differ clearly, or the missed headlines share clear features.
- **Abandon:** agrees with the Gaussian prediction, the two ends are symmetric, and no pattern is visible in the missed headlines. In that case the original question is formally closed.

## Note

The literature check has already been done (see `research/tail_screening/literature.md`), so this task does not need to search again. Its purpose is to give the original question a definite answer, not to find new theory.
