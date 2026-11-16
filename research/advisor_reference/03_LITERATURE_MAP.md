# 前沿文献地图

**这份地图是怎么来的：** 2026-11-15，导师做了约 40 次网络检索，读的是摘要、检索摘要和二手综述，**不是全文**。所以：

- "置信度"一列是导师对"这条描述准确"的判断，不是对论文质量的判断。
- "空白"判断都是**假设**，需要文献题 Q1–Q32 去核实。
- 第 J 节列出的是导师凭记忆引用、本轮**没有**检索核实的经典文献。

---

## A. 文本金融 LLM：主流做法

**结论：** 主流是在 7B–32B 的开源底座上做后训练，包括推理轨迹蒸馏、GRPO 强化学习、继续预训练加指令微调。架构上没有看到金融特有的创新。

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| Fin-R1 | 7B；先用 DeepSeek-R1 蒸馏出的金融推理数据做 SFT，再做 GRPO | 中 | [arXiv 2503.16252](https://arxiv.org/abs/2503.16252) |
| DianJin-R1 | Qwen2.5 7B / 32B；推理增强监督 + GRPO；数据来自 CFLUE、FinQA 和合规语料 | 中 | [2504.15716](https://huggingface.co/papers/2504.15716) |
| Agentar-Fin-R1 | Qwen3 8B / 32B；按专业标签把金融任务分类来组织训练 | 低 | [2507.16802](https://arxiv.org/abs/2507.16802) |
| FinDAP / Llama-Fin | 8B；联合优化继续预训练和指令微调；用生成式奖励模型的过程信号蒸馏偏好数据；EMNLP 2025 | 中 | [2501.04961](https://arxiv.org/abs/2501.04961) |
| 金融 LLM 综述 | 覆盖分类、抽取、摘要、问答和多模态 | 中 | [2503.22693](https://arxiv.org/abs/2503.22693) |
| 轻量 LLM vs FinBERT | Qwen3 8B、Llama3 8B 只用 5% 的训练数据就超过 FinBERT | 中 | [2512.00946](https://arxiv.org/abs/2512.00946) |
| FinBERT2 | 主张"小型领域编码器 + 通用 LLM"的组合部署 | 中 | [2506.06335](https://arxiv.org/abs/2506.06335) |

**对我们的含义：** 在能力上竞争没有意义。这些配方里可能可以迁移的是数据课程和奖励设计，Q25 负责核实。

## B. 非文本金融基础模型

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| Kronos | 把 K 线（OHLCV）离散成 token 后做自回归预训练；超过 120 亿条 K 线，45 个交易所；AAAI 2026 | 中 | [2508.02739](https://arxiv.org/abs/2508.02739) |
| MarS / LMM | 订单级生成模型，用于市场模拟；ICLR 2025 | 中 | [2409.07486](https://arxiv.org/abs/2409.07486) |
| TradeFM | 成交流与市场微结构的生成式基础模型 | 低 | [2602.23784](https://arxiv.org/abs/2602.23784) |

**对我们的含义：** 金融特有的架构创新集中在非文本模态的 tokenization。它们需要大量数据和算力，本项目不做。

## C. Point-in-time 模型与前视偏差（P1 的主战场）

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| ChronoBERT / ChronoGPT | 1999 年起每年一个模型，只用当时可得的文本训练；结论是前视偏差在他们的测试里不大 | 中 | [2502.21206](https://arxiv.org/abs/2502.21206) |
| ChronoGPT-Instruct | 无前视偏差的指令模型；作者承认能力有折损 | 中 | [2510.11677](https://arxiv.org/abs/2510.11677) |
| DatedGPT | 12 个 1.3B 模型，每年一个截止日，2013–2024；指令数据也按年限定。**作者承认没有证明所有泄漏通道都已关闭** | 中 | [2603.11838](https://arxiv.org/abs/2603.11838) |
| TiC-LM | 时间持续预训练的 web 规模 benchmark | 低 | [2504.02107](https://arxiv.org/abs/2504.02107) |
| Dated Data | 用困惑度探测模型的有效知识截止日 | 中 | [2403.12958](https://arxiv.org/abs/2403.12958) |
| Lookahead Propensity 检验 | 用回归中的交互项检验记忆是否放大了预测力 | 中 | [2512.23847](https://arxiv.org/abs/2512.23847) |
| The Memorization Problem | LLM 能回忆截止日前的经济数据；证据只是下界 | 中 | [2504.14765](https://arxiv.org/abs/2504.14765) |
| All Leaks Count, Some Count More | 把模型理由拆成原子陈述，逐条判断是否泄漏，用 Shapley 加权；提出生成时校验的 TimeSPEC | 中 | [2602.17234](https://arxiv.org/abs/2602.17234) |
| HindsightBench | 只需 API 访问的黑盒行为审计；结果对量化等部署细节敏感 | 低 | [2607.18867](https://arxiv.org/abs/2607.18867) |
| Temporal Non-Interference | 把"无前视"定义成可验证的正确性性质，用于回测和交易管线 | 低 | [2607.04958](https://arxiv.org/abs/2607.04958) |
| Temporal Leakage in LLM Backtesting | 测量泄漏并给出调整后的分数 | 低 | [2608.02985](https://arxiv.org/abs/2608.02985) |
| FinDendro | GPT-5 答对 76% 的受控事实，却只声称知道 38%；结论是自我报告不能认证回测 | 中 | [2611.06808](https://arxiv.org/abs/2611.06808) |
| 匿名化 / entity neutering | Glasserman–Lin 发现匿名化后的标题反而带来更高收益（"分心效应"）；entity neutering 反复改写直到模型认不出公司 | 中 | [2309.17322](https://arxiv.org/abs/2309.17322) |
| 匿名化的信息损失 | 匿名化会损害波动率和公司业绩的预测 | 低 | [2511.15364](https://arxiv.org/abs/2511.15364) |
| New News is Bad News | 用 RNN 衡量新闻熵（新颖度），新颖度高预示收益低 | 中 | [2309.05560](https://arxiv.org/abs/2309.05560) |
| The Inefficient Pricing of News | 把新闻分为可预测部分和"纯新闻"；后者有预测力；NBER 2026 | 低（数字来自二手专栏） | [CEPR 专栏](https://cepr.org/voxeu/columns/inefficient-pricing-news) |

**导师的空白假设：** 造模型（ChronoGPT、DatedGPT）和检测（LAP、HindsightBench、FinDendro）两类工作都有。但**对学习得到的模型参数**、在**残余时间戳错误**下给出**可证明界**的工作，没有看到。Temporal Non-Interference 最接近，需要确认它是否覆盖模型参数这条通道（Q3）。

## D. 可认证性与鲁棒性

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| Lipschitz 约束的 transformer | 约束权重谱范数，配合 Muon 优化器，训练到 145M 参数；全局界在大规模时偏松 | 中 | [2507.13338](https://arxiv.org/abs/2507.13338) |
| 可证明单调网络 | 单调性由架构精确保证；已用于 LHCb Run 3 触发系统 | 高 | [2112.00038](https://arxiv.org/abs/2112.00038)、[2307.07512](https://arxiv.org/abs/2307.07512)、[2312.14265](https://arxiv.org/abs/2312.14265) |
| Text-CRS | 用随机平滑认证词级别的替换、重排、插入、删除 | 中 | [2307.16630](https://arxiv.org/abs/2307.16630) |
| SAFER | 同义词替换的认证，只需黑盒访问 | 中 | [2005.14424](https://arxiv.org/abs/2005.14424) |
| 非空的 LLM 泛化界 | 压缩 + 把 token 当数据点的鞅集中不等式；在 LLaMA2-70B 上得到非空界 | 中 | [2312.17173](https://arxiv.org/abs/2312.17173)、[2407.18158](https://arxiv.org/abs/2407.18158) |

**导师的空白假设：** 没有看到对**金融文本里的数值**给出可证明单调性或 Lipschitz 界的语言模型。

## E. 数字表示与单位

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| xVal | 一个数一个 token，用数值缩放一个专用 embedding；范围和精度有限 | 中 | [2310.02989](https://arxiv.org/abs/2310.02989) |
| FoNE | 用 base-10 的傅里叶特征编码数字；加法很强，乘法弱 | 中 | [2502.09741](https://arxiv.org/abs/2502.09741) |
| BitTokens | 用 IEEE 754 二进制表示编码；小模型上加减乘除都接近完美 | 中 | [2510.06824](https://arxiv.org/abs/2510.06824) |
| 量纲等变机器学习 | Buckingham Pi：函数单位等变当且仅当它只依赖无量纲量 | 高 | [2204.00887](https://arxiv.org/abs/2204.00887)、[2301.13724](https://arxiv.org/abs/2301.13724) |

**导师的空白假设：** 没有看到单位等变被用在语言模型的数字通道上，也没有看到它被用在金融文本上。

## F. 可验证的监督

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| FinChain | 每道题附可执行的 Python 轨迹，逐步验证；58 个主题；ACL 2026 | 中 | [2506.02515](https://arxiv.org/abs/2506.02515) |
| FinTagging | 映射到完整 US-GAAP taxonomy 的 XBRL 标注 benchmark | 中 | [2505.20650](https://arxiv.org/abs/2505.20650) |
| FinAuditing | 关系一致性和基于 taxonomy 的数值核验；1,102 个实例，平均超过 3.3 万 token | 中 | [2510.08886](https://arxiv.org/abs/2510.08886) |
| Lean 4 数理金融库 | 两百多个没有 sorry 的定理，含 Black–Scholes 和二叉树到 BS 的极限 | 中 | [2606.01356](https://arxiv.org/abs/2606.01356) |
| 机器验证的 Itô 积分 | 作者称是第一个在证明助手里构造 Itô 积分和 Itô 公式的工作 | 中 | [2606.15089](https://arxiv.org/abs/2606.15089) |

**导师的空白假设：** 没有看到把会计恒等式作为神经文本模型硬约束的工作。

## G. 可迁移的架构与训练方法（探索级）

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| TRM | 5M–19M 参数的递归小模型；ARC-AGI-1 上 44.6% | 中 | [2510.04871](https://arxiv.org/abs/2510.04871) |
| 对 TRM 的批评 | 成绩主要来自任务专门的条件化和激进的测试时计算，不是深层推理 | 中 | [2512.11847](https://arxiv.org/abs/2512.11847) |
| LLM-JEPA | 在 LM 损失之外，加一个跨视图预测 embedding 的目标；适用于天然成对的数据 | 中 | [2509.14252](https://arxiv.org/abs/2509.14252) |
| 时间感知 PFN | 用合成先验预训练做零样本时间序列预测 | 低 | [2603.15802](https://arxiv.org/abs/2603.15802) |

## H. 统计保证

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| Non-exchangeable conformal risk control | 允许变点和漂移的风险控制 | 中 | [2310.01262](https://arxiv.org/abs/2310.01262) |
| Conformal Selective Acting | 在模型实际放行的答案上，做 anytime-valid 的选择性风险控制 | 低 | [2605.20270](https://arxiv.org/abs/2605.20270) |
| Domain-shift-aware conformal | 按与测试 prompt 的接近程度重新加权校准样本 | 低 | [2510.05566](https://arxiv.org/abs/2510.05566) |
| 用 betting 做序贯 LLM 评测 | 用 test supermartingale 构造置信序列 | 低 | [2607.17409](https://www.alphaxiv.org/abs/2607.17409) |
| 码长、log-loss 与 e-process | 把压缩、预测和序贯检验联系起来 | 低 | [2602.04146](https://arxiv.org/abs/2602.04146) |
| LLM + Black–Litterman | 用 LLM 自己的收益预测和预测方差作为观点和置信度（不是文本作者的观点） | 中 | [2504.14345](https://arxiv.org/abs/2504.14345) |

## I. 可解释性

| 工作 | 要点 | 置信度 | 来源 |
|---|---|---|---|
| Binding ID | 模型用 binding ID 向量把实体和属性绑定起来 | 高 | [2310.17191](https://arxiv.org/abs/2310.17191) |
| 动态实体追踪中的重新绑定 | 2026 | 低 | [2606.08644](https://arxiv.org/abs/2606.08644) |
| A Financial Brain Scan of the LLM | 用 SAE 特征解释 LLM 的超额收益；调节"金融风险"特征能改变资产配置 | 中 | [2508.21285](https://arxiv.org/abs/2508.21285) |
| SAE-FiRE / SAE 公司相似度 | 用 SAE 特征做盈余意外预测和配对交易 | 中 | [2505.14420](https://arxiv.org/abs/2505.14420)、[2412.02605](https://arxiv.org/abs/2412.02605) |

---

## J. 导师凭记忆引用、本轮未检索核实的经典文献

**使用这些文献前，必须先核实标题、作者、venue 和结论。**

| 主题 | 文献 | 用途 |
|---|---|---|
| 投毒认证 | Levine & Feizi, "Deep Partition Aggregation", ICLR 2021 | T1.3 |
| 投毒认证 | Wang, Levine & Feizi, "Improved Certified Defenses against Data Poisoning with (Deterministic) Finite Aggregation", ICML 2022 | T1.3 |
| 投毒认证 | Jia, Cao & Gong, "Intrinsic Certified Robustness of Bagging against Data Poisoning", AAAI 2021 | T1.3 |
| 集体证书 | Schuchardt, Bojchevski, Gasteiger & Günnemann, "Collective Robustness Certificates", ICLR 2021 | T1.3 |
| 差分隐私 | Dong, Roth & Su, "Gaussian Differential Privacy", JRSSB 2022 | T1.2 |
| 污染检验 | Oren 等, "Proving Test Set Contamination in Black-Box Language Models", ICLR 2024 | Q4 |
| 同单调 | Dhaene, Denuit, Goovaerts, Kaas & Vyncke, "The Concept of Comonotonicity in Actuarial Science and Finance: Theory", IME 2002 | T3.1 |
| 依赖不确定性 | Embrechts, Puccetti & Rüschendorf, "Model Uncertainty and VaR Aggregation", JBF 2013 | T3.2 |
| 有序回归 | McCullagh, "Regression Models for Ordinal Data", JRSSB 1980 | T2.2 |
| 单调网络 | Liu 等, "Certified Monotonic Neural Networks", NeurIPS 2020 | T2.2 |
| 反事实不变性 | Veitch 等, "Counterfactual Invariance to Spurious Correlations", NeurIPS 2021 | T2.1 |
| 反事实增强 | Kaushik, Hovy & Lipton, "Learning the Difference that Makes a Difference", ICLR 2020 | T2.1 |
| 对比集 | Gardner 等, "Evaluating Models' Local Decision Boundaries via Contrast Sets", Findings of EMNLP 2020 | T2.1 |
| 行为测试 | Ribeiro 等, "Beyond Accuracy: Behavioral Testing of NLP Models with CheckList", ACL 2020 | T2.1 |
| 评测误差棒 | Miller, "Adding Error Bars to Evals", 2024 | WP0.1 |

---

## K. 可迁移性总表（导师判断）

| 来源领域 | 想法 | 金融里的对应 | 状态 | 对应 |
|---|---|---|---|---|
| 数据投毒的认证防御 | 对 k 个污染样本的可证明界 | 至多 k 篇错标文档时，无泄漏回测统计量的被证明区间 | 未见，待核实 | P1、Q3、Q29 |
| 差分隐私 | group privacy | 同上，DP 路线 | 预计偏空 | P1、Q3 |
| 抽样审计 | 精确置信上界 | 时间戳错标率 → k | 方法成熟，组合是新的 | P1、Q30 |
| 高能物理触发系统 | 架构保证的单调性 | 对数值证据单调；模型的 Greeks | 未见 | P2、Q10、Q31 |
| 物理的量纲分析 | 只依赖无量纲量 | 对货币和尺度精确不变 | 未见 | P2、Q13 |
| 科学数据的数字编码 | 一个数一个 token | 财报数字 | 成熟，可直接用 | P2、Q12 |
| 精算的同单调与凸序 | 最坏情形耦合 | 部署风险证书 | 可能已知 | P3、Q20 |
| AI for Math 的生成–验证 | 以验证器为奖励 | XBRL 勾稽、会计恒等式、区间算术 | 环境可做，训练需要算力 | Q27 |
| 天气模型的 CRPS 训练 | 用 proper scoring rule 训练分布输出 | 输出 (VaR, ES) 而不是三分类 | 部分有人做 | Q17 |
| 递归小模型 | 小模型做约束满足 | 在会计恒等式约束下补全报表 | 投机性高 | Q22 |
| JEPA | 成对视图的表示预测 | 叙述段落 ↔ XBRL facts | 可以低成本尝试 | Q23 |
| 机制可解释性 | binding 回路 | target 和 holder 的绑定 | 可做 | Q26 |
