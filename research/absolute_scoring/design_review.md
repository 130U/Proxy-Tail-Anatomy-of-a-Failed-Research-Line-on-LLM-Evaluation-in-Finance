# Absolute-scoring experiment: pre-execution design review

2026-11-16. Based on [the new TASK.md](https://github.com/130U/RESEARCH-Proxy-Tail-Anatomy-of-a-Failed-Research-Line-on-LLM-Evaluation-in-Finance/blob/main/TASK.md) and the experimental conventions saved earlier. This page is an internal AI's independent analysis of the design; it is not an experimental result or Fable feedback. No new sample has been drawn yet, no final scoring prompt written, no scoring agent called and no existing result adjusted; the literature veto check is being done first by another research branch.

## Recommended minimal explicit version

Use one fixed model configuration, 1,000 new lexical families with one entity headline each, and 8 rounds of re-randomized batching. Each round has 25 batches of 40 items; the prompt and the 5 external anchors stay verbatim unchanged, and every call uses a fresh context; the output is only IDs and 0–100 integers. Split the rounds by their fixed order into two groups, 1–4 and 5–8; the main analysis uses the same prefixes m=1, 2, 4. The main interpretation uses p=10%, while 5% and 20% are reported in full; do not pick the most favorable result among the three values of p or the two tails.

The existing source statistics allow drawing 1,000 families from the remaining 1,282 families after excluding the earlier 288 families from the original 1,570 test families. These sets should be checked directly again before sampling; do not read old labels or model predictions to select the sample. One item per family and the original test split only reduce some lexical repetition; they do not guarantee independent events and do not prove that LLM pretraining never saw the headlines.

The new headline inputs should be stored in a local experiment directory outside the repository. Content committed to this repository is limited to IDs, scores, batch IDs and order, the anchor prompt, the source description, analysis code, summaries and figures. Just putting files in a directory called private does not satisfy the new task's requirement "do not commit the original headline text", because that directory was explicitly uploaded before. How to handle the existing historical files is a separate scope question; they should not be deleted silently.

## Controls: reuse the original 40-item contexts rather than building a new small pool

First draw 100 control targets uniformly without replacement from the 1,000 IDs. Keep the **complete 40-item batches and original order** that these targets belonged to in round 1; give each batch involved to two additional new agents with the same configuration. Verbatim identical means not only the order of the 100 targets, but also the other headlines in the same batch, the serialization format, the prompt and the anchors. Do not pull out only the targets to form smaller batches.

If the 100 random targets cover all 25 round-1 batches, 50 calls are added, for 250 in total rather than 206. The expected number of batches involved is

`25 × [1 − C(960,100)/C(1000,100)]`, so it is usually close to 25. This call count is determined by the sampling rule. Do not pick 100 items concentrated in a few batches after the fact to save calls, unless a separate design that samples by batch is explicitly set up. The initial budget can be written as 200 calls for the main experiment and at most 50 for the controls; the 8 rounds are not reduced.

Rescoring complete batches also produces scores for non-control items. These actual outputs should be kept, but the main noise comparison uses only the 100 targets drawn in advance. Non-target scores cannot be swapped into the control group after seeing the results, used to enlarge the main 8 rounds, or used to fit r. In this way the added contexts are companion data needed to keep the experimental conditions, and they do not pose as more independent targets.

The same-batch correlation is based mainly on the two added control scorings C1 and C2. The other two pairs, the original round-1 scoring against C1 and against C2, can be pre-registered sensitivity results; do not select only the highest correlation. The different-batch comparison must be on the **same 100 targets**, using the mean and range of the 28 pairwise correlations from the main 8 rounds. A same-batch correlation over 100 items cannot be compared directly with a different-batch correlation over 1,000 items, because differences in between-target signal variance and content composition change the correlation coefficient.

Splitting the 100 items into batches of 40, 40 and 20, filling the 20-item batch up to 40 with 20 random fillers to make 120 items, and scoring twice for 6 calls in total, is a feasible low-cost "different fixed context" experiment. But it does not reuse the main experiment's original contexts and covers only three distinct batches; conditional on the 100 chosen targets, the share of targets within each batch and the context distribution also change. The difference between these 6 calls and the main 8 rounds cannot be called directly the pure contribution of batch composition. If the budget forces this option, the different estimand must be stated in advance; the version that keeps the original 40-item contexts is preferred.

## How far a "noise decomposition" can be claimed

Comparing the same-batch C1/C2 r with the 28 different-batch pairs answers "does keeping the input conditions fixed go together with higher retest correlation". The different-batch condition changes batch composition and position at the same time, so the two factors cannot be separated further. Changes in model service time, the underlying version or the generation process may also affect the difference. Record call times and configuration, and do not treat fresh sessions as proof of independent errors.

If one wants a single number for "how much of the noise is batch", `(r_same − r_different)/(1 − r_different)` has a variance-share interpretation only under the same scale, the same variance decomposition, independent additive errors and a corresponding shared-context effect model. Here the scores are rounded to 0–100 and then normal-rank transformed, which does not automatically satisfy these conditions. We recommend mainly reporting r_same, r_different, their difference and a paired interval. If the ratio above is shown, it should be stated clearly as a descriptive index that depends on extra assumptions; do not write "X% of the noise comes from batches" directly. Do not clip negative values to 0 or values above 1 to 1 to hide model misfit.

The same-batch control calls should be interleaved with the main tasks or scheduled in advance at different positions, so that the same-batch calls do not all fall into one separate time window. This is still not enough to prove that the model's internal version is constant, and it does not give a purely causal noise decomposition.

## Exact definitions of reliability and the untuned formula

For each round, take the raw integer scores on the same 1,000 items, compute average ranks (midranks for ties), then apply `Phi^{-1}((rank−0.5)/N)`; compute the Pearson correlation for each unordered pair of the 8 rounds, giving 28 values of r. The main r is the arithmetic mean of the 28 values, with the range also given. After seeing the averaged results, it cannot be switched to a Fisher-z mean, the best pair, or a tail-only correlation.

If a round has all scores tied and the correlation is undefined, mark it directly as insufficient measurement; do not fill in 0 or 1. If an r falls outside the range where the classical positive reliability model applies, do not force-clip it and plug it into Spearman–Brown; keep the observed value and report that the baseline does not apply.

The m-score averages should be computed on the **original 0–100 scores**:

- m=1: round 1 against round 5.
- m=2: mean of rounds 1 and 2 against mean of rounds 5 and 6.
- m=4: mean of rounds 1–4 against mean of rounds 5–8.

In the implementation it is enough to keep integer sums with a common denominator m, so that floating-point decimals do not break means that are truly equal. Do not switch to rank-transforming first and then averaging while still claiming to implement the original task's item-wise mean of absolute scores.

The main r is taken only from the 28 pairs of single scores. Plug it as a fixed value into `r_m = m*r/[1+(m−1)*r]` and then do the Gaussian integration; do not back out or calibrate r from the m=2, 4 overlap or pass-through results. This comparison is an **in-sample plug-in test without extra tuning**: r and the predicted m=2, 4 statistics come from the same 8 rounds of raw data, so it is not an independent-sample prediction. The comparison is still falsifiable, but its independence must not be overstated.

The classical variance model of Spearman–Brown and "average the raw scores, then normal-rank transform" are not identical. Using it as an explicit simple baseline is fine. A mismatch with the formula may come from correlated errors, a nonlinear scale, heteroscedasticity, rounding or non-Gaussian dependence, and does not automatically identify a new tail mechanism. The sources for this theoretical limit should be supplied by the dedicated mathematics/literature branch.

## Tail lists, directions and the ties gate

The nominal count is k=floor(Np); with N=1,000, p=20%, 10% and 5% correspond exactly to 200, 100 and 50 items. For each direction, m and p, first locate the score of the k-th item, then include the whole tie group at the boundary. The upper and lower tails are computed separately; ties in score must not be broken by ID or input order.

The two lists A and B can have different actual sizes. The main "overlap fraction" should report both `|A∩B|/|A|` and the reverse direction `|A∩B|/|B|`, and list the nominal size, the actual sizes and the intersection. Do not quietly switch to Jaccard, divide by the nominal k, or pick only the direction with the smaller denominator. The Gaussian equal-nominal-budget curve is continuous and symmetric, so a single prediction line can be shown next to the observed points from both directions.

Reaching 90% reference recall needs at least `ceil(0.9*|A|)` items. Candidates may use only complete score-group boundaries; choose the smallest complete boundary that reaches that count. The main widening factor is `B_selected/(N*p)`. B_selected/|A| can be listed separately to explain the actual list fraction, but the main denominator must not be swapped. Keep both reference directions.

**The new task's ties veto gate is stricter than the old protocol:** it says "the number of ties at the top-list boundary exceeds 20% of the nominal count", so the **size of the whole boundary tie group** should be compared with 0.2k, not only the number of items added by including the ties. Even if the extra expansion beyond the threshold is a single item, a boundary group of 30 items already exceeds the threshold at k=100. Both can be reported, but the old expansion gate cannot replace the new gate.

We recommend registering this gate for every single-round score and for both panels at m=1, 2, 4. For the p=10% conclusion, if any boundary used to support that conclusion exceeds the threshold, mark the tail judgment for that end/level as tie-limited; keep the original statistics, but do not use them as evidence that the formula succeeded or failed. A failure at 5% or 20% alone should be listed separately, not hidden, and the other parts that can be interpreted need not be treated as if they were never measured. How the final question "does a line continue" is handled must be fixed before scoring: the most conservative option, closest to the task, is that if any pre-specified main boundary fails, the overall conclusion is inconclusive, and local results are only descriptive.

Ties make the actual p_A and p_B deviate from the nominal p, which by itself can produce a gap from the continuous Gaussian baseline. The main figure can fix the nominal p as the task says, but must show the actual sizes. If a diagnostic integrating at the actual p_A and p_B is added, it can only be a pre-declared sensitivity analysis for discrete boundaries; it does not replace the main figure and does not re-tune the reliability.

## Headline bootstrap and prediction uncertainty

The main tail analysis resamples the 1,000 headline IDs in pairs, drawing 1,000 each time and carrying all 8 rounds of scores for each headline; all m, directions and p within the same bootstrap use the same set of sampled indices. Headlines drawn more than once are observations with repeat weights and must not be deduplicated by ID; in each draw, the threshold, the full ties, the intersection and the 90% minimum pass-through amount are recomputed within the resampled multiset.

The control comparison separately draws 100 times from the 100 pre-specified control targets, each time carrying both their main 8 rounds and C1/C2; the difference between same-batch and different-batch correlations is recomputed from this. Do not resample each round or the two controls separately, which would destroy the pairing. With only 100 targets this interval is usually coarser than the main tail intervals, and this uncertainty should be shown directly.

We recommend fixing 5,000 resamples and independent random seeds before scoring, and outputting percentile 95% intervals. The measurement intervals on the figure are given as the task requires. To judge "whether the gap between prediction and measurement is clear", recompute r from the single scores within each identical headline resample, plug it into the formula, and form a paired "observed − predicted" interval; this is not tuning with m=2, 4. Drawing only a fixed prediction line and ignoring the uncertainty in the r estimate treats the prediction as a known constant.

These are headline-level conditional resampling intervals; agent outputs and batches were not regenerated. Every 40 items share one context, and lexical families are not necessarily independent events, so we cannot claim to have covered all batch and call uncertainty, nor upgrade it to a rigorous population guarantee by the number of bootstrap draws. The intervals for the three values of p, both tails and the several m are item-wise 95%, not simultaneous 95%; any significant difference seen should not automatically be called a systematic deviation.

## How the three outcomes need to be worded

The task gives "below 75%" and "above 90%" as examples, and gives no statistical operational definition for "clearly", "fits everywhere" or "the largest share of the noise". Working rules, with p=10% as the main case, should be fixed before scoring; one cannot wait until after seeing the results to decide how many points "clearly" needs. We recommend reporting at least both the point estimate and the position of the interval relative to 75%/90%, and distinguishing support for an outcome from mere lack of precision.

"The formula fits everywhere" cannot be inferred from all differences failing to reject zero. To claim practical equivalence, acceptable ranges of overlap error and pass-through error must be declared in advance; otherwise one can only write "no clear deviation detected in this sample", which does not prove the formula is accurate enough. Only low overlap together with a pre-defined deviation that is consistent across m, or a difference between the tails, supports continuing; a chance deviation at a single 5% point should not decide the whole line.

A failed ties gate, an undefined correlation, or an interval spanning decision regions should all allow an honest verdict of inconclusive. Do not change the 0–100 scale, anchors, prompt or number of repeats on the same 1,000 items just to get a binary success/failure. If the literature search finds the same top-list measurement together with a formula comparison, then, as the task says, stop before any scoring and tell Theodore.

The most important execution choices in this design review are: fix the complete 40-item control contexts; compare same-batch and different-batch on the same 100 items; interpret the new ties gate by the whole boundary group; keep the directional asymmetry and headline pairing; and treat the reliability formula as a baseline without extra tuning, not as an unproven identity.
