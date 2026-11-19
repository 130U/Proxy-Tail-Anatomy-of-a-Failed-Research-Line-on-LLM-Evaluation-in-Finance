# T1f: Novelty check: has anyone done the five candidate insights

Branch `task/t1f`, directory `research/t1f_novelty/`. Needs internet searches. This is currently the most important task and is worth taking the time to do thoroughly.

## Background, from the start

The project is auditing the financial QA benchmark FinQA (Chen et al., EMNLP 2021). The goal is a short paper at a top conference. The full exploration map is on the repository homepage [README](../archive/README-before-closeout.md), and the short-paper draft is at [`paper/finqa_short_v0.md`](../archive/finqa_short_paper_draft_v0.md); read these two files first.

The homepage uses colours to show research value:

- 🟢 Can become a paper: **the novelty check confirms that no one has done it**, and the evidence is complete. A single 🟢 is enough for the paper to stand.
- 🟡 A candidate worth exploring: so far this only means "the advisor found nothing".
- ⚪ No longer a focus: others already hold a similar view.

All five are currently 🟡. **This round decides which way each one goes.** Finding that someone has done the same thing, and downgrading it to ⚪, is as valuable as confirming that no one has. Do not describe related work as further from ours than it is in order to keep a candidate alive.

## The five items to check

Under each item are the similar views the advisor already knows of. They are only a starting point; most of the sources are at the level of abstracts or memory, and **all of them need you to read the original and verify**, and to keep searching further out.

### 🟡1 Rounding precision cannot determine the answer: a law and an exact count

**Our claim.** Filing figures are rounded. Treating each input as the interval "displayed value ± half a last-digit unit" and computing the exact range of the gold solution, for at least 10.7% of FinQA test questions (40% of growth-rate questions) the answer cannot be determined to 1%. A rule predicts this in advance: two figures must differ by about 100 last-digit units for the growth rate to be exact to 1%; with no fitted parameters, it agrees completely with the exact classification on 5,337 questions.

**Known similar views.**

- In numerical analysis, "subtracting nearby numbers loses significant digits"; textbook material.
- Gittings (1991, Chicago Fed *Economic Perspectives*): distortion of economic growth rates by rounding.
- The XBRL Calculations 1.1 specification: rounding intervals and interval arithmetic.
- Community debate about the FinQA scoring tolerance (1% relative error or the displayed number of digits), for example the pull request on EnvCommons/FinQA.
- FinanceReasoning (ACL 2025) mentions that models struggle with numerical precision.

**What counts as "already done".** Work that, on FinQA, TAT-QA, ConvFinQA or a similar benchmark, has counted the determinacy of answers by the rounding precision or condition number of the inputs; or that has applied the rule above to financial statement analysis and tested it on data.

### 🟡2 Redundant information in the document cannot rescue them

**Our claim.** Adding duplicate disclosures of the same quantity elsewhere in the document and sum relations within tables as constraints, and solving exactly with rational linear programming, only 1 of the 196 questions becomes determined again.

**Known similar views.** The XBRL specification has intersection of duplicate facts and calculation consistency checks. The advisor does not know the accounting-research work that uses reconciliation relations to recover pre-rounding values; check this closely.

**What counts as "already done".** Work that uses accounting identities or duplicate disclosures to tighten the range of quantities computed from rounded figures, and reports the effect of the tightening.

### 🟡3 The model knows the precision but does not use it unprompted

**Our claim.** Unprompted, the number of significant digits the model prints is unrelated to the number of truly reliable digits of the answer (rank correlation 0.02). With just a one-sentence reminder that "the figures are rounded", 98.4% of answers give the correct answer interval. The ground truth is the exact range of the model's own expression.

**Known similar views.**

- There is a lot of research on uncertainty expression, calibration and verbal confidence in language models, but the object is "the probability of being right", not the precision of a number.
- Evaluations of language models' numerical ability, significant digits and unit handling.
- Evaluations of significant-figure rules in scientific QA; the advisor has no specific references, so search for them.

**What counts as "already done".** Work that uses exactly computable intervals as ground truth and measures language models' ability to report numerical precision, significant digits or error ranges; or that reports a difference of the "does not say it unless asked, gets it right when asked" kind.

