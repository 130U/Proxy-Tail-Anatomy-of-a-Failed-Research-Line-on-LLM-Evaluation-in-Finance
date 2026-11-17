# Analysis and peer-review agreement for the five candidate paths

Date: 2026-11-15. The task comes from the user's latest request: analyze in depth at least three to five feasible paths, write an analysis report for each, and hand the open questions to the designated senior assistant for discussion.

## Charter

The goal is to support the decision on the next research investment: for each of the five candidates, give an explicit mathematical question, the strongest existing alternative, a testable increment, where the evidence is insufficient, a minimal validation, and rejection conditions; keep an independent adversarial review and the authors' responses. The goal is not to claim that all five candidates hold, and still less to split one main line into five "innovations".

The scope is certifiable financial language models and the statistical decision theory directly related to them. The objects are information sets, numeric sensitivity, audit design, deployment risk, and text-based numeric tasks with checkable computation traces. The concrete unit of each report is one target quantity, one candidate proposition, one set of necessary assumptions, and one experiment that can end the investment. The research type is an exploratory comparison; working-level knowledge of the project is in hand, but there is not yet a complete novelty conclusion, a real historical information certificate, or a final flagship.

Questions: R1 Which path can produce a mathematical increment that is not a renaming of existing techniques? R2 Can the weakest link of the certificate be verified locally? R3 Are training from scratch and language understanding each necessary? R4 Can simple symbolic/statistical/frozen-encoder baselines solve the same problem? R5 What negative result is enough to make us stop? R6 Which specific dispute needs the senior assistant's judgment?

## Canonical sources

1. Original papers actually opened, each marked with its version and whether the full text or only the abstract was read; see `../literature/literature_review.md`. Keep the existing search boundary, and do not infer the absence of precedents from new keywords.
2. Fixed source code, mathematical proofs, JSON from actual runs, and test logs; mathematical inputs and real training results are labelled separately.
3. Hashes, sources, times, and license metadata of the local raw files; see `../reports/local_data_inventory.md`. File existence and hash matches are actual checks; historical times and license statements keep the evidence level of their sources.
4. The advisor package is a source of research hypotheses and decision rules; its authority is not treated as proof.

The current boundary of no new external access is kept. On 2026-11-16 the user stated that the senior assistant referred to is Fable and allowed discussion with Fable; the current tools have no direct connection to Fable, so the material was prepared for forwarding. Reviews by internal AI sub-agents and Fable's actual feedback are recorded separately; there is no claim that Fable's comments have been received.

## Evaluation rules (written down before forming the final ranking)

Use qualitative, tiered judgments in the advisor's order, without producing a falsely precise weighted total score:

1. **Novelty and attributable contribution**: existing theorems must not be counted as increments; insufficient search is recorded as unknown.
2. **Non-vacuity and testability**: an explicit target quantity, real premises, and a minimum useful threshold. Small hand-made examples only show possibility.
3. **Execution feasibility**: whether the data can legally be used locally, whether annotation/audit is doable, and whether the CPU/T4 budget is measured or only estimated.
4. **Fit with research style**: whether the work centers on definitions, proofs, executable bounds, and necessary experiments.

The following are separate hard questions that cannot be hidden by an average score: no reliable target quantity; key premises that cannot be verified, with their conditional nature not acknowledged; a simple baseline already solves the problem completely with no theoretical difference; the necessity of training from scratch does not hold, yet it is still used as the core contribution. If "must train from scratch" is kept as a literal hard gate, the report should state directly which paths cannot be selected.

Candidate IDs are not final ranks: 01 complete information-set certificate, 02 numeric sensitivity, 03 audit-cost frontier, 04 dependence-robust deployment risk, 05 numeric text reasoning with computation evidence. 03 is a mathematical branch of 01; 02 and 05 share the parsing bottleneck, so the two cannot be treated as fully independent risk diversification.

## Findings ledger

The factual evidence in this round reuses the following existing ledgers, so that repeated writing is not counted as new evidence: the L01–L17 literature ledger; the C01–C46 repository audit; the T0–T3 theory; the CM1–CM5 proofs for collective statistics; the JSON for local_foundations, collective_metrics, and planning; the local corpus inventory. Each report cites the corresponding files and IDs. New candidate theorems, budgets, and experiment thresholds must be marked as proposals/estimates and not mixed with these executed results.

## Scope filter

Exclude inferences such as "renaming something as a financial application is innovation", "a small model is a contribution in itself", and "a perfect score on a synthetic task proves the method works". Risk reports, numeric computation tools, and language-model research are different objects, and each needs its own explanation of why it belongs in this project.

## Object filter

Check applicability against the current local material: FOMC can support retraining or preparation for extracting numeric paragraphs, but does not automatically support certification of historical content versions; SEntFiN sentiment does not automatically equal author stance; without XBRL gold labels, one cannot claim complete parsing supervision exists. The missing predictions of the old model cannot be used to deny that the local raw corpus exists.

## Conclusions

No winner is pre-filled here. After the independent analysis of each path is complete, a reviewer who did not write these reports attacks the assumptions, necessity, simple baselines, and extrapolation of evidence; the authors' responses are recorded; and then the comparison report is written. The senior assistant's actual comments are listed separately; if none have been received, this is stated explicitly as awaiting feedback.

## Next steps / Risks

Five reports → independent adversarial review → item-by-item responses/revisions → comparative ranking and the question package for Fable. The internal analysis is complete; Fable's real feedback still has to be obtained after forwarding. The core risks are that the candidates share the same unresolved premise, that literature coverage is insufficient, and that parts of the original plan that need revision are quietly treated as passed.

## Method and contributing sources

This round used the local skills "Academic research - topic selection and adversarial discussion" and "Academic research - organizing adversarial research review", for independent analysis, explicit rejection conditions, keeping dissent, and review responses. Three internal AI sub-agents each wrote candidates, and a new independent reviewer received only the material under review; these are not human peer review, and they are not Fable's opinion. The candidates come from the advisor's plan and this round's breakdown of the problem, and the authors had seen the earlier material, so topic selection was not fully blind; the independent ranking and adversarial review are meant to reduce this anchoring effect.

The skill sources are pinned to K-Dense-AI/scientific-agent-skills at `154988403bb5a18e9d3c0ce4e6d5e2e4b184a298` and K-Dense-AI/science-superpowers at `0374bdf82c2372bdf1667e3c762146c3a29215f5`. The former's local SKILL.md suggests citing Kassis et al. (2026), *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*, arXiv:2609.00065. This bibliographic information comes from the skill metadata and was not separately verified online in this round; it is disclosed only as the source of the process and is not used as academic support for any research path.
