# T1b: How much of the conclusion remains after adding the other information in the document

Prerequisites as for T1a. Branch `task/t1b`, directory `research/t1b_tighten/`.

## Question

T1 assumes that for each input only its own rounding interval is known. But the document contains other information that can narrow the intervals: the same quantity appearing elsewhere at higher precision; "total = sum of the items" relations in tables. After using all of this, how many of the 196 "undetermined" questions T1 found on the test set remain?

This is a veto test of T1's conclusion.

## What to do

1. **Duplicate disclosures.** For each input of the 196 questions, find other occurrences of the same quantity in the whole document (tables and text). After unifying units, take the intersection of the rounding intervals. The 35 pairs T1 already confirmed can be used directly, but extend this to all 196 questions.
2. **Sum relations.** In each table, automatically find relations of the form "some row approximately equals the sum of several rows" (allowing last-digit deviations caused by rounding). Each relation gives one linear constraint.
3. **Exact range on the feasible region.** The feasible region of the inputs is the intersection of the rounding box with these linear constraints, a polytope. Find the minimum and maximum of the answer over it: use linear programming for linear objectives; ratios and growth rates are linear-fractional objectives, which the Charnes–Cooper transformation turns into linear programs. Use rational arithmetic, or verify floating-point solutions after the fact, so that the range given is a reliable outer envelope.
4. **Manual review.** Randomly draw 40 of the 196 questions and check each one: is the input binding correct; is the quantity really a rounded amount (rather than an exact count, a contract term or a defined value); does the gold solution match the question. Record the judgment and reason for each question.
5. **Summary.** Of the 196: how many remain undetermined, how many are narrowed to determined by duplicate disclosures, how many are narrowed to determined by sum relations, and how many turn out in review to have binding or semantic problems.

## Deliverables

- One figure: the number of the 196 questions remaining after each tightening step (waterfall chart).
- A one-page summary.
- Per-question records, the list of constraints, code.

## Decision

- **Conclusion kept:** after tightening and review, the undetermined questions in the test set are no fewer than 5% of all 1,147 questions (that is, at least 58).
- **Conclusion downgraded:** fewer than 58. Then no longer say "the document cannot determine the answer"; keep only "the answer is sensitive to which source is used".
- If more than a quarter of the 40 manually reviewed questions have binding or semantic problems, first fix T1's rules and recompute, and say so.
