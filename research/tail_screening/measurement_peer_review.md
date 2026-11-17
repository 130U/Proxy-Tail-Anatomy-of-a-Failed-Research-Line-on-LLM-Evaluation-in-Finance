# Pairwise comparison and multi-ranking aggregation: independent internal review

2026-11-16. The reviewer is an AI agent in another independent execution context; it is not Fable, and not an outside human peer reviewer. No model scoring, training, network access or modification of the raw results was done. The scope of the work is the consistency of the measurement code, the raw inputs/outputs, the numbers and the interpretation; it does not include redoing the full literature search or vouching for the originality of the theory.

**Conclusion: no calculation error was found that would change this round's pass/stop decision. In stage 1, only Sol four-run ranking aggregation passed, as a single model; in the new 128-item confirmation this candidate passed seven items and failed one, so under the frozen rules it should not move to 512 items. This failure is close to the working threshold and should not be exaggerated into severe instability or overall unusability.**

## How the independent recomputation was done

The review code [review_measurements.py](review_measurements.py) does not import the original analysis programs. It recomputes, from the raw ordered groups, the negative of the sum of twice the midranks, whose ordering matches the original integer Borda numerators; from the raw pair left/right endpoints and the L/R/T judgments it reconstructs the item preferences, records a win/loss only when the two preferences agree, and records a half tie in other non-U cases.

The minimum 90% pass-through amount is computed separately by enumeration: it goes through every complete score-group boundary of the candidate ranking, forms the list explicitly, and takes the smallest set whose recall reaches ceil(0.9×actual target count). This is implemented independently of the original program's shortcut of using a quantile within the target subset. The two approaches agree on the 32 rows of stage 1 (two methods, two models, two directions, two tail fractions), and on the 36 rows of stage 2 (m=1/2/4, two directions, three fractions, both tails). Counts, intersections, recall, widening factors and tie expansion were checked; the stage 2 correlation coefficients also agree.

In addition, from the private mapping, the 128 development families, the 32 stage 1 families and the 128 stage 2 families were actually computed, and all pairwise intersections of the three sets are zero; the ID–text mappings of the eight stage 2 inputs are identical, and the prompt is byte-for-byte identical to stage 1. This proves sampling isolation in the saved materials; it cannot prove that LLM pretraining never saw these headlines, nor equate lexical families with fully independent events.

The review script was actually run in the existing environment: exit code 0, all asserts passed, about 2.7 seconds. It only reads saved data and outputs a check summary; it did not overwrite reports or machine results. Recomputation command:

```powershell
& '..\130U-FinLLM\.venv\Scripts\python.exe' 'research/tail_screening/review_measurements.py'
```

## Check of the stage 1 results

| Method/model | Independently computed rank correlation | Worst equal-budget recall | Maximum q90/p | Single-model working gate |
|---|---:|---:|---:|---|
| Pairwise/Luna | 0.825016 | 0.625 | 2.25 | Failed |
| Pairwise/Sol | 0.919584 | 0.875 | 1.875 | Failed |
| Four-run aggregation/Luna | 0.865328 | 0.875 | 2.75 | Failed |
| Four-run aggregation/Sol | 0.987358 | 1.000 | 1.00 | Passed |

This matches the [stage 1 conclusion](stage1_conclusion.md) and the [formal JSON](methods_stage1_all.json). For pairwise Luna, the swap disagreement counts of the two panels are 248 and 230, with 131 and 113 strictly opposite; for Sol they are 56 and 63, and 14 and 8; all recompute identically. Luna's strict three-edge cycles 8/508 and 7/543, and Sol's 0/1964 and 0/2125, also match the saved results.

The formal count should be 48 formal scoring calls, of which 32 are pair batches and 16 are lists; 3,968 is the number of pair judgments, not the number of independent calls or independent text samples. The other 2 whole-batch attempts with 496 pairs produced no output and must not be counted as completed scoring data. The protocol keeps the chronological explanation of the originally planned 24 calls versus the actual 48, and the latest conclusion correctly reports the actual count.

