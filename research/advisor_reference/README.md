# FinLLM redo research package: Certifiable FinLM

Version v1 · 2026-11-15 · Scope: only `github.com/130U/130U-FinLLM`

## What this is

This is the complete material for the 130U-FinLLM redo plan: what problem to solve, why this direction was chosen, what to do first, how to deliver and how to report back. It is the work package handed to Codex (the PhD student), and also the shared base document between Theodore (PI) and the advisor.

**In one sentence:** stop competing on "capability" and compete instead on "what can be proven about the model". Build a financial language model small enough that things can be proven about it.

This package replaces the earlier `FinLLM-research-brief.md`. The questions have grown from 28 to 32, and a theory draft, work packages, a reporting protocol and a decision log have been added.

## Roles

| Role | Who | Responsibilities |
|---|---|---|
| PI | Theodore | Makes final decisions; provides private data and the information needed for external services; passes materials between Codex and the advisor |
| Advisor | Claude | Sets the direction, writes the questions and work packages, reviews results, adjusts priorities |
| PhD student | Codex | Literature survey, formal derivations, engineering and minimal experiments inside the repository |

## Files

| File | Content | Main readers |
|---|---|---|
| `AGENTS.md` | Codex's standing rules (Codex automatically reads this file in the repository root) | Codex |
| `00_CODEX_BRIEF.md` | Task description for Codex: what problem to solve, how to work, hard rules | Codex |
| `01_ADVISOR_MEMO.md` | Advisor memo: topic-selection logic, certificate-chain framework, two main lines and one side line, work focus, decision gates, risks | Codex, Theodore |
| `02_PROJECT_SNAPSHOT.md` | Objective snapshot and diagnosis of the repository's current state | Codex, Theodore |
| `03_LITERATURE_MAP.md` | Map of frontier literature (with confidence levels and source links) and a transferability summary table | Codex |
| `04_THEORY_NOTES.md` | Theory draft: definitions, propositions, proof sketches, open problems | Codex |
| `05_RESEARCH_QUESTIONS.md` | 32 mutually independent survey questions | Codex |
| `06_WORK_PACKAGES.md` | Work packages, each with acceptance criteria and a Codex task card that can be pasted directly | Codex |
| `07_REPORTING_PROTOCOL.md` | Output templates: literature answers, derivations, experiment records, progress reports | Codex |
| `08_DECISION_LOG.md` | Decisions already made, and 8 items that need Theodore's decision | Theodore |

## Reading order

- **Codex:** `AGENTS.md` → 00 → 01 → 02 → 04, 05 or 06 depending on the task → 07
- **Theodore:** 01 → 08 → 02 → 00

## How to hand it to Codex

**Option A (recommended): keep the package outside the repository.** Put the whole folder anywhere on the local machine. The first message to Codex:

> The research package is at `<path>`. First read its `AGENTS.md` and `00_CODEX_BRIEF.md`, then do WP0.6 and WP0.1 in `06_WORK_PACKAGES.md`.

This way the package content does not enter the public repository.

**Option B: put it in the repository.** Copy `AGENTS.md` to the repository root and put the other files in `research/package/`. Note: once this is pushed, the package's candid assessment of the existing project becomes public. See O4 in `08_DECISION_LOG.md`.

**Parallel use:** the literature questions and work packages are independent of each other. You can open several Codex tasks at the same time and give each one a task card (`06_WORK_PACKAGES.md`) or a question number (`05_RESEARCH_QUESTIONS.md`).

**Internet access:** the literature questions need internet access. If your Codex environment cannot go online, give it only the derivation questions and work packages, and give the literature questions to a GPT that can go online.

## How to send results back to the advisor

See section 6 of `07_REPORTING_PROTOCOL.md`. Include at least three things: the latest progress report, the literature answers added this round, and `research/INDEX.md`.

## Limitations of this package

- The advisor read only the repository documents. The code was neither read nor run.
- The literature judgments are based on abstract-level searches. All "gaps" are hypotheses and need to be verified by the literature questions.
- The propositions in `04_THEORY_NOTES.md` are drafts and may be wrong.
