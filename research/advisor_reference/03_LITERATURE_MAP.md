# Map of frontier literature

**How this map was made:** on 2026-11-15 the advisor ran about 40 web searches and read abstracts, search snippets and secondary surveys, **not full texts**. Therefore:

- The "Confidence" column is the advisor's judgment that "this description is accurate", not a judgment of the paper's quality.
- All "gap" judgments are **hypotheses** that need to be verified by literature questions Q1–Q32.
- Section J lists classic works that the advisor cited from memory and that were **not** checked by search in this round.

---

## A. Text-based financial LLMs: mainstream practice

**Conclusion:** the mainstream is post-training on open-source bases of 7B–32B, including reasoning-trace distillation, GRPO reinforcement learning, and continued pretraining plus instruction tuning. No finance-specific architectural innovation was seen.

| Work | Key points | Confidence | Source |
|---|---|---|---|
| Fin-R1 | 7B; first SFT on financial reasoning data distilled from DeepSeek-R1, then GRPO | Medium | [arXiv 2503.16252](https://arxiv.org/abs/2503.16252) |
| DianJin-R1 | Qwen2.5 7B / 32B; reasoning-augmented supervision + GRPO; data from CFLUE, FinQA and compliance corpora | Medium | [2504.15716](https://huggingface.co/papers/2504.15716) |
| Agentar-Fin-R1 | Qwen3 8B / 32B; organizes training by classifying financial tasks with professional labels | Low | [2507.16802](https://arxiv.org/abs/2507.16802) |
| FinDAP / Llama-Fin | 8B; jointly optimizes continued pretraining and instruction tuning; distills preference data using process signals from a generative reward model; EMNLP 2025 | Medium | [2501.04961](https://arxiv.org/abs/2501.04961) |
| Survey of financial LLMs | Covers classification, extraction, summarization, QA and multimodality | Medium | [2503.22693](https://arxiv.org/abs/2503.22693) |
| Lightweight LLMs vs. FinBERT | Qwen3 8B and Llama3 8B beat FinBERT using only 5% of the training data | Medium | [2512.00946](https://arxiv.org/abs/2512.00946) |
| FinBERT2 | Advocates a combined deployment of "small domain encoder + general LLM" | Medium | [2506.06335](https://arxiv.org/abs/2506.06335) |

**What it means for us:** competing on capability is pointless. What might transfer from these recipes is the data curriculum and reward design; Q25 is responsible for verifying this.

## B. Non-text financial foundation models

| Work | Key points | Confidence | Source |
|---|---|---|---|
| Kronos | Discretizes candlesticks (OHLCV) into tokens and does autoregressive pretraining; more than 12 billion candlesticks, 45 exchanges; AAAI 2026 | Medium | [2508.02739](https://arxiv.org/abs/2508.02739) |
| MarS / LMM | Order-level generative model for market simulation; ICLR 2025 | Medium | [2409.07486](https://arxiv.org/abs/2409.07486) |
| TradeFM | Generative foundation model for trade flow and market microstructure | Low | [2602.23784](https://arxiv.org/abs/2602.23784) |

**What it means for us:** finance-specific architectural innovation is concentrated in tokenization of non-text modalities. These need large amounts of data and compute, and this project does not do them.

## C. Point-in-time models and look-ahead bias (the main battlefield for P1)

| Work | Key points | Confidence | Source |
|---|---|---|---|
| ChronoBERT / ChronoGPT | One model per year from 1999, trained only on text available at the time; conclusion: look-ahead bias is small in their tests | Medium | [2502.21206](https://arxiv.org/abs/2502.21206) |
| ChronoGPT-Instruct | Instruction model without look-ahead bias; the authors admit a loss of capability | Medium | [2510.11677](https://arxiv.org/abs/2510.11677) |
| DatedGPT | 12 models of 1.3B, one cutoff per year, 2013–2024; instruction data is also limited by year. **The authors admit they have not proven that all leakage channels are closed** | Medium | [2603.11838](https://arxiv.org/abs/2603.11838) |
| TiC-LM | Web-scale benchmark for time-continual pretraining | Low | [2504.02107](https://arxiv.org/abs/2504.02107) |
| Dated Data | Probes a model's effective knowledge cutoff with perplexity | Medium | [2403.12958](https://arxiv.org/abs/2403.12958) |
| Lookahead Propensity test | Uses interaction terms in a regression to test whether memorization amplifies predictive power | Medium | [2512.23847](https://arxiv.org/abs/2512.23847) |
| The Memorization Problem | LLMs can recall economic data from before their cutoff; the evidence is only a lower bound | Medium | [2504.14765](https://arxiv.org/abs/2504.14765) |
| All Leaks Count, Some Count More | Splits model rationales into atomic statements, judges each for leakage, weights by Shapley; proposes TimeSPEC for checking at generation time | Medium | [2602.17234](https://arxiv.org/abs/2602.17234) |
| HindsightBench | Black-box behavioral audit needing only API access; results are sensitive to deployment details such as quantization | Low | [2607.18867](https://arxiv.org/abs/2607.18867) |
| Temporal Non-Interference | Defines "no look-ahead" as a verifiable correctness property, for backtesting and trading pipelines | Low | [2607.04958](https://arxiv.org/abs/2607.04958) |
| Temporal Leakage in LLM Backtesting | Measures leakage and gives adjusted scores | Low | [2608.02985](https://arxiv.org/abs/2608.02985) |
| FinDendro | GPT-5 answers 76% of controlled facts correctly but claims to know only 38%; conclusion: self-report cannot certify a backtest | Medium | [2611.06808](https://arxiv.org/abs/2611.06808) |
| Anonymization / entity neutering | Glasserman–Lin find that anonymized headlines actually yield higher returns (the "distraction effect"); entity neutering rewrites repeatedly until the model cannot recognize the company | Medium | [2309.17322](https://arxiv.org/abs/2309.17322) |
| Information loss from anonymization | Anonymization harms prediction of volatility and company performance | Low | [2511.15364](https://arxiv.org/abs/2511.15364) |
| New News is Bad News | Uses an RNN to measure news entropy (novelty); high novelty predicts low returns | Medium | [2309.05560](https://arxiv.org/abs/2309.05560) |
| The Inefficient Pricing of News | Splits news into a predictable part and "pure news"; the latter has predictive power; NBER 2026 | Low (numbers from a secondary column) | [CEPR column](https://cepr.org/voxeu/columns/inefficient-pricing-news) |

**The advisor's gap hypothesis:** there is work both on building models (ChronoGPT, DatedGPT) and on detection (LAP, HindsightBench, FinDendro). But no work was seen that gives **provable bounds** for **learned model parameters** under **residual timestamp errors**. Temporal Non-Interference is the closest; it needs to be confirmed whether it covers the model-parameter channel (Q3).

## D. Certifiability and robustness

| Work | Key points | Confidence | Source |
|---|---|---|---|
| Lipschitz-constrained transformers | Constrains the spectral norm of weights, with the Muon optimizer, trained up to 145M parameters; global bounds are loose at large scale | Medium | [2507.13338](https://arxiv.org/abs/2507.13338) |
| Provably monotone networks | Monotonicity guaranteed exactly by the architecture; already used in the LHCb Run 3 trigger system | High | [2112.00038](https://arxiv.org/abs/2112.00038), [2307.07512](https://arxiv.org/abs/2307.07512), [2312.14265](https://arxiv.org/abs/2312.14265) |
| Text-CRS | Uses randomized smoothing to certify word-level substitution, reordering, insertion and deletion | Medium | [2307.16630](https://arxiv.org/abs/2307.16630) |
| SAFER | Certification for synonym substitution, needing only black-box access | Medium | [2005.14424](https://arxiv.org/abs/2005.14424) |
| Non-vacuous LLM generalization bounds | Compression + martingale concentration inequalities treating tokens as data points; non-vacuous bounds on LLaMA2-70B | Medium | [2312.17173](https://arxiv.org/abs/2312.17173), [2407.18158](https://arxiv.org/abs/2407.18158) |

**The advisor's gap hypothesis:** no language model was seen that gives provable monotonicity or Lipschitz bounds for **numbers in financial text**.

## E. Number representation and units

| Work | Key points | Confidence | Source |
|---|---|---|---|
| xVal | One token per number, scaling a dedicated embedding by the value; limited range and precision | Medium | [2310.02989](https://arxiv.org/abs/2310.02989) |
| FoNE | Encodes numbers with base-10 Fourier features; strong at addition, weak at multiplication | Medium | [2502.09741](https://arxiv.org/abs/2502.09741) |
| BitTokens | Encodes with the IEEE 754 binary representation; near-perfect addition, subtraction, multiplication and division on small models | Medium | [2510.06824](https://arxiv.org/abs/2510.06824) |
| Dimensionally equivariant machine learning | Buckingham Pi: a function is unit-equivariant if and only if it depends only on dimensionless quantities | High | [2204.00887](https://arxiv.org/abs/2204.00887), [2301.13724](https://arxiv.org/abs/2301.13724) |

**The advisor's gap hypothesis:** no use of unit equivariance in the numeric channel of a language model was seen, nor any use of it on financial text.

## F. Verifiable supervision

| Work | Key points | Confidence | Source |
|---|---|---|---|
| FinChain | Each problem comes with an executable Python trace, verified step by step; 58 topics; ACL 2026 | Medium | [2506.02515](https://arxiv.org/abs/2506.02515) |
| FinTagging | XBRL tagging benchmark mapped to the full US-GAAP taxonomy | Medium | [2505.20650](https://arxiv.org/abs/2505.20650) |
| FinAuditing | Relational consistency and taxonomy-based numeric verification; 1,102 instances, averaging more than 33,000 tokens | Medium | [2510.08886](https://arxiv.org/abs/2510.08886) |
| Lean 4 mathematical finance library | More than two hundred theorems without sorry, including Black–Scholes and the binomial-tree-to-BS limit | Medium | [2606.01356](https://arxiv.org/abs/2606.01356) |
| Machine-verified Itô integral | The authors say it is the first work to construct the Itô integral and Itô's formula in a proof assistant | Medium | [2606.15089](https://arxiv.org/abs/2606.15089) |

**The advisor's gap hypothesis:** no work was seen that uses accounting identities as hard constraints on a neural text model.

## G. Transferable architectures and training methods (exploratory)

| Work | Key points | Confidence | Source |
|---|---|---|---|
| TRM | Recursive small models with 5M–19M parameters; 44.6% on ARC-AGI-1 | Medium | [2510.04871](https://arxiv.org/abs/2510.04871) |
| Critique of TRM | The scores come mainly from task-specific conditioning and aggressive test-time compute, not deep reasoning | Medium | [2512.11847](https://arxiv.org/abs/2512.11847) |
| LLM-JEPA | Adds a cross-view embedding-prediction objective on top of the LM loss; suited to naturally paired data | Medium | [2509.14252](https://arxiv.org/abs/2509.14252) |
| Time-aware PFN | Zero-shot time-series forecasting through pretraining on synthetic priors | Low | [2603.15802](https://arxiv.org/abs/2603.15802) |

## H. Statistical guarantees

| Work | Key points | Confidence | Source |
|---|---|---|---|
| Non-exchangeable conformal risk control | Risk control allowing change points and drift | Medium | [2310.01262](https://arxiv.org/abs/2310.01262) |
| Conformal Selective Acting | Anytime-valid selective risk control on the answers the model actually lets through | Low | [2605.20270](https://arxiv.org/abs/2605.20270) |
| Domain-shift-aware conformal | Reweights calibration samples by their closeness to the test prompt | Low | [2510.05566](https://arxiv.org/abs/2510.05566) |
| Sequential LLM evaluation by betting | Builds confidence sequences from a test supermartingale | Low | [2607.17409](https://www.alphaxiv.org/abs/2607.17409) |
| Code length, log-loss and e-processes | Connects compression, prediction and sequential testing | Low | [2602.04146](https://arxiv.org/abs/2602.04146) |
| LLM + Black–Litterman | Uses the LLM's own return forecasts and forecast variances as views and confidences (not the views of the text's authors) | Medium | [2504.14345](https://arxiv.org/abs/2504.14345) |

## I. Interpretability

| Work | Key points | Confidence | Source |
|---|---|---|---|
| Binding ID | Models bind entities and attributes with binding ID vectors | High | [2310.17191](https://arxiv.org/abs/2310.17191) |
| Rebinding in dynamic entity tracking | 2026 | Low | [2606.08644](https://arxiv.org/abs/2606.08644) |
| A Financial Brain Scan of the LLM | Uses SAE features to explain LLM excess returns; steering a "financial risk" feature changes asset allocation | Medium | [2508.21285](https://arxiv.org/abs/2508.21285) |
| SAE-FiRE / SAE company similarity | Uses SAE features for earnings-surprise prediction and pairs trading | Medium | [2505.14420](https://arxiv.org/abs/2505.14420), [2412.02605](https://arxiv.org/abs/2412.02605) |

---

## J. Classic works cited by the advisor from memory and not checked by search this round

**Before using these works, first verify the title, authors, venue and conclusions.**

| Topic | Work | Use |
|---|---|---|
| Poisoning certification | Levine & Feizi, "Deep Partition Aggregation", ICLR 2021 | T1.3 |
| Poisoning certification | Wang, Levine & Feizi, "Improved Certified Defenses against Data Poisoning with (Deterministic) Finite Aggregation", ICML 2022 | T1.3 |
| Poisoning certification | Jia, Cao & Gong, "Intrinsic Certified Robustness of Bagging against Data Poisoning", AAAI 2021 | T1.3 |
| Collective certificates | Schuchardt, Bojchevski, Gasteiger & Günnemann, "Collective Robustness Certificates", ICLR 2021 | T1.3 |
| Differential privacy | Dong, Roth & Su, "Gaussian Differential Privacy", JRSSB 2022 | T1.2 |
| Contamination testing | Oren et al., "Proving Test Set Contamination in Black-Box Language Models", ICLR 2024 | Q4 |
| Comonotonicity | Dhaene, Denuit, Goovaerts, Kaas & Vyncke, "The Concept of Comonotonicity in Actuarial Science and Finance: Theory", IME 2002 | T3.1 |
| Dependence uncertainty | Embrechts, Puccetti & Rüschendorf, "Model Uncertainty and VaR Aggregation", JBF 2013 | T3.2 |
| Ordinal regression | McCullagh, "Regression Models for Ordinal Data", JRSSB 1980 | T2.2 |
| Monotone networks | Liu et al., "Certified Monotonic Neural Networks", NeurIPS 2020 | T2.2 |
| Counterfactual invariance | Veitch et al., "Counterfactual Invariance to Spurious Correlations", NeurIPS 2021 | T2.1 |
| Counterfactual augmentation | Kaushik, Hovy & Lipton, "Learning the Difference that Makes a Difference", ICLR 2020 | T2.1 |
| Contrast sets | Gardner et al., "Evaluating Models' Local Decision Boundaries via Contrast Sets", Findings of EMNLP 2020 | T2.1 |
| Behavioral testing | Ribeiro et al., "Beyond Accuracy: Behavioral Testing of NLP Models with CheckList", ACL 2020 | T2.1 |
| Error bars for evals | Miller, "Adding Error Bars to Evals", 2024 | WP0.1 |

---

## K. Transferability summary table (advisor's judgment)

| Source field | Idea | Counterpart in finance | Status | Corresponds to |
|---|---|---|---|---|
| Certified defenses against data poisoning | Provable bounds for k poisoned samples | A proven interval for the leakage-free backtest statistic when at most k documents are mislabeled | Not found, to be verified | P1, Q3, Q29 |
| Differential privacy | group privacy | Same as above, DP route | Expected to be largely vacuous | P1, Q3 |
| Sampling audit | Exact confidence upper bound | Timestamp mislabel rate → k | Method is mature; the combination is new | P1, Q30 |
| High-energy-physics trigger systems | Monotonicity guaranteed by the architecture | Monotone in numeric evidence; the model's Greeks | Not found | P2, Q10, Q31 |
| Dimensional analysis in physics | Depend only on dimensionless quantities | Exact invariance to currency and scale | Not found | P2, Q13 |
| Number encoding for scientific data | One token per number | Numbers in filings | Mature, usable directly | P2, Q12 |
| Actuarial comonotonicity and convex order | Worst-case coupling | Deployment-risk certificate | Possibly known | P3, Q20 |
| Generate–verify in AI for Math | Verifier as reward | XBRL cross-checks, accounting identities, interval arithmetic | The environment is doable; training needs compute | Q27 |
| CRPS training of weather models | Train distributional outputs with a proper scoring rule | Output (VaR, ES) instead of three classes | Partly done by others | Q17 |
| Recursive small models | Small models for constraint satisfaction | Completing statements under accounting-identity constraints | Highly speculative | Q22 |
| JEPA | Representation prediction across paired views | Narrative paragraphs ↔ XBRL facts | Can be tried at low cost | Q23 |
| Mechanistic interpretability | Binding circuits | Binding of target and holder | Doable | Q26 |
