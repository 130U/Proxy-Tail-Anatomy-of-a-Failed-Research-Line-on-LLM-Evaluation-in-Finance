# Advisor memo: why redo it, what to do, what to do first

To Codex.

The work packages and question list tell you **what** to do. This memo explains **why**, so that where I have not written something down, you can still make the same judgment I would. After reading it you should be able to answer three questions: what is this project's contribution? Why are we the ones to do it? If there is only time for one thing, which one?

---

## 1. Diagnosis: why this project looks like a toy

What marks a toy project is not small scale. It is two things: the question it answers already has better answers, and nothing in its design is necessary.

Looked at by this standard, the current state is:

- **The question already has better answers.** For three-class headline sentiment, open-source large models already do well zero-shot or few-shot.
- **The design is not necessary.** Training from scratch brings no benefit for this task. The 24M scale is a result of compute limits, not something the problem itself needs.
- **The evidence cannot tell "effective" from "noise".** The gap between 0.655 and 0.609, on a dev set with only 10 bearish items, is very likely within sampling error. WP0.1 will quantify this.
- **Engineering and research investment are out of balance.** A large amount of the code in the repository is Colab / Kaggle plumbing, notebook generators and export scripts. These are necessary hygiene, but they are not contributions.

But three things are good, and they happen to be exactly what the new direction needs:

1. **The `as_of` field and the discipline of "split families first, then derive views".** This is the data precondition for the information-set certificate.
2. **Deterministic training, checkpoint-resume semantics, global denominator bookkeeping.** The shard-aggregation certificate requires each shard's training to be a deterministic function of its data. The earlier engineering is exactly the precondition for the certificate to hold.
3. **Semantic permissions.** This is an early form of the sensitivity specification.

So this redo does not tear everything down and start over. It **raises the existing engineering hygiene to the status of preconditions for certificates**. Make this point clearly in the writing; it gives the old work a new meaning.

---

## 2. Topic-selection logic: three filters

**Filter 1: necessity.** Keep only questions that "can only be answered by training a small model from scratch". There are only four kinds of such questions:

- Controlling the information set: a pretrained model has seen the future, and this cannot be removed afterward.
- Controlling the architecture: Lipschitz constraints, exact invariance and monotonicity must be written into the architecture before training.
- Controlling the representation of numbers and units: changing the tokenizer and embedding is only free when training from scratch.
- Full inspectability: a small model allows complete mechanistic analysis, and its training data is fully known.

**Filter 2: comparative advantage.** All of Theodore's other work is certified bounds. The new direction should let this method be reused directly: define a quantity, prove a bound, give an executable certificate, and show on real data that the bound is non-vacuous.

**Filter 3: robust to compute competition.** The contribution must not be easily overtaken when others double their compute. "A bigger model is more accurate" will be overtaken; "this bound holds under these assumptions" will not.

The intersection of the three filters is: **a certifiable financial language model (Certifiable FinLM)**.

---

## 3. Core thesis

**Thesis:** for small financial language models, valuable progress is not making them more accurate but making the conclusions about them testable. Small scale makes certificates computable, and training from scratch makes the premises of the certificates controllable.

The three research questions (RQ1 information set, RQ2 sensitivity, RQ3 deployment risk) are in section 2.2 of `00_CODEX_BRIEF.md`.

---

## 4. Unifying framework: the certificate chain

This is the central concept of the whole project. Please understand it first.

Any conclusion about a model depends on a chain of links. Take this sentence:

> "On events after 2019, the model's backtest hit rate is 0.58, with no look-ahead bias."

It depends on four links:

1. The data pipeline admits only documents with timestamp ≤ t. This is a **constructive link**, guaranteed by code audit and tests.
2. The timestamps themselves are correct, or not wrong by much. This is a **statistical link**, estimated by a sampling audit.
3. The effect of a small number of mislabeled documents on the model's output is bounded. This is a **bound link**, guaranteed by a theorem.
4. The sampling uncertainty of the test statistic itself. This is another **statistical link**.

**The strength of the conclusion is set by the weakest link.** A deterministic link has failure probability 0; the failure probabilities α of the statistical links add up (union bound).

The framework has three uses:

- **A unified narrative.** P1, P2 and P3 are the same idea applied to three objects. The paper and the repository therefore have one central concept, not a pile of tricks.
- **Allocating effort.** Always strengthen the weakest link. Spending a month making an already strong link stronger is waste.
- **Generating research questions.** Which link is weakest in practice? Can a statistical link be turned into a deterministic link through data selection or architecture design?

