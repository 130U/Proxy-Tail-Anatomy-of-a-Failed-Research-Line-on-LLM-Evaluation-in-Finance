# Reporting protocol and templates

All outputs go in the repository's `research/` directory. Theodore will bring these files back to the advisor. After reading them, the advisor gives the questions and priority adjustments for the next round.

**Source-tier labels** (every number must be labeled):

- `full text`: read in the body of the paper;
- `abstract`: read only in the abstract;
- `secondary`: from a survey, blog or news item;
- `advisor memory`: from a citation given by the advisor that has not been verified;
- `our experiment`: give the experiment ID.

---

## 1. Template for literature answers (`research/answers/Qxx.md`)

```markdown
# Qxx: <short title of the question>

Date: YYYY-MM-DD · Online: yes / no · Search cutoff: YYYY-MM

## 1. Conclusion
(At most 5 sentences, answering the question directly)

## 2. Evidence
| Work | Year / venue | ID or URL | Specific content or numbers relevant to this question | Source tier |
|---|---|---|---|---|

## 3. Novelty judgment
- Judgment: already done / partly done / not found
- Confidence: high / medium / low
- Search keywords:
- Relation to the advisor's hypothesis: confirms / overturns / revises (state which hypothesis)

## 4. Minimal viable check
(A draft theorem statement with all assumptions; or an experiment design that can be completed within a few hours on a T4)

## 5. Kill conditions
(What finding would make us abandon this direction)

## 6. Uncertainties
```

---

## 2. Template for derivation questions (`research/theory/Txx.md` or written into `notes.tex`)

```markdown
# Txx: <proposition name>

Status: proven / draft / has counterexample / open

## Statement
(Complete list of assumptions + conclusion)

## Proof
(Or counterexample)

## Differences from the advisor's draft
(What was changed, and why)

## Numerical example
(If applicable)

## Literature results relied on
| Result | Source | Source tier |
|---|---|---|
```

---

## 3. Template for experiment records (`research/experiments/<id>/record.md`)

```markdown
# Experiment <id>: <one-sentence purpose>

## Proposition or question to test
(Points to Txx, Qxx or WPx.x)

## Budget (fill in before starting the run)
- Hardware: CPU / T4
- Estimated time:
- Estimated GPU memory:
- Data size:

## Configuration
- commit:
- config file:
- seeds:
- Data version and hash:
- Actual hardware and actual time:

## Results
| Configuration | Metric | Point estimate | 95% confidence interval | n |
|---|---|---|---|---|

## Certificate checker output (if applicable)
(Paste the JSON as is)

## Conclusion
(Measured against the "proposition to test", what is the conclusion)

## Anomalies and limitations
```

---

## 4. Template for progress reports (`research/reports/YYYY-MM-DD-roundN.md`)

This is the file Theodore most needs to bring back to the advisor. Write it so that the advisor can make decisions **without opening any other file**.

```markdown
# Round N progress report

Date: YYYY-MM-DD · Branch: research/certifiable · Latest commit:

## 1. One-paragraph summary
(What is the most important finding of this round)

## 2. What was completed
| ID | Output file | One-sentence conclusion | Strength of evidence |
|---|---|---|---|

## 3. Status of the advisor's hypotheses
| Hypothesis | Source | Status | Basis |
|---|---|---|---|
| The provable bound of P1 is not found in the literature | 01 §5.1 | confirmed / overturned / not checked | Qxx |
| The audit resolution limit holds | T1.4 | proven / wrong / not done | Txx |
| ... | | | |

## 4. Decision gate materials
(If this round is close to G0 / G1, give the materials item by item according to the criteria in 01 §8)

## 5. Unexpected findings
(Results that differ from expectations, including negative results)

## 6. Where we are stuck

## 7. Needs PI decision
(Items that Theodore needs to provide or decide; numbering continues the O series in 08_DECISION_LOG.md)

## 8. Suggested next steps
(What you think the next round should do, and why. The advisor will take it into account but may not adopt it)
```

---

## 5. Index (`research/INDEX.md`)

One line per output:

```markdown
| Date | ID | File | One-sentence conclusion |
|---|---|---|---|
| 2026-11-20 | WP0.1 | experiments/wp0_1/record.md | The gap between 0.655 and 0.609 is within the 95% interval |
```

---

## 6. What to bring when reporting back to the advisor

**Every round, bring at least:**

1. The latest progress report;
2. All `answers/Qxx.md` added or modified this round;
3. `research/INDEX.md`.

**Bring as needed:**

- Outputs of derivation questions (always bring them if the progress report mentions "has counterexample" or "differs from the draft");
- `claims_audit.md` (bring it the first time it is completed);
- Experiment records (always bring them if a conclusion differs from expectations).

**How to package:** put the files above in one folder, or merge them into one Markdown file, and hand that to the advisor.
