> Historical draft; work on it stopped (2026-11-17). The original text is kept for the record. The unfinished full-test-set experiment, the citations still to be verified, and the inferences are not to be read as verified results. For the final conclusions, see the [project retrospective](../README.md).

# FinQA at Its Ceiling: Reference Errors, Conventions, and the Precision of Rounded Filings

Draft v0 · 2026-11-17 · target: ACL short paper (4 pages)

Numbers marked † come from a 392-question stratified sample of the test set. They will be replaced by full-test-set numbers after the last experiment (task T1e). Citations marked [verify] must be checked against the source before submission.

---

## Abstract

Two current language models, across four runs and three prompts, score 81–83% on a 392-question sample of the FinQA test set†, and they are marked wrong on the same questions: 63 questions are rejected in all four runs and only 13 in some runs but not others†. Two independent blind reviews attribute 55 of 68 rejections to the benchmark (32 reference errors, 23 defensible alternative conventions) and none to a definite model error†. We then ask what a correct reference would look like. Filings report rounded figures, and differences and growth rates amplify the rounding. We prove a one-line rule: two figures must differ by about 100 units of their last displayed digit for their growth rate to be determined to 1%. Exact interval computation shows that for at least 10.7% of test questions the filing does not determine the answer to the 1% tolerance in common use. Models print digits unrelated to this precision, yet return the exact interval in 98% of cases when reminded that figures are rounded†. Numeric gold answers should be sets, not numbers.

## 1 Introduction

FinQA (Chen et al., 2021) asks numerical questions about tables and text from annual reports and scores a system by executing its program and comparing the result with a reference value. Reported accuracies of strong systems have gathered in the low-to-mid 80s [verify]. We ask what is left in the remaining errors.

Our first finding is that the errors are a property of the questions, not of the models. Different models and prompts are marked wrong on almost exactly the same items (Section 3). Independent review of those items finds reference errors and ambiguous conventions, and no clear model mistakes (Section 4). Annotation noise in financial QA has been reported before: FinanceReasoning revised 15.6% of the questions it took from four public datasets (Tang et al., 2025) [verify]. What we add is the item-level picture on the original test set and a mechanical check that needs no judgment: FinQA's written answer and the output of its own gold program contradict each other in 6.2% of test questions.

Our second finding concerns a source of indeterminacy that no relabeling can remove. A filing states "137" and "133" in millions. The growth rate computed from them, 3.01%, is in fact anywhere between 2.25% and 3.77%. We give an exact rule for when this matters, verify it without fitted parameters on 5,337 questions, and count how often the filing fails to determine the answer (Section 5).

Our third finding is that models already know this. Asked for the range of their answer, they return the exact interval (Section 6). The benchmark never asks.

Contributions: (i) an item-level account of residual FinQA error; (ii) a closed-form precision rule for answers computed from rounded figures, with an exact audit of FinQA; (iii) evidence that models can state the precision of their answers; (iv) exact answer intervals for 5,337 FinQA questions and adjudicated labels for the audited items, to be released.

## 2 Setup

**Data.** FinQA has 8,281 questions; the test set has 1,147. Each has a gold program, its executed value, and a separately written answer string.

**Sample.**† 392 test questions: the 196 identified as rounding-sensitive in Section 5 and 196 others matched by operation type. Section 5 itself uses the whole test set.

**Runs.** Each question is answered in a fresh session from the table, the surrounding text, and the question. The model returns a number, a unit, and an arithmetic expression over displayed figures.

| Run | Model | Prompt |
|---|---|---|
| A | runtime default (identity not exposed) | answer and expression |
| B | gpt-6-astra | A, plus: figures are rounded; give low, high, reliable digits |
| C | gpt-6-astra | B, plus a one-paragraph propagation rule |
| B′ | gpt-6.1-sol | B |

**Scoring.** We execute the model's expression with the official executor and apply the official rule (equality at five decimals). Scoring the expression rather than the printed number avoids penalising a model for how many digits it prints.

## 3 Models disagree with the reference, not with each other

| Run | Official accuracy† |
|---|---:|
| A | 82.7% |
| B | 82.2% |
| C | 82.4% |
| B′ | 81.1% |

