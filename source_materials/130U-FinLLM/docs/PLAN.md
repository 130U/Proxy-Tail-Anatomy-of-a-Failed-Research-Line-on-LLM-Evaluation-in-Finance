# 130U-FinLLM | 130U Financial Large Language Model: execution plan

> This document keeps the v1.1 design and evidence limits that were frozen before work started; it is not a list of what is currently complete. The repository has entered implementation; for actual deliverables, tests and unfinished experiments, [STATUS.md](STATUS.md) and [HANDOFF.md](HANDOFF.md) are authoritative. Statements in the text such as "repository/code not yet created" describe the state at the time the plan was written.

Version: v1.1 · 2026-10-09; the single main specification for implementation in the next conversation.
Project name: **130U-FinLLM | 130U Financial Large Language Model** (the original Chinese name has the same meaning). English expansion: 130U Financial Large Language Model. First model identifier: `130U-FinLLM-24M`. Suggested repository name: `130U-FinLLM` (not yet created; availability of the name not checked).
Execution environment: Google Colab, a single Tesla T4; the user's screenshot shows total GPU memory of about 14.56 GiB.
Document status: research and implementation plan. Public source code and materials have been checked, and parameters and budgets computed; the training environment has not been installed, full datasets have not been downloaded, and nothing has been run on the user's GPU. All performance targets and timelines are plans, not completed results.

**Reading order and precedence:** the next conversation reads this file first, then the note "START_HERE: starting the next conversation". This file supersedes the old v1.0 main plan and the differing suggestions in the research attachments. The attachments are for tracing sources; they are not a separate implementation specification. In particular, this file's four partitions, the internal two-way split of the calibration set, the semantic review of labels, label-only supervision in SFT/DPO, and the single next-token shift take precedence.

## Charter

- Goal: deliver a complete training specification that can be implemented at the start of the next conversation, stating the code sources, materials, the division of work between user and agent, how to run on Colab, and stage-by-stage acceptance.
- Knowledge depth: working. Existing models, data and training source code have been checked; real corpus permissions, label quality, connection to the user's runtime and throughput have not been measured.
- Scope / Object / Subject: training a finance-specific language model from scratch / a 24M English target-asset stance model on a single T4 / MiniMind pinned source, tokenizer, data shards, full-parameter training and GitHub–Colab–Drive collaboration.
- Type: descriptive research and implementation handoff; this round only writes the plan and does not create a remote repository, install dependencies or start training.
- Q1: which repositories to reference and what to reuse? Q2: how to carry out the complete workflow and acceptance? Q3: which materials must the user provide? Q4: under the current tool conditions, how to get the code into Colab and get the results back?
- Done when: Q1–Q4 have executable steps and limits; a new conversation can start directly from sections 13–15; unresolved items have their own closing gates.

## Canonical sources

