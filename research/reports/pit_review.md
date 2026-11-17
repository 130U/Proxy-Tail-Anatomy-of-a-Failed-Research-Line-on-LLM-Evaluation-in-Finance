---
artifact: independent_adversarial_review
scope: T1.1 and PIT construction
source_files: [research/theory/notes.md, research/theory/pit_noninterference.md, research/pit/PROTOCOL.md, research/pit/pipeline.py, research/pit/test_pipeline.py, research/pit/run_checks.py, research/pit/seed_checks.py, research/pit/results.json]
theorem_ids: [T1.1, PNI1, PNI2, PNI3, PNI4, PNI5, PNI6]
issue_ids: [PIT-R1, PIT-R2, PIT-R3, PIT-R4, PIT-R5, PIT-R6]
commit: 8e4dd0b plus uncommitted PIT work
generated: 2026-11-16
generator: internal independent reviewer; mathematical proof review quick-start procedure
status: completed_with_external_scientific_gates_open
---

# T1.1 / PIT independent adversarial review

Date: 2026-11-16. Network access: no. Identity: internal independent review agent, not Fable; no Fable feedback was received or invented. No private text, labels or weights were read, and no main-line training was run. G0 has not passed. This report reviews only the mathematical propositions, the implementation of finite primitives and the constructive checks. It cannot serve as empirical financial evidence.

## 1. Conclusion and review scope

After the fixes, the conditional mathematical propositions PNI1–PNI6 pass this independent pen-and-paper reading. The type-equality bypass at the entry point of the reference implementation, found during this review, has been reproduced, fixed and re-checked. Within the reviewed scope, no unfixed implementation issue remains that blocks this **finite constructive prototype**. This does not mean that the whole program is free of defects or that all inputs are machine-certified.

The more important correction in this round is to separate four obligations: non-interference relative to the records, measurability in a given information model, historical source admission of the real versions, and identifiability of the clean comparator statistic. The first two cannot by themselves prove the last two. A checkpoint fixed after the fact can be treated mathematically as a constant, but that does not give it a historical source certificate. The finite future-append tests of the original WP1.2 cannot imply non-interference over all permitted inputs, and timestamp filtering cannot prove that the timestamps are true.

The advisor package files AGENTS, 00, 01, 02, WP1.2 of 06, and 07 were read independently, together with the original T1.1 and this round's PROTOCOL. The quick-start method of "academic research - mathematical proof review" was used: normalize the quantifiers and input domains, check the factorization dependencies, construct counterexamples, and record the fixes and the open scientific gates. The ledger for this single-proposition review is kept in this file. All constructive numbers are mathematical witnesses or explicitly labeled finite program checks; no authority is borrowed from the literature.

## 2. Attack list drawn up before implementation

| ID | Minimal attack | Boundary that must hold |
|---|---|---|
| C1 | An old document is overwritten after the cutoff by a new version with the same ID | Project by knowledge time first, then choose a version among the visible versions; do not take the latest version first and filter afterwards |
| C2 | A tombstone after the cutoff deletes an old document | A future deletion must not retroactively change the old snapshot; a past deletion and a future re-creation are separate version events |
| C3 | The full text is unchanged, but source, core, label, family or weight is modified only in the future | Every field that can affect training shares the knowledge time of the complete version, or is versioned separately |
| C4 | Two old duplicate clusters are bridged by a future document | Project first, then build the duplicate graph; do not delete future nodes from whole-corpus clusters while keeping the connectivity the future created |
| C5 | The current candidate grid, regularization cost or validation-set rule was chosen in the future | The configuration, source code and selection rules must themselves be historically measurable or exogenous; a comparison with fixed parameters cannot certify where they came from |
| C6 | The full-log hash, length, future count or iteration order is used to determine the seed/sampling | The stable result depends only on the history projection and frozen exogenous inputs; the operational envelope must not flow back into it |
| C7 | A future payload is invalid, or a future event ID duplicates a historical one | Future payloads should not enter the validation of the old snapshot; the valid input domain for headers and the rules for visible conflicts must be stated explicitly |
| C8 | A Snapshot is forged by hand construction or dataclass.replace, or given a different cutoff | Check the construction entry point and the time binding; do not infer from the class name that it is already a valid historical snapshot |
| C9 | Empty history, empty train/dev, equal cutoffs, reversed order, tied versions, boolean times | Fix all boundary behavior, the canonical ordering and the type domains in advance |
| C10 | Contamination removal uses future ground truth, or the record time is backfilled | Historical measurability of the deletion choice and trustworthiness of the knowledge clock are additional premises; they cannot be inferred from the full text being old |
| C11 | The same seed / same output hash is taken as proof of whole-program determinism or of identical inputs | Guarantees apply only to explicitly stable bytes; reverse binding through a hash is not an unconditional mathematical equivalence |