Of the 392 questions, 316 are accepted in every run, 63 are rejected in every run, and 13 have mixed outcomes. Pairwise Jaccard overlap of the rejected sets is 0.89 to 0.93. A change of model or prompt moves at most a handful of items. If the rejections were model errors, we would expect them to move.

## 4 What the rejections are

Two reviewers, blind to each other and to the experimental grouping, classified each of the 68 rejections of run A from the source document, the question, the reference program, and the model's expression. They agree on 63 (92.6%; κ = 0.88).

| Agreed label | n | Sub-type (our coding of the reviewers' rationales) |
|---|---:|---|
| Reference error | 32 | wrong or missing operation in the program (10); change computed in the wrong direction or on the wrong base (10); wrong row, year or concept (9); missing unit conversion (3) |
| Defensible alternative | 23 | sign of a "decrease" (12); denominator or base (4); period or wording (4); absolute versus percentage change (3) |
| Unresolved | 8 | question truncated, or document insufficient |
| Reviewers disagree | 5 | |

Neither reviewer labelled any rejection a definite model error. Counting the 55 agreed benchmark-side cases as correct raises accuracy from 82.7% to 96.7%†; the rounding-sensitive and the matched questions end at 96.4% and 96.9%.

Some reference errors need no judgment. A question asking "by what percent did net cash from operations increase" has the program `subtract(1410.5, 1229.0), subtract(#0, 1229.0)`, which returns −1047.5; the written answer is 14.77, which is what the model computes. The largest single convention is the sign of a decrease: the reference returns −0.34 for "what was the percentage decrease", the model returns 34%.

**A mechanical check.** FinQA stores a written answer and an executed program value. Comparing them at the written answer's own precision, and allowing a factor of 100 for percentages, they differ in 508 of 7,952 parseable questions (6.4%) and in 68 of 1,101 test questions (6.2%); a further 1.0% differ only in sign. The official metric uses the program value. In 12 of the 68 rejections the model's answer equals the written answer while the program value does not.

A reviewer shown 60 questions drawn at random from the 196 matched questions, without knowing which questions had been rejected, judged that the gold program fails to answer the question in 13 of them†.

## 5 What a correct reference cannot fix: precision

### 5.1 A rule

A figure displayed with last-digit unit *u* stands for any value within *u*/2 of it. Let *g* = (*b* − *a*)/*a* be a growth rate from two figures of the same sign and unit, and let Δ = |*b* − *a*|/*u* be their difference counted in last-digit units. The largest relative error of *g* over all values consistent with the display is exactly

  *R* = (1 + *g*/2) / (Δ − |*g*|/2),

so *g* is determined to relative tolerance τ if and only if Δ ≥ (1 + *g*/2)/τ + |*g*|/2. For small growth this reads Δ ≳ 1/τ: **the two figures must differ by about 100 last-digit units for their growth rate to be good to 1%.** Equivalently, a growth rate *g* computed from *k*-digit figures has about *k* − log₁₀(1/|*g*|) meaningful digits. Differences, ratios and sums obey the analogous first-order rule |*f*(*x*) − *y*| + Σᵢ |∂ᵢ*f*| *h*ᵢ ≤ τ|*y*|, with *h*ᵢ the half-units and *y* the reference value.

The mathematics is the classical loss of significance in subtracting nearby numbers, and the distortion of growth rates by rounding was studied for economic series by Gittings (1991) [verify]. Rounding intervals and their arithmetic are standard in XBRL (Calculations 1.1) [verify]. What is new is the test on a benchmark.

**Verification.** The formula equals the exact extreme, in rational arithmetic, on all 1,411 two-figure growth questions with equal units. The first-order rule, which has no fitted parameter, reproduces the exact classification of all 5,337 analysable questions at τ = 1% (five misses in total at four other tolerances). The bare "Δ < 100" rule agrees on 97.8% of 1,425 growth questions; its misses are large growth rates and mixed units. Assuming only log-uniform leading digits, together with the empirical distributions of growth and of digit counts, predicts that 41.5% of growth questions are undetermined at 1%; the observed share is 40.5%.

### 5.2 A count

