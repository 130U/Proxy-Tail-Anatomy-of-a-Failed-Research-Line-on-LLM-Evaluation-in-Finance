# Project progress and how it is counted

2026-10-30. The numbers below measure project work and the training processing volume of the original plan. They are not the model's financial prediction ability or accuracy.

## Original pretraining budget

| Stage | Effective tokens processed | Original plan | Computed along the model path |
|---|---:|---:|---:|
| General pretraining: seed + expansion | 4,914,941 + 19,988,195 = 24,903,136 | 100,000,000 | 24.9% |
| Financial domain stage: 80/20 mix | 1,211,960 | 25,000,000 | 4.85% |
| Total | 26,115,096 | 125,000,000 | 20.9% |

Here seed and expansion are combined as the whole general training path; comparing only against the 100M configuration cap of expansion itself gives 19.99%. The 1,211,960 of the domain stage are effective processed positions of finance / general mixed data, not independent text that all comes from finance. The numbers record cumulative processing and cannot be taken as a deduplicated corpus size. The evidence for the domain stage and the Drive backup is the Colab output provided by the user; see the [domain record](../reports/colab_t4_domain_20261030.json).

## Rough estimate for the whole project

A rough estimate that gives the following eight stages equal weight by convention comes to about **35%**: architecture and vocabulary, and training tools, are counted as complete; general pretraining is counted as 25%, financial domain training as 5%, review and asset data preparation as 50%; real SFT, DPO, calibration and independent evaluation each as 0%. The calculation is `(1 + 1 + 0.25 + 0.05 + 0.5) / 8 ≈ 35%`. This is only a coarse way to communicate project planning. The stages differ in workload; this is not a scientific measurement and does not mean the project is only 65% away from being usable or from reaching its capability targets. Budgets will be adjusted according to experimental results and resource constraints.

| Stage | Current status |
|---|---|
| Model, vocabulary, training tools | The 24.26M randomly initialized model, the 8K vocabulary, and training and checkpoint tools are implemented; the engineering chain has been tested |
| General pretraining | About 24.9M effective tokens on the general path; still short of the original 100M processing budget |
| Financial continued pretraining | A bounded trial of 1.212M effective tokens is complete; the original 25M budget is not |
| Annotation and asset data | Of the 2000 headlines, 1993 reviewed according to the user's confirmation, of which 114 excluded and 1879 three-class candidates; 7 pending; asset identity and event grouping not yet accepted |
| SFT and DPO | The engineering path exists; real SFT has not been run; DPO preference pairs have not been reviewed or trained |
| Calibration and task evaluation | Real task calibration, independent testing, baseline comparison and validation on short X texts are not done |

The current financial validation and retention-set losses are next-token prediction losses and cannot be converted into bullish/bearish accuracy. Next, use the reviewed results to check asset type, security identity, event grouping and data permissions, fix the partitions, then verify the domain parent checkpoint and start real SFT.