## 3. Important theoretical issues found and required fixes

### PIT-R1 (S1): randomness that is only marginally independent of the future can still leak

The original T1.1 summarized the randomness as "Ω is independent of future data". If this is used to claim further that the randomness introduces no future information, the condition is not enough. Take a historical bit H and a future bit B that are independent and uniform, and let Ω = H xor B. Ω is marginally independent of B, but the training output θ = H xor Ω is exactly B. This counterexample is an exact mathematical witness, not a fitting experiment.

Fix: separate three propositions. Measurable composition gives θ ∈ F_t ∨ σ(Ω), which needs no independence. Path non-interference under one fixed seed needs no independence either. "The randomness provides no additional future information" needs conditional independence given the history; independence from the whole data world is a stronger, sufficient condition. The history can itself predict the future, so one cannot claim that θ is marginally independent of the future or that it cannot predict the future correctly.

Communication and status: sent to the root agent and the theory agent. Lines 39–43 of notes.md and the corresponding paragraph of notes.tex were read and checked, and the fix has propagated. The root agent added seed_checks.py, which uses Fraction to enumerate all 16 deterministic boolean seed maps on uniform, independent historical/future bits: 6 pass marginal independence, 4 pass conditional independence given the history, and the difference is exactly XOR and XNOR. The reviewer ran it independently and got the same result. This is an exact enumeration on a specified finite domain and is not generalized into a computational proof for all probability spaces.

### PIT-R2 (S2): set-theoretic factorization is not automatically measurable factorization

"The output is equal on each fiber of the same history projection" guarantees that F = G ◦ H exists in the set-theoretic sense. On an arbitrary measurable space with an arbitrary prescribed snapshot σ-algebra, it does not automatically guarantee that G is measurable. The fix can use a finite/countable canonical byte domain with the discrete σ-algebra, a suitable quotient σ-algebra, or a separate proof of a measurable-section / measurable-factorization condition. Alternatively, the algebraic proposition can be kept strictly separate from the stochastic measurability proposition.

Communication and status: the theory agent was notified, and Sections 1 and 2 of the new draft were read and checked. The new draft uses a countable canonical byte/JSON domain with the discrete σ-algebra and states separately the conditions needed for general spaces; CLOSED-VERIFIED. The restricted result was not quietly passed on as a conclusion about arbitrary reals or arbitrary measurable spaces.

### PIT-R3 (S1, statement in the original WP1.2): finite future-append tests are not a proof over the full domain

Any finite test set can always be passed by a program that reads the future only on untested inputs. Even if the property held abstractly for every valid single future append, extending it to every history-equivalent world would also require that the valid history projection can itself be an input, step-by-step closure under finite extensions, or connectivity of extensions within the same fiber. These premises cannot be omitted on a general input domain.

Fix: the pen-and-paper proof states the full-domain conditions explicitly; the source review explains how the implementation is constrained by these conditions; the finite tests report only the inputs and components actually covered. PNI2 states the base-log and finite-extension reachability conditions explicitly and gives a counterexample with a physical end-of-file append. PNI3 proceeds by induction over deterministic components with closed inputs. The scope/limitations sections of PROTOCOL, README and the runner all state that the checks are finite; CLOSED-WEAKENED. The advisor's original files were not rewritten to make it look as if they had this restriction from the start.

### PIT-R4 (open scientific gate): non-interference with respect to records cannot certify real history

If a future document is written with knowledge_time ≤ cutoff, a correct projection will keep it too. If the knowledge times of the trusted core, the labels or the configuration are not true, there is leakage as well. Event time, accounting period, database record time, public availability and system knowledge time are different concepts.

