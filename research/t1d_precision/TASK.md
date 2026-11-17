# T1d: Does the model know how many digits of its own answer are reliable

The last round. After it is done, the advisor writes the short paper. Branch `task/t1d`, directory `research/t1d_precision/`. Only read the results of T1, T1a, T1b and T1c; do not change their files. Do not train models and do not call paid APIs.

## Why this round

The conclusion of T1c is that the rounding precision of the inputs does not change current scoring. The reason is simple: the gold answer and the model use the same displayed figures. But T1c also saw that the model reports 12 to 16 significant digits, of which only 1 to 3 are meaningful.

Existing benchmarks cannot measure this. We have the exact answer interval for every question, so we can. There is only one question:

> If we ask the model directly "how many digits of your answer are reliable", does it answer correctly? And after we teach it a one-sentence rule?

This round has a second job: the semantic reviews in T1b and T1c were both done by one AI, and another AI needs to redo them independently.

---

## Part one: precision experiment

### Questions

Reuse T1c's 392 questions (196 witness questions and 196 stable questions matched by operation type) with the same document text. Do not resample.

### Three conditions

| Condition | Method | New calls |
|---|---|---:|
| A not asked | Use T1c's existing 392 answers directly | 0 |
| B asked, not taught | Prompt B below | 392 |
| C asked and taught the rule | Prompt C below | 392 |

Each call is a fresh session given only the prompt, the document and the question. The answering agent cannot access this repository and cannot use code or tools. Use the prompts verbatim; once finalized, do not change them.

If the call budget is not enough, condition B must cover all 392 questions; condition C may cover only a fixed random half (98 pairs drawn by pair, seed 20261117).

If conditions allow, run condition B again with another model tier. If that is not possible, say so.

### Prompt B

```
Solve the financial question using only the document below. Do not use external sources, code or tools.

Figures in the document are rounded to the precision shown: a displayed figure may stand for any value that rounds to it. Counts, years, dates and contractual terms are exact.

Give a final numerical answer, its unit, and a brief arithmetic expression showing your calculation. Your expression must use the figures exactly as displayed, with arithmetic operators (+, -, *, /, parentheses), and evaluate to your answer in the stated unit.

Then state how precisely the document determines your answer:
- "low" and "high": the smallest and largest values your answer could take, given the rounding of the figures you used.
- "reliable_digits": how many significant digits of your answer you would report as reliable (an integer; 0 if not even the first digit is reliable).

Do not include prose outside the JSON. Return JSON with exactly these fields:
{"answer": "numerical value as a string", "unit": "unit, or percent, ratio, times, years, etc.", "expression": "arithmetic expression", "low": "numerical value as a string", "high": "numerical value as a string", "reliable_digits": "integer as a string", "explanation": "one brief sentence"}

DOCUMENT
{document}

QUESTION
{question}
```

### Prompt C

Identical to prompt B, except that the following paragraph is inserted after the second paragraph ("Figures in the document are rounded…"):

```
How to work it out: a figure shown to a last digit of size u may be any value within u/2 of the displayed figure. The smallest and largest values of your answer are reached at extreme values of the inputs. For a difference b - a, or a growth rate (b - a)/a, of two figures with the same last-digit unit u, the result is uncertain by about u/|b - a| in relative terms; the two figures must differ by about 100 units for the result to be reliable to 1%.
```

### How the ground truth is computed

The ground truth is computed from **the expression the model itself wrote**, not from the gold solution. This measures "whether the model knows the precision of its own method", independent of whether its expression agrees with the gold answer.

1. Bind each number in the expression to a displayed figure in the document. For those that bind, give a rounding interval of half a last-digit unit according to the decimal places shown in the document. If the same fact appears several times, use the same variable.
2. Numbers that do not bind and are clearly constants (100, 12, 1000 for conversion, etc.) are treated as exact.
3. Compute the exact range [L*, U*] of the expression over the rounding box, using T1c's rational corner method.
4. Let the centre value c be the value of the expression on the displayed figures, the half-width h* = (U* − L*)/2, and the **true reliable digits** d* = log10(|c| / h*).
5. If the expression cannot be parsed, or some number neither binds nor is a constant, the answer does not take part in precision scoring and is counted separately. Questions with h* = 0 (all inputs exact) and with c = 0 are also counted separately.

For condition A: the model reported no interval, so only count how many significant digits it printed.

### Metrics

For each answer under conditions B and C:

1. **Interval width ratio** r = (high − low) / (U* − L*). Three classes:
   - accurate: 0.5 ≤ r ≤ 2;
   - too narrow (overstating precision): r < 0.5;
   - too wide: r > 2.
2. **Containment**: low ≤ L* and high ≥ U*, allowing an error of 5% of the true width.
3. **Digit error** e = reliable_digits − d*. Report the median, the share with |e| ≤ 1, and the share with e > 1 (overstating by more than one digit).
4. **1% judgment**. If the model's interval satisfies max(|high − answer|, |answer − low|) ≤ 1% × |answer|, count it as the model judging "the answer is determined to 1%". The ground truth is computed from [L*, U*] and c by the same formula. Report the accuracy, and report separately: among truly undetermined questions, how many it recognized; among truly determined questions, how many it got right.
5. **Self-contradiction**: the number of digits implied by the model's own interval is log10(|answer| / half-width). Report the share where reliable_digits exceeds it by more than one digit.

