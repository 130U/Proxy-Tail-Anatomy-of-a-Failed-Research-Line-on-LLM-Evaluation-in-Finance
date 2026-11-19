# Fable complete research handoff package: start here

> Everything below this note is the historical entry point for the earlier nine-round research package. The current direction is "what does a cheap model miss in the tail". For the latest measurements, mathematical corrections and the complete deliverable, start from the [current report](tail_screening/FABLE_CURRENT_REPORT.md); the old package does not contain the later agent experiments.

Delivery date: 2026-11-16 (America/New_York). Project: 130U-FinLLM / Certifiable FinLM. Recipient: Fable, forwarded by Theodore. Scope: all existing research output through round 9, plus a reference snapshot of the original advisor materials that the user provided. This step only summarizes and packages. It adds no new experiments, literature searches or research conclusions, and nothing was sent externally.

## The fastest way to read this

1. **Read the [full research report](FABLE_FULL_REPORT.md) first.** It integrates the research motivation, the five paths, all core theory, real and constructed experiments, negative results, review disputes and the items awaiting a decision. You do not need to trace the nine rounds of messages to understand the conclusions.
2. When choosing a direction, read the [five-path comparison](paths/COMPARATIVE_ANALYSIS.md) and the [review request for Fable](paths/SENIOR_REVIEW_REQUEST.md), then open the full text of the relevant path.
3. For item-by-item review, read the [complete merged reading edition](https://github.com/130U/RESEARCH-Proxy-Tail-Anatomy-of-a-Failed-Research-Line-on-LLM-Evaluation-in-Finance/blob/closeout-2026-11-17/research/FABLE_REVIEW_BUNDLE.md). It merges all Markdown full text in this package, keeps the source headings, the content in its original order and the evidence links. The newest material comes first, followed by historical records and background material.
4. When you need to check formulas, numbers or reproduction, use the [file-by-file index](INDEX.md), the [reproduction notes](REPRODUCE.md), and the standalone source code/JSON/TeX/PDF inside the ZIP. The merged edition does not replace the machine-readable results or the source code.

The file to forward directly is **[FABLE_HANDOFF_COMPLETE_2026-11-16.zip](https://github.com/130U/RESEARCH-Proxy-Tail-Anatomy-of-a-Failed-Research-Line-on-LLM-Evaluation-in-Finance/blob/closeout-2026-11-17/research/FABLE_HANDOFF_COMPLETE_2026-11-16.zip)**. After unzipping, keep the relative paths with `research/` as the root; this page is at `research/START_HERE.md`. If only text upload is convenient, provide the full report and the complete merged reading edition first. The ZIP itself is not nested inside the unzipped directory; the ZIP link above is the download entry point at the original local delivery location.

## What this "complete edition" contains

| Content | Entry point and scope |
|---|---|
| Integrated full report | [FABLE_FULL_REPORT.md](FABLE_FULL_REPORT.md), new in this delivery |
| Five feasible paths | [Comparison and Top 3](paths/COMPARATIVE_ANALYSIS.md); 01 information set, 02 numeric sensitivity, 03 audit frontier, 04 dependence risk, 05 verifiable numeric reasoning; all five full texts are in `paths/` |
| Literature research | [17-entry evidence ledger](literature/literature_review.md), [32-question coverage matrix](literature/question_status.md), 7 focused answers in `answers/`, precedent and gap review |
| All mathematical derivations | `theory/`: foundations T0–T3, collective statistics, impact audit, historical non-interference, semantic envelopes, localization value and randomized-audit optimality; the corresponding assumptions, proofs and counterexamples are kept |
| All research rounds | Round 1–9 reports in `reports/`; the process by which conclusions were corrected by stronger controls is kept, and old narratives are not overwritten |
| Experiment and execution evidence | Complete tables, JSON, budgets, configs, source code and actual logs in `experiments/`, `planning/`, `pit/`, `numeric/`, `checks/` and elsewhere, including negative results and records of write failures |
| Peer-style internal review | Adversarial opinions on the paths, point-by-point responses, independent math/statistics/code/paper reviews and check scripts; all are labeled as internal AI |
| Technical manuscript | `paper/manuscript.md`, `.tex` and the [reading PDF](paper/output/pdf/audit_budgets_working_report.pdf); these are the round 7 draft and must be read together with the round 8/9 supplements |
| Reproduction and integrity | [REPRODUCE.md](REPRODUCE.md), the [actual reproduction log](reproduction_log.json), the [SHA256 manifest](https://github.com/130U/RESEARCH-Proxy-Tail-Anatomy-of-a-Failed-Research-Line-on-LLM-Evaluation-in-Finance/blob/closeout-2026-11-17/research/HANDOFF_MANIFEST.json), the packaging script |
| Original advisor materials | [Reference snapshot notes](advisor_reference/ORIGIN.md); the 11 original files provided by the user are saved verbatim, with source hashes; the ideas in them are not treated as proven conclusions |

## Research status you must know first

What is complete in this package is **the research material to date**. It does not mean that a complete certifiable financial language model has been built, and it does not mean that literature novelty or G0/G1 has passed.

- The five path reports form four research families: 03 is a mathematical branch of 01, and 02 and 05 share semantic risk. The number of files does not support a claim of five independent flagships.
- None of the 32 questions meets the systematic-review standard of all sub-questions completed: 12 have partial evidence and 20 are incomplete. The 17 ledger entries come from different source tiers and cannot all be treated as close full-text readings.
- The real SEntFiN baseline, hand-constructed checks, analytic proofs and research suggestions are labeled separately. Non-empty intervals from constructed examples are not described as certification of real historical sources.
- The round 9 proof gives optimality only under an explicit homogeneous threat family and an all-zero must-issue-a-certificate contract. A simple strategy already attains the lower bound; this is not evidence that a complex model is necessary or that the work is original.
- Fable has not yet received this package and has not given feedback on this round. Internal AI review cannot replace Fable's judgment.

## Which files are excluded, and why

This package keeps all deliverable research full text, proofs, code, aggregate results and review evidence. Following the existing data boundary, it does not include private raw headlines, row-level labels/predictions, vocabularies, model weights, checkpoints, run caches, environment directories or old ZIP copies; these are not omitted research conclusions. The source hashes, code, aggregate scores and limitations of the real-data experiments are kept; rerunning the real experiments still requires the corresponding local raw data. There is no promise that the ZIP alone can rebuild the missing old 24M predictions or independently rerun all real experiments.

The 11 original advisor files are attached to the local package as background material. This does not authorize public release of their content. The mentions in those files of internet access, SEC contact information, next-round training and so on are historical plans; this request was only to deliver existing research, and none of those actions were carried out.

## A note that can be forwarded to Fable as is

> Fable, this is the complete delivery of all research so far. Please read FABLE_FULL_REPORT first, then the five-path comparison and the review request. We hope you will judge each path as "continue, narrow, keep only as a supporting component, or stop", and attack these first: whether the existing narrow theorems are only direct corollaries of existing theory; whether there is a real task that simple baselines cannot solve; and how to handle the original "must train from scratch" filter and the missing G0 materials. Please state one falsifiable next step, and do not treat more constructions, passing tests or engineering scale as evidence of originality.

File integrity is governed by `HANDOFF_MANIFEST.json`: the manifest records the size and SHA256 of every archived payload, and also records the list of documents included in the merged reading edition. The generated manifest does not compute its own hash; the ZIP checksum is given separately at delivery time.