## Key boundary in the new 128-item confirmation

The Spearman between the two four-run aggregation panels is 0.992865, but this cannot replace checking the tail lists. For the lower 10% tail with panel 1 as reference, the nominal count is floor(128×0.1)=12, and ties at the reference boundary make the actual A 14 items; the candidate's equal-budget list has 12 items, and the intersection is 11. So the equal-budget recall is 11/14=78.5714%, below the pre-set 80%.

For this reference list to reach 90% needs at least 13 items; when the candidate passes 16 items it actually recovers all 14, and q90/p=16/12.8=1.25. Here the widening-factor condition and the tie-expansion condition (16.7%) are met; **it fails only on equal-budget recall**. The reverse comparison gives 11/12=91.7%, and the reverse direction cannot be picked to cover the failing item.

Of the eight direction × tail × fraction combinations, the other seven pass; over all main combinations the maximum q90/p is only 1.25 and the maximum boundary expansion 16.7%. The [stage 2 report](stage2_report.md) and the [formal JSON](validation_stage2.json) keep these facts accurately.

## Scientific limitations and disputes that are not errors

**The working gate is not a statistical test.** 78.6% being slightly below 80% is a fact about a pre-set decision boundary, not proof that population recall is significantly below 80%. It cannot be changed to a pass after the fact because it is close, nor exaggerated into strong counterevidence. Continuing the research with a new method, more repeats or a different threshold needs a new protocol and new data, and cannot relabel this confirmation.

**"Equal budget" means the same nominal p.** After each side keeps its complete boundary ties, the actual counts can differ. The original code and report both list the actual counts separately, and the convention is consistent; but it is not a set comparison at strictly identical actual counts. The denominator of q90/p is Np, not floor(Np), so with 128 items factors below 1 can appear; this is compatible with a 90% rather than 100% target and with discrete rounding. If Fable prefers uncertain boundary ranges for strict top-k, that is a different statistical object, not an error in the current program.

**A larger sample and a stricter tail changed at the same time.** The main p was 25% in stage 1 and 10%/20% in stage 2, and the candidate pool was also changed. The failed confirmation cannot be attributed causally to "the larger the sample, the less stable". The accurate statement is "this candidate failed the confirmation gate on 128 completely new items at stricter tail fractions".

**Choosing the branch after seeing the results has been disclosed honestly.** After the original two-model gate failed, the Sol single-model validation was chosen because the user asked to continue with the passing branch. This is not a success of the original two-model plan, nor a fully pre-specified candidate selection; confirmation on independent new data can evaluate the selected candidate, but it cannot erase the selection process.

**Low resolution being mitigated does not mean a fixed continuous score exists.** The aggregated scores depend on the candidate pool, the prompt and multiple generations; a higher number of levels and a higher overall correlation do not prove that a stable document score exists independently of the list. Repeated calls do not add independent financial observations, and errors are not guaranteed to be independent; reordering fluctuation also does not separately identify a pure position effect. The current results neither estimate the asymptotic α nor measure investment returns.

## Recommendation on the deliverable's conclusion

The deliverable should state both "aggregation does improve things" and "the current confirmation gate failed"; the two do not contradict each other. Keep the failure results of pairwise comparison, the direct list and Luna aggregation; stop scaling up to 512 items under the original frozen rules. The original tail hypothesis for financial LLMs has been neither validated nor rejected by this measurement.

The updated [current full report](FABLE_CURRENT_REPORT.md) was reread: its account of 64 completed scorings, 2 more attempts with no output, 288 distinct lexical families, and seven items passed / one narrowly failed on the new 128 items all match this check; the full text keeps the limitations that the new sample and p changed at the same time, that the single model was selected after the fact, and the uncertainty from ties and repeats.

This review supports the statistical implementation and the current finite-sample decision. It does not prove that the method is generally valid or invalid, does not prove that the two models have a stable two-tail difference, and does not replace Fable's judgment on the economic meaning of the question and its theoretical contribution.
