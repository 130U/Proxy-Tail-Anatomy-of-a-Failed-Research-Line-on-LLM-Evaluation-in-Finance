# 并行调研问题 Q1–Q32

## 使用说明

- **32 个问题彼此独立**，没有先后顺序，可以一次全部发出，也可以任意分批。
- 每个问题开一个任务。任务开始时先读 `00_CODEX_BRIEF.md`、`01_ADVISOR_MEMO.md`、`02_PROJECT_SNAPSHOT.md`，以及题目里提到的 T 编号对应的 `04_THEORY_NOTES.md` 小节。
- **需要联网。** 没有联网能力时不要作答。
- 输出到 `research/answers/Qxx.md`，格式见 `07_REPORTING_PROTOCOL.md` 第 1 节。每题 800–1500 字为宜，文献覆盖到 2026 年 11 月。
- 题目里提到的论文编号，来自导师的摘要级检索，**可能有误**。请以一手来源为准；如果发现编号或描述错了，请指出。
- **推翻导师的假设，和确认它，同样有价值。**

**每题都要回答的五件事：**

1. 结论
2. 证据表（每个数字标注来源层级）
3. 新颖性判断：已有人做 / 部分做 / 未见，附检索关键词和置信度
4. 最小可行验证：一个定理陈述草稿，或一个 T4 上几小时能跑完的实验设计
5. 否决条件：什么发现会让我们放弃这个方向

---

## A. 信息集（P1）

**Q1. Point-in-time 语言模型的全景与成本。**

为以下每个模型填一张表：ChronoBERT / ChronoGPT（2502.21206）、ChronoGPT-Instruct（2510.11677）、DatedGPT（2603.11838）、TiMaGPT、NoLBERT、StoriesLM、PiT-Inference，以及你找到的其他模型。

列包括：参数量、语料来源与 token 数、日期范围、时间戳如何确定、vintage 频率、多个 vintage 是各自从零训练还是增量训练、总算力、评测方式、作者自己承认的未关闭泄漏通道。

另外回答两个问题：有没有参数量不超过 50M 的 point-in-time 模型？产生过已发表经济学结论的最小模型有多大？

**Q2. 泄漏通道的完整分类。**

除了"训练文档的日期晚于截止日"，未来信息还能通过哪些通道进入一个号称 point-in-time 的模型？请至少考察以下通道：

- tokenizer 词表（用未来文本训练，会泄漏哪些词的存在）
- 在未来数据上调出来的超参数和架构选择
- 指令微调数据
- 由更晚的模型生成的合成数据或蒸馏数据
- 用于去重和过滤的模型
- 文档修订（发布时间和最后修改时间不同）
- 标签定义
- early stopping

对每个通道回答：有没有论文测过它的量级？哪些通道完全没人测过？对照 `04_THEORY_NOTES.md` 的 T1.1，看定义是否覆盖了所有通道。

**Q3. Look-ahead 的形式化定义与可证明的界。**（对应 T1.1–T1.3）

(a) 有没有对"学习得到的模型"的 look-ahead bias 的形式化定义？例如：参数关于 σ-代数 F_t 可测、互信息 I(θ; D_{>t}) 有界、信息流安全里的 non-interference。请读"Look-Ahead-Freedom as Temporal Non-Interference"（2607.04958），说明它的定义覆盖的是数据管线，还是也覆盖模型参数这条通道。

(b) 有没有论文给出"回测统计量因污染而偏移多少"的可证明上界？逐一检查以下技术路线是否被用于 look-ahead：

- 差分隐私的 group privacy
- 数据投毒的认证防御（Deep Partition Aggregation、Finite Aggregation、bagging）
- certified unlearning
- 算法稳定性

(c) 如果没有，请核对 T1.2 和 T1.3 的陈述，并估算两个数：