I expect one key finding (you need to verify it): in P1, the weakest link is not the model but the timestamp audit. See the "audit resolution limit" in section 5.1.

---

## 5. Two main lines and one side line

### 5.1 P1 information-set certificate (main line, flagship candidate)

**Current state.** The guarantee given by existing point-in-time models (ChronoGPT, DatedGPT) is "the training data was filtered by time". This is a statement about a procedure, not a certificate. It does not answer three things:

- (a) Did the tokenizer, hyperparameters, dedup model and instruction data also use only information from before t?
- (b) What if the timestamps themselves are wrong?
- (c) If k documents are wrong, how far can the backtest conclusion shift at most?

FinDendro (2026-11) further shows that a model's self-report of its own knowledge cutoff cannot be used to certify a backtest.

**My approach, in four steps:**

1. **Define** an F_t-measurable training pipeline. It must cover all components, not just the data. This is the constructive link.
2. **Turn "k contaminated documents" into a bound on the backtest statistic.** There are two routes:
   - **DP route:** document-level differential privacy → group privacy → a bound on the expected shift. I expect it to be essentially vacuous for k > 1; its role is to serve as a baseline.
   - **Shard-aggregation route:** hash the documents in the suspect window into m shards, train a small classification head on each shard, then vote. k documents can affect at most k shards, so predictions whose vote margin exceeds 2k are certified as unchanged. From this, the whole backtest statistic gets a proven interval. A small model makes this route cheap: a shard head can be logistic regression on frozen backbone features, and a CPU can train hundreds of them.
3. **Audit.** Spot-check the true availability time of n documents to get a confidence upper bound on the number of mislabels, then convert it into k.
4. **Connect into a certificate chain.** The final conclusion has the form: with probability at least 1−α, the **leakage-free backtest statistic** lies in [L, U]. This is the same kind of conclusion as the "proven price interval" Theodore gives in option pricing.

**Audit resolution limit (the point I think most deserves to be written as a proposition, T1.4).** When n documents are spot-checked in a suspect window of size N_W and zero mislabels are found, the upper bound on the mislabel count that can be certified is about N_W·ln(1/α)/n. For α = 0.05 this is about 3N_W/n, the rule of three. Shard aggregation needs at least m ≥ 2k+1 shards.

So: **if the suspect window is large, the certificate is necessarily vacuous, no matter how good the model is.** For example, with N_W = 10⁵ and n = 1000, k ≈ 300, which needs more than 600 shards, each getting only about 160 documents.

**Corollary: whether the certificate is non-vacuous is determined mainly by corpus selection, not by the model.** Corpora with **authoritative machine timestamps** should be preferred: EDGAR's acceptance datetime, FOMC release times, Federal Register publication dates. Then the timestamp link for most of the data becomes a deterministic link, and the suspect window is squeezed to be very small.

This is the design of **trust tiers**:

- **Trusted core** (authoritative timestamps): trains the shared backbone and the tokenizer.
- **Suspect edge** (sources with unreliable timestamps): small heads trained on shards, with the certificate given by shard aggregation.

**Contribution of this line:** a formal definition + a certificate-chain theorem + the audit-resolution-limit proposition + a non-vacuous certificate computed on real data + validation with planted contamination in a synthetic world.

**Risks:**

- Someone has already done it. Q3 and Q29 will check.
- Even with authoritative timestamps, the realistic k still makes m infeasible.
- The small heads after sharding are too weak, and almost no predictions are certified. This is **not** a kill condition ("how much accuracy must be paid to obtain a certificate" is itself a result), but it must be reported.

### 5.2 P2 sensitivity certificate: "the model's Greeks" (main line, most likely to give results fastest)

**Current state.** The existing semantic permissions are a soft loss: they make the model "tend to" be invariant or respond, but guarantee nothing. Hard guarantees for general text edits are difficult, because edits are discrete and of variable length. But for **numbers** and **units** exactness is achievable, because they are continuous and structured.

**Design (you need to verify every step):**

1. **Numeric channel.** Numbers in the text are replaced by placeholders; the values themselves go through a separate continuous channel (see xVal, FoNE, BitTokens; see Q12).
2. **Dimensions.** Only **dimensionless groups** are fed into the numeric channel: ratios of quantities with the same unit, growth rates, shares. By the Buckingham Pi theorem (Villar et al., JMLR 2023), the model is then **exactly invariant** to currency redenomination and reporting scale (thousands of yuan / millions of yuan). This is a constructive certificate (T2.3).
3. **Ordered monotone head.** Labels such as metric direction are ordered (down < flat < up); use a cumulative logit model. Write the latent variable as η = h(g, c) + λ·g, where h is λ-Lipschitz in g (the monotone networks of Kitouni et al.). Then:
   - ∂η/∂g ∈ [0, 2λ];
   - as g increases, the output distribution shifts up in first-order stochastic dominance;
   - |∂P(up)/∂g| ≤ λ/2.

   These are the proven "model's Greeks": the direction is proven and the magnitude is bounded (T2.2).