Fix: this round's conclusion is restricted to record non-interference, valid for the given event headers and complete versions. Real history needs independent source evidence, version integrity, time-zone and clock conventions, label availability, core eligibility, the time at which the configuration was set, and any necessary sampling audit. This item was not eliminated by the constructive tests and remains open.

### PIT-R5 (S1, implementation entry point): dataclass equality validation allows type forgery

The first version of `_validate_snapshot` rebuilt the valid snapshot and then only compared `rebuilt != snapshot`. Python dataclass comparison uses ordinary field equality, and `False == 0`, `True == 1`. So `label=0` in a valid document could be changed by `replace(doc, label=False)` into a boolean label that the original event validation explicitly rejects, and `core=True` could be changed to the integer `1`. With `visible_history_bytes` unchanged, `run_pipeline` still accepted the input, and the bytes of `snapshot.json` changed. `replace(snapshot, cutoff=True)` also passed the entry point for the call argument `cutoff=1`.

Reproduction before the fix: the three inputs above were constructed on a hand-made record with `knowledge_time=1`, `core=True`, `label=0`. When the reviewer ran them, all three were accepted. The record is a hand-made public fixture and contains no private data. This shows that the anti-forgery validation for inputs with the same canonical history bytes was not strict. It does not refute the mathematical factorization proposition for the trusted construction entry point.

Fix and re-check: the entry point at `pipeline.py:175` now checks types strictly field by field, checks the immutable storage form, and compares the history bytes and the canonical serialized bytes of the documents. The State check at `pipeline.py:207` also adds type checks. `test_pipeline.py:111` adds a regression test for the bool/int bypass. The reviewer reran the original three attacks and got `snapshot cutoff must be an integer, not bool` and, twice, `Invalid document core/label type`; all were rejected. CLOSED-VERIFIED. The README also records the gap in the first round and does not hide the insufficient coverage of the first tests.

### PIT-R6 (S1, scope of interpretation; S2 for the endpoints): measurability cannot replace the admission of real sources

The first version of PNI6 in the new draft interpreted the wrong knowledge time in the two-world, same-observation example as "the PNI4 measurability premise is not satisfied". This step does not hold. In a probability space that contains only these two worlds with the same log, the history projection is constant, and hence measurable with respect to any information σ-algebra. Similarly, fixing some after-the-fact checkpoint as a constant does not prove that it could have been built from compliant material at the time.

Fix: the new draft adds, at `pit_noninterference.md:140`, a dedicated distinction between measurability and historical constructibility. Line 174 changes the two-world example into a violation of the authenticity of per-version source admission, without claiming that it is necessarily non-measurable. The necessary condition for identifying the clean statistic still holds: if the same observation is compatible with clean values 0 and 1, a reliable closed interval must contain both. Line 162 also adds a non-empty set of compatible worlds, a bounded statistic and closed-interval output, and makes explicit the domain of validity for the infimum/supremum endpoints. The corrected proposition, proof and example were read and checked; CLOSED-VERIFIED. Future main reports must still treat provenance as a separate scientific gate.

## 4. Reading of the implementation and the theory draft

### Mathematical dependencies and item-by-item assessment

| Unit | Location | Result and necessary conditions |
|---|---|---|
| PNI1 | theory/pit_noninterference.md:49 | Being constant on fibers is equivalent to a unique factor on the image space; measurability additionally uses the countable discrete-space condition |
| PNI2 | Same file:64 | The forward direction holds directly; the reverse direction relies on reachability through finite extensions of a valid common base log, and the induction includes the zero-length case |
| PNI3 | Same file:78 | Same initial state, closed inputs, determinism, finitely many stages and fixed serialization give stage-by-stage equality; this does not follow directly from "there is a cutoff parameter" |
| PNI4 | Same file:130 | Composition of a measurable random vector with a measurable function; by itself it needs no independence of the randomness, and it does not certify provenance |
| PNI5 | Same file:148 | Conditional independence given the history is preserved under historically measurable transformations; a bounded-function/monotone-class argument applies |
| PNI6 | Same file:164 | A closed interval that contains a non-empty, bounded set of compatible values must contain its infimum and supremum; the scope of the two-world witness and of the union bound for random coverage is now explicit |