- 对参数量不超过 50M、从零训练的语言模型，DP-SGD 实际能达到的 ε 或 μ（引用 DP 语言模型预训练的结果）。
- 对由 m 个不相交分片组成的集成，能认证的 k 与 m、投票差距之间的关系。

最后回答：界在什么参数范围内不是空的？

**Q4. 泄漏的统计检验：哪些有真正的保证。**

对以下每种方法，说明它的原假设、检验统计量、所需假设、是否有有限样本的第一类错误控制、是否 anytime-valid：

- Lookahead Propensity 检验（2512.23847）
- The Memorization Problem（2504.14765）
- All Leaks Count, Some Count More（2602.17234）
- HindsightBench（2607.18867）
- Temporal Leakage in LLM Backtesting（2608.02985）
- FinDendro（2611.06808）
- Dated Data（2403.12958）
- Sarkar–Vafa 的 lookahead 检验
- Oren 等人基于可交换性的测试集污染检验

另外回答：有没有任何 look-ahead 或污染检验是用 e-value、test martingale 或 testing-by-betting 构造的？在带时间戳的语料里，哪种原假设带有可交换结构，从而允许精确检验？

**Q5. 带可靠时间戳的公开语料。**

列出满足以下条件的公开语料：可以合法使用；每篇文档有可靠时间戳；适合在 Colab 上训练参数量不超过 50M、按年或按月分 vintage 的模型。

至少考察：SEC EDGAR（含 EDGAR-CORPUS）、FOMC 文件、Federal Register、Wikipedia 修订历史、arXiv q-fin、CC-News、GDELT、专利、TiC-LM（2504.02107）的数据。

对每个语料给出：每年约多少 token、日期范围、许可证、时间戳的含义（发布、受理还是最后修改）、时间戳是否由机器生成（这对 T1.4 的"信任分层"很关键）、已知问题。

**Q6. 新闻新颖度这条线做到了哪里。**

说明以下两篇工作如何定义新颖度（或"可预测新闻 / 纯新闻"），用了什么模型，如何处理 look-ahead，主要数字是什么：

- Glasserman–Mamaysky–Qin，"New News is Bad News"（2309.05560）
- Didisheim–Kelly–Pourmohammadi–Tian，"The Inefficient Pricing of News"（2026，NBER）

然后回答：用一个小的 point-in-time 语言模型计算逐文档 surprisal（−log p，模型只见过 t 之前的文本），作为研究对象还有没有空间？哪些方面没人做过？候选包括：prequential 码长的精确解释、条件于公司历史的 surprisal、实体中性的 surprisal。

---

## B. 语义敏感度（P2）

**Q7. Lipschitz 约束的 transformer。**（对应 T2.5）

详细说明 Newhouse 等人"Training Transformers with Enforced Lipschitz Constants"（2507.13338）：

- 注意力如何变成 Lipschitz 的；
- 权重约束是什么；
- 优化器（Muon）起什么作用；
- 被证明的界和经验界各是多少；
- 在 nanoGPT 规模上的性能代价（给数字）。

相关工作：LipsFormer、nGPT、L2 self-attention（Kim 等 2021）、CertViT（2302.10287）、LipShiFT（2503.14751）。

**核心问题：** 对一个 6 层、d=512、24M 的 decoder，从 embedding 到 logits 的全局 Lipschitz 界能做到多小？困惑度损失多少？这个界相对于分类 margin 是不是空的，也就是认证半径是否大于典型改写在 embedding 空间里的距离？有没有用 Lipschitz transformer 做文本认证鲁棒性的已有结果？

**Q8. 小 transformer 的形式化验证。**

2024–2026 年，transformer 分类器的完全验证和不完全验证做到了什么程度？考察以下工作及其后续：auto_LiRPA / α,β-CROWN 对注意力的支持、DeepT、Shi 等 2020 "Robustness Verification for Transformers"、Bonaert 等 2021。

回答：

