# Decision log and items awaiting the PI's decision

## Decisions already made

| ID | Date | Decision | Reason | Who decided | Reversible? |
|---|---|---|---|---|---|
| D1 | 2026-11-15 | This round works only on `130U/130U-FinLLM` | Theodore's request | Theodore | Yes |
| D2 | 2026-11-15 | Do not modify theodoreoy.com | Theodore's request | Theodore | — |
| D3 | 2026-11-15 | `130U/agent-evaluation-methodology` is left for later | Theodore's request | Theodore | Yes |
| D4 | 2026-11-15 | Assume there is no GPU; the contribution is mainly theoretical, and experiments are only minimal T4-level checks | Theodore's constraint | Theodore | Yes |
| D5 | 2026-11-15 | New positioning: a certifiable financial language model (Certifiable FinLM) | See the three filters in section 2 of 01 | Advisor's suggestion; Theodore then asked for it to be packaged in this direction for Codex | Yes, reviewed at G1 |
| D6 | 2026-11-15 | Do not chase leaderboard scores, do not do R1-style reasoning distillation, do not build candlestick / order-flow models, do not build alpha-mining agents | See section 10 of 01 | Advisor's suggestion | Yes |
| D7 | 2026-11-15 | Run feasibility on the two main lines (P1 information set, P2 sensitivity) in parallel, and choose the flagship at G1 | Both have novelty hypotheses, but neither has been verified | Advisor's suggestion | Yes |
| D8 | 2026-11-15 | Keep the old 24M Trial: move it to `legacy/` and label it truthfully, do not delete it | The old engineering is a precondition for the new certificates; deleting it would lose traceability | Advisor's suggestion | Yes |
| D9 | 2026-11-15 | Division of roles: Theodore is the PI, the advisor sets the direction, Codex is the PhD student | Set by Theodore | Theodore | Yes |

---

## Items Theodore needs to decide or provide

These questions **do not block** most of the work. When Codex runs into them, it skips the related steps and continues with the other parts.

| ID | Question | Why it matters | Work packages affected | Default if not answered |
|---|---|---|---|---|
| O1 | Has the private 2.4B model finished training? If so, what evidence can be made public? | Determines the wording of the 2.4B statements in the README | WP0.6, Phase 3 | The audit report labels it "design only" |
| O2 | Does the private SFT data come from SEntFiN? Can Codex access it (without committing it to the public repository)? | Determines whether WP0.1 and WP0.2 can be reproduced on the original data | WP0.1, WP0.2 | Rebuild on the public SEntFiN |
| O3 | What contact information goes in the User-Agent when accessing SEC EDGAR? | The SEC requires automated access to declare contact information; an email address used without consent is not allowed | WP0.4, WP1.1 | Write only code and tests; send no requests |
| O4 | Can this research package go into the public repository (for example in the `research/` directory)? | The package contains candid criticism of the existing project; putting it in makes that public | All | Keep it outside the repository and let Codex read a local path |
| O5 | Roughly how much time can be put in each week? Is Colab the free tier or Pro? | Determines the pace and the available T4 hours | All | Plan for free Colab and 10 hours per week |
| O6 | Is it acceptable that the flagship result is no longer "headline sentiment classification"? | Under the new positioning, the old task becomes a demo use case | Phase 2, 3 | Accepted by default |
| O7 | What is the target publication format? An arXiv technical report, an ML workshop (such as FinNLP or ICAIF), or a finance journal? | Determines the writing style and the depth of experiments | Phase 2, 3 | arXiv technical report |
| O8 | Is Chinese financial text in scope? | Affects corpus choice; EDGAR is English only | WP0.4, WP1.2 | English only |

---

## Decisions to be recorded (fill in later)

| ID | Date | Decision | Basis |
|---|---|---|---|
| G0 | | Whether Phase 0 passes | |
| G1 | | Whether the flagship is P1 or P2 | |
| G2 | | Whether to narrow the scope mid-way through Phase 2 | |
