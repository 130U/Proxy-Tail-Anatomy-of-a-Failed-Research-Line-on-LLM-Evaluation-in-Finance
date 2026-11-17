# T1e: Extend the sample conclusions to the whole test set

Branch `task/t1e`, directory `research/t1e_full_test/`. Only read the results of earlier rounds; do not change their files. Do not train models and do not call paid APIs.

## Why this round

When the advisor recomputed from T1d's per-question table, they saw something more important than "the model knows the precision":

- The official accuracy of all four runs (two known models, three prompts) is between 81% and 83%.
- The questions marked wrong are almost the same set: of 392 questions, 63 were marked wrong in all four runs, 316 were never marked wrong, and only 13 had inconsistent results.
- Of these 68 rejections, two independent reviews agreed that 32 are reference errors and 23 are defensible alternative conventions; none was judged a definite model error.
- A mechanical check that needs no judgment: FinQA's own two gold fields (the human-written `answer` and the program-executed value `exe_ans`) contradict each other in 6.2% of the test set.

In other words, models have reached the ceiling on this benchmark, and the remaining "errors" belong to the benchmark itself. The first draft of the short paper has already been written on this basis (`paper/finqa_short_v0.md`).

The problem is that these numbers come from 392 questions drawn by stratification, not from the whole test set. This round extends them to all 1,147 questions. The four parts below do not depend on each other and can be done at the same time.

---

## Part one: the remaining 755 questions (needs agents)

1. For the 755 test questions not among those 392, use T1d's **prompt B verbatim**, without changing a word.
2. Two models each do one pass: `gpt-6-astra` and `gpt-6.1-sol`. A fresh session for each question; rules as in T1d.
3. Scoring follows T1d: the expression goes to the official executor and is marked right or wrong by the official rule; the precision metrics are computed as before.
4. Merge with T1d's conditions B and B′ to get both models' results on all 1,147 questions.

Report:

- The official accuracy of both models on all 1,147 questions, with intervals.
- The overlap of the two models' rejected sets: the number of questions both get wrong, only one gets wrong, and both get right; Jaccard.
- The precision metrics on the whole test set (the table from T1d's one-page summary, with columns for conditions B and B′).

## Part two: attribute every rejection (needs agents)

1. Items: questions marked wrong for at least one model in part one; plus the 9 questions among the 392 that were marked wrong in B, C or B′ but were never attributed by T1c.
2. Method as in part two of T1d: two reviewers who cannot see each other, using `REVIEW_RUBRIC.md`; disagreements go to a third.
3. Each case is additionally given a **sub-type**, chosen from the fixed list below. The existing 68 cases are also relabelled by both reviewers with this list (the advisor's preliminary counts are in Section 4 of the short-paper draft; label everything independently first, then compare).

| Category | Sub-type |
|---|---|
| Reference error | wrong or missing operation in the program; change computed in the wrong direction or on the wrong base; wrong row, year or concept; missing unit conversion; other |
| Defensible alternative convention | sign of a "decrease"; choice of denominator or base; ambiguous period or wording; absolute versus percentage change; other |
| Definite model error | wrong figure taken; arithmetic error; other |
| Inconclusive | question truncated; document information insufficient; other |

Report:

- On the whole test set, counts of officially rejected questions by category and sub-type: one table for each model, plus a separate table for the part where "both models are wrong".
- The accuracy of each model after counting as correct the cases that "both reviews agree lie on the benchmark side".
- The agreement rate and κ of the two reviews.

## Part three: do the two gold fields contradict each other (no agents needed)

For all 8,281 questions, mechanically compare the human-written `answer` with the program-executed value `exe_ans`. Use no model judgment.

Rules:

1. Strip %, $ and commas from `answer`, parse it as a number, and record the number of decimal places it shows. Count unparseable ones separately.
2. Count as "consistent" if either holds: `exe_ans` rounded to the decimal places of `answer` is equal; or the relative error between the two is at most 1%.
3. If `exe_ans` multiplied or divided by 100 satisfies rule 2, count it as "differs only by the percent sign".
4. If the negation satisfies rule 2 or 3, count it as "differs only in sign".
5. Count everything else as "contradiction".

The advisor's own results, to be independently reproduced and checked: of all questions, 7,952 are parseable, with 508 contradictions and 79 differing only in sign; on the test set, 1,101 are parseable, with 68 contradictions and 10 differing only in sign.

Report two more numbers:

- The share of "contradiction" questions that are marked wrong in part one, compared with "consistent" questions.
- How many rejection cases have the model's answer equal to `answer` but not to `exe_ans`.

## Part four: test the rounding law on another dataset (no agents needed)

The short paper currently has only one benchmark, FinQA. Redo T1's exact interval audit on the TAT-QA development set. TAT-QA's arithmetic questions come with derivations and a scale. If it cannot be obtained, use the ConvFinQA development set.

Report:

- The number of analysable questions, and the share of them whose answer is not determined by the input precision within the 1% tolerance, grouped by operation type.
- The agreement rate between T1a's first-order rule and the exact classification.
- The predicted value from T1a's a priori prediction method, and the observed value.

This part has no gate; whatever the numbers are, write them down.

---

## Optional

- **Another provider's model.** If a model from outside OpenAI is available, run it on those 392 questions with T1c's original prompt, and report how much its rejected set overlaps with "the 63 wrong in all four runs". If that is not possible, say so.
- **A spot-check sheet for Theodore.** Randomly draw 10 cases each from "reference error" and "defensible alternative convention" and generate `human_check_20.csv`: question ID, question, gold program and its executed value, the human-written answer, the model's expression and answer, the reviewer's one-sentence reason, and an empty "agree / disagree" column. At submission, reviewers will ask whether anyone checked by hand; this sheet is prepared for that.

## Deliverables

- A one-page summary, opening with this table filled in:

| | gpt-6-astra | gpt-6.1-sol |
|---|---:|---:|
| Official accuracy on all 1,147 questions | | |
| Number of rejected questions | | |
| Of which both reviews agree are reference errors | | |
| Of which both reviews agree are defensible alternative conventions | | |
| Of which judged definite model errors | | |
| Accuracy after counting benchmark-side cases as correct | | |
| Number of questions both models get wrong | | |

  Then write: the four numbers from part three; the three numbers from part four.
- `results.json`: all the numbers and intervals above.
- Per-question table (reusing the columns of T1d's `per_response.csv`, plus the sub-type), all raw answers, review records, code.

No checklists, hash tables, packaging scripts, or reviews of reviews.

## Watch out for

- Use prompt B verbatim, without changes. Do not retry based on whether an answer is right.
- Reviewers cannot see which model got a question wrong, the other reviewer's conclusion, or the results of earlier rounds.
- If the results differ from the conclusions on the 392-question sample (for example, the overlap of rejected sets is much lower on the whole test set, or a sizeable number of definite model errors appears), report it as it is. In that case the main conclusion of the short paper must change, and that is itself an important result.