- 在 T4 或 CPU 上，多大的模型（层数、宽度、序列长度）能得到有用的紧度？
- 支持哪些扰动集合（embedding 的 ℓp 球、同义词集合、token 替换集合）？
- 对有限的编辑集合（比如所有实体别名、所有单位缩放）直接枚举来认证，是不是一个被认可的做法？
- 随机平滑一类的文本认证（SAFER 2005.14424、Text-CRS 2307.16630）给出的是什么类型的保证？

**Q9. Semantic permissions 的理论归位。**（对应 T2.1）

把仓库的 semantic permissions（四种关系、三项损失，见 `02_PROJECT_SNAPSHOT.md` 第 3.1 节）对应到已有理论：counterfactual invariance（Veitch 等 2021）、counterfactually augmented data（Kaushik 等 2020）及对其有效性的理论解释、contrast sets（Gardner 等 2020）、CheckList、ARTS、counterfactual logit pairing（Garg 等 2019）、一致性正则（UDA、R-Drop）、IRM、内容–风格可识别性（von Kügelgen 等 2021；2311.08815）、群等变学习。

回答三点：

1. "成对一致性 + 改标签 margin"的损失，在什么条件下能识别因果特征？有没有可识别性或样本复杂度定理？
2. "标签保持不等于分布保持"（同类别，但置信度可以变）有没有被形式化过，例如写成预测分布之间的序约束或随机占优？
3. "log-odds 差的 margin"这个损失，最接近的已有工作是什么？

**Q10. 可认证的单调性与"模型的 Greeks"。**（对应 T2.2）

总结可认证单调网络的工作：Liu 等 2020 "Certified Monotonic Neural Networks"；Kitouni–Nolte–Williams 的 Lipschitz 单调网络（2112.00038、2307.07512）及其在 LHCb Run 3 触发系统中的应用（2312.14265）。

回答：

- 有没有人让语言模型的输出，对文本中出现的某个数值**被证明**单调（配合连续数字 embedding）？
- 什么架构能让 P(metric direction = up | 含数字 x 的文本) 对 x 可认证地单调，而其余部分仍是 transformer？请对照 T2.2 的设计，找出漏洞。
- 把模型输出对输入数值的导数当作"Greeks"来定义、估计、给出界，有没有先例？可行性如何，主要障碍是什么？

**Q11. 实体中性与精确不变性。**（对应 T2.4）

综述实体匿名化文献：

- Glasserman–Lin（2309.17322）的匿名化与"分心效应"；
- Engelberg 等 2025 的 entity neutering；
- 批评匿名化损失信息的工作（2511.15364；MemGuard-Alpha 2603.26797 引用的 Wu 等）。

回答：

- 实体泄漏在金融任务中的效应量有多大？
- 有没有架构能**由构造**对实体身份精确不变？候选包括：占位符、指针或复制机制、类似 de Bruijn 索引的变量绑定、对实体槽置换等变。
- 这样的模型如何仍然完成依赖目标实体的判断？损失了什么？

---

## C. 数值与可验证监督

**Q12. 数字表示的比较。**

比较以下方法：xVal（2310.02989）、Number Token Loss（Zausinger 等）、FoNE（2502.09741）、BitTokens（2510.06824）、Abacus embeddings（McLeish 等 2024）、NumeroLogic、对数量级或科学计数法的编码。

对每个方法给出：编码方式、范围与精度、对哪些运算有帮助、输出如何解码、在参数量不超过 50M 的模型上的结果、失败模式。

然后回答：

- 哪一个最适合金融文本？金融文本的特点：动态范围从 1e-4 到 1e12、有符号、有百分比和基点、带单位、用括号表示负数。
- 哪一个最容易接上 T2.2 的"数字只走连续通道"的设计？
- 有没有任何一个被用在金融语言模型或 FinQA / TAT-QA / XBRL 任务上？

**Q13. 量纲与单位等变。**（对应 T2.3）

