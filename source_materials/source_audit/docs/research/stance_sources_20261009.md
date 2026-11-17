# English asset stance data check — 2026-10-09

This round used the primary-source check required by the Research skill: can we obtain data with explicit usage conditions that contain target entities and can be mapped to asset stance? Conclusion: **first adopt SEntFiN as a candidate pool for human review, and exclude the texts of the whole pool before pretraining; the source's positive/negative still cannot be taken automatically as this project's bullish/bearish labels.** This lets pretraining preparation continue while asset mapping and label review proceed in parallel.

## Selected candidate: SEntFiN 1.0

The [original authors' repository](https://github.com/pyRis/SEntFiN) is maintained by the GitHub account pyRis; the [GitHub user metadata](https://api.github.com/users/pyRis) return the name Rishu Kumar, which matches one of the paper's authors. The [pinned LICENSE](https://github.com/pyRis/SEntFiN/blob/eba43610fe3cb57a3e5773cd6c037da1f8992ad5/LICENSE) is MIT, with copyright attributed to Ankur Sinha, Satishwar Kedas, Rishu Kumar, Pekka Malo. The repository home page explicitly publishes the dataset and codes; apart from README and LICENSE, the root directory holds two data files. The license evidence here comes from the authors' release repository and cannot be used to give additional rights guarantees on behalf of the original news publishers. This round uses the data for local review of research candidates, keeps the copyright notice, and does not commit the texts to the project's GitHub.

[The authors' paper, §3](https://arxiv.org/html/2305.12257), states that the samples come from Indian financial news from 2011–2015; three human annotators judged entity-related financial sentiment, and the final labels use consensus plus a small number of author adjudications. The paper reports 10,753 news items and 14,404 entity labels. Its neutral class also includes entities, such as regulators, to which financial sentiment does not apply. Therefore "human labels by the original authors" and "asset stance confirmed by humans in this project" must use different fields; news sentiment and an explicit investment direction are not inherently equivalent.

Pinned revision: `eba43610fe3cb57a3e5773cd6c037da1f8992ad5`.

| File | Pinned download URL | Bytes | SHA256 |
|---|---|---:|---|
| Main data | [SEntFiN.csv](https://raw.githubusercontent.com/pyRis/SEntFiN/eba43610fe3cb57a3e5773cd6c037da1f8992ad5/SEntFiN.csv) | 1,118,162 | `570af7ba58f724f3fcc414dd5ba80da5b1a3b342134d76c6ebdf53a32c54a92f` |
| Entity name table | [entity_list_comprehensive.csv](https://raw.githubusercontent.com/pyRis/SEntFiN/eba43610fe3cb57a3e5773cd6c037da1f8992ad5/entity_list_comprehensive.csv) | 90,424 | `6ace045edc54c90bc0695ee5a78afec9f7a5294844ccfd0c9e85a14aeea4916b` |
| License | [LICENSE](https://raw.githubusercontent.com/pyRis/SEntFiN/eba43610fe3cb57a3e5773cd6c037da1f8992ad5/LICENSE) | 1,110 | `961d32986ac3fa2fe2e55ebc7bbae1ba8d632412e98493d73bdf59f0ad8fc65f` |
| Introduction | [README.md](https://raw.githubusercontent.com/pyRis/SEntFiN/eba43610fe3cb57a3e5773cd6c037da1f8992ad5/README.md) | 48 | `543e1779ccb4e13b23107b3c4443891f581041d56adf676daa8db173c730e03a` |

An independent local read gave: the CSV fields are `S No., Title, Decisions, Words`; there are 10,753 rows in total, 10,686 completely distinct news texts, and 67 rows of duplicate text. `Decisions` is a Python-style dict string mapping entities to `positive/negative/neutral`; 13 rows do not conform to Python literal syntax because of unescaped apostrophes in entity names. These rows are isolated from the review sampling pool, but their news texts are still added to the exclusion pool; the remaining rows yield 14,371 target labels. No dates were fabricated, and entity names were not guessed as stock symbols. The source CSV provides no reliable per-row dates or verified security identifiers.

## Preparation done

Added `scripts/prepare_sentfin_review.py`, which depends only on the Python standard library. Download mode accepts at most four pinned files totalling 1,209,744 bytes, each checked against its pinned size and SHA256; an existing review output directory is not overwritten. To run:

```bash
python scripts/prepare_sentfin_review.py \
  --source-dir data/raw/candidates/sentfin \
  --output data/raw/sentfin_review_v1 --download
```

In this round the original files were downloaded locally and the script was run; the files are in the Git-ignored `data/raw/` and do not enter the public repository.

Outputs:

- `review_200.csv`: UTF-8 BOM; 200 distinct news texts, original negative/neutral/positive 67/67/66, of which 85 are multi-entity news items. Stratified by original label, seed=130; it cannot be treated as a simple random sample of the population.
- `task_exclusions.jsonl`: 10,686 completely distinct texts, keeping the attribution to the source IDs of all 10,753 rows, including unsampled and syntactically anomalous rows. This file is used to exclude tokenizer/pretraining leakage, independently of whether this project's labels have been obtained.
- `manifest.json`: source version, hashes, counts, isolated rows, sample counts and output checksums.
- `SOURCE_LICENSE.txt`, `review_instructions.md`: the original copyright license and the review rules.

The review table contains `id,text,source_entity,source_sentiment,source_entity_count,source_entities,entity_is_literal_substring,proposed_stance,asset_identifier,human_stance,human_reviewed,notes`. `proposed_stance`, `asset_identifier` and `human_stance` are all empty, and `human_reviewed` is false everywhere; no human-confirmed or automatically guessed asset stance labels were produced.

A human should first confirm the target asset and then judge bullish/bearish/neutral by this project's rules, or record exclude with a reason. Regulators, unclear targets, sarcasm and cases of unclear attribution cannot be forced into neutral. When the text only reports past rises or falls, an investment stance cannot be produced automatically just because the original source label is positive/negative. The first 200 rows are for identifying problems with the label convention and the asset mapping before expanding; they are not enough to claim that financial performance has been validated. If there is only one reviewer, report single-person review truthfully.

Dedicated tests verify the isolation of all candidate texts, the retention of the texts of anomalous rows, the absence of fabricated human labels, reproducible sampling output, no overwriting of old review files, and rejection of import when the source hash changes: `tests/test_sentfin_review.py`, locally **3 passed**.

## Why the other sources did not go directly into formal training

| Source | Primary evidence checked | Handling in this round |
|---|---|---|
| SemEval 2017 Task 5 | The [official data page](https://alt.qcri.org/semeval2017/task5/index.php?id=data-and-tools) requires filling in a data release agreement before download; the gold standard needs a separate form request. The [original task paper](https://aclanthology.org/S17-2089/) does evaluate by company/stock from -1 bearish to +1 bullish. | The closest definition, but in this round there is no evidence of a completed source agreement; not downloaded, not signed on anyone's behalf, not circumvented through mirrors. |
| FiQA 2018 Task 1 | The [official home page](https://sites.google.com/view/fiqa/home) gives the `sentence/info/target/sentiment_score/aspects` format with scores from -1 to 1; the Train/Test Data sections each state non-commercial use. | Has a non-commercial research note and a target field, but fetching from the original links failed; mirror license labels are not treated as stronger evidence of the original rights. |
| Financial PhraseBank | The [original release page uploaded by Pekka Malo](https://www.researchgate.net/publication/251231364_FinancialPhraseBank-v10) confirms the source authors and the archive. The original download link could not be obtained in this round; common mirrors label it CC BY-NC-SA 3.0. | Not imported on the basis of mirror licenses alone. Even if obtained, entities and asset mappings would need to be added; the original format is sentence/sentiment. |
| zeroshot/twitter-financial-news-sentiment | The [publisher's data card](https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment) marks MIT and says the data come from the Twitter API; the data fields are only text/label; the card's statements differ from the counts on the page. | Not downloaded. It lacks a specified target field; the publisher's MIT label cannot remove the issue of the upstream X usage conditions. |

The official FiQA Task 1 training link is [Drive file 1icRTdnu8UcWyDIXtzpsYc2Hm6ACHT-Ch](https://drive.google.com/open?id=1icRTdnu8UcWyDIXtzpsYc2Hm6ACHT-Ch), which returned 404 on a direct request in this round; the test link is [Drive file 1t3E2D7sBD3rG-OHNkvu2Fk7tbMzrMws0](https://drive.google.com/open?id=1t3E2D7sBD3rG-OHNkvu2Fk7tbMzrMws0). Only the official links were confirmed; there is no claim that the content was obtained or the counts determined. The question-answering corpus of FiQA Task 2 cannot be used as Task 1 stance data.

The current [X Developer Agreement, 2026-04-27 version, III.A(k)](https://docs.x.com/developer-terms/agreement) restricts training or fine-tuning foundation/frontier models; the [Developer Policy's Content redistribution section](https://docs.x.com/developer-terms/policy) also restricts redistribution of third-party data. This fact is enough to support this project's choice not to treat API-sourced mirrors by default as checked training permission; no comprehensive judgment is made here about arbitrary older datasets or legal exceptions. This round did not crawl or re-fetch any X posts.

## Stage decision

Q1 (source conditions): the SEntFiN authors' repository has an explicit MIT release license and attribution, and the pinned small files have been obtained. Q2 (targets and labels): there is entity-related human sentiment, but this project's asset mapping and investment-stance semantics still await human review. Q3 (quantity): the candidate pool is large enough to start a 200-row check of the label convention, but the actual number of usable asset stance samples is unknown. **Pretraining corpus preparation can continue; formal label acceptance for SFT/DPO is not complete.**
