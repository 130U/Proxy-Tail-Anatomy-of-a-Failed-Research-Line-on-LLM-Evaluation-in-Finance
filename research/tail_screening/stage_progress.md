# Pairwise comparison and multi-ranking aggregation: stage log

**All stages are complete. The stage 1 comparison is in the [stage 1 report](stage1_conclusion.md). The only passing method, Sol four-run aggregation, has completed the [new 128-item confirmation](stage2_report.md): seven of eight items passed, and negative 10% recall in one direction was 78.6%, slightly below 80%, so under the frozen rules it does not move to 512 items. The [current full deliverable](FABLE_CURRENT_REPORT.md) keeps the improvement, the failure and the independent review. The first batch of records below is kept as execution history.**

2026-11-16. This page records interim facts during execution; the final judgment rests on the complete stage 1 analysis and the later independent-sample results.

Stage 1 uses 32 new samples from 32 distinct lexical families, with 0 intersection with the previous round's 128 families. The two models share 8 ranking permutations and 2 complete pairwise panels; within each panel left and right are swapped pair by pair. The first whole-batch attempt with 496 pairs did not complete, so the formal implementation was changed to 4 batches of 124 pairs, with the statistical rules and pass conditions unchanged. The formal 32 pairwise calls and 16 ranking calls are currently running.

The first completed swap comparison contains only the 124 pairs of panel1/batch01 and does not yet represent the other batches:

| Model | Swap inconsistencies, including preference/tie differences | Opposite items clearly chosen in the two runs | Inconclusive |
|---|---:|---:|---:|
| Luna | 67/124 | 45/124 | 0 |
| Sol | 26/124 | 5/124 | 0 |

These are repeated judgments of the same set of pairs, not 124 independent financial events; the differences mix position, within-batch context and the generation process. At present this cannot be used to declare which aggregation method passes. All formal inputs/raw outputs are saved in `research/private/agent_tail_methods/stage1_n32/`, and the statistics code is `analyze_agent_methods.py`. The final report will keep the failed executions and all results, not only the most favorable combination.