| Priority | Source | Use |
|---|---|---|
| 1 original author's source | [MiniMind pinned commit](https://github.com/jingyaogong/minimind/tree/f659b55761b754d306bd140573493a6543cafd7f) and [license](https://github.com/jingyaogong/minimind/blob/f659b55761b754d306bd140573493a6543cafd7f/LICENSE) | Main architecture, pretraining/SFT/DPO and the limits of modification, Apache-2.0 |
| 1 original authors' repositories | [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch), [nanoGPT](https://github.com/karpathy/nanoGPT), [Tokenizers](https://github.com/huggingface/tokenizers) | Teaching, training loop and tokenizer tools; several model codebases are not spliced together |
| 1–2 Google official | [Colab FAQ](https://research.google.com/colaboratory/faq.html), [GitHub notebook example](https://raw.githubusercontent.com/googlecolab/colabtools/main/notebooks/colab-github-demo.ipynb) | Cloud runtime, persistence, how to open public/private GitHub notebooks |
| 1–2 original sources for methods and data | S2–S12 at the end; original papers, data cards, SEC and platform terms checked earlier | Conditions of data use, basis for DPO, calibration and evaluation; data not yet obtained are not treated as licensed |
| Project input | User-confirmed English, target-asset bullish/bearish/neutral, 10–30M, T4 screenshot and existing research attachments | Requirements and arithmetic budget, not evidence of model performance |

## Findings ledger

| ID | Finding | Evidence and nature | Question |
|---|---|---|---|
| F1 | MiniMind has pretraining, full-parameter SFT and DPO implementations; the current main-line default is about 64M and must be customized to about 24M | Pinned source S1; original author's README. Fact; the modification is not yet done | Q1, Q2 |
| F2 | The nanoGPT README is marked deprecated; LLMs-from-scratch has teaching material on pretraining, classification, instruction tuning and DPO | Original authors' repositories in the table above, checked 2026-10-09. Kept only as auxiliary references | Q1 |
| F3 | An 8192 vocabulary, 6 layers, hidden size 512, 8Q/4KV, FFN 1664 and shared embeddings give 24,255,744 parameters | S1 source and the arithmetic in "Training engineering check"; count again during implementation | Q2 |
| F4 | 125M uint16 token IDs take about 250MB for the main payload; they can be sharded and read on demand | "Corpus preparation and memory/space budget" and official HF/NumPy materials; a calculation, not a measured peak | Q2, Q3 |
| F5 | 8k–12k qualified target-level labels have not been obtained; public generic positive/negative labels cannot be used directly as ground truth for this task | "Data and source check", sections 4–5 and S7–S9; permissions and additional labeling remain conditional | Q2, Q3 |
| F6 | Colab can open GitHub notebooks; private repositories can be authorized by the user in the browser; a shared notebook does not share its VM | Google FAQ and official GitHub example; details in "Colab and GitHub collaboration check" | Q3, Q4 |
| F7 | No direct connection to the user's Colab kernel has been verified; the existence of browser tools does not prove they can operate its GPU | Tools and operation record of this session; the user's notebook was not accessed or run. Capability limit | Q4 |
| F8 | The old attachments contain split, label-mapping and EOS-supervision suggestions that differ from the main specification; MiniMind's built-in shift and an external shift must not be stacked | Read-only consistency review by a subagent, S1 source, corpus budget attachment | Q2 |
| F9 | Model performance, sustained availability, actual RAM/VRAM and training time are still unknown | The user only provided a GPU availability screenshot; no training measurements this time. Known gap | Q2, Q3 |

## Scope filter

This project is limited to stance judgments on a specified asset in short English texts. Removed as unrelated to the goal: multimodality, web crawling, free chat, trade execution, PPO/GRPO and online serving. Kept: pretraining from scratch, full-parameter SFT and DPO learning experiments. Upstream training cost/time figures are not transferred to the user's T4, and financial sentiment classification scores are not called probabilities of a price rise.

## Object filter

The default 64M model, the Chinese tokenizer and the ready-made upstream corpora do not apply directly; instead, use the pinned source, a self-built English 8K tokenizer and material for this task. Generic sentiment data must go through target and semantic review. A notebook share link is not a kernel connection; the collaboration method is decided by the actual connectivity check in section 14. F5, F7 and F9 remain open items; estimates do not replace verification.

## Conclusions

- Use MiniMind as the main implementation reference, LLMs-from-scratch as the teaching reference, and nanoGPT as a reference for a concise training/data-reading setup; complete all training stages with our own tokenizer and random weights. [F1–F3]
- Sharding, micro-batches and checkpoint resume give this configuration reasonable starting conditions on a T4; only short experiments can give the actual resource budget. [F3, F4, F9]
- The user does not need to buy a server, provide an API key, or prepare thousands of labels up front. First complete account sign-in and the review of a small data batch; acceptance of formal task ability still depends on qualified data. [F5–F7]
- This document gives a clear specification for starting engineering work; real task quality and unattended execution are not yet guaranteed. The next conversation can first complete independent local work and verify the Colab collaboration path. [F5, F7–F9]

## Implementation steps / Acceptance criteria

The following is the complete implementation specification. Sections 1–12 specify the product, data, model and acceptance; sections 13–15 specify materials, connectivity, start order and current status. Suggested values are not measured results.

## 1. Project goal and boundaries

Build an English autoregressive language model of about 24M parameters from random weights, completing a self-built tokenizer, general pretraining, financial-domain continued pretraining, supervised fine-tuning (SFT), preference post-training (DPO), probability calibration and evaluation, and finally provide a notebook for batch-processing short financial texts.

The final input is "text + specified asset"; the output is the bullish, bearish or neutral stance the text expresses toward that asset, plus a sentiment direction score. The user has confirmed this target-conditioned definition. For example, `Long $AAPL, short $TSLA.` should give different results for AAPL and TSLA.

The first version should focus on English, single short texts and explicitly specified US stocks/ETFs. This is a working scope that reduces labeling ambiguity, not a restriction on later extension to other assets. Input can come from tweets, short news sentences or own texts that the user has the right to process. The model does not log in to X automatically, crawl the web, predict future prices or execute trades.

This is a project for a small specialized language model using LLM training methods. Completing the full workflow and reaching the accuracy of a mature financial classifier are two goals that are accepted separately. The main model trains all parameters at every stage, does not load pretrained weights from other models, and does not replace full-parameter training with LoRA. FinBERT serves only as an external comparison baseline.

## 2. How exactly the training stages are divided

```mermaid
flowchart LR
    A[Data and label rules approved for use] --> B[Self-built English BPE tokenizer]
    B --> C[Random weight initialization]
    C --> D[General English pretraining]
    D --> E[Financial-domain continued pretraining]
    E --> F[Supervised fine-tuning SFT]
    F --> G[DPO preference training comparison]
    F --> H[Model selection on development set]
    G --> H
    H --> I[Fit temperature on independent calibration set]
    I --> J[Evaluate on locked test set]
    J --> K[Batch labels and score output]
```

"Ordinary training" is not an independent, unified technical stage. This plan implements it concretely as financial-domain continued pretraining and SFT. SFT itself is already post-training; DPO is another method within post-training. The complete workflow can include DPO but does not require adding PPO, a reward model or online reinforcement learning. The original DPO method uses preference pairs and a fixed reference policy and does not need a separately trained reward model. [S3]

| Stage | Learning material | What it should learn | Main objective |
|---|---|---|---|
| Tokenizer | English and financial text in the training partition | Convert text to tokens stably | BPE vocabulary training |
| General pretraining | Continuous English text | Basic language structure and continuation | Next-token cross-entropy |
| Financial continued pretraining | Financial text + a little general replay | Financial vocabulary, sentence patterns and expressions | Next-token cross-entropy |
| SFT | Text, target asset, human label | Judge stance on a fixed task | Cross-entropy of the correct label token |
| DPO | Correct/better and wrong/worse answers to the same input | Strengthen the label preference on hard cases | DPO loss relative to the SFT reference policy |
| Calibration | Held-out labeled data | Make probability values more trustworthy | Negative log-likelihood as a function of the temperature parameter |

## 3. Exact definition of the product output and the score

The first version requires only one target asset per input; multi-asset texts are run once per target by the calling program. A stable mapping of asset ID, ticker and name must be prepared in advance, so that ordinary English words such as `CAT` are not mistaken for stocks.

**The target-link gate is the responsibility of the input layer.** V1 requires a verifiable target cashtag, company name or alias in the text or in metadata approved for use; a bare ordinary English word cannot be taken directly as a ticker. When there is no clear link or the relation is ambiguous, return an empty label/score and request review; do not claim that the three-class logits automatically recognize "unrelated". `target_not_supported` is a conservative input-rule status, not a trained fourth class. Formal data keep the link evidence or character positions, for review and for use by the target baseline.

The following is a hand-constructed format example, not a training result:

```json
{
  "text": "$AAPL demand looks strong. I expect another good quarter.",
  "target": "AAPL",
  "label": "bullish",
  "probabilities": {"bearish": 0.06, "neutral": 0.14, "bullish": 0.80},
  "sentiment_score": 74.0,
  "confidence": 0.80,
  "needs_review": false
}
```

At a fixed answer position, the model outputs logits for three dedicated label tokens. Take the values at these three positions and apply temperature scaling:

\[
p_k=\frac{\exp(z_k/T)}{\sum_{j\in\{bearish,neutral,bullish\}}\exp(z_j/T)},\quad T>0.
\]

This is probability normalization within a predefined three-class output space. The model learns this label space through SFT; calibration is done only on the finally selected model. [S4] The program generates the JSON and computes the values, so the model does not freely generate decimals and fields.

\[
\text{sentiment\_score}=100(p_{bullish}-p_{bearish}),\qquad
\text{confidence}=\max_k p_k.
\]

This score is the expected direction computed directly once this project encodes the three classes as −1, 0, +1. It is not an actual return, not a probability of a price rise, and not an independently measured sentiment intensity. If it later needs to correspond to human continuous intensity ratings, a separate regression target and validation experiment are needed; the two cannot be equated directly.

| Probability distribution (bearish / neutral / bullish) | Score | How to read it |
|---|---:|---|
| 0.05 / 0.90 / 0.05 | 0 | Very likely neutral |
| 0.50 / 0.00 / 0.50 | 0 | Direction very uncertain |
| 0.05 / 0.15 / 0.80 | 75 | Leans bullish, with some classification uncertainty |

At low confidence, keep the candidate label and show `needs_review=true`. When the target cannot be resolved, truncation of the text loses key content, or the language is unsupported, `label=null, sentiment_score=null` is allowed, with a reason. When the target itself is valid but the text and approved metadata cannot support its relation to that target, return `status=target_not_supported` with an empty label/score; do not classify it as neutral. Do not use "neutral" in place of "inconclusive". The review criteria are pre-registered during development. After the final model is fixed, the calibration partition is split again by group into a temperature-fitting set and a threshold-selection set: the first fits T, the second selects the review threshold. If there are too few data, fix and publish the threshold and report the coverage curve; it cannot be adjusted after looking at the final test labels.

## 4. Labeling rules: define the object of judgment first, then prepare large amounts of data

The first version judges "the investment stance or outlook toward the specified asset that the text directly supports". Labels are not filled in from later stock prices, and asset views that the author did not express are not inferred from general macro knowledge.

| Class/status | Labeling principle | Hand-constructed example |
|---|---|---|
| Bullish | Expresses a positive outlook, buying/going long, or an expected rise for the target | `Still bullish on $MSFT after this guidance.` |
| Bearish | Expresses a negative outlook, shorting, or an expected fall for the target | `I am short $TSLA; margins look unsustainable.` |
| Neutral | Mentions the target but expresses no clear investment direction | `$AAPL reports earnings on Thursday.` |
| Needs review | Sarcasm, unclear attribution of quotes, contradictory stance, missing context | `Great, another flawless quarter...` |

`Shares rose 5% yesterday.` is a statement about past price movement; under this "investment stance" rule it is neutral by default unless the text also expresses a direction. If an adopted public dataset labels such a sentence as positive, keep the original label; the sentence enters the main task only after review and relabeling. Positive labels from every source cannot automatically be equated with bullish.

First label 200 rows and check the rules for negation, conditionals, irony, multiple assets and quotation; then extend to at least 500 rule-validation samples. Ideally a second person independently reviews at least 20%; if there is only one person, use delayed relabeling and report it truthfully; it cannot be called two-person independent annotation. Record disagreements and the reasons for adjudication. Samples without adjudication are not forced into the three-class gold standard.

## 5. Data plan and permissions

This project distinguishes three kinds of material: unlabeled pretraining text, labeled SFT samples, and preference pairs. All quantities are planning targets; actual numbers must be recounted and deduplicated at a fixed revision after the files are obtained.

| Data source | Suggested use | Checked information and access limits |
|---|---|---|
| Controlled English subset of FineWeb-Edu | General pretraining | The data card offers streaming reads, states ODC-By, and is subject to Common Crawl terms; save the version, source and applicable terms; do not download the full corpus. [S5] |
| SEC English financial education material, filing full text | Financial continued pretraining | Full text must be extracted, deduplicated and segmented; filing language differs in domain from tweets and cannot replace tweet task labels. [S6] |
| SemEval-2017 Task 5 | Reference for target-conditioned financial sentiment, scoring/evaluation research | The original task targets companies/cashtags and has continuous scores from −1 to +1. Obtaining the files and the data release agreement must be completed first; full training permission was not confirmed this time. Some labels depend on context from external links; at intake, check whether they can be supported from this project's input alone; do not convert scores to labels by a threshold only. [S7] |
| FiQA 2018 | Reference for target- and aspect-related financial sentiment | The original task includes target/aspect and continuous scores; the official site lists non-commercial restrictions for the train/test sets; the full files were not read this time. [S8] |
| zeroshot/twitter-financial-news-sentiment | Conditional auxiliary labeling source | Only text and label, with no target asset or continuous intensity; actual counts, source and usable permissions must be re-checked, and target/review semantics added. [S9] |
| English short financial texts owned by the user and explicitly approved for training | Main-task SFT, DPO, independent testing | Label by the rules in this document; record source, license scope, time, target, duplicate cluster and annotator. |

X's current developer agreement restricts using its API or content to train/fine-tune foundation/frontier models; the AI-training restrictions in the enterprise agreement may be broader. The applicable terms and explicit authorization should be confirmed when data are obtained. Being publicly visible, copyable by the user, or declared MIT by a third-party mirror is not by itself enough to prove the data can be used for training in this project. The specific locations are Developer Agreement III.A(k) and Enterprise MLA §4.1(k); their scopes are checked separately. [S12] X content without explicit training permission does not enter pretraining, SFT or DPO; the workflow can first be completed with English financial material we have rights to and with self-written samples. No licensing conclusion is drawn here for data not yet obtained.

### First-round data budget

- **General pretraining: 100M tokens processed cumulatively.** First a 1M-token technical trial run, then expand after the checks pass. Data come from a frozen manifest and need not fit into memory at once.
- **Financial continued pretraining: 25M tokens processed cumulatively.** Suggested initial mix: 80% finance, 20% general replay, i.e. about 20M finance + 5M general; this ratio is an experimental setting still to be validated.
- **Target-conditioned labels: plan 8,000–12,000 qualified samples.** If there are not enough, first run a small experiment with 500–1,000 samples, report by the actual sample count, and do not count synthetic data as real human samples.
- **DPO: 500–2,000 pairs.** Built only from the training partition and additional material approved for training; prefer targets, negations and conditional expressions that SFT easily confuses, with the preferences checked by a human.

"Tokens processed cumulatively" includes repeated passes; also report the deduplicated amount of independent text, the number of independent tokens and the number of repetitions. 100M + 25M is an adjustable first-round compute budget, not a standard for sufficient training. If validation is still improving and resources allow, enlarge the budget through a pre-recorded experiment, rather than enlarging the model from the start.

### Splitting and leakage control

1. Save the text source, time, original ID, target asset, source license, content hash, duplicate/event cluster ID, label and adjudication record.
2. Plan the main task by time as about 70% train, 10% development, 10% calibration, 10% test. The proportions are targets; actual counts are decided by group constraints and the class distribution.
3. Different targets of the same tweet, retweets, near-duplicate texts and rewrites of the same event must not cross partitions. Set the time boundary first, then remove cross-boundary contamination or keep the whole cluster in the later partition; future texts must not be moved into the training partition.
4. Sources without reliable timestamps are split only by group and explicitly marked as "not a temporal extrapolation evaluation"; keep the official test partition and do not feed it back into training.
5. Before tokenizer training and all pretraining, freeze the development, calibration and test data, and remove their texts and near-duplicates from the training corpus. Where contamination from public web pretraining cannot be ruled out, disclose the scope of detection and add a test on newly collected text.
6. Run a separate stress test on unseen assets or unseen authors; do not claim that a time split alone proves cross-asset generalization.

Before formal pretraining starts, at least the **text pool** of the evaluation partitions must be sealed; labels can be completed later. Training data added later are checked batch by batch for hash and near-duplicate collisions with the sealed pool, recording the detection method and threshold. While there is no formal data, self-written samples are used only for `smoke` technical verification; their tokenizer, data and weights live in separate directories and are not used as the initialization checkpoint for formal training. The main task's development/calibration/test partitions are not used to tune pretraining loss; a separate held-out text set is used only for pretraining diagnostics.

## 6. Model and engineering choices

The main engineering uses **MiniMind's pinned source as the starting point for modification**, with our own tokenizer, data, configuration and random model weights. Pinned reference commit: `f659b55761b754d306bd140573493a6543cafd7f`. It already has pretraining, full-parameter SFT and DPO paths; the current main-line default configuration differs from the early 26M tutorial. [S1]

| Item | Main specification |
|---|---:|
| Architecture | Decoder-only Transformer, MiniMind's dense model, MoE off |
| Vocabulary | 8,192, including all special tokens and three label tokens |
| Layers | 6 |
| Hidden size | 512 |
| Query heads / KV heads | 8 / 4 |
| FFN intermediate size | 1,664 |
| Input and output embedding | Shared weights |
| Q/K normalization | On, matching the counting convention of the pinned commit; all other effective configuration exported in full |
| Total parameters | **24,255,744, about 24.26M**, computed with the pinned source's default normalization and other components |
| Pretraining context | 256 for the trial run first, then fixed at 512 |
| GPU compute | FP16 autocast + GradScaler; optimizer master weights kept in FP32 |
| Initial micro-batch / accumulation steps | 4 / 8; on OOM, reduce the micro-batch first, then adjust accumulation by effective token count |

The same configuration with 7 layers is about 27.60M and can serve as a later comparison. During implementation, re-verify with `sum(p.numel() for p in model.parameters())`; changes in vocabulary size, special tokens or network components all change the parameter count.

This step needs somewhat more configuration work than the nanoGPT suggestion of the previous round, but it reuses the existing SFT/DPO structure and fits this round's goal of a "complete training chain" better. Code and architecture sources should be credited in the final project README; self-trained weights do not mean a new architecture was invented.

### Required source modifications

These are work items still to be implemented, not features the upstream repository supports out of the box; for details see the companion note "Training engineering check" in the same directory.

- Unify the model configuration and tokenizer path. The existing CLI does not fully expose the parameters needed for a self-built 8K tokenizer; we cannot just replace the tokenizer file and keep the default 6,400 vocabulary.
- Fix the English task template and remove the random Chinese/English system prompts and empty thinking templates this project does not need. Train the tokenizer only on training text; save the special token IDs and the version hash. [S2]
- Pretraining does full segmentation/packing with EOS inserted between documents; V1 allows ordinary causal attention across document boundaries and does not implement block-diagonal attention. The tail of a long document must not be silently dropped; the corpus tail is handled by keeping/masking padding, and effective tokens are counted.
- **Single shift scheme:** each pretraining sample reads 513 IDs, `x=ids[:-1]`, `y=ids[1:]`; the model is called only for logits, **without passing `labels`**, and `CE(logits,y)` is computed outside, so MiniMind's internal shift is not triggered. SFT/DPO take the logits that predict the label directly at the last position of the full prompt and do not shift the label a second time. The SFT label CE still covers the full vocabulary; DPO uses the full-vocabulary log-softmax at the same position. Check the target indices with hand-made short sequences.
- SFT computes no loss on the prompt; it computes the full-vocabulary cross-entropy of the correct label only on the logits at the last prompt position; all model parameters are still updated. The three reserved tokens `<|bearish|>`, `<|neutral|>`, `<|bullish|>` must each be a single token, and each valid sample has exactly one label supervision term. Inference uses the three-class logits at the same position, normalized within the three classes. If we later switch to three-class-only cross-entropy, record it as a separate experiment.
- In SFT/DPO, EOS, prompt and padding carry no supervision loss for this task; once the template is fixed, training and inference are consistent. Over-long task inputs are first rejected/sent for review; the asset or label is never silently truncated. On-disk uint16 stores only non-negative IDs; the `-100` labels needed at runtime can only be built in signed int64 tensors.
- DPO's chosen/rejected use the same prompt and single-label answers and compute only the two label log probabilities at that prediction position; the reference model is kept fixed, gradient-free and in eval mode. Assert per sample that the two labels are valid and different and that the supervision term exists; differences in prompt/padding/EOS must not decide the preference loss. Limit the number of pairs per original input or weight by original input, so that one post is not overcounted through many pairings.
- Unify the output, load and resume paths. Upstream has fixed relative directories; do not assume that changing `save_dir` solves all checkpoint locations at once.
- At the boundary after an optimizer update completes and gradients are zeroed, save the FP32 master weights, optimizer, scheduler, GradScaler, RNG, data position, cumulative tokens, configuration and data/tokenizer hashes. Keep best and latest separately; do not save only half-precision inference weights.
- The scheduler advances only with successful optimizer updates; record cumulative processed tokens, overflow-skipped steps and successful updates separately. Initially `num_workers=0`, and the resume cursor points to the next batch not yet consumed. A Drive backup is first copied as a temporary file, the hash is checked, and then a completion marker is written; resume accepts only a complete version whose manifest and hashes agree, not merely the presence of a file name.
- Compile is off by default; use the available PyTorch SDPA path first; a separate installation of external FlashAttention is not required. Check CUDA/PyTorch, dependency and data-format compatibility stage by stage.

## 7. Execution plan for each training stage

The learning rates below are preset starting values for experiments and must be tuned with development data and loss/gradient diagnostics; they are not optima that upstream validated for financial tweets.

| Stage | Initial training setup | Deliverables and gates |
|---|---|---|
| P0: task, sources and baselines | Labeling rules v1, data manifest, small-sample review; majority class and TF-IDF + linear classifier | Clear task convention, permissions and splits; baselines reproducible |
| P1: tokenizer and model | Byte-level BPE, 8K vocabulary; random initialization; trial runs of forward, backward, save and resume | Round-trip encoding of cashtags/numbers/punctuation; about 24.26M parameters; fixed token IDs |
| P2: general pretraining | A 1M-token trial run, then a 100M-token total budget; AdamW, peak LR starting at 3e-4, warmup over about the first 2%, then cosine decay; gradient clipping 1.0 | English held-out loss improves; save learning curves and fixed-prompt continuations |
| P3: financial continued pretraining | Continue from the best P2 weights; 25M-token total budget, 80/20 mix; LR starting at 1e-4, with a new schedule for this stage | Measure both financial and general held-out sets; record domain gain and general degradation |
| P4: SFT | All parameters trainable; LR starting at 1e-5–5e-5; try at most 1–3 epochs first; select the checkpoint by dev macro-F1 | Label mapping/masking correct; the model outputs three-class probabilities; SFT baseline established |
| P5: DPO | Start from the same SFT checkpoint; freeze that SFT reference model; LR starting at 1e-6–1e-5, beta starting at 0.1, 1 epoch first, micro-batch starting at 1 pair | Preference learning experiment completed; compared with SFT and with an SFT control trained further on the same amount of new label data |
| P6: selection and calibration | Choose SFT or DPO on development; after locking, fit T on the temperature subset of calibration, then select the review threshold on the independent threshold subset | Final model, temperature, review threshold and configuration frozen |
| P7: final test and demo | Test used only for the final report; offline batch CSV/JSONL | Labels, scores, confidence, review flags, error analysis and model card |

Pretraining validation uses fixed held-out text and the same tokenizer; perplexities under different tokenizers cannot be compared directly. The domain gain in P3 cannot be judged by financial loss alone; general loss and later task performance must also be examined.

In this project DPO is a learning experiment that must be completed, but whether it is used as the final model depends on development-set evidence. For single-label three-class classification, it essentially strengthens a class preference and is not necessarily better than supervised classification; DPO results from text-generation research cannot be taken directly as a guarantee of improvement in financial classification. [S3] If DPO is worse, the deliverables still include the DPO checkpoint, the training records and the negative result, and final inference uses SFT. Calibration must be applied to the finally selected checkpoint; SFT's temperature cannot be reused to calibrate a DPO model that has changed. A single positive temperature T preserves the argmax, so it does not improve the F1 of a fixed-argmax classification; what it changes is the probability values and the review behavior that thresholds determine. [S4]

## 8. T4, Colab and time budget

The screenshot proves that a GPU is available; it provides no training throughput for this model. For the 24.26M model, FP32 parameters, gradients and the two Adam states come to roughly 0.36 GiB at 16 bytes/parameter; actual training also needs activations, logits, workspace and CUDA cache, and DPO adds a reference model and paired inputs, so this number is not peak memory.

Each stage first runs 50 forward/backward micro-batches as warmup, then measures about 200 micro-batches, with gradient-accumulation updates proceeding as usual; these are micro-batches and must not be written up as 250 optimizer updates. Excluding validation and saving time, record effective non-padding tokens/s, peak allocated/reserved memory, and gradient overflows/skipped steps. Also record end-to-end speed including evaluation and saving, and report the tokens actually consumed by the test. Pretraining, SFT and DPO are measured separately; trial runs and the formal budget are accounted for separately.

In the full-length pretraining configuration with a single GPU, micro-batch 4, length 512 and accumulation 8, each optimizer step processes 16,384 tokens. The 100M and 25M token budgets correspond to about 6,104 and 1,526 updates respectively; stopping is by actual effective token count.

The following are scenarios derived from the formula only, not T4 measurements:

| Assumed measured throughput | Pure training time for 125M tokens |
|---|---:|
| 1,000 tokens/s | about 34.7 hours |
| 3,000 tokens/s | about 11.6 hours |
| 6,000 tokens/s | about 5.8 hours |

The formula is `hours = cumulative training tokens / measured tokens_per_second / 3600`. The table excludes data processing, validation, saving, SFT/DPO, waiting after disconnects and re-runs. Colab resources, session duration and GPU allocation have no sustained guarantee; the whole project cannot be scheduled as one long task that is sure to finish without interruption. [S10]

The plan does not assume buying compute or paid APIs. Data are read in shards from the local runtime disk, complete checkpoints are synced to Drive regularly and verified to reload, and a mapping table between local and persistent paths is kept. Whether to enlarge the token count or the model is decided by the remaining compute budget, not by free GPU memory alone.

## 9. Experimental comparisons and acceptance

### Comparison groups

| ID | Model/experiment | Question answered |
|---|---|---|
| B0 | Majority class | Lowest reference under class imbalance |
| B1 | Target-aware TF-IDF + linear classifier: the current asset replaced by TARGET, other assets by OTHER_ASSET, with word bigrams and local-window features around the target | How far a simple supervised method gets; not just a ticker prepended to the full text |
| B2 | FinBERT raw output and a clearly disclosed adapted version | Comparison reference from a mature financial sentiment model; not an initialization source for the main model [S11] |
| A0 | Random model of the same architecture with direct SFT, small-scale control | Whether pretraining brings a task gain |
| A1 | General pretraining → SFT | General pretraining baseline |
| A2 | General pretraining → financial continued pretraining → SFT | Incremental value of financial continued pretraining |
| A3 | A2 → DPO | Whether preference training improves hard samples |
| A4 | A2 with continued SFT on the correct labels of the samples added for DPO | Separates the gain from "more labeled data" from that of the DPO method itself |

B2's generic sentiment definition may differ from target-conditioned stance; the limits of the comparison must be stated. In a unified comparison, use the same test convention and a fixed label-name mapping; integer labels encoded differently in the sources cannot be compared. Early pretraining has a single seed, which is reported explicitly; if resources allow, priority goes to re-running SFT/DPO with 3 seeds, which cannot be described as independent repetitions of the whole pretraining workflow.

### Metrics and suggested gates

- Primary metric: three-class macro-F1; with per-class precision/recall/F1, confusion matrix and balanced accuracy.
- Probability metrics: NLL, three-class Brier score, reliability diagram and ECE with the binning rule stated. The calibration set is for fitting, the test set for reporting. [S4]
- Score metrics: the first version checks direction, consistency and distribution; only if a continuous human gold standard matching this task's semantics is obtained are MAE, Spearman etc. measured separately; the three-class expected score is not passed off as an intensity regression result.
- Slices: negation, conditionals, multiple targets, irony, quotation, unseen tickers, non-English, missing context, repeated marketing text; report the sample size of each slice.
- Review mechanism: report coverage and the error rate of accepted samples under different thresholds; a low-confidence flag by itself does not prove that all out-of-domain inputs can be recognized.
- Uncertainty: bootstrap intervals over deduplicated/event-grouped units, so that several posts about the same event are not treated as independent samples.

**Training engineering completion gate:** every stage actually executed, with complete logs and checkpoints; weights restorable; output mapping, score formula, templates and data boundaries pass the checks. Numerical verification of continued training should record the allowed tolerance and the environment and should not claim bitwise identity across hardware.

**Task ability gate (provisional engineering target, not a guarantee from the literature):** the main model aims for macro-F1 ≥ 0.70 and at least 0.03 above B1; per-class recall aims for ≥ 0.60. These thresholds are frozen in P0 after seeing the sample distribution and annotation agreement in the train/development partitions, and cannot be changed repeatedly before the final test. Meeting them on the development set is for model selection; final acceptance for use must be confirmed on the sealed test set with the same pre-registered convention, reporting the sample size and the interval for the difference. If they are not met, the project can still be delivered as a "complete training experiment", but it cannot be said to have passed acceptance for practical use.

**DPO selection gate:** the comparison is decided in advance to be primarily by development macro-F1; training preference accuracy does not substitute for it. Also check per-class recall, NLL and review coverage. When results are close and evidence is insufficient, keep the simpler SFT. Look at the test set only after the final model is frozen; if development continues, demote the viewed test set to development material and obtain new final test data.

## 10. Schedule and first-day actions

The table below is an organizational suggestion for a personal project, assuming data acquisition and labeling proceed as planned; four weeks is not a promise of training quality or compute availability.

| Time | Focus | Outputs that can be accepted |
|---|---|---|
| Week 1 | Labeling handbook, sources and splits, baselines, self-built tokenizer, MiniMind configuration cleanup, T4 trial run | Data manifest, a model of about 24M, resumable short training |
| Week 2 | General pretraining, financial continued pretraining; human labeling in parallel | Weights and learning curves of both stages, actual compute ledger |
| Week 3 | SFT, error analysis, hard cases and preference pairs, limited ablations | SFT baseline, frozen preference data, per-class metrics |
| Week 4 | DPO comparison, model selection, calibration, final test and batch notebook | Final model, scoring interface, evaluation report, model card |

**First-day priorities:** fix the input and label rules; review 200 candidate samples and the data permissions; record the Colab environment; create a small tokenizer/model; complete one forward pass, backward pass, save, resume and throughput measurement. The first day's success criterion is that the minimal part of the training chain runs verifiably, not a claim that financial judgment is already reliable. If the main data are not yet available, self-written short samples can be used for a technical trial run, labeled separately as such.

## 11. Expected deliverables

Later implementation should set up a separate project directory; the following is a proposed structure and does not mean the files have been implemented:

```text
130U-FinLLM/
  README.md
  configs/                 # per-stage configs, upstream commit, environment lock
  data/                    # source manifest, split indices, labeling handbook; large data not committed to Git
  tokenizer/               # self-built BPE and fixed special token IDs
  notebooks/               # environment/data, pretraining, SFT, DPO, evaluation, batch prediction
  src/                     # data, training, label probability and score computation
  checkpoints/             # base, finance, sft, dpo; best/latest kept separately
  evaluation/              # metrics, slices, calibration, error analysis, compute records
  model_card.md
```

The final demo should read a CSV/JSONL with `text,target` and output, for each valid input, the three-class probabilities, direction score, confidence and review flag. Saving the model weights and tokenizer is still not enough to reproduce the results; the template, label mapping, temperature, threshold, code version and data version must also be saved.

## 12. Current conclusions and items still to verify

Recommended: complete the full chain with **a MiniMind dense model of about 24.26M + a self-built 8K English vocabulary + full-parameter training**, organizing experiments first around a budget of 100M general + 25M financial-stage tokens. With small batches and a short context, the model has reasonable starting conditions on a T4; final peak memory and speed depend on the trial runs.

The main open items are: data permissions suitable for training and the obtainable quantity, consistency of target-conditioned labels, compatibility with the current Colab environment, measured T4 throughput, and the real gain of a small model trained from scratch over simple baselines. These are closed, respectively, by the source review in P0, the labeling trial, the trial runs in P1/P2 and the controlled evaluations in P4–P7.

What has been completed this time is the plan, the investigation of original sources, the configuration check of the pinned source and the arithmetic budget. No promise is made about model quality, investment value or finishing all training in one day.

## 13. GitHub reference repositories and code delivery

| Repository | How this project uses it | What is not reused directly |
|---|---|---|
| [jingyaogong/minimind](https://github.com/jingyaogong/minimind) | **Main implementation reference.** Take the dense model, pretraining, full-parameter SFT and DPO code from the pinned commit, and reorganize the configuration and training loop per section 6 | Ready-made weights, the default 64M configuration, the default tokenizer, Chinese templates and the full upstream corpus |
| [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | **Teaching and cross-check reference.** Explains attention, random initialization, next-token training, classification and DPO; cite it first, do not copy code by default | No second parallel main model is created, to avoid mixing architectures and checkpoint formats |
| [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) | **Auxiliary engineering reference.** Borrow the clear training loop, binary token files and small-batch reading; pin the version actually referenced during implementation | The repository is marked deprecated; it is not treated as a maintenance guarantee for this project, and its old environment install commands are not copied |
| [huggingface/tokenizers](https://github.com/huggingface/tokenizers) | **Tool dependency.** Train and save our own English byte-level BPE vocabulary | Ready-made tokenizers of other large models are not loaded as this project's self-built vocabulary |

The engineering is mainly PyTorch, with only the dependencies that are needed; upstream demos, Agent, MoE or UI packages are not all installed. Check Colab's existing CUDA/PyTorch, and lock the Python and dependency versions after verifying compatibility. The first environment record is saved as `environment.json` / a locked dependency file; Colab's bundled CUDA is not replaced blindly at the start.

The source code credits the reference projects, pinned commits, scope of modification and licenses. Keep MiniMind's Apache-2.0 license and the applicable NOTICE; check the license of a file before copying specific code from other repositories. Usage conditions for self-trained weights and data are recorded separately; the code license does not automatically cover the data and model weights.

The proposed repository contents include:

```text
130U-FinLLM/
  README.md                         # start-up notes in Chinese + English project summary
  LICENSE / THIRD_PARTY_NOTICES.md
  pyproject.toml / requirements-colab.txt
  configs/                          # smoke, formal 24M, per-stage and resolved effective configs
  src/finllm/                       # model, tokenizer, data, training, inference
  scripts/                          # entry points for data validation, sharding, training, evaluation and resume
  notebooks/
    00_setup_and_smoke.ipynb
    01_prepare_data.ipynb
    02_pretrain.ipynb
    03_domain_pretrain.ipynb
    04_sft.ipynb
    05_dpo.ipynb
    06_evaluate_and_predict.ipynb
  data/manifests/                   # sources, versions, hashes, partition indices; no private text
  docs/                            # this plan, labeling handbook, operating notes, model card
  tests/                           # the necessary correctness checks listed below
  reports/                         # summary results and figures that the licenses allow to be published
```

All the files above are still to be implemented. Large corpora, private texts, training checkpoints, credentials and sensitive outputs of user notebooks are not committed to Git. Notebooks act as thin operating interfaces that call the same set of scripts, so that each notebook does not copy its own training logic. For a public release, review the model/data licenses separately and clear the notebook outputs.

## 14. What the user needs to prepare, and how to collaborate through Colab

### Materials and responsibilities

| Material | Required now? | How the user helps | What the agent is responsible for |
|---|---|---|---|
| Google account and Colab | Required when GPU trial runs start | Sign in in their own browser, select T4, complete the necessary interactive authorizations | Write the notebooks, check the environment output, arrange short training and resume verification |
| Google Drive | Recommended before long training | Sign in and prepare a project directory; about 10GB of free quota is recommended, adjusted after an actual check | Shard/checkpoint manifests, backup verification and resume code; the runtime working disk is checked separately |
| GitHub account and repository | Can be added after the engineering is set up | If already created, provide the link; if not, there is no need to create it yet; the next conversation will make the scope of repository creation/push explicit | Prepare the code locally first; with usable authentication, perform authorized GitHub operations; without it, provide a source bundle |
| A small batch of real task samples | Not needed for the technical smoke test; required for the formal task | Initially, ideally 20–50 English short texts with training rights, with target, source and time; leave unknown fields empty, do not invent them | Build the labeling table, look up public candidates, clean, deduplicate, pre-label and count |
| Label review | Needed before the task rules are fixed and before formal performance acceptance | Review the first ~200 rows and explain disagreements; can be done over several sessions | Provide label definitions, explanations of hard cases and a review table; AI pre-labels and human confirmations are recorded separately |
| 8k–12k qualified samples | Formal data target; the user is not required to deliver everything before work starts | Help provide sources we have the right to use; review key disagreements | Check public files and their conditions, organize targets, build the real data manifest; when there is not enough, shrink the experiment and say so |
| API key, X login or paid GPU | Not a prerequisite for the first version | No need to provide passwords, cookies, PATs or API keys in chat | By default use normal account authorization, clearly licensed data and the existing Colab; any extra payment is decided separately |

The minimal sample fields are `id,text,target,source,created_at,rights_note`; with labels, add `label,annotator,adjudication_note`. CSV or JSONL is fine; mark missing fields truthfully. `rights_note` is a record of the source and cannot by itself replace real authorization; public candidates not yet downloaded and approved are marked pending. `Long $AAPL, short $TSLA.` must produce two target samples that keep the same original id/duplicate cluster.

### Recommended connection: GitHub manages code, Colab runs, Drive keeps results

This is a file and version collaboration path; it does not mean the current agent is already connected to the user's GPU.

1. The agent prepares inspectable scripts, tests and notebooks in a separate local `130U-FinLLM` directory and produces a source bundle at a pinned commit.
2. Once there is a repository, the user signs in to GitHub/Colab and opens the notebook. Public source can be downloaded at runtime by pinned commit; a private notebook can use `Include Private Repos` on Google's official GitHub opening page, authorized in the user's browser.
3. **Browser OAuth for a private notebook does not mean that git at runtime has access to the private repository.** The first round uses a simple method: the user downloads a source ZIP of the specified version from the signed-in GitHub and puts it in Drive or uploads it through Colab; the runtime checks the archive hash/version manifest before unpacking. Without a remote repository, a similar source bundle delivered by the agent can be uploaded instead, so the smoke test is not blocked.
4. The user selects a GPU in Colab and mounts Drive through the notebook's normal authorization interface. Hot training data are copied to `/content/130U-FinLLM`; large numbers of small files on Drive are not read remotely batch by batch. Drive uses `MyDrive/130U-FinLLM/`, containing data, checkpoints, runs and source-bundles.
5. First run environment diagnostics: GPU/CUDA/PyTorch, RAM, disk/Drive headroom, writable paths and version hashes. Only then are the usable micro-batch and resource budget given.
6. Run a short training, save a complete checkpoint, disconnect/restart the runtime, reinstall the locked dependencies, restore the checkpoint and run the next batch. Move on to long stages only after this succeeds.
7. Each stage exports `run_summary.json`, `metrics.csv`, environment information, code/data/tokenizer hashes and a checkpoint manifest. Results can be uploaded by the user back into the current conversation, or read through file/browser paths that are authorized for this task and actually readable; it is not assumed that sending a Drive link automatically grants access.

If the browser tools in the next conversation can access the signed-in notebook, they can help perform visible operations; sign-in and authorization are done by the user. If the browser is not available, the user clicks to run the notebook cells, and the agent fixes problems from the returned logs and provides a new version. **Sharing a notebook does not share the running VM; there is currently no verified direct Colab kernel connection, and no promise of unattended or persistent background control across sessions.** The basis is Google's official FAQ/example and the actual capability status of this session. [F6, F7]

The suggested repository name is `130U-FinLLM`, Private during development; whether to make it public is the user's decision. The user does not need to fork all of MiniMind. If the user wishes to create it first, they can create an empty repository and provide the link; there is no need to place data manually or configure complex services first. Whether the agent can create it later depends on the authenticated GitHub tools/CLI actually available in the next conversation and cannot be guaranteed in advance.

## 15. Start order for the next conversation, acceptance and current status

### Milestones by dependency

| Gate | Work that can be done immediately | Pass condition / how to continue when there are dependencies |
|---|---|---|
| M0 Local engineering | Read this file; set up a separate directory, upstream source records, configuration, data schema, labeling handbook and notebook skeletons | Other resume/research files in the current workspace are not modified; source structure complete; no dependence on Colab sign-in |
| M1 Minimal training chain | Self-written samples clearly marked as smoke, tokenizer, random model, tiny pretraining/SFT/DPO runs, and save/resume | Necessary CPU/local checks pass; parameter count correct; output probabilities/scores correct; all smoke files kept separate from formal data |
| M2 Colab connectivity | Upload/pull of the source bundle, T4 environment record, a little GPU training, complete Drive backup, resume after runtime restart | Continuation from the resume point succeeds; real throughput and peaks reported; connection problems do not stop continued preparation of local code and data |
| M3 Formal materials | Check the conditions for obtaining data, review 200 rule samples, seal the eval text pool, split/deduplicate, train the formal tokenizer | Data manifest traceable; no detected duplicates across train/dev/cal/test; valid targets and labels consistent; data not obtained are not reported as done |
| M4 Two-stage pretraining | First a 1M-token trial run in the formal configuration, then general and financial pretraining per the budget | Loss/numerics normal, complete checkpoints restorable, throughput ledger complete, formal and smoke runs not mixed |
| M5 SFT/DPO | Full-parameter SFT, building and reviewing preference pairs, DPO and the SFT control with the same added samples | Each stage actually executed, with checkpoints and development results; if DPO is worse, keep the negative result; this learning stage cannot be omitted |
| M6 Final delivery | Development-set selection, independent calibration, frozen thresholds, one final test, batch prediction notebook, model card | Engineering completion and task performance reported separately; if the performance gate is not met, deliver the experimental status truthfully |

The tiny DPO run in M1 only proves that the path can execute; it cannot replace the formal DPO experiment in M5. M0–M2 can start with self-written samples; formal-data training in M4 depends on M3. When data are insufficient, small-scale experiments can continue with their scale stated; a smoke run cannot be claimed as a full-budget training result. Time is estimated from measured throughput and human labeling progress; there is no promise of reaching a specified accuracy within one day/four weeks.

### Correctness that must be verified

- Each of the three labels is a single token; the tokenizer round-trips while preserving cashtags, numbers and negation words; the 8192 already include the special tokens.
- Hand-made short sequences prove that the next-token alignment shifts only once; the last segment of a long pretraining document really enters the samples; prompt/pad/EOS contribute no SFT/DPO task loss.
- In DPO the policy has gradients, and the reference parameters and gradients do not change; chosen/rejected labels are valid and different; the loss for an initially identical policy matches the expected value.
- Multiple targets of the same tweet and near-duplicate clusters cannot cross splits; inputs to the baseline and to the main model really differ when the target is switched; targets that cannot be linked and over-long inputs return explicit statuses.
- On FP16 AMP overflow, the scheduler is not advanced by mistake; saving happens at the specified boundary; after a checkpoint restore, the data cursor, optimizer/scheduler and cumulative counts agree. A short uninterrupted run and an interrupted-and-resumed run are compared within the recorded tolerance; bitwise equality across hardware is not required.
- JSON fields are stable, the three-class probabilities sum to 1, scores lie in [-100,100] and are computed by the specified formula; temperature/threshold correspond to the final model and tokenizer hash.

These are tests of training correctness and data boundaries; no extra tests are built for reversible documentation/format changes. Run the necessary tests after the environment is locked; after a failure is fixed, re-verify the corresponding item. GPU tests are recorded as passed only after they have actually been run on the user's Colab.

### Done, not done, and principles for taking over

- **Done:** requirement definition, naming, source checks, fixed model specification, arithmetic budget, stage design, list of code modifications, division of materials, collaboration path and acceptance criteria.
- **Not yet done:** project code and notebooks, GitHub repository, qualified formal corpus and labels, verification of the connection to the user's Colab, training, measurement, real performance evaluation.
- **Do not re-ask settled matters when starting:** English, target-conditioned three classes, random initialization, about 24M, T4, self-trained tokenizer, full-parameter pretraining/SFT/DPO and the score formula are all settled. Ask only about real gaps that would change execution.
- **Work independently:** while waiting for the user to sign in, upload logs or add material, continue with code, check and documentation work that does not depend on this information. When the user needs to do something manually, give one specific action and the reason for it.
- **Continuity record:** after implementation starts, maintain `docs/HANDOFF.md` and `runs/<run_id>/run_summary.json`, recording the actual code version, items passed, open items and next steps; do not rewrite planned status as actual completion.

## Original sources and check attachments

- **S1** [MiniMind pinned commit](https://github.com/jingyaogong/minimind/tree/f659b55761b754d306bd140573493a6543cafd7f): model, pretraining, SFT, DPO, data loader and resume implementation. Item-by-item notes are in the attachment "Training engineering check".
- **S2** [Hugging Face Tokenizers Quicktour](https://huggingface.co/docs/tokenizers/quicktour): BPE training and saving/using a tokenizer.
- **S3** [Direct Preference Optimization, original paper](https://arxiv.org/abs/2305.18290); [TRL DPOTrainer official documentation](https://huggingface.co/docs/trl/dpo_trainer): method and input structure of preference training. This plan uses the MiniMind implementation; TRL is only a cross-reference.
- **S4** [On Calibration of Modern Neural Networks, original paper](https://proceedings.mlr.press/v70/guo17a.html): temperature calibration and reliability evaluation. A separate calibration partition is an experimental design choice of this project, not a requirement of the paper.
- **S5** [FineWeb-Edu authors' data card](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu): data, streaming reads, license and limitations.
- **S6** [SEC: Accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data); [SEC: Beginners' Guide to Financial Statements](https://www.sec.gov/about/reports-publications/beginners-guide-financial-statements).
- **S7** [SemEval-2017 Task 5 original paper](https://aclanthology.org/S17-2089/): fine-grained sentiment task on financial microblogs and news. The actual download and license status are in the data attachment.
- **S8** [FiQA 2018 official task page](https://sites.google.com/view/fiqa/home): targets, aspects and sentiment scores. The original task files and the non-commercial use conditions must be checked before intake.
- **S9** [zeroshot/twitter-financial-news-sentiment data card](https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment): fields, labels and the card's statements. Count conflicts and the limits of the rights check are in the data attachment.
- **S10** [Google Colab FAQ](https://research.google.com/colaboratory/faq.html): runtime, resource and persistence limits.
- **S11** [ProsusAI/FinBERT](https://github.com/ProsusAI/finBERT); [model card](https://huggingface.co/ProsusAI/finbert): external comparison baseline.
- **S12** [X Developer Agreement](https://docs.x.com/developer-terms/agreement), updated 2026-04-27, III.A(k); [X Enterprise Master License Agreement](https://legal.x.com/data-terms/us/mla.html), §4.1(k). The applicable agreement and the scope of authorization must be confirmed separately.

Research attachments in the same directory (Markdown files): "Data and source check", "Training engineering check", "Post-training and evaluation check". Browser automation timed out twice when connecting; the sources this time were checked by reading web pages and through official code interfaces; the browser failures were not interpreted as the materials not existing.
