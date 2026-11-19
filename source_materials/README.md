# Source Materials

Material from the earlier project that the Stage A reports and recomputations refer to. Virtual
environments, account settings and unrelated personal files were not copied.

**`130U-FinLLM/`** is a snapshot of the author's earlier financial language-model project,
[130U/RESEARCH-Financial-Large-Language-Model](https://github.com/130U/RESEARCH-Financial-Large-Language-Model),
as used for the claims audit, together with locally saved source data and supplementary files. It is
a source snapshot, not a full Git history. Every original text listed in
[`research/claims_sources.json`](../research/claims_sources.json) was checked byte for byte against it
in the original language.

**`source_audit/`** holds the local versions actually read by the historical FOMC and rights review,
because four documents differ from the claims-audit version. It contains the 120 FOMC minutes as
JSONL, the 120 matching HTML pages, 12 index snapshots, a manifest, and eight rights and semantic
evidence files that match `research/data/source_audit.json` exactly. Keeping both lets each historical
audit be checked without overwriting older evidence with newer versions.

**SEntFiN.** The raw CSV, entity list, README, candidate manifest and the original authors' MIT
licence are in `130U-FinLLM/data/raw/candidates/sentfin/`
([licence](130U-FinLLM/data/raw/candidates/sentfin/LICENSE)). Derived entity rows, lexical families,
fixed splits and per-row predictions are in [`research/private/real_baseline/`](../research/private/real_baseline/).

**FOMC records** state the Federal Reserve Board as the source, the retrieval time and the rights
notes. Pages saved in 2026 do not prove that the same bytes were available in earlier years; the
original study's limits on point-in-time claims still apply. The old manifest also lists corpora that
the experiments here did not use; listing them is not a claim that they are included.

Source code and source data keep their existing licences. No new common licence is declared for
third-party content. Recomputation commands are in the [root instructions](../REPRODUCE.md).