解释以下工作：Villar 等 "Dimensionless machine learning: Imposing exact units equivariance"（JMLR 2023，2204.00887）、"Towards fully covariant machine learning"（2301.13724）、基于 Buckingham Pi 的网络。

回答：

- 单位等变或量纲分析有没有被用于 (a) 语言模型的数字通道，(b) 金融或会计数据（基本量纲：货币、时间、股数、计数）？
- 对一个带数字通道的文本模型，"货币重计价等变"和"报告尺度不变（千元与百万元）"分别意味着什么？请形式化。
- 能否由构造精确实现？请对照 T2.3，指出其中的问题。
- 神经定价模型里的 numéraire 不变性，有没有可以借用的先例？

**Q14. XBRL 作为免费的可验证监督。**

描述以下数据和规则：SEC 的 Financial Statement Data Sets 与 Financial Statement and Notes Data Sets（各包含哪些文件，是否包含 calculation linkbase，`sub` 文件里的 `accepted` 字段的精确含义）、companyfacts API、calculation / presentation / definition linkbase、XBRL US 的 DQC 规则、units / decimals / scale 属性、inline XBRL 中文本与 fact 的对齐。

给出 2009 年以来每年的数据量和许可证。

回答：哪些任务可以自动标注并精确校验？候选包括：标签映射、fact 抽取、calc 一致性、符号错误、尺度错误、期间对齐、重述检测。

总结 FinTagging（2505.20650）、FinAuditing（2510.08886）、FiNER-139、FNXL 的结果：大模型在哪里失败？小的专用模型是否更好？

**Q15. 会计恒等式和无套利关系作为硬约束。**

有没有工作把会计恒等式（资产 = 负债 + 权益；三张表的勾稽；小计关系）或无套利关系，用在面向文本的神经模型或 LLM 上？形式可以是损失、约束解码、投影层或 verifier。

相关技术：硬约束网络（DC3、HardNet、投影层）、用 SMT 或 CP 求解器做约束解码、数据调和（data reconciliation）。

有没有"在会计恒等式约束下补全被遮蔽的财务报表"这样的 benchmark？如果没有，请给出任务的精确定义和可自动校验的评分方式。

**Q16. 合成的可控世界（金融版 TinyStories）。**

综述用带真值世界模型的合成语料研究小语言模型的先例：TinyStories、合成 PCFG 语言、Othello-GPT、BabyLM。

回答：

- 有没有人做过这样的合成金融文本生成器：一致的会计模拟器 + 随机价格过程 + 模板化叙述 + 时间戳，使得信息集、数字和立场都由构造已知？
- 什么设计原则能让合成世界里的发现迁移到真实文本？
- 在验证成员推断或泄漏检验时，"植入已知污染"的实验是怎么做的？检验功效是怎么报告的？

---

## D. 输出语义与决策（P3 及其扩展）

**Q17. Elicitability 与 proper scoring。**

综述用严格一致的评分函数训练神经网络或语言模型的工作：

- 分位数、expectile、(VaR, ES) 的 Fissler–Ziegel 损失（Patton–Ziegel–Chen 2019）；
- 用 CRPS 或 energy score 训练的天气模型（GenCast、FGN）；
- 语言模型的分布头（分位数头、分箱头）。

回答：有没有人训练文本模型，输出公告后收益或波动的 (VaR, ES) 或完整预测分布，并用 proper scoring rule 训练？在这个视角下，bearish / neutral / bullish 这个类别标签对应什么泛函？"立场"是 elicitable 的吗？

**Q18. 观点的结构化输出。**

参考对象：Black–Litterman 的 (P, q, Ω)、entropy pooling（Meucci）、opinion pooling。

回答：有没有工作从文本中抽取"作者的观点"（目标、方向、幅度、期限、置信度、条件），并映射为这样的形式对象？请考察：

