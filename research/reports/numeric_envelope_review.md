# Round 6 P2 semantic envelopes: independent internal review

Date: 2026-11-16. Review baseline: `research/certifiable`, `8e4dd0b`; the object of review is the uncommitted new files on top of it. Status: **conditional mathematics and finite implementation checks passed; no open S0/S1 defects; validity on natural text not verified.** "Independent" here means independent derivation and counterexample checking by another agent; it is not certification by Fable, an external referee or a proof assistant. Fully offline throughout; no private text, labels or weights were read, and no model was trained.

## Conclusion

SE1–SE6 hold under their respective explicit assumptions: independent rectangles with positive denominators give tight ratio/affine images; middle classes must be checked for interior peaks; the joint result is the minimal coordinate box; the width and acceptance-rate bounds apply only to the specified candidate specification. The code uses exact rational outer envelopes for the exponential tail terms and all subsequent operations, and can return a result only once the budget is reached. No implementation defect was found that passes off numeric centre values as certified endpoints, misses an interior peak, or mixes different declared targets.

What is genuinely new in this round is a reviewable interface for propagating ambiguity, together with veto conditions. Whether the candidates cover the true semantics, whether they are too wide, whether the class direction is reasonable, whether the probabilities are calibrated, and whether this beats a symbolic rule are all not resolved by mathematical correctness. G0/G1, the real P2 parsing experiment and the paper's novelty cannot be upgraded on this basis.

## Review scope and budget

The scope is T2.2 of `theory/notes.md`, the finite semantic candidate propositions of `paths/PATH_02_numeric_sensitivity.md`, and this round's pending `theory/semantic_envelopes.md` and `numeric/semantic_envelope.py`. The method of the "academic research - mathematical proof review" procedure was used: proposition by proposition, assumption propagation, boundaries and counterexamples; all review ledgers for this review are merged into this file.

The advisor files AGENTS, 00, 01, 02, 06 and 07 were read. Under 00 §5 and Phase 1 of 06, theory may proceed while G0 has not passed; the execution checks here are only mathematical/implementation soundness checks on hand-made rational examples, and are not evidence that the natural-language P2 main-line experiment has been completed.

Budget before running: mainly single-core CPU, GPU/VRAM 0; no training tokens; no more than 5 minutes; only hand-constructed rational inputs, with independent scripts run through standard input and no separate outputs created. The budget and the later test numbers are all labelled "our experiment: round6-numeric-review".

## Up-front counterexamples and list of burdens

| ID | Improper conclusion that can be broken | Counterexample or necessary condition |
|---|---|---|
| C1 | For a middle class it is enough to compute the interval endpoints | With thresholds −1, 1 and η∈[−3,3], the middle-class maximum is at η=0; the endpoint values are strictly smaller. |
| C2 | The width of the envelope over any candidate set is ambiguity that text cannot remove | If the true coupling is x=b∈[1,2], the true growth rate is always 0; the independent-rectangle abstraction gives [−1/2,1]. One can only claim the minimal width under the chosen candidate specification. |
| C3 | Monotonicity within each branch implies monotonicity across inputs | η₁(t)=t, η₂(t)=t−100; when the input changes and the selection switches from branch 1 to branch 2, the output can decrease. The branch correspondence, context, thresholds and direction must be fixed, or there must be a separately proven pairing contract. |
| C4 | Every vector in the minimal coordinate box is jointly reachable | On a non-degenerate η interval, the maximum of the first class and the maximum of the last class are reached at opposite endpoints; the upper corner of the box usually does not even lie in the probability simplex. |
| C5 | A numeric outer envelope proves that semantic parsing is correct | A candidate set that misses the true baseline, period, metric, direction or context can still produce an arithmetically flawless certificate; the coverage event must check the complete object. |
| C6 | Raw numbers have a uniform positive direction or a fixed Greek upper bound | At b=0 the ratio is undefined; for b<0 the x direction flips; as b→0⁺ the derivative with respect to raw x can be unbounded; for x<0 the direction with respect to b is the opposite of that for x>0. |
| C7 | A comparison label needs a learned ordered-probability head | If the label is defined by sign(x−b), the gold tuple plus the sign rule already gives the oracle label; the necessity of an ordered head and of training from scratch has not been established. |
| C8 | A numeric outer bound crossing the width gate proves that certification is impossible | If the true width lies inside the numeric envelope and the envelope straddles τ, it can only be marked undetermined; numeric slack must not be mistaken for a minimal-width lower bound above τ. |
| C9 | Any class coordinates of different branches can be merged | Each branch must have a shared, frozen task target and the same meaning of the ordered classes; equal dimension does not guarantee that the coordinates have the same semantics. |
| C10 | The audit α equals the failure probability of each output | r is the deployment risk under the final acceptance event; α is the coverage error of the randomized audit upper-bound procedure. The envelope failure risk is at most the semantic miss risk, not necessarily equal to it. |

## Proposition-by-proposition review and dependencies

The line numbers below refer to [semantic_envelopes.md](../theory/semantic_envelopes.md) at the time of review; all proof units are classified COMPLETE, and the local mathematical verdict is PROVABLE AS STATED / Verified under stated assumptions. The actual parsing premises were not also marked Verified.