We bind each program input to its place in the document, give it a half-unit box, and compute the exact range of the gold program. Of the 1,147 test questions, 731 pass strict parsing and binding.

| Step | Test questions not determined to 1% |
|---|---:|
| Rounding boxes only, with an explicit witness | 196 (17.1%) |
| After intersecting repeated disclosures (21) and exact linear programming over additive relations (511) | 195 |
| After two blind semantic reviews (inputs really rounded; program answers the question; κ = 0.76) | **123 (10.7%)** |

Everything else in the document rescues one question. For the 123, the median worst-case deviation from the reference is 3.7%, and for one in five it exceeds 10%. Under independent uniform rounding errors, the expected number whose true value lies outside the 1% band is 62 (5.4% of the test set). By type, before semantic review and over all splits, the share undetermined at 1% is 40% for growth rates, 38% for differences, 20% for sums and 18% for ratios. The sign of the answer is always determined.

### 5.3 It does not change today's scores

The reference and the model both compute from the displayed digits, so they agree. The rounding-sensitive questions are rejected 5.1 points more often than the matched ones (95% interval −2.6 to 12.6), and no rejection is explained by input precision alone†. This is therefore not label noise. It is a limit on what the reported number means: the benchmark's five-decimal rule, and the 1% tolerance used in much follow-up work, are both finer than the document.

## 6 Models know the interval

Without being asked (run A), models print a median of 5 significant digits where 2.1 are supported. The number of digits printed is unrelated to the supported precision (Spearman ρ = 0.02), and 62% of answers carry more than one unsupported digit†.

Run B adds two sentences: figures are rounded, and please give the smallest and largest values of the answer and the number of reliable digits. We score against the exact range of the model's own expression.

| | B | C (rule taught) | B′ |
|---|---:|---:|---:|
| Interval width within a factor 2 of exact | 98.4% | 98.1% | 98.1% |
| Interval contains the exact range | 98.7% | 98.7% | 98.7% |
| "Determined to 1%?" correct | 99.7% | 99.5% | 99.5% |
| Stated reliable digits versus true (Spearman ρ) | 0.92 | 0.95 | 0.91 |
| Overstates by more than one digit | 0.3% | 0.3% | 0.5% |

Teaching the rule adds nothing; the models already apply it. Their stated digit counts are conservative: 17% of run-B answers understate by more than a digit, 2% once the rule is given.

## 7 Implications

1. **Report FinQA against a repaired reference**, or stop interpreting differences of a few points. On our sample the measured error of a current model is almost entirely the reference's.
2. **Make the gold answer a set**: the union, over the admissible conventions of the question (sign, base, percent or fraction), of the interval implied by the rounding of the inputs. Score by membership. The interval is computable automatically for the 5,337 questions we release.
3. **Ask for the interval.** It costs two sentences, models answer it correctly, and it exposes false precision that a point answer hides.

## Limitations

The item-level results of Sections 3, 4 and 6 come from a stratified, not random, sample of 392 test questions†. The reviewers are language models; agreement between them is high, and a subset of reference errors is mechanically verifiable, but a human-checked subset is still needed. All runs use models from one provider. FinQA is public and may have been seen in training, although the models consistently contradict the published reference on the rejected items. The half-unit, independent-rounding model and the 1% tolerance are audit conventions; 416 test questions could not be analysed and are counted as determined. We study one benchmark.

## References to add and verify

- Chen et al. (2021), FinQA. EMNLP.
- Zhu et al. (2021), TAT-QA. ACL. Chen et al. (2022), ConvFinQA. EMNLP.
- Tang et al. (2025), FinanceReasoning. ACL. [verify authors and the 15.6% figure]
- Northcutt et al. (2021), Pervasive label errors in test sets. NeurIPS Datasets and Benchmarks.
- Gema et al. (2025), Are we done with MMLU? NAACL. [verify]
- Gittings (1991), rounding and growth rates. Economic Perspectives, Federal Reserve Bank of Chicago. [verify title]
- XBRL International, Calculations 1.1. [verify sections]
- Higham (2002), Accuracy and Stability of Numerical Algorithms, on cancellation.
- Reported FinQA accuracies of recent systems. [find and verify]
