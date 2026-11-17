# T1g: Where rounding precision really has consequences

Branch `task/t1g`, directory `research/t1g_consequence/`. Only read the results of earlier rounds; do not change their files. The first three parts do not need agents to answer questions; they only need data and computation.

## Background, from the start

The project is auditing financial QA benchmarks. The full exploration map is on the repository homepage [README](../README.md); read it first. So far only one item stands:

> The numbers in filings are rounded. Treating each input as "displayed value ± half a last-digit unit" and computing the exact range of the gold solution, for at least 10.7% of FinQA test questions the answer cannot be determined to 1%. A rule with no fitted parameters predicts which questions this applies to: two numbers must differ by at least about 100 last-digit units for the growth rate to be exact to 1%.

The novelty check (T1f) confirmed that no prior work on this item was found. But it has a known weakness (T1c): **it does not change current scoring.** The gold answer and the model use the same displayed figures and compute the same number, so nobody is marked wrong.

On its own, this item is a note about a benchmark and cannot carry a paper. This round has to answer two questions:

1. Is there a setting where rounding precision has a **visible consequence**: the document contains two numbers that contradict each other, or the conclusion of the gold answer itself cannot be determined?
2. Does the rule still hold on another dataset?

The four parts below do not depend on each other and can be done at the same time. Any part may end with "no consequence"; that is also a result, and should be reported as it is.

---

## Part one: changes the document prints itself, versus changes recomputed from the printed figures

### Idea

Filing tables often print two years of figures together with their change. For example, they print 137, 133 and "change 2.6%". The company computed this 2.6% from the unrounded original figures. Recomputing from the printed 137 and 133 gives 3.0%. Many filings state directly in a footnote that "percentages are calculated on unrounded amounts".

This is a natural experiment: **the document itself leaks information from before rounding.** It brings three things at once:

- a test of our rounding model on real data (until now we only had the worst case and an assumed uniform distribution);
- a visible contradiction: the same document supports two different answers, and the one the company printed itself has the stronger claim to be "right";
- a consequence for evaluation: the benchmark's gold solution recomputes from the printed figures and gets an answer different from the one the document prints.

### What to do

1. **Find such table rows.** In all tables of FinQA and TAT-QA (all splits), find rows that print both "two level values" and "their change". There are two kinds of change: amount difference (common column names Change, Increase/Decrease, Variance) and percentage change (% Change, %). Handle negatives in parentheses, "n/m", "—" and different scales. For each row found, record the two level values, the printed change, and the displayed decimal places of each.
2. **First test the model itself.** For each row, compute the exact range of the "recomputed value" over a rounding box of half a last-digit unit, then check whether the interval represented by the printed change intersects it.
   - Rows with no intersection show that our assumption fails on that row (the company used a different base, the column means something else, or the parsing is wrong). Read 50 such rows by hand to find the reasons, and report the share of each kind of reason. These rows do not enter the later statistics.
3. **Measure how common contradictions are.** Among the rows that intersect:
   - Amount difference: the share where the printed difference is not equal to the difference of the two printed level values. **The advisor's estimate: if all three numbers were rounded independently from the original values, this share should be 1/4.** First derive it yourself, then compare with the observed value.
   - Percentage change: the share where the recomputed value, rounded to the printed decimal places, is not equal to the printed value; and the share where the relative difference between the two exceeds 1%.
4. **Can the rule predict it.** For each row, compute the probability of "not equal" under the assumption of independent uniform rounding (no parameter may be tuned on the observed data). Group by Δ (the difference between the two level values converted into a count of last-digit units), and plot the predicted probability against the observed share.
5. **Where the printed value falls in the range.** Plot a histogram of the relative position (0 to 1) of the printed change within the exact range. This tests the "uniform rounding" assumption itself.
6. **Check again with existing data.** T1b has already compiled 511 "total = sum of the items" relations. Compute the residual of each relation (the printed total minus the sum of the printed items, in last-digit units), and compare with the theoretical distribution under independent uniform rounding.
7. **Consequences for QA.** Find questions where the gold solution computes exactly the change between two cells, another cell in the table prints this change, and the two disagree under that dataset's scoring rule. For FinQA, count once under each of the official rule, 1% and displayed digits; for TAT-QA, use its own rule.
   - Report how many such questions there are, and their share of all "compute a change" questions.
   - For those among the 392 questions of T1c and T1d, check the existing model answers: did the model use the recomputed value, or read the printed value directly? Was it marked right or wrong?

### Decision

- **Has consequences:** the questions found in step 7 make up more than 5% of the "compute a change" questions in either dataset; or in step 3, more than 30% of percentage changes in rows with Δ < 100 are not equal.
- If neither holds: write the numbers out clearly; the conclusion is "contradictions within documents exist but are rare".

---

## Part two: comparison questions

### Idea

Questions that ask for a number have a tolerance as a safety net. **Comparison questions do not**: "which year grew faster", "does this ratio exceed some value", "which segment has the highest margin". The answer is "yes / no" or a name. If the ranges of the two quantities being compared overlap, the gold answer cannot be determined by the document, and there is no tolerance to speak of.

T1 excluded this kind of question at the time (none of the 154 FinQA questions containing `greater(` was analysed), so this area has not been looked at at all.

Directly comparing two printed numbers (137 vs 133) cannot flip unless the two are tied. What can flip is **comparing two computed quantities**: two growth rates, two ratios, two differences.

### What to do

