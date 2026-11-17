# Task: how stable is a model's own top list

For the agent executing this task. Do the scoring with the agent itself only; do not call paid APIs, and do not train models.

## Question

When the same model scores the same batch of financial headlines repeatedly, how much does its own top 10% change? After averaging several scorings, does the gain in stability follow a simple formula?

This decides a choice that costs money: in screening, should tokens be spent on asking the model several more times, or on casting a wider net.

## Why the previous attempt does not count

Last time the agent was asked to rank 128 headlines in one long list. There were two problems: the top 10% had only 12 items; and a headline's rank depended on which other headlines were in the same list. This time switch to **scoring each item on an absolute scale**, and measure separately the effect of "who else is in the same batch".

## Data

- 1,000 public English financial news headlines, each with one designated entity. Choose the source yourself; its licence must allow research use; record the source and version.
- Take only one item from each lexical near-duplicate cluster.
- Do not look at any existing labels or existing model predictions when selecting.
- Do not commit the original headline text to this repository; commit only IDs, scores and summary results.

## Scoring

**Scale.** Integers from 0 to 100: how the headline portrays the designated entity, from most negative (0) to most positive (100), with 50 as neutral or no direction. The prompt gives 5 fixed anchor examples (one each at about 5, 25, 50, 75 and 95); the anchor examples do not come from these 1,000 items. Once finalized, the prompt stays verbatim unchanged.

**Batching.** Each call gets 40 headlines and is asked to score each one independently, stating explicitly "do not compare them with each other, do not rank them".

**Repetition.** Score each headline 8 times. For each repetition, re-randomize the batches and the order within batches, and use a new session. 8,000 scores in total, about 200 calls.

**Control.** Take another 100 items (randomly drawn from these 1,000) and score them 2 more times with **exactly the same batch composition and order**. This separates two kinds of noise: the model's own generation variability, and the variability caused by batch composition.

If the call budget is not enough, you may shrink to 500 items × 8 times, but do not reduce the number of repetitions.

## Analysis

Split the 8 repetitions in order into two groups of 4. Let m be the number of scorings averaged within each group, m = 1, 2, 4.

1. **Single-scoring reliability r.** The correlation coefficient between two single scorings, computed on normal scores (after a rank transform). Report the mean and range over all pairwise combinations.
2. **Top-list self-overlap.** For p = 20%, 10%, 5%, at the top and bottom ends separately: what fraction of one group's top p by average score overlaps with the other group's top p. Compute once each for m = 1, 2, 4.
3. **Widening factor.** To recover 90% of one group's top list, how much the other group has to pass through, divided by p.
4. **Comparison with the formula.** Use the r from step 1 to predict the results for m = 2 and m = 4; tuning on the m = 2, 4 data is not allowed:
   - Reliability after averaging m times: r_m = m·r / (1 + (m − 1)·r).
   - Overlap fraction and widening factor: the corresponding values under a bivariate normal distribution with correlation r_m, obtained by numerical integration.
5. **Noise decomposition.** Using the control group, compare the correlation between two scorings with the same batches against the correlation between two scorings with different batches.
6. **Ties.** Report how many distinct score values each scoring uses, and the number of items tied at the top-list boundary. Keep all boundary ties; do not break them by ID or order.
7. **Uncertainty.** Bootstrap over headlines to give 95% intervals for each number in steps 2 and 3.

## Deliverables

- One figure: x-axis m, y-axis the top-list self-overlap fraction; observed points with intervals, overlaid with the predicted curves from step 4. Plot the top and bottom ends and the three values of p separately.
- A one-page summary: what is the overlap rate of a single scoring with its own top 10%; how many averaged scorings are needed to reach 90%; how accurate the formula's predictions are; whether the two ends differ; how large the batch effect is.
- The original prompt text, the batching plan, all raw scores (by ID), the analysis code.

No checklists, hash tables, packaging scripts, or reviews of reviews.

## What counts as an interesting result, and what ends the line

**Worth continuing:** the top-list self-overlap of a single scoring is clearly low (for example below 75% at 10%), and at least one of the following appears: the formula systematically deviates from the observations in the tail; the top and bottom ends clearly differ; the batch effect makes up the bulk of the noise.

**Stop here:** the single-scoring overlap is already high (above 90% at 10%), or the formula agrees everywhere and the two ends are symmetric. Then the conclusion is "just choose the number of repetitions by the reliability formula"; write it up as a one-page rule of thumb, and this line ends.

**Inconclusive:** too many tied scores, with ties at the top-list boundary exceeding 20% of the nominal count. Report it as it is in that case; do not change the scale and rerun on the same data.

## Check one thing before starting

Spend half a day on the literature: whether anyone has already studied test-retest reliability of LLM scoring, ranking instability, and the gain from "sampling several times and averaging" specifically for top lists, with the same comparison against a formula. If you find it, tell Theodore first, and do not continue running.