Dependency chain: the factorization semantics of PNI1 → the finite composition construction of PNI3. PNI2 independently clarifies the quantifier over appends. PNI4 additionally requires adaptedness in the real information model. PNI5 further requires conditionally exogenous randomness. PNI6 separately limits identifiability under uncertified sources. No circular dependency was found. All six were reviewed as complete conditional propositions. No non-trivial proof sketch that would need hidden completion was found; the number of unclosed sketches is zero. The above is a human-readable pen-and-paper review, not certification by a proof assistant.

### Implementation checks and attack coverage

`canonical_history` (pipeline.py:114) is the only main-flow component that reads the complete log. After reading the valid headers it first projects by knowledge_time, and only then validates the visible bodies, hashes, unique event IDs and complete state. It replays versions and tombstones in the same canonical order. Future payloads are not read; even if they repeat an old event ID or carry invalid objects, the old result is not affected. Visible conflicts are rejected deterministically. Corrupted future headers are explicitly outside the committed domain.

Filtering, deduplication, sampling, splitting, vocabulary fitting and hyperparameter selection are at pipeline.py:224, 236, 277, 285, 297 and 310 respectively. All later calls receive only the historical State and exogenous parameters. Future duplicate bridges do not take part in building the historical graph. The vocabulary uses only train. The development unknown-word rate and the capacity penalty use Fraction. With empty development tokens, the frozen first candidate is chosen explicitly. Outputs are serialized uniformly from pipeline.py:336, and the ten stable outputs contain no full-log length, future count, system clock or full-log hash. The history hash is a digest of all visible events, and the theoretical history equivalence also uses all visible events, so the two agree.

The declared scope of the six stages is the composition of states produced through the main entry point. An arbitrary hand-made State is not an independently certified object, as the README states explicitly. One cannot infer from an identical `historical_hash` that an arbitrary hand-made State really comes from the same history. The fixed configuration, source code, Python/Unicode environment and external dependencies are still preconditions for deterministic runs. The current checks do not cover arbitrary cross-version runs, concurrent modification of inputs or third-party model training.

### Record of checks actually run

Budget: the PROTOCOL's budget was kept: CPU only, no GPU and no training, at most one minute for constructive checks. The reviewer did not repeat the main runner's full set of cases. Only the entry-point attacks, the relevant unit tests and the exact seed enumeration were rerun independently. In addition, read-only arithmetic and hash checks were done on the existing results.

| Check | Evidence level and actual result | Strict scope |
|---|---|---|
| `python -X utf8 -m unittest research.pit.test_pipeline -v` | Our finite constructive check; run independently by the reviewer, all 18 pass, unittest reports 0.120 seconds | Includes 72 specified cutoff/future-extension combinations; not the set of all possible futures |
| Snapshot type bypass in the first version | Our finite constructive check; all three inputs accepted before the fix, all three raise ValueError after the fix | Boolean cutoff, integer core and boolean label on the same hand-made record |
| `research.pit.seed_checks.run_checks()` | Our finite exact enumeration; 16 boolean seed functions, 6 marginally independent, 4 conditionally independent, difference XOR/XNOR | Fixed world with independent uniform H/B; Fraction arithmetic |
| Saved results of the main runner | Our finite constructive check; read-only recomputation confirms 30 = 2 × 3 × 5 base cases, 210 pairwise comparisons, 2,100 full-output byte comparisons, and development documents in 29 base cases | Hash comparisons are not passed off as byte comparisons; some `existing_future` cases add no records at the largest cutoff, so 210 is the number of compared pairs, not 210 distinct non-empty appends |
| Wrong-time witness | Synthetic ground-truth check of the main runner; three records with wrong times are admitted, and the future-append invariance still passes | Shows directly that record non-interference is not enough to certify real availability; no financial model was run |
| Summary of existing public source metadata | Recomputed on the existing fixed, non-random set of 10 saved source records; counts of claimed release dates up to 2015/2020/2025 are 3/6/10, proven historical byte versions are 0 in each case, and local acquisition times claimed ≤ cutoff are 0 in each case | Only a gap in the historical version evidence; it cannot be used to infer that the content was not public at the time; it is not a population sampling audit or a real text pipeline |