- LLM-BL（2504.14345）。注意它用的是 LLM 自己的收益预测，不是文本作者的观点。
- 分析师报告的目标价与评级抽取。
- structured sentiment analysis（SemEval-2022 Task 10 的 holder–target–expression 元组）。
- FinEntity、SEntFiN、FiQA。
- 事件事实性与 hedging、条件句。

另外回答：金融领域有没有同时标注 holder、target、条件、期限的数据集？"条件立场"有没有形式语义，例如写成条件期望或情景观点？

**Q19. 时间漂移下选择性预测的保证。**

考察：conformal risk control、non-exchangeable CRC（2310.01262）、adaptive conformal inference（Gibbs–Candès）、Conformal Selective Acting（2605.20270）、"When Can Conformal Risk Control Certify LLM Outputs?"（2606.29054）、domain-shift-aware conformal（2510.05566）、quantile / CVaR 风险控制（Snell 等 2022）、基于 e-value 的 anytime-valid 风险控制。

回答：哪些保证在以下三种情况下仍然成立？

- (a) 按时间排序且有漂移的数据；
- (b) 校准样本成簇相关（同一事件的多个视图）；
- (c) 校准集很小。

请给出 n = 101、1,000、4,000 时有限样本界的具体数值。

**Q20. 依赖不确定下的错误数风险。**（对应 T3.1、T3.2）

核实 T3.1 的论证：簇内同单调在凸序下最大，凸序在独立相加下保持，ES 与凸序相容。

回答：

- 这个"部署风险证书"是否已知？
- 把"依赖不确定性下的风险聚合"理论（Embrechts–Puccetti–Rüschendorf、rearrangement algorithm、Fréchet 界、joint mixability）与机器学习评测（cluster-robust 标准误、Miller 2024 "Adding Error Bars to Evals"、design effect、有效样本量、block bootstrap）对接，有没有人做过？
- Bernoulli 之和在依赖不确定下的最坏 VaR 有没有闭式？

**Q21. Log-loss、Kelly 与鞅视角。**

序贯 log-loss、压缩和 Kelly 增长率是同一个量。相关理论：Cover–Thomas；Cover 的 universal portfolio；Shafer–Vovk 的博弈论概率；Dawid 的 prequential 分析；Grünwald 的 MDL；2602.04146 把码长、log-loss 和 e-process 联系了起来。

回答：有没有人把语言模型在按时间排序的文本流上的累计对数似然比当作财富过程或 e-process，用于以下目的？

- (i) anytime-valid 的模型比较；
- (ii) 变点或知识截止日检测；
- (iii) 评估 point-in-time 模型。

参考 2607.17409（用 betting 做序贯 LLM benchmark）。正确的原假设是什么？有效性上有哪些陷阱，比如复合原假设、非平稳？

---

## E. 架构与训练的迁移

**Q22. 递归小模型。**

考察：HRM、TRM（2510.04871，5M–19M 参数）、对 TRM 的批评（2512.11847）、ARC Prize 对 HRM 的分析、Komisarczyk 等 2026 的 SMC 解释、Universal Transformer、deep equilibrium models、deep supervision。

回答：

- 哪些结论是稳健的？
- 有没有应用到网格谜题以外的任务，比如类语言任务、表格、带实数算术的约束满足？
- "补全一张被部分遮蔽、必须满足会计恒等式的财务报表"能否写成 TRM 式的任务？
- 关于实数上的算术约束，已有证据说明了什么？

**Q23. JEPA 与多视图目标。**

说明 LLM-JEPA（2509.14252）的方法细节、额外计算代价、增益、消融，以及 2026 年的后续工作。它与 SimCSE、data2vec、多视图冗余理论（Tosh 等 2021）、VICReg 是什么关系？

金融里有一些天然成对的视图：叙述段落 ↔ XBRL facts、标题 ↔ 正文、原文 ↔ 许可的编辑。对这些视图，理论预测表示会保留哪些信息、丢弃哪些信息？有没有参数量不超过 50M、从零训练的证据？

