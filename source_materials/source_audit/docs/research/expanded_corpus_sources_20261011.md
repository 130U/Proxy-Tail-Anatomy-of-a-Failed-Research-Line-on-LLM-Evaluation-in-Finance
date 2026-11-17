# Expanded corpus: source verification and acquisition contract

Verification date: 2026-10-11. This follows the completed 300-step training of `seed_v1`. This file records only the sources, acquisition limits and verification of the new candidate corpora; it does not prove that any new Colab training has been completed.

## Sources and selection

This round continues with the two sources already reviewed in the first round: a pinned English Wikipedia snapshot and original FOMC minutes from the Federal Reserve Board. A longer, limited Wikipedia prefix is added, and the FOMC meetings are extended to 2011–2025. The source order is fixed; a convenience subset is not described as a random or representative sample.

| Source | Primary evidence | Execution contract for this round |
|---|---|---|
| `wikimedia/wikipedia` | [Pinned data card](https://huggingface.co/datasets/wikimedia/wikipedia/blob/b04c8d1ceb2f5cd4588862100d08de323dccfbaa/README.md), [pinned raw data card](https://huggingface.co/datasets/wikimedia/wikipedia/resolve/b04c8d1ceb2f5cd4588862100d08de323dccfbaa/README.md) | Pinned revision `b04c8d1ceb2f5cd4588862100d08de323dccfbaa`, config `20231101.en`, streaming iteration over `id/url/title/text` of `train`; by default the JSONL is capped at 200,000,000 bytes, at most 50,000 articles, and each article body at most 1MB. |
| Recent FOMC minutes | [Official calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) | Get the 2021–2025 meetings from the actual HTML links and save the real release dates shown on the page; do not guess minutes URLs, and do not treat the meeting date as the release date. |
| Historical FOMC minutes | [Official historical year index](https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm), [2011 page](https://www.federalreserve.gov/monetarypolicy/fomchistorical2011.htm), [2020 page](https://www.federalreserve.gov/monetarypolicy/fomchistorical2020.htm) | Get the 2011–2020 pages from year links that actually exist in the index, then read the corresponding minutes HTML links; by default at most 128 articles in total, with the finance JSONL capped at 12,000,000 bytes. |

The official current calendar covers only recent meetings; reusing that page alone is not enough to get the 2011–2020 minutes. The real 2011 minutes use the old page structure `#printThis.generalContentText` and `#leftText`; newer pages use `#article`. The new extractor checks these two structures separately; the old structure must also carry an explicit FOMC minutes title. Articles that fail the structure check are recorded as skipped; the extractor cannot fall back to scraping the whole page. [Actual 2011 minutes](https://www.federalreserve.gov/monetarypolicy/fomcminutes20110126.htm)

## Basis for reuse and attribution

On 2026-10-11 the pinned Wikipedia raw data card was read directly: HTTP 200, 130,835 bytes; the card records `cc-by-sa-3.0` and `gfdl`. Wikimedia's current terms use CC BY-SA 4.0 and allow attribution to be given through the article URL. The version difference between the two continues to be stored in each record's `license` and `rights_note`, and is not rewritten as public domain. The original article URL, snapshot revision, body hash and fetch time are all kept. [Wikimedia official Terms of Use §7](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use/en#7._Licensing_of_Content)

The Federal Reserve Board states that information on its website is in the public domain unless otherwise marked, and asks that the Board be credited as the source; non-Board material and external links do not automatically get the same permission. So this round takes only original FOMC body text from the Board website, does not follow external links, and does not take images, PDFs or other meeting materials; body text with an explicit copyright mark is skipped and the reason saved. Each record keeps the Board URL, release date, original HTML hash, body hash, extraction notes and the basis for public-domain status. [Board website notice](https://www.federalreserve.gov/disclaimer.htm)

This round did not crawl X/Twitter, paid financial articles or new commercial datasets, and did not generate bullish/bearish labels from the minutes. The style of these sources is still mostly encyclopedic and macro-policy; asset stance supervision data need a separate review.

## Memory, space and interruption recovery

The entry point is `scripts/fetch_expansion_corpora.py --output data/raw/expansion_v1/corpora`. The output contract is `general_candidate.jsonl`, `finance_candidate.jsonl` and a schema 1 `manifest.json`, compatible with the existing source snapshot verification. `status: complete` is written atomically only when both parts verify successfully; when a completed result is run again, it is only read back and verified, and files are not overwritten.

Wikipedia writes the JSONL article by article and commits a progress log with the cumulative byte count and SHA256 every 100 source rows. After an interruption, it re-iterates the fixed source up to the committed boundary, first verifies the committed prefix, discards only the uncommitted tail after that boundary, and then continues writing. This re-reads some source data but does not re-admit committed articles. A first initialization and damaged states that cannot be verified raise explicit errors; the fetcher cannot silently rebuild from an empty file.

Fed requests reuse the original `FedFetcher`: HTTPS `www.federalreserve.gov` only, serial, at most one request per second, at most 2MB per HTML response, with bounded timeouts and retries. Each page first commits an atomic cache entry containing the URL, byte count, body SHA256 and HTML, and the original HTML snapshot is then kept. After an interruption, the unfinished finance part is rebuilt from verified page caches; completed parts are not fetched again. If the parameters or the source version change, a new expansion version must be chosen, and the old output is kept.

Streaming iteration does not require downloading the full English Wikipedia or turning it into an in-memory list, but Parquet decoding and network reads still buffer, so it cannot be called zero-memory. [Hugging Face Datasets official streaming documentation](https://huggingface.co/docs/datasets/stream)

The default 200MB + 12MB are caps on the candidate JSONL, not token counts, and they do not include all caches, cleaned text and checkpoints. Formal outputs also need to keep the HTML, recovery caches, cleaning results and `uint16` token files; the latter have a net payload of 2 bytes per token. Actual space use and token counts are recorded after the build; there is no promise that these sources alone reach 100M general or 25M independent financial tokens.

## Conditions before training

- Keep the original `seed_v1` tokenizer unchanged; the new candidate set cannot retrain or replace the vocabulary.
- Exclude the original seed's train and validation document identities, text duplicates / near-duplicates, and the frozen task evaluation texts; enlarging the Wikipedia prefix cannot by itself be counted as a number of entirely new documents.
- Split the new data into train/dev by document, keep the original validation set for comparable evaluation, and report the new independent documents and the actual tokenizer token counts separately.
- When carrying over weights, record the hash of the original 300-step checkpoint and the provenance of the new corpus. New data cannot pose as an exact optimizer/cursor continuation of the same data stream; later resumes must verify the new stage's own run contract.

## Verification record

The offline test `tests/test_expansion_sources.py` passed 11 tests, covering: read-only reuse of completed results; Wikipedia recovery from the committed prefix, handling of an uncommitted tail and rejection of a damaged prefix; an interruption between the completion marker and the atomic rename; the whitelist of real links and release dates; old-structure extraction / exclusion by copyright mark; finance cache recovery and rejection of damage; rejection of changed parameters; rejection of modified original HTML snapshots.

On 2026-10-11 a small real network verification was run: general cap 1MB and at most 30 articles; finance years 2011 and 2025, at most 2 articles, 200KB cap. Finance took the first two articles by date and actually got two old-structure examples from 2011. All candidate files stay in the Git-ignored local directory `data/raw/expansion_network_probe_20261011/corpora`; no text was uploaded.

| Small-scale candidate | Actual articles | Actual bytes | SHA256 |
|---|---:|---:|---|
| General English | 28 | 980,278 | `0dc2e5955a33057ef735e99cdea8dcfebc19c2746f4102d3a0e1a9312fb270e6` |
| FOMC financial English | 2 | 116,347 | `ecbc426ab4bbfec62f1ba03efe9bfde3e51037276406868216ee9bae8658516d` |

The small-scale directory, including recovery caches, totals 2,262,672 bytes. There were no finance skips; the manifest is `complete`. Re-running with exactly the same parameters returns `reused: true`. This only verifies acquisition, parsing and reuse; it does not claim formal corpus scale, training throughput or model performance. The actual statistics of the default limited download and preparation should be recorded in the stage report.

## Actual results of the default limited download

On 2026-10-11 acquisition was run with the default 200MB Wikipedia cap and the 2011–2025 FOMC sources. The manifest completed at `2026-10-11T10:42:25.249898+00:00`; the local files are in `data/raw/expansion_v1/corpora`, and no text was committed to Git.

| Default candidate | Actual articles | Actual bytes | SHA256 |
|---|---:|---:|---|
| General English | 28,486 | 199,996,572 | `5b2b8def467868f177afd438c27ba4254fe41d746a5bbabb4bbbf3046769d547` |
| FOMC financial English | 120 | 6,977,681 | `5a9b357c4b979b5e85dc7622e28c5793068baeb67a48abbd218e81e7d8219a0a` |

The directory, including source HTML, recovery caches and metadata, totals 247,243,919 bytes; this is the size of the output directory, excluding external HF buffers / caches and preparation outputs, and it is not the peak memory of the process. Finance saved 12 discovery-page snapshots; all 120 articles passed the reviewed checks of the new/old body structures and of copyright marks, and `skipped` is empty.

These are source candidate counts, including overlap with the old seed, and cannot be written up as numbers of new independent documents. New document counts, partitions and tokenizer token counts are given by the later build report; this record did not start any new-stage Colab training.