### 🟡4 The rejections fall on the same questions

**Our claim.** Two models, three prompts, four runs: official accuracy is always 81%–83%. Of 392 questions, 63 are wrong in all four runs, 316 right in all four, and only 13 inconsistent. Two independent reviews attribute 55 of the 68 rejections to the benchmark side (32 reference errors, 23 convention ambiguities) and 0 to a definite model error. The largest class of convention ambiguity is the sign of a "decrease".

**Known similar views. This item is the one others have said the most about.**

- FinanceReasoning (ACL 2025): re-audited and revised 15.6% of the questions in four public financial numerical-reasoning datasets, with revision rates from 9.72% to 30% per dataset, and pointed out that strong models are close to saturating the old benchmarks. Read the full text and find out whether the four datasets include the original FinQA test set, what error types were revised, and whether there is a per-question cross-model analysis.
- Northcutt et al. (2021): label errors are pervasive in ten commonly used test sets.
- Benchmark-cleaning work such as "Are We Done with MMLU?" (MMLU-Redux) and Platinum Benchmarks.
- DocMath-Eval, BizBench and FinanceMath filtered or relabelled FinQA-derived data when they were built.
- The original FinQA paper reports expert accuracy of about 91%, which in itself implies a ceiling.

**What counts as "already done".** Work that has done a per-question cross-model overlap analysis of rejections on the original FinQA test set; or that has given an attribution classification and proportions for FinQA rejections; or that has stated explicitly, with evidence, that "the remaining errors of current models on FinQA come mainly from the benchmark".

### 🟡5 The two gold fields contradict each other

**Our claim.** Each FinQA question has a human-written `answer` and a program-executed value `exe_ans`. Comparing at the displayed precision of `answer` itself, and allowing a difference of a percent sign, 508 of the 7,952 parseable questions among the 8,281 (6.4%) contradict each other, and a further 1.0% differ only in sign. Official scoring uses `exe_ans`.

**Known similar views.** The advisor found none. But the check takes a few lines of code, so there is a fair chance someone has done it. Check FinQA's GitHub issues, the data-cleaning notes of later datasets, and the appendices of papers that use FinQA.

**What counts as "already done".** Work or public discussion that has reported the inconsistency rate of these two fields, or has filtered data on that basis.

## Method

1. Use at least 10 different sets of search terms for each item, trying both Chinese and English. Cover the ACL Anthology, arXiv, Semantic Scholar, Google Scholar and GitHub issues. **Record every search term.**
2. Follow the citation chains: among the works citing FinQA, TAT-QA and ConvFinQA, those from 2023 onward that do evaluation analysis, data cleaning or error analysis.
3. For relevant work, read the full text and appendices, not just the abstract. For each paper read, record one line: title, year, link, which sections were read, and which item it relates to.
4. Verify every entry under "known similar views" above: is the source correct, and what exactly does it say. Point out directly where the advisor misremembered.

## Deliverables

**A one-page summary**, opening with this table:

| ID | Conclusion | Suggested colour | Closest work (title, year, link) | What they did | What we add | Confidence |
|---|---|---|---|---|---|---|

- "Conclusion" is one of three: someone has already done the same thing / partly done / still not found after reading the full text.
- "Suggested colour": already done → ⚪; partly done → 🟡, and state clearly whether the remaining novelty is enough to support a paper; still not found → may be upgraded to 🟢 (whether the evidence is complete is judged separately by the advisor).
- "Confidence": high / medium / low, with a note on what has not yet been found.

**Attachments:**

- The three closest works for each item, each with a one-paragraph excerpt from the original, with page or section.
- All search terms.
- The list of references whose full text was read.
- The results of verifying each entry under "known similar views".

## Watch out for

- Mark the source level of every fact: full text / abstract / secondhand.
- Check only, change nothing: do not change the README, and do not change the short-paper draft. The advisor changes the colours once the conclusions come back.
- When you find work that overlaps heavily with one of the items, write a paragraph and send it back first; there is no need to wait until everything has been checked.