**Q24. 从零训练的领域小模型在哪里赢。**

跨领域比较"从零训练"与"改造通用模型"：

- 生物医学和科学文本：PubMedBERT、SciBERT；
- 生命科学：蛋白质语言模型（ESM）、化学和基因组语言模型、单细胞基础模型（Geneformer 的 rank-value encoding、scGPT），以及"简单基线与之持平"的批评；
- 小规模语言建模：BabyLM 的结论、TinyStories；
- 金融：BloombergGPT 与 GPT-4 的比较、FinBERT2（2506.06335）、轻量 LLM 与 FinBERT 的比较（2512.00946）。

请提炼"从零训练是合理的"的条件。候选包括：非自然语言模态、分词不匹配、信息集控制、隐私、可认证性。

另外回答：有没有任何参数量不超过 50M、从零训练的 decoder，在任何 FinNLP benchmark 上有竞争力？

**Q25. 前沿金融 LLM 配方里真正的 idea。**

对以下模型，逐一给出：底座模型、数据、训练目标、RL 奖励的设计（可验证的，还是 judge 打分的）、评测，以及一句话概括"真正的 idea"：

Fin-R1（2503.16252）、DianJin-R1（2504.15716）、Agentar-Fin-R1（2507.16802）、FinDAP / Llama-Fin（2501.04961）、Open-FinLLMs、Fino1、FinGPT / FinLoRA、XuanYuan、Kronos（2508.02739）、MarS / LMM（2409.07486）、TradeFM（2602.23784），以及仓库文档引用的 Eva-4B、FinanceParam、FinLCR。

然后回答：

- 哪些 idea 不依赖算力，可以迁移到 24M 模型上？候选：数据课程、奖励设计、非文本模态的 tokenization、评测协议。
- 以下评测里，哪些对极小模型是可行的：FinBen、FinanceBench、FinChain（2506.02515）、FinAuditing、FinTagging、FinDendro、HindsightBench？

**Q26. 机制可解释性：target binding。**

考察：

- Binding-ID 机制（Feng–Steinhardt，2310.17191）；
- Gur-Arieh–Geva–Geiger 2025 "Mixing Mechanisms"；
- Oh–Demberg 2026（2606.08644）；
- 情感的线性表示（Tigges 等 2023）；
- 否定回路；
- 金融方向的 SAE 工作："A Financial Brain Scan of the LLM"（2508.21285）、SAE-FiRE（2505.14420）、2412.02605、2505.24650。

回答：

- binding 机制在多大的模型上出现？
- 有没有人研究过依赖目标实体的情感回路、引述或归属（holder）回路，或者反事实样本对训练如何改变回路？
- 对一个 24M 模型，可行的研究设计是什么（probing、activation patching、小型 SAE 或 transcoder）？
- 什么样的结果算得上"证书式"的？候选：causal abstraction、interchange intervention accuracy。

**Q27. AI-for-Math 的 verifier-in-the-loop。**

AlphaProof、AlphaGeometry 2、DeepSeek-Prover-V2、Kimina、Seed-Prover 的范式是"生成 → 验证 → 以验证结果为奖励"。Lean 4 的数理金融库（2606.01356）、机器验证的 Itô 积分（2606.15089）、Nagy 的"从 Itô 到 Black–Scholes"（SSRN 6336503）已经存在。

回答：这个范式的哪一部分能在极小规模上迁移？

- (i) 金融里有可验证奖励的环境：会计校验、无套利校验、用区间算术给数值声明出证书、FinChain 式的可执行轨迹。
- (ii) "带证明的答案"：模型输出附带一个可以校验的证书。

另外回答：

- 有没有工作把 LLM 的输出和验证数值计算（区间算术、认证舍入）结合起来，用于量化金融？
- 一个参数量不超过 50M 的模型，要在 XBRL facts 上输出可以校验的计算程序，最小的 DSL 应该是什么样？