4. **Entity slots.** The target entity and other entities are all replaced by slots, so the model is exactly invariant to entity identity (T2.4). The cost is measured separately.

**Why this line suits Theodore:** it brings the language of derivatives in directly: bounded Delta, proven direction. There is an extra gain: the previously vague "label-preserving vs. distribution-preserving" becomes an order constraint of first-order stochastic dominance in the ordered model, with a clean formalization (T2.1).

**Two objections you need to take seriously:**

- **"If the numbers have already been extracted, isn't metric direction just a threshold on g?"** Yes. So the cleanest application is not "numbers with a complete comparison baseline", but cases where the text contains only some of the numbers, the comparison baseline is implicit in the wording, or the numbers are only one piece of evidence for a stance judgment. Please discuss this question seriously in T2.6.
- **Is "monotone in the numbers" a reasonable specification for stance?** Contrarian investors and "already priced in" are counterexamples. The monotonicity specification needs to be argued for. But even if monotonicity does not apply, **the Lipschitz bound itself still has value**: it gives a certificate for "how much the output can change at most when a number is rounded or its scale is misparsed by δ".

**The certificate chain applies here too.** All certificates are conditional on "numbers and units are parsed correctly". Parsing is a statistical link (Q32, WP2.1). If the parsing error rate is too high, the certificates are meaningless. This is the main risk of P2.

**Contribution of this line:** a numeric-channel architecture for financial language models; three kinds of constructive certificates (unit invariance, monotonicity, bounded Greeks); a comparison of soft and hard constraints, which incidentally answers "is the permission loss useful at all"; and an error bound for the parsing link.

### 5.3 Side line P3: deployment-risk certificate (quick win, at most 10% of effort)

After the model is calibrated, each prediction has an error probability p_i. A batch of new samples is clustered by event, with unknown within-cluster dependence.

With fixed marginal distributions, **the within-cluster comonotone coupling maximizes the total number of errors in convex order** (Dhaene et al. 2002). So the worst-case variance and ES both have exactly computable forms.

VaR is not monotone in convex order, so the worst-case VaR is not given by the comonotone coupling and needs methods of the rearrangement type. That is exactly the language used in Theodore's ES paper.

Note the distinction between two things. When estimating overall accuracy on a test set, if the clusters are known and numerous enough, the cluster bootstrap already handles the unknown within-cluster dependence. The value of P3 is in **forward-looking risk at deployment time**: what is the tail risk of the number of errors among the next batch of n events?

This may be a known result (Q20 will check). Even if it is known, it is the method that should be used in the Phase 0 evaluation foundation.

---

## 6. Answering Theodore's four original questions

Theodore asked: is there substantive innovation in architecture, core logic, functionality or research?

| Dimension | Substance | Corresponds to |
|---|---|---|
| Architecture innovation | Dimensionless numeric channel + ordered monotone head; trust tiers (the trusted core trains the backbone, small heads are trained on shards of the suspect edge) | P2, P1 |
| Core logic innovation | Certificate chain; audit resolution limit; "label-preserving / distribution-preserving" formalized as stochastic dominance | Section 4, P1, P2 |
| Functionality | Every output comes with certificates: whether the information set is compliant, an upper bound on the sensitivity to numbers, a proven interval for the backtest statistic | P1, P2 |
| Research | 2–3 theorems or propositions + a non-vacuous certificate on real data + a technical report | All |

Also make clear **what does not count as innovation**: a more accurate model, a larger scale, a higher score on some benchmark.

---

## 7. Work focus and allocation of effort

| Phase | Suggested duration | Focus | Allocation of effort |
|---|---|---|---|
| Phase 0 foundation | about 2 weeks | WP0.1–WP0.6 | Engineering 70%, theory 30% |
| Phase 1 feasibility | about 3–4 weeks | Numerical feasibility of the two main lines + prototypes | P1 40%, P2 35%, literature 15%, P3 10% |
| Decision gate G1 | — | Choose the flagship | — |
| Phase 2 flagship | about 6–8 weeks | The flagship's complete certificate | Early: flagship 70%, the other line 20%, writing 10%; later, writing rises to 40% |
| Phase 3 closeout | about 2 weeks | Repository reorganization, README, technical report | — |

