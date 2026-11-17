# T1c: Does this have any real effect on model evaluation

Prerequisites as for T1a. Branch `task/t1c`, directory `research/t1c_models/`. Needs agents to answer questions; no paid APIs are called.

## Question

T1 shows that for about 17% of questions, the answer is not determined within the benchmark's tolerance by the rounding precision of the inputs. Does this cause a model's correct answers to be marked wrong? Are the model's errors concentrated on these questions?

If not, T1 is only a note about the semantics of the benchmark. If so, it is a quantifiable source of noise in the evaluation of financial models.

## What to do

1. **Select questions.** The 196 test questions for which T1 found a witness, plus 196 control questions certified as stable. Match the controls one by one by operation type.
2. **Answer.** Give each question's document (table and the text before and after it) and the question to an agent, and ask for a final value and a short arithmetic expression. The prompt is fixed and does not mention rounding or this study. Use a new session for each question so that questions do not influence one another. If conditions allow, have two model tiers each do one pass.
3. **Score.** Compute all three rules: the official rule (equality at five decimal places), relative 1%, and the number of digits shown in the gold answer.
4. **Attribution.** For each answer marked wrong, decide which class it belongs to:
   - it lies within the answer interval given by T1 (that is, it is consistent with the document and only differs from the way the gold answer was taken);
   - it equals the result computed from another figure in the document with a different precision;
   - the expression differs from the gold solution but is reasonable (for example the denominator is taken at the end of the period rather than the start);
   - a genuine error.
5. **False precision.** How many more significant digits the model reports compared with the "meaningful digits" computed by T1a's rule.

## Analysis

- The difference in error rate between the witness group and the control group, with an interval (bootstrap clustered by document; several questions from the same page count as one cluster).
- Among the answers marked wrong, what share falls in the first two classes (consistent with the document).
- How much the accuracy of each group changes under a different scoring rule.

## Deliverables

One figure (accuracy of the two groups under the three scoring rules, and the attribution breakdown of errors), a one-page summary, and all raw answers and scoring records.

## Decision

- **Real effect:** the error rate of the witness group is more than 5 percentage points higher than that of the control group and the interval excludes zero; or more than 10% of the answers marked wrong are actually consistent with the document.
- **Small effect:** neither condition holds. Report it as it is.

## Watch out for

- FinQA is public data, and models may have seen it during training. This raises accuracy, but its effect on the two groups should be similar. State this limitation in the summary.
- The attribution in step 4 is done first by a program (the first two classes can be decided exactly); the third and fourth classes are then reviewed by a human or another agent, and disagreements are kept.
