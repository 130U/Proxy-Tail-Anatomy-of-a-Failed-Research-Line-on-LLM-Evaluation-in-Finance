# Parallel tasks

Four small topics that do not depend on each other, so each can be run in its own conversation at the same time. Each topic should reach "continue" or "abandon" within one day.

| ID | Topic | Needs agent scoring? | Output directory |
|---|---|---|---|
| [T1](../tasks/T1_rounding.md) | For how many questions does the rounding precision of filings fail to determine the answer | No | `research/t1_rounding/` |
| [T2](../tasks/T2_magnitude.md) | The model's response curve to the size of a number | Yes | `research/t2_magnitude/` |
| [T3](../tasks/T3_combination.md) | How a model combines one good and one bad piece of news | Yes | `research/t3_combination/` |
| [T4](../tasks/T4_cross_model.md) | Top-list overlap between a cheap model and an expensive model (finishing the original question) | Yes | `research/t4_cross_model/` |

## Second batch (2026-11-16): push only T1

T1 passed the prior-art check and the advisor's independent review, and it is currently the only direction worth investing in. T2 is archived because prior work exists. The substantive conclusion of T3 is "the model combines news additively"; it ends after one post-hoc check. T4 is no longer needed.

The three topics below do not depend on each other and can run at the same time:

| ID | Topic | Needs an agent? | Output directory |
|---|---|---|---|
| [T1a](../tasks/T1a_law.md) | Write the phenomenon as a law and test it with a zero-parameter prediction | No | `research/t1a_law/` |
| [T1b](../tasks/T1b_tighten.md) | How much of the conclusion remains after adding the other information in the document | No | `research/t1b_tighten/` |
| [T1c](../tasks/T1c_models.md) | Does this have any real effect on model evaluation | Yes | `research/t1c_models/` |

## Third batch (2026-11-17): the last round

T1a and T1b passed. The conclusion of T1c is "it does not affect current scoring". The advisor has reviewed all three results against the per-question records. The last round has only one topic; after it the advisor writes the short paper.

| ID | Topic | Needs an agent? | Output directory |
|---|---|---|---|
| [T1d](../tasks/T1d_precision.md) | Does the model know how many digits of its own answer are reliable; a second AI redoes the semantic review | Yes | `research/t1d_precision/` |

## Fourth batch (2026-11-17): extend the sample conclusions to the whole test set

The conclusion of T1d is "the model already knows". During recomputation the advisor also found that the four runs are marked wrong on almost the same set of questions, and the review judged that the great majority of these rejections lie on the benchmark side. The short-paper draft is at [`paper/finqa_short_v0.md`](finqa_short_paper_draft_v0.md).

| ID | Topic | Needs an agent? | Output directory |
|---|---|---|---|
| [T1e](../tasks/T1e_full_test.md) | The remaining 755 test questions, attribution of all rejections, a mechanical cross-check of the two gold fields, a rounding audit on a second dataset | Partly | `research/t1e_full_test/` |
| [T1f](../tasks/T1f_novelty.md) | Novelty check of the five candidate insights on the homepage | No (needs internet access) | `research/t1f_novelty/` |

## Fifth batch (2026-11-17): after the novelty check

Conclusion of the T1f novelty check: of the five candidates, only "the rounding law and the exact count" has no prior work; the other four have been done before. The first three parts of T1e are therefore on hold.

| ID | Topic | Needs an agent? | Output directory |
|---|---|---|---|
| [T1g](../tasks/T1g_consequence.md) | Where rounding precision really has consequences; predict first, then test, on TAT-QA | Not for the first four parts | `research/t1g_consequence/` |

## Common rules

- Write files only in your own output directory, each on its own branch `task/t1` … `task/t4`, so tasks do not interfere.
- First spend half a day checking whether anyone has done this before. If you find the same question with the same measurement, write one paragraph explaining it that same day, then stop.
- Do not train models and do not call paid APIs. Scoring follows the method already validated in `research/absolute_scoring/`: integers 0–100, fixed anchors, 40 items per batch, each item scored independently, a new session each time.
- The single test-retest correlation of that method is about 0.975. Repeat each condition at least 4 times and then take the average.
- Deliver only three things: one figure, a one-page summary, and the raw scores with the analysis code. No checklists, hash tables, packaging scripts, or reviews of reviews.
- The decision thresholds are written in each task. When a result lands right on the line, report the number as it is; do not call it "inconclusive" because it missed by a little.
- Original headline text and self-made text may be committed; do not commit any new original text from SEntFiN.