The durations are suggestions, not commitments. Theodore's schedule takes priority.

---

## 8. Decision gates

### G0: at the end of Phase 0

Must satisfy:

- The evaluation foundation is in place: the current 24M results have bootstrap confidence intervals clustered by family, and three baselines.
- The permission-loss ablation has results, whether positive or negative.
- Synthetic world v0 can plant a specified amount of contamination.

If these are not satisfied, do not start the Phase 1 experiments. Literature and derivation questions are not subject to this restriction.

### G1: at the end of Phase 1, choose the flagship

Score on four criteria, in descending order of weight:

1. **Novelty:** the literature questions confirm "not found" or "only partly done".
2. **Non-vacuity:** under realistic parameters (real corpus size, T4 budget), the certificate is not vacuous.
3. **Feasibility:** it can be completed within the T4 budget.
4. **Narrative fit:** it is the same style as Theodore's certified-bounds research.

Decision rules:

- P1 novel and non-vacuous → P1 is the flagship, and P2 becomes a second paper or an appendix.
- P1 has already been done, or is vacuous → P2 is the flagship. P1 is downgraded to a short paper: negative result + audit resolution limit.
- Neither works → return to the advisor to choose a new topic. The alternative is to expand P3 into a standalone piece of work.

### G2: mid-way through Phase 2

Has the certificate been computed on real data? If not, **narrow** the scope (fewer corpora, fewer kinds of certificates); do not expand it.

---

## 9. Risks and kill conditions

| Risk | Early signal | Response | Kill condition |
|---|---|---|---|
| P1 has already been done | Q3 or Q29 finds a provable look-ahead bound on learned model parameters | Switch to the differentiated parts (audit limit, trust tiers), or make P2 the flagship | Existing work covers all three links of the certificate chain |
| P1's bound is vacuous | The numbers from T1.4 show that a realistic k needs m > 1000 | Switch to corpora with authoritative timestamps and shrink the suspect window | Even with corpora like EDGAR, no non-vacuous certificate can be given for k ≥ 1 |
| P2 has already been done | Q10 or Q31 finds certifiable numeric monotonicity for language models | Focus on the dimensionless and financial-specification parts | Similar work on financial text has been published |
| P2's parsing link is too weak | Parsing accuracy in WP2.1 is below about 95% | Restrict to text aligned with inline XBRL | On any obtainable text, parsing errors dominate the certificate |
| Conclusions from the synthetic world do not transfer to real data | Results on the synthetic world and on real data point in opposite directions | Use the synthetic world only to verify "the certificate holds", not to argue about "accuracy" | — |
| Not enough compute | A single experiment exceeds about 6 hours on a T4 | Shrink the model; switch to frozen backbone features | — |

---

## 10. What not to do, and why

| Not doing | Reason |
|---|---|
| Chasing leaderboard scores such as FinBen | Fails filters 1 and 3 |
| R1-style reasoning distillation plus GRPO | Needs a base model of 7B or more, violates the compute constraint, and does not need training from scratch |
| Candlestick / order-flow foundation models (the Kronos, MarS, TradeFM kind) | Need large amounts of data and compute, and are not language models |
| LLM alpha-mining agents | Unrelated to "training a language model from scratch"; backtest conclusions overfit easily |
| Scaling up the private 2.4B model | The public evidence cannot support it; a large model is not needed in the certificate framework |
| Changing the website | Theodore explicitly asked that it not be touched |

---

## 11. Research discipline

1. **Every number is traceable:** commit, config, seed, hardware, data version.
2. **Write the theorem statement first, then the code.** The role of the code is to test the theorem's premises and the tightness of the bound.
3. **Report negative results as usual.** "This bound is vacuous under realistic parameters, because of X" is a publishable conclusion.
4. **Do not report dev-set scores after repeated model selection on the dev set.**
5. **Distinguish three kinds of statements:** the advisor's hypotheses, conclusions from the literature, and our own results.
6. **Commit in small steps.** One draft PR per work package, not merged.

---

## 12. Form of the outputs

- **Technical report 1 (flagship), with one of two tentative titles:**
  - "Certifying Look-Ahead Freedom: A Certificate Chain for Point-in-Time Language Models"
  - "Model Greeks: Certified Numeric Sensitivity for Financial Language Models"
- **Technical report 2, or as an appendix:** the other main line.
- **Repository:** an executable certificate command, for example `python -m finllm certify --config ...`, which outputs a JSON certificate containing the conclusion, all assumptions, the α of each link and the checker version.
- **README:** the new positioning. Needs Theodore's approval. The old Trial is moved to `legacy/` and labeled truthfully.
