# From Colab to Kaggle: carrying over the existing domain model

This migration reads the completed `domain_v1` domain checkpoint, the user-confirmed entity labels, the 8K vocabulary and the upstream exclusion pools, and leaves the original Drive artifacts as they are. SFT on Kaggle is a new experiment: it loads only the domain model weights and creates a new optimizer. The T4 ×2 in the screenshot has two GPUs; this implementation uses one of them and does not treat the memory of the two as a single block.

## 1. Export on a Colab CPU runtime

Open [04b Kaggle export](https://colab.research.google.com/github/130U/130U-FinLLM/blob/main/notebooks/04b_kaggle_export.ipynb), choose "Runtime → Change runtime type → None", run the cells in order and mount the original Drive. The program first verifies the domain weights, the vocabulary, the task labels, the four real pretraining exclusion pools and the upstream weight chain, then packages them as a stream.

Record the ZIP SHA256 and `manifest_sha256` from the output. When the browser asks to download, wait until `130u_kaggle_transfer.zip` has finished downloading. The file may exceed 1GB; the actual output is authoritative. The package contains model weights and original headlines; keep it on your own computer and treat it as private data. The user's Drive has not been read independently so far; the actual cloud verification result is whatever the run output shows.

## 2. Prepare the Kaggle input and notebook

In your own Kaggle account, create a **Private** dataset from the transfer ZIP, and check that the notebook itself is also Private. In the user's existing notebook, import this project's `notebooks/04c_kaggle_sft.ipynb` through File → Import Notebook, then add the private dataset just created through Add Input. Keep GPU T4 ×2 and Internet on in Session options.

In the configuration cell of 04c, paste the ZIP SHA256 and the manifest SHA256 printed by 04b. Kaggle may unzip an uploaded ZIP automatically: the notebook recognizes the unzipped directory and verifies it by the manifest SHA and the per-file SHAs; if the ZIP is kept, it verifies the ZIP SHA. Leave the two recovery SHAs empty on the first run.

## 3. Run and back up

Run in order and record the full 40-character code SHA shown in the first cell. The program verifies the domain → expansion → seed parent-model chain and the actual exclusion pools, runs a single-step check, then trains and compares on the development set. Run results are in `/kaggle/working`. You need to download the final private recovery ZIP and its two SHAs, or make sure the private notebook version saved the outputs; the working directory cannot be treated as a permanent backup.

To resume across sessions, attach the original transfer dataset and the private recovery dataset, fill in the recovery manifest or ZIP SHA, and pin REF in the first cell to the full code SHA of the first run. Strict resume also requires the run identity (path, data, device, AMP and PyTorch/CUDA) to match; if it does not, the run stops rather than pretending to be an exact continuation. On a sudden interruption, local progress that was not saved separately may be lost.

The project output is a trial of literal entity stance in news headlines. Security identity, complete events and temporal isolation have not been verified, so it cannot represent the X scenario or investment returns. Acceptance in the user's actual Kaggle and Drive environment is still to be run.

Local verification: 31 combined tests of transfer, the four-pool check, SFT and interruption recovery passed; the format and Python syntax of 17 notebooks were also checked. The tests cover simulated Kaggle auto-unzipping and a tiny seed → domain training → export → import → one SFT step and recovery, but this is not the same as real success in the user's cloud environment.