1. FinQA: questions in all splits containing `greater(`, and questions whose gold answer is yes / no. Split them into two classes: comparing printed numbers; comparing computed quantities.
2. TAT-QA: questions whose answer comes from a comparison or ranking (the answer is a year, a category name or yes / no, and the derivation involves computed quantities). First write down clearly the rule you use to identify such questions, then draw 40 and check by hand how accurate the identification is.
3. For each question, compute exactly over the rounding box whether the ranges of the two compared quantities overlap, that is, whether there is a set of inputs consistent with the displayed precision that flips the conclusion. Give the witness of the flip.
4. Using T1a's uniform rounding assumption, compute the probability that each question's conclusion flips, and the expected share.
5. Write the rule for comparing two growth rates: how large must the difference between the two growth rates be for the conclusion to be determined. Use it to predict, and compare with the exact classification.

### Decision

- **Has consequences:** among questions that "compare computed quantities", more than 10% have undetermined conclusions.
- Below 10%, or too few such questions in total (fewer than 100 across the two datasets): report it as it is.

---

## Part three: another dataset, predict first, then compute

### Idea

The earlier a priori test of the rule used FinQA's own distributions, so it does not count as out-of-sample. TAT-QA tables are mostly in thousands, and the numbers have more digits. According to the rule, the more digits, the fewer undetermined questions. This is a prediction that can be written down first and checked afterwards.

### What to do

1. **Predict first, and commit once.** For TAT-QA arithmetic questions, count only two things: the distribution of significant digits of the input numbers, and the distribution of the size of the answers (growth rates, differences, ratios). Do not compute the exact range of any question. Use T1a's method to predict the share that cannot be determined at the 1% tolerance, by operation type. Write the prediction into a file and **commit it separately, once**, with a commit message stating "prediction, observed values not yet computed".
2. **Then compute.** Redo T1's exact interval audit on the TAT-QA arithmetic questions (its derivation and scale fields can be used directly).
3. Report: the number of analysable questions; the undetermined share (by operation type); the difference between prediction and observation; the agreement rate between T1a's first-order rule and the exact classification.
4. Put FinQA and TAT-QA together in one figure: x-axis the significant digits of the inputs, y-axis the undetermined share, with the rule's prediction curve overlaid.

If TAT-QA cannot be obtained, use the ConvFinQA development set and say so.

### Decision

- **Rule holds:** the overall prediction differs from the observation by no more than 5 percentage points, and the agreement rate of the first-order rule is at least 95%.
- Otherwise report it as it is, and explain where the rule fails.

---

## Part four: the same quantity at two precisions (smaller, can be done last)

In the FinQA test set, T1 found 35 pairs where "the same quantity appears twice at different precisions" (for example, the text says 1.2 billion and the table says 1,201 million). Extend this scan to all splits of FinQA and TAT-QA.

For each pair, compute the gold solution's answer from each of the two sources, and report: the distribution of the relative difference between the two answers; the share with a relative difference above 1%; and whether the range T1's rule gives for the coarser source contains the answer computed from the finer source (this is another test of the rounding model on real data).

No gate.

---

## If part one or part two "has consequences", do this step as well (needs agents)

Take at most 200 of the questions found, use T1c's original prompt verbatim, and have two models each answer once, with a fresh session per question. Report: which answer the model chose; whether it was marked right or wrong under that dataset's scoring rule; and how many of the answers marked wrong actually agree with the value the document prints.

If there are no consequences, do not do this.

---

## Spend half a day checking first

Only for parts one and two. What to look for: has anyone, on a financial QA or table QA benchmark, counted "the change printed in the table disagrees with the result recomputed from the printed figures"; has anyone analysed by input precision whether the gold answers of comparison questions are determined. Adjacent directions include numeric consistency checks in financial statements, table fact checking, and numeric hallucination detection.

If you find the same measurement, write a paragraph, send it back, and then stop that part.

## Verify two things along the way

In the previous novelty check, the advisor could not verify two points; give original-text evidence (title, authors, link, an excerpt of the relevant passage):

- Whether FINESSE-Bench (arXiv 2605.15482) counted shared rejections on FinQA's 1,147 questions across 53 models; in which section.
- Whether arXiv 2611.02461 exists; what exactly it says about "a rounded label corresponds to a set". If this paper exists, it is directly relevant to our only remaining candidate; read the full text, and write clearly what it did and what it did not do.

## Deliverables

- **A one-page summary**, opening with this table filled in:

| Part | Key numbers | Decision |
|---|---|---|
| One: printed change vs recomputed change | Number of rows found; share of unequal amount differences (predicted / observed); share of unequal percentages; number and share of affected questions | Has consequences / rare |
| Two: comparison questions | Number of questions comparing computed quantities; share with undetermined conclusions; expected flip share | Has consequences / rare |
| Three: second dataset | Prediction; observation; first-order rule agreement rate | Holds / does not hold |
| Four: two precisions | Number of pairs; share of answers differing by more than 1% | — |

- **One figure**, four panels: predicted vs observed for part one; the position histogram for part one; for part two, the difference between two growth rates against whether the conclusion flips; for part three, the two datasets with the prediction curve.
- Per-row and per-question result tables, all witnesses, code.
- The one-paragraph novelty check, and the original-text evidence for the two verifications.

No checklists, hash tables, packaging scripts, or reviews of reviews.

## Watch out for

- When a result lands right on the line, report the number as it is and classify it by the gates above; do not write "inconclusive".
- The "no intersection" rows in part one must not be quietly dropped. Their share and reasons are part of the results: a high share means our rounding model has a problem.
- The prediction in part three must be committed first. After seeing the observed values, do not change the prediction or the prediction method.
- Mark the source level of every fact: full text / abstract / secondhand / our experiment.
- Write only in your own directory; do not change the README, and do not change the short-paper draft.