Reference rows: on the same questions, the accuracy of T1a's first-order rule on item 4; and the accuracy of "always answer determined".

Give every number a bootstrap 95% interval clustered by page (reusing T1c's 237 page clusters). Condition C minus condition B differences use same-question pairing.

Report all metrics twice: on all scorable answers; and on the subset whose expression agrees with the gold answer under the official rule. Then report each again separately by witness / stable question and by operation type.

### How to conclude

Look mainly at three numbers: the "accurate" share in item 1, the "overstating by more than one digit" share in item 3, and the accuracy in item 4. There are only three possible conclusions, fixed before execution:

| Conclusion | Condition |
|---|---|
| The model already knows | Condition B: accurate share ≥ 80%, and 1% judgment accuracy ≥ 90% |
| It learns from one sentence | Condition B fails; condition C meets the same two criteria |
| It does not learn even when taught | Condition C also fails |

When a result lands right on the line, report the number as it is and classify it by the table above. Do not write "inconclusive" because it missed by a little. There is only one exception: if more than 10% of answers cannot be scored, report the reasons first.

All three conclusions can go into the short paper; none of them counts as a failure.

---

## Part two: have another AI redo the semantic review

### Review T1b's judgments

1. Items: T1b's 196 witness questions, plus 60 questions drawn by fixed random selection from the stable questions (seed 20261117). 256 questions in total, in shuffled order. Adding stable questions serves two purposes: the reviewer cannot assume every question has a problem; and we get, as a by-product, the share of semantic problems among stable questions.
2. The reviewer is a fresh session, using a model tier different from the first time where possible. It sees only: the document, the question, the gold solution, and the location each input is bound to. It **does not see** the first judgment and its reasons, the intervals and witness values, or which group a question belongs to.
3. The criteria follow T1b: is the input binding correct; is the quantity a rounded amount (rather than an exact count, a contract term or a defined value); does the gold solution match the question. Output valid / invalid / uncertain and a one-sentence reason.
4. Questions where the two judgments disagree go to a third fresh session. It sees both reasons but does not know which came first. All three judgments are kept.

Report:

- The agreement rate and Cohen's κ of the two reviews, and the 3 × 3 cross-table.
- The number of questions "kept", reported under each of three definitions: the first review (139); valid in both reviews; valid in the majority of the three judgments. **The short paper uses the strictest definition (valid in both reviews) as the headline number.**
- The share of stable questions judged invalid or uncertain, compared with the witness questions.

### Review T1c's attributions

1. Items: the 68 answers in T1c that the official rule marks wrong.
2. Likewise re-judged independently by a fresh session, using T1c's `REVIEW_RUBRIC.md`, without seeing the first attribution. Disagreements go to a third session.
3. Report the agreement rate, κ, and, among cases where both reviews agree, how many are "reference error" and how many are "defensible alternative convention".

---

## Deliverables

- **One figure**, three panels:
  1. Under conditions A, B and C, a scatter or box plot of the digits the model claims against the true reliable digits;
  2. The distribution of the interval width ratio under conditions B and C (log scale), with 0.5 and 2 marked;
  3. Accuracy of the 1% judgment: condition B, condition C, the first-order rule, "always answer determined".
- **A one-page summary**, opening with this table filled in:

| | Condition A not asked | Condition B asked | Condition C asked and taught |
|---|---:|---:|---:|
| Number of scorable answers | | | |
| Median claimed digits | | | |
| Median true reliable digits | | | |
| Share overstating by more than one digit | | | |
| Share of intervals "accurate" | — | | |
| Share of intervals "too narrow" | — | | |
| 1% judgment accuracy | — | | |

  Then write: which of the three conclusions applies; and what the number 139 becomes after the semantic review.
- `results.json`: every number and interval in the table above, plus all counts from part two.
- Per-question table `per_response.csv`: question ID, group, operation type, condition, scorable or not, whether the expression agrees with the gold answer, L*, U*, d*, low, high, reliable_digits, r, contained or not, e, the model's 1% judgment, the true 1% judgment.
- All raw answers, the original text of both prompts, and the scoring and analysis code.

No checklists, hash tables, packaging scripts, or reviews of reviews.

## Watch out for

- The prompts do not mention this study, T1 or the groups.
- Do not retry based on whether an answer is right. Keep and count answers with broken formatting.
- Before the formal run, you may use 10 questions to check that the JSON can be parsed. These 10 come from the training set and must not come from the 392. After seeing the formal results, do not change the prompts or the metric definitions.
- The prompt for condition B itself tells the model that "the figures are rounded". This is part of the task definition, and the summary must explain it: condition B measures "whether it can compute it after being reminded", not "whether it thinks of it unprompted". Whether it thinks of it unprompted is answered by condition A.
- FinQA is public data, and models may have seen the questions and answers. The effect on the precision question should be very small, because the benchmark has no gold answers in interval form. State this limitation as it is.