| Unit and location | Strategy and key checks | Conditions and verdict |
|---|---|---|
| SE1, L27–38 | Monotone in x, directed in b according to the sign of x; the continuous image of a compact rectangle is connected, so there is no gap between the corner extremes; negative/zero slope is included separately | Positive denominators, independent rectangles; only outer under additional coupling. Passed |
| SE2, L40–80 | σ′=1/(2+2cosh) is an even function decreasing in distance; the midpoint of adjacent thresholds is the unique peak; the interval minimum is at an endpoint; the extremes of each coordinate can be realized separately | Shared task/schema, fixed thresholds, full η interval; the box is not the joint image. Passed |
| SE3, L82–101 | The two reachable ends directly force width ≥D; shifting to the midpoint gives D/2 + distance; counting per task with frozen weights gives an exact upper bound on accepted mass | "Sound for all candidates" is a specified specification and cannot be upgraded to an information lower bound for natural text. Passed |
| SE4, L103–111 | A non-singleton label set breaks every deterministic prediction; the minimum label mass is ≤1/s, and uniform allocation attains the worst-case error 1−1/s | The adversary chooses the label before the prediction's randomness is realized; the target must truly be defined by the sign rule. Passed |
| SE5, L113–137 | After fixed branches are ordered term by term, min/max preserve order; swapping z,z′ gives Lipschitz; the derivative of the middle probability is the difference of two numbers in [0,1/4] | A shared edit domain and a true branch correspondence; the jump counterexample with a dynamically changing set holds. Passed |
| SE6, L139–171 | A∩E⊆A∩Cᶜ, then divide by the same P(A); conditional union bound; inversion of the low-count tail of the binomial CDF | Frozen final acceptance rule, representative IID acceptance audit, correct reference. r_C and α are kept on separate levels. Passed |

The dependency chain is A0/positive-baseline domain → SE1 → SE2 → SE3; SE4 depends only on the task definition and the exact difference set; SE5 depends on a fixed branch mapping and the probability derivative bound; SE6 depends on the earlier certificates being sound within the coverage event, plus a sampling assumption. No circular proof was found, and statistical coverage was not swapped for a per-output posterior probability.

Two S3 clarity issues have been patched by the author and re-checked: the audit now explicitly requires 0<α<1 and fixed n≥1, and lists U=1 separately for n=0; "differentiable almost everywhere" is restricted to the interior of real intervals / open Euclidean domains. The patches did not change the core propositions or add hidden empirical assumptions. The strict decrease of the binomial CDF in p can also be checked directly: for x<n its derivative is −n·C(n−1,x)·p^x·(1−p)^(n−1−x)<0, which is enough to support the author's unique-inversion-root argument. Sketch detection found 0; there are no key proofs left to expand.

## Review of the numeric implementation

Key locations reviewed in [semantic_envelope.py](../numeric/semantic_envelope.py): the exponential tail bound from L101, the sigmoid from L126, the point probabilities and extremes at L198–241, the branch join at L267–284, and the width gate at L297–311.

For y≥0, the code's total is S_n=Σₖ₌₀ⁿ y^k/k!, and next_term is y^(n+1)/(n+1)!. The ratio of successive later terms is at most y/(n+2), so for y<n+2 the remainder is ≤next_term/(1−y/(n+2)). This gives strict rational upper and lower bounds; negative arguments are enveloped in reverse through the reciprocal of the positive value. The two stable mappings of the sigmoid in terms of exp(|y|) are monotone, and when that exponential is ≥1 the derivative magnitude is ≤1/4. Point probabilities internally use tolerance/4; middle classes are computed by cross-subtracting upper and lower ends and intersecting with [0,1]; min/max do not enlarge the largest single-term numeric width. So the uncertainty width of every final extreme is controlled by the tolerance, while the semantic range itself may be very wide.

The width gate first gives upper and lower bounds on the width of each exact coordinate, then takes the maximum; it passes only if the upper bound ≤ the threshold, fails only if the lower bound > the threshold, and is otherwise undetermined. Equality, zero width, budget exhaustion, empty branches, duplicate branch IDs, different K/target/class labels, float/bool and non-positive denominators all have rejections or boundary checks. If any branch computation fails, the whole computation raises an exception; failed branches are not silently dropped.

This only verifies that the declared model/domain agrees with the target schema. The default example target/class labels are not a semantic proof; the public dataclass is also not an authenticated format against maliciously forged certificate objects. Users must still construct outputs through the calculator and maintain the listed premises. The program accepts negative slopes in order to cover general affine branches; this does not mean it automatically issues global monotonicity certificates.

## Results of independent execution

The source of all numbers is **our experiment: round6-numeric-review**; all are deterministic checks on hand-made rational inputs.