**Q28. 语言模型的泛化证书。**

考察 Lotfi 等人的两篇工作："Non-Vacuous Generalization Bounds for Large Language Models"（2312.17173）和 "Unlocking Tokens as Data Points"（2407.18158，用了鞅集中不等式）。给出：精确的假设、在 GPT-2 规模上得到的界、所需算力、2025–2026 年的后续工作。

回答：

- 能否在 T4 上，为一个从零训练的 24M 模型算出非空的界（通过量化压缩）？
- 在时间分布漂移下（训练用 t 之前的数据，测试用 t 之后的数据），token 级的鞅界会怎样？
- 有没有 prequential 或在线版本（online-to-batch、基于 regret、MDL 的 prequential 码长），能在没有 IID 假设时给出对未来有效的保证？

---

## F. 新增：由理论草稿引出的问题

**Q29. 数据投毒的认证防御能否直接用于 look-ahead。**（对应 T1.3）

考察：Deep Partition Aggregation（Levine–Feizi，ICLR 2021）、Finite Aggregation（Wang–Levine–Feizi，ICML 2022）、bagging 的内禀认证鲁棒性（Jia–Cao–Gong，AAAI 2021）、collective robustness certificates（Schuchardt 等，ICLR 2021），以及 2023–2026 年的后续工作，包括对生成模型、语言模型、对比学习的投毒认证。

对每个方法给出：精确的认证条件、平局规则、对确定性训练的要求、可认证的 k 与分片数 m 的关系、在文本任务上已报告的认证准确率。

另外回答：

- 有没有人把这些方法用于时间污染或 look-ahead？
- 对"整个回测统计量"这种集体量，有没有比逐点认证更紧的集体证书？计算复杂度是多少？
- 用"冻结骨干 + 分片线性头"这种设计时，已有工作怎么报告准确率代价？

**Q30. 时间戳审计的统计学与证书组合。**（对应 T0.2、T1.4）

如何设计抽样审计，来估计语料中时间戳错标的文档数，并给出精确的置信上界？考察：超几何精确区间、按来源的分层抽样、用 e-process 做序贯审计和提前停止。

另外回答：

- 审计结论如何与一个确定性证书组合成一个整体的概率证书？union bound 之外有没有更好的组合方式？有没有关于"概率证书 + 确定性证书"组合的已有文献（例如 PAC 验证、统计模型检测）？
- 对 EDGAR、FOMC、Federal Register、Wikipedia、新闻这几类来源，已知的时间戳错误或修订机制分别是什么？哪些时间戳是机器生成、事后不可更改的？

**Q31. 有序模型、单调性与随机占优。**（对应 T2.1、T2.2、T2.6）

考察：累积链接模型（McCullagh 1980）、神经网络有序回归（CORAL、CORN 等）、带单调约束的有序模型。

回答：

- 有没有工作保证"某个输入增大时，输出的类别分布按一阶随机占优上移"？
- 这个性质与单调网络（Q10）结合，是否已有人做过？
- 在金融文本的 stance 任务上，"对数值证据单调"作为规范是否合理？有没有心理学或金融学证据表明作者立场对证据强度单调？反例有哪些（逆向投资者、预期已被定价）？

**Q32. 金融文本的数量与单位抽取。**（P2 的统计环节）

从金融文本中抽取数值、单位、尺度、期间和比较基准，最新的方法和准确率是什么？考察：quantity extraction 工具、FinQA / TAT-QA 的程序解析、inline XBRL 对齐、用 LLM 抽取。

常见的错误类型包括：括号负数、"bps"、"x"倍数、"千 / 百万 / 十亿"、货币符号、财年与日历年。

另外回答：

- 能否给解析错误率一个统计证书？例如在有 inline XBRL 标注的文本上，用 XBRL fact 作为真值自动评估。
- 小规则系统和小模型的准确率差距有多大？