The 5 source_hash values of the main runner match the current files. The summary of the old source_audit and the selected metadata counts above were also checked by the reviewer. The review read no private headlines or labels; it only recomputed the existing public source-audit metadata. The full project tests are treated separately in the incremental verification below and are not passed off as an independent rerun.

### Digests of the reviewed snapshot

The SHA-256 values below bind the snapshot read in this review. They are meant for detecting later changes and do not serve as an unconditional cryptographic proof of input equivalence:

| File | SHA-256 |
|---|---|
| theory/pit_noninterference.md | `1dfbf8d487decac60f1230cec27c01cd0ee1041b743cbbcbd6b926a3653e11e8` |
| pit/pipeline.py | `b6902b9e68a00bde1b32c39e4d7688e6f81ea6aab48b78e43fd9621f0aba1847` |
| pit/test_pipeline.py | `144e57fe38dd66ceef0730ac8023837b7d51244cf64ea4e5ad33d295bf91fd41` |
| pit/run_checks.py | `4d2494b14f6dcec3442315a2b3bcb37a364f76596ea60b37bf55bd5ecafa6206` |
| pit/seed_checks.py | `35177c39d0a62a165721d2285c195affc1b3b38fcd1d9ef9a33b51b41129d6d7` |
| pit/results.json (after integration; only the timing changed) | `bd129035930c9fe82b186ea0be2de9bb37b0f5667f13d2c801279cc7c78c70ed` |

### Incremental verification after integration

After the root agent completed the non-training integration rerun, the reviewer checked `research/reproduction_log.json` read-only. All 10 commands return 0; unittest reports 92 passed, and the source-parsing self-test reports 10 passed. The command table contains no `--train` or ablation. This is a check of the run record, not a re-execution of these 102 checks by the reviewer.

The latest main runner time is 1.4966408000036608 seconds. After the reviewer replaced the only `elapsed_seconds` value in the latest results bytes with the first run's 1.4680437999995775, the first run's digest `ace287b0daf795d76f837d8abb0bf6ed7eec5241139ff574cf646ed44b9303c3` was recovered, and the five source digests all still match. So this increment is only an operational timing update; the original numbers, comparison targets and conclusions are unchanged. This check uses existing digests as evidence of version consistency and does not claim a cryptographic collision-freeness theorem.

The [run record](../pit/record.md) and the [round-5 progress report](2026-11-16-round5.md) were read and checked. They keep the stated limits: the checks are finite, wrong times are still admitted, there is a gap in the source evidence, measurability is separate from real admission, and there is no Fable feedback. The README now restricts byte-for-byte determinism to the same Python/Unicode runtime environment. The acceptance status of the existing permission negative result was checked against completion_audit, and its wording is corrected in the next section. The earlier completed status is not withdrawn just because this round did no training.

## 5. Open scientific gates

- G0 has still not passed: the real family-cluster intervals for the old 24M model and the three same-test-set baselines specified by the advisor are missing, and this round's PIT primitives do not fill that gap. The synthetic permission negative result with four configurations and three seeds, as allowed by WP0.2, has been accepted as complete; its scientific question and the validity of its control remain partial. The latter must not be misstated as "the permission ablation has no result", and a positive gain is not required for acceptance. See the WP0.2 and G0 rows of completion_audit.
- There is still no proof of historical versions/timestamps for real sources, and no certificate for a real trusted core.
- There is still no end-to-end certification of a complete tokenizer, model training, shard training, checkpoints or the model-selection process. This round's finite vocabulary primitive must not be presented as certification of these components.
- Novelty has not been checked online. Novelty cannot be inferred from passing code or from an internal mathematical review.
- There is no non-empty backtest certificate on real financial data, and this round makes no performance comparison on that basis.
- There is no full-domain formal verification in a proof assistant such as Lean. Python regression results can support only explicit finite inputs.
- The package waiting to be sent to Fable and the internal collaboration should be recorded separately. This report is an internal review, not an outside reviewer's opinion.

## 6. Needs a decision from the PI

This review did only authorized local mathematical and constructive checks, and no new decision is needed. Real-source access, later empirical work and sending materials outside continue to follow the current project constraints and were not done in this review.