| Check group | Result | Meaning and limits |
|---|---|---|
| Independent rational reference cross-computation | 258 exp/sigmoid/exact-extreme assertions pass; inclusion checks at 24 branches and 729 interior probability coordinates pass; 0.860 seconds timed within Python | The reference first halves the absolute argument repeatedly until ≤1, brackets exp with an exact 80th-order Taylor polynomial and a rational geometric remainder, then recovers by repeated squaring; this differs from the production code's direct-argument Taylor iteration path. Covers ±50, very small rational arguments, positive/negative/zero slopes, interior peaks, narrow threshold spacing. No guessing of libm error |
| Ratios and rejection boundaries | 65 assertions pass | Negative/zero/positive x, positive unit scaling, non-positive denominators, invalid types/arguments, budget exhaustion, different K / duplicate IDs, sign labels and conflict rejection; also exact verification that (19/20)^59<1/20<(19/20)^58, which is only the mathematical threshold of the zero-finding binomial budget |
| Final schema and width boundaries | 8 assertions pass | Different task / class orders rejected; exact zero-width gate passes; equality of the numeric lower bound and intermediate thresholds remain undetermined; fail only when strictly too wide |
| Independent re-run of the author's formal tests | All 14 unittests pass, 0.103 seconds | The formal tests also use a 96th-order Lagrange remainder reference with e^y≤3^ceil(y), so they are not pure self-verification relying on the same tail bound. Finite passes still cannot replace formal program verification over all inputs |

To reproduce the formal tests: at the repository root, use the adjacent original repository's `.venv/Scripts/python.exe -m unittest research.numeric.test_semantic_envelope -v`. The independent exp/sigmoid reference arguments are each integer of Python `range(-150,151,7)` divided by 3, plus 0, 50, −50, 10⁻⁸, −10⁻⁸. The random branch sequence uses Python Random(240616); the 24 IDs use 1, 2, 4 thresholds in turn, with thresholds i−2; ID 3 is changed to ±10⁻¹⁰; each branch draws in order the lower end of g `randint(-8,0)/2`, the upper end of g `randint(0,8)/2`, slope `randint(-3,3)`, offset `randint(-2,2)`, and each η interval takes 9 equally spaced points. So there are 216 interior support points and 729 coordinate inclusion checks, and the two must not be merged into a single count. The independent reference and boundary checks were run through standard input and produce no data files; this report is the only new review output.

Supplementary static check of the parent task's [run_checks.py](../numeric/run_checks.py) and [results.json](../numeric/results.json): they record the frozen 25 equally weighted hand-made cells; width gates 0.05, 0.10, 0.20 have 2, 3, 5 passes respectively, 0 undetermined in each case, and the remaining 23, 22, 20 cells respectively are proven too wide; the main gate is 0.10. The source code agrees with the source hash inside the results. Interior peaks, retention of discrete branches, x=b coupling, 5 positive unit scales, branch-selection jumps, sign agreement/conflict and the numeric-bound probe all match the scope of the report. This is an independent check of the parent task's run record and logic; its 25 cells were not re-run, and the hand-made proportion was not treated as an acceptance rate on natural text. It was found that the protocol had miswritten the 729 coordinate checks divided by 3 as 243 support points; the author has kept an erratum and changed this to the actual 216 points, and the protocol hash in the results has also been updated and re-checked as consistent. This is a record-count issue and does not change the numeric conclusions.

## Issues closed and limits kept

The improper versions of C1–C10 are all blocked by the current premises, counterexamples or rejection interfaces; they are not conclusions the current draft still claims. The two theoretical S3 items, the count erratum above, and the boundary wording in the Lagrange reference text that y=0 should take equality have all been re-checked and closed; the last item changed only the README and a test docstring, not the execution logic, so the same tests did not need to be run again. There are no open S0/S1 items; this is an internal conditional verification result, not external endorsement.

Items not yet verified must be kept: the natural-language parser has not been built; no audit of real complete semantic gold labels / candidate coverage has been done; it has not been verified that unit words and number words cannot bypass and change the context; real task direction, calibrated probabilities, the deployment distribution and semantic branch probabilities have not been established; it has not been proven that an ordered head or training from scratch beats the symbolic rule; no literature search was done in this round; the Lipschitz constant of a general transformer has not been proven. The mathematical conditions holding here does not remove these burdens, and does not mean G0/G1 have passed.

## Reviewed versions

Source file SHA-256 (if a file changes later, assess whether re-review is needed):

- `theory/semantic_envelopes.md`: `a7bb88f3db025b7e1c8c9779ccf5350bedbd66d0d08b3378f3bdaa4c0c49661a`
- `numeric/semantic_envelope.py`: `78743f8efcdd9f2ec01f99b11df37ab3a181e7e416c5f658092c584f80316e84`
- `numeric/test_semantic_envelope.py`: `b356b2ce1089d0d731ede0f0b5b9dd890075491a2927d245f816a1f3755d0651` (after execution, only the ≤ in a docstring was corrected)
- `numeric/run_checks.py`: `c1ecf3bf2110982a883cc75e3b2f2420784008482fc8f211f41663e22f4b4b24`
- `numeric/PROTOCOL.md`: `3b6bd3f819f91e8e271ffe2386dad8b5f6d609325333fa18ca70ecdbf26a2163` (consistent with the results record after the count erratum)
