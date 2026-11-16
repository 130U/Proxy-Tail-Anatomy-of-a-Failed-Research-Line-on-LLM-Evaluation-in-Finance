# 绝对评分新题：LLM 文献否决检查

检索日期：2026-11-16。对应仓库 TASK.md 的问题是：同一模型对金融标题重复绝对评分，均分后 top-p 名单是否稳定，以及单次信度能否通过 Spearman–Brown 加二元正态分布预测这种稳定性。本文件只负责 LLM 评分、重测、分批和聚合文献；不包含新的模型评分。

**结论：已找到理论骨架和多项测量的直接前例；尚未确认某一篇原文完成了本题全部对象与验证组合。不能把“重复评分、均分、批次效应、LLM 筛选召回、信度公式”中的任何一项单独声称为新贡献。** 最接近的两篇分别已经研究 LLM 在不同批次下的决定变化及 Gaussian 聚合预测、LLM 对人工头部候选人的筛选召回。本题若继续，定位应当是已知模型在“同一模型的双端头部自我重合”上的事前检验，价值取决于是否出现可复核的预测失败；金融标题换域本身不是理论创新。

这是本轮有明确边界的定向速查，**没有声称已完成半天检索或系统综述**。搜到的摘要、搜索片段只用来定位；以下证据来自打开的原文或作者稿中注明的部分。未做完整引文网络追踪，也未排除尚未索引的论文。

## 最接近的先例

### 1. Xie 与 Alanwar：Judged in Company（2026）

