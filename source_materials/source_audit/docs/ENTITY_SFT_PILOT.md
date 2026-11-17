# 04a: quick entity stance SFT trial

This trial starts from the completed 74-step `domain_v1` checkpoint, reuses the original 8K vocabulary, and trains three-class stance toward the literal target in a headline. It is a research trial meant to help the project get a testable model quickly: the target is not a verified security, and the samples are financial news headlines rather than X posts.

## Run on Colab

1. Open the [04a notebook](https://colab.research.google.com/github/130U/130U-FinLLM/blob/main/notebooks/04a_entity_sft_pilot.ipynb) and select the T4 GPU.
2. A private upload package already exists on this machine: `runs/task_pilot/entity_v1_upload.zip`. Run in order from the top and mount Drive; when the upload prompt appears, choose this ZIP.
3. This notebook verifies the data package against the existing pretraining exclusion lists, and the domain checkpoint and the original vocabulary in Drive, freezes the parent model, then runs a single-step check and two passes of training. It then compares the domain parent model and the best SFT model on the same development set, and finally runs the backup.
4. Keep the final training and development-set output and the `verified: true` backup result. After a disconnect, first confirm that the old training process has stopped, then resume from the first cell; the complete state is checked automatically. Do not run two training copies in parallel.

The ZIP contains 1008 user-confirmed headline stances: train 705, development 101, calibration 101, test 101; the last two are not used for model selection or automatic evaluation in this notebook. Lexical and source-ID isolation is in place; semantic events and time have not been fully verified; development metrics are exploratory results. The third-party rights of the original publishers have not been independently verified; the data stay on the local machine and in the personal Drive and are not uploaded to public GitHub.

The model receives the target in the word form used in the headline text; evaluation and inference need an explicit `--target-mode literal_entity`. It returns three-class probabilities and a direction score, is not yet calibrated, and has not established any ability to predict stock prices. Real security mapping, more samples, DPO, calibration and the final independent test still have to be done later.

Locally, 23 combined checks of data / entity prediction / SFT and resume, and format checks of 15 notebooks, were completed; there is a real tiny CPU domain → SFT → development evaluation → backup test. They do not prove that training on the user's actual Colab T4, Drive or formal data has been run. Data package SHA256: `e87d12013271eb8f93f926b0b2c71cef15b0c777cc58d6e08348773dbd6a7be6`.

## Fix for the 04a exclusion-list mismatch

The user's screenshot shows that verification of the uploaded task package and of the Drive snapshot succeeded, but the preparation stage reported `Task package exclusions differ from the actual pretrained-data lineage`; SFT had not been started at that point. The cause was that the entry point wrongly required the locally prepared exclusion list and the historical cloud pretraining list to have the same file SHA. The two were built independently, so headline coverage cannot be judged only by whether their bytes are identical.

After the fix, the four real exclusion lists in Drive (train and validation for seed and for expansion) are read; the list snapshots and their linkage to the actual pretraining checkpoint, shards and domain mixed data are verified; then the headlines of all five task partitions are confirmed one by one to be in the corresponding exclusion sets. Differing versions proceed to training only after all of the above verifications pass; missing lists or headlines, damaged lists and source mismatches still raise errors. The real cloud situation must be verified by the user running Colab; local tests do not replace cloud results.

After the fix is merged, restart the Colab runtime and run in order from the first cell so that the kernel loads the latest code. An existing `tasks/entity_v1` snapshot is reused once it passes verification, so there is no need to upload again; finally, keep the actual output and the verified backup.