[原文 HTML，arXiv:2610.40241v1](https://arxiv.org/html/2610.40241v1)。阅读 §3、§5.2–5.6、§6，附录 H.3–H.5 和 I 的预测表。它将同一项目重新分批，区分成员、顺序和位置影响；在潜在 Gaussian 分数模型下，以精确二元正态积分从相关预测决定翻转，并研究跨排列/跨批投票。部分投票预测在新增运行之前作出，另有回拟合结果，不能混称全部独立验证。

**重复程度：很强。** 独立 context 均分降低噪声、阈值不稳定性及其 Gaussian 预测均已出现。未在所读部分看到本题的整数原始分均值、两组 m=2/4 的 top-p 双端重合与 q90/p 完整实验。它的主要实测对象是固定类别阈值和多数投票，潜在分数不是直接观察到的 0–100 分。

这里还有一个重要的数学对应（以下是本次分析的推论，而非声称作者使用了本题术语）：在平行测量模型

\[
X_{ij}=T_i+\epsilon_{ij},\qquad
r=\frac{\operatorname{Var}(T)}{\operatorname{Var}(T)+\operatorname{Var}(\epsilon)},
\]

条件独立、同方差的两组 m 次均分相关为

\[
r_m=\frac{mr}{1+(m-1)r}.
\]

若标准化均分为联合正态，令 h=Φ⁻¹(1−p)，同一边际比例 p 下的翻转概率 F 与头部重合 H 满足

\[
H=\frac{P(Z_1>h,Z_2>h)}p=1-\frac{F}{2p}.
\]

所以，“SB 再接 Gaussian 头部重合”在这些假设下是已有随机效应/阈值模型的直接组合，不能仅靠改写成头部语言宣称新定律。是否已有完全相同的头部测量仍是另一问题。

### 2. Stockdale、Hickman 与 Liu：Scoring Employment Interviews With Large Language Models（2026）

[作者提供的全文稿](https://www.researchgate.net/publication/403780997_Scoring_employment_interviews_with_large_language_models_Evaluation_design_components_validity_investigations_and_best_practice_recommendations)，[正式 DOI](https://doi.org/10.1037/apl0001396)。读到作者稿的评价设计、intrarater reliability、test–retest correlations、ensemble 讨论，以及表 7、14 与相应筛选正文；作者稿不保证与出版版逐字一致。

它研究行为锚定量表、示例、单人/九人批次、温度和聚合；**直接测量不同 selection ratio 下 LLM 留住人工头部候选人的 recall**，并考察先筛选再人工复核。作者特别指出，诚实回答与求职情境回答之间的 test–retest correlation 并不是真正同输入重测信度。

**重复程度：很强的应用与测量前例。** “高分候选人是否被 LLM 漏掉”及加宽筛选已有实测。所读正文和全文关键词检索未发现单次 r→SB→Gaussian→m=2/4 头部自我重合的无调参对照；不能以未搜到关键词代替排除全部公式等价形式。

### 3. Apartsin 与 Aperstein：CoEval（2026）

[原文 PDF，arXiv:2606.03650](https://arxiv.org/pdf/2606.03650)。阅读 §3.4、§5 的 panel-size 结果和附录 A。原文明确使用平均评委间相关和
\(R_k=k\bar r/[1+(k-1)\bar r]\)，并报告 ICC 与 SB 预测的吻合。

**重复程度：公式直接先例，但对象不同。** 它主要考察不同评委组成与模型排行榜，不是同一模型重复评分的标题头部。其同面板 ICC 与 SB 的数值一致也不能替代本题用单次相关预测未用于调参的头部结果。

## 其余已读原文

| 原文 | 实际读到的部分与支持内容 | 与新题的关系 |
|---|---|---|
| [Yuan 等，BatchEval，arXiv:2401.00437](https://arxiv.org/pdf/2401.00437)；[ACL 2024 记录](https://aclanthology.org/2024.acl-long.846/) | arXiv 作者版本 §2.2、§3、§4.3–4.5：迭代改变批次并平均分数，研究均分收益和批次参考；给出平方误差的 ensemble 分解。ACL PDF 下载超时，因此未把作者版本当作出版 PDF 已核读。 | 改分批与多次均分并非新设计。它主动利用批内比较、还按已有分数调分批，和本题固定提示/随机重分批不同；目标是对人工评分的整体相关。 |
| [Messing，Hidden Measurement Error in LLM Pipelines…，arXiv:2604.11581v1](https://arxiv.org/html/2604.11581v1) | §2.4、2.6、4.2–4.3 与 SI.1.6–1.7：分解项目、提示、评委、重复等方差，依据 D-study 预测增加重复或评委的收益。小 pilot 与 full-run 比较使用重叠数据，作者说明并非真正样本外验证。 | 测量误差分解和重复预算预测已有成体系工作；未见本题 top-p 双端名单对象。 |
| [Yagubyan，The Coin Flip Judge?，arXiv:2606.13685v1](https://arxiv.org/html/2606.13685v1) | §5.9–5.10：重复投票达到 50 次投票参考结论的概率随次数变化，以及 50 次 pointwise 分数的 ICC/方差分解。 | 重复次数—稳定性曲线已有前例；50 次参考共识不等于真值，投票忠实度也不等于头部名单重合。 |
| [Lau，Same Input, Different Scores，arXiv:2603.04417](https://arxiv.org/pdf/2603.04417) | §3–4：固定提示下数值评分重复十次，比较模型、温度、逐项目评分标准差。 | 数值评分不稳定已有直接证据；没有在所读结果中找到均分后的头部预测实验。 |
| [Stadler 等，JMIR Medical Education 2026，e94666](https://mededu.jmir.org/2026/1/e94666/) | Methods/Procedure、Data Analysis、RQ1：122 条临床摘要，四模型、四提示条件、五次无对话记忆重复；同时报告 ICC 和类别一致性。 | 锚定/示例量表和重测已有。尤其注意其 ICC 按五次平均计算，不能直接当本题单次 r；未见头部集合或 Gaussian 预测。 |
| [Liu 等，Evaluating large language models for abstract evaluation tasks，2026](https://www.frontiersin.org/journals/research-metrics-and-analytics/articles/10.3389/frma.2026.1807672/pdf) | PDF 方法与讨论第 6–7 页：摘要评分、人工/LLM 一致性；讨论明确用 SB 解释增加评委平均评分，并提出筛选/triage 应用。 | SB＋LLM 评分＋筛选在同文中出现；所读部分为解释与应用建议，没有本题同模型重复均分的 top-p 事前预测试验。 |

## 对本题的具体影响

本轮没有确认一篇原文同时满足“同一模型、同一项目重复绝对评分、两组均分、按 top-p 自我重合/固定召回加宽、仅单次 r 输入的 SB–Gaussian 实测验证”。因此不能据此宣布完全重复；同样不能宣布新颖。最接近的 Gaussian 批次论文必须优先交给 Fable，它使“新理论”的空间显著缩小。

如果按 TASK.md 继续，成立的工作定位是：**测量已知基准在指定、冻结的评分协议下何时失败**。将 raw 整数分取平均，同时从单轮秩的正态分数计算 r，并不自动满足平行测量的线性加性假设；所以公式应作为事前基准，而不是无需验证的保证。偏离可能来自分值非线性、异方差、并列、批次依赖或尾部依赖，不能只归因于“尾部失效”。这一点是对本题方法的推论，不是引用论文给出的实验结论。

同样，同模型头部自我重合只说明重测稳定性；不能据此断言金融事实正确、人工头部召回高、跨模型筛选可靠或经济价值为正。是否达到 90% 必须报告实际集合与不确定性，不能用与自身共识一致代替真实性。

本轮检索覆盖的关键词组合包括：`LLM test-retest reliability scoring`、`LLM Spearman-Brown`、`LLM Spearman-Brown selection/Gaussian`、`LLM top-p Spearman-Brown`、`repeated scoring top-k overlap`、`batch context judge score reliability`、`employment interview LLM selection recall`，并追读了上述直接相关全文的方法、公式和结果部分。搜索未返回精确组合不是不存在的证明；较旧心理测量与选拔公式的完整检索由另一条理论文献工作负责。
