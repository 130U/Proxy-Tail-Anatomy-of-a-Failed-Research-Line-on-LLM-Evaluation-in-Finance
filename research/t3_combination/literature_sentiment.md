# T3 情绪组合查重：金融情绪与顺序效应分支

检索日：2026-11-16（America/New_York）。这是有边界的定向查重，不是系统综述，也不声称已耗时半天。未执行模型评分。

## Charter

- 目标：核对是否已有“单条事实得分 → 成对拼接 → 相加、平均、负面权重及顺序反转”的同问题、同测量研究；查到即建议停止重复实验。
- 范围 / 对象 / 单位：LLM 情绪测量 / 同一实体的好坏事实组合 / 单条与组合数值评分、无关中性信息、顺序效应。
- 类型：探索性；对测量定义已有理解，对文献覆盖不预设新颖性。
- Q1：同一情绪整合测量是否已出现？Q2：中性稀释、负面不对称和顺序效应分别有哪些先例？Q3：哪些先例只能作为背景？
- 来源：原始论文正文与附录（1），作者上传全文（1，但单独标记出版状态）；检索摘要仅作线索。

## Canonical sources

| 来源 | 已核读部分 | 用途 |
|---|---|---|
| Socher et al. (2013), [Recursive Deep Models for Semantic Compositionality Over a Sentiment Treebank](https://aclanthology.org/D13-1170.pdf) | §5.3，Figure 7，论文第 8 页 | 对立子句的经典情绪组合 |
| Temkit (2026), [AMEL: Accumulated Message Effects on LLM Judgments](https://arxiv.org/html/2605.22714v1) | §3.1–3.4、§4.5、§9 | LLM 评价历史的负面不对称；预印本 |
| Alessa et al., [Quantifying Cognitive Bias Induction in LLM-Generated Content](https://www.jskirzynski.com/static/cognitive_bias_llm.pdf) | §4、§7.2、§7.4、Appendix A.6 | 摘要情绪漂移与前部内容偏重；作者全文 |
| Mavillonio et al. (2026), [Measuring sentiment news with transformer-based language models](https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3283~df0633dfd3.de.pdf?495f4d0ec675f3cbda625976eb20dff3=) | 封面、摘要、Appendix A / Table A.1 | 金融新闻句子得分的显式聚合；ECB WP 3283，2026 年 9 月 |
| Liu et al. (2024 online; 2025 volume), [Longitudinal Sentiment Analysis with Conversation Textual Data](https://link.springer.com/article/10.1007/s40647-024-00417-0) | §4.2、§4.3.2–4.3.3 | 算术平均的中性稀释及零值降权 |
| Rawat, Kang & Vardham (2026), [Beyond Accuracy: Adversarial Robustness and LLM Benchmarking for Financial Sentiment Analysis in Social Media](https://www.researchgate.net/publication/403468872_Beyond_Accuracy_Adversarial_Robustness_and_LLM_Benchmarking_for_Financial_Sentiment_Analysis_in_Social_Media) | §3、§5.1；作者 2026-04-03 上传全文 | 排除标题和“signal dilution”关键词造成的假撞车 |

## Findings ledger

| # | 可核查发现 | 证据、等级 | 回答 |
|---|---|---|---|
| S1 | Socher 等在 131 个 X-but-Y 测试例中联合检查子句与整句情绪，明确以第二子句承载主论点。该研究是训练式情绪分类，未做 T3 的独立数字基线、平均/相加比较或双顺序配对。 | Socher §5.3 / Fig.7；1 | Q1、Q3 |
| S2 | AMEL 比较同一目标在无历史、90% 肯定、90% 否定、50/50 历史下的二元判断；负面历史效应强于正面。但其“中性”是正负评价历史各半，绝非添加一条无情绪事实。作者明确限制为 yes/no、代码审查/内容审核/饮食判断。 | Temkit §3.1–3.4、§4.5、§9；1 | Q2、Q3 |
| S3 | Alessa 等比较原文和摘要的三类情绪是否一致，并用摘要与原文前、中、后三段的嵌入相似度量化内容偏重。不是对两个单独事实打分后估计其数值组合函数。 | Alessa §4、§7.2、Appendix A.6；1 | Q2、Q3 |
| S4 | ECB 工作论文先用 FinBERT 给金融新闻句子分类，再由研究者定义多种文章级指标。包含中性句的 (pos−neg)/(pos+neg+neu) 会稀释；排除中性句的指标不会。该比较是外加聚合规则，不是发现生成式 LLM 自行取平均。 | Mavillonio et al., Appendix A / Table A.1；1 | Q2、Q3 |
| S5 | Liu 等使用 sentimentr 的词典情绪提取，明确指出将中性零分纳入算术平均会稀释整体分数，并比较零值降权方案。不是 LLM 行为实验。 | Liu et al. §4.2、§4.3.2–4.3.3；1 | Q2、Q3 |
| S6 | Rawat 等所谓“signal dilution”是长、多主题推文中改动方向词后 FinBERT/VADER 分数不变；LLM 部分主要是三类分类对照。未发现单条/成对数字评分及平均/相加模型选择。 | Rawat et al. §3、§5.1；1（课程项目作者稿，非已确认同行评审） | Q1、Q3 |

检索实际使用的核心查询包括：`LLM sentiment analysis neutral information dilution effect negative positive order bias`；`large language models sentiment composition averaging positive negative information integration`；`"large language models" "dilution effect"`；`"sentiment" "order" "positive and negative" "large language models"`；`"LLM" "averaging" "sentiment" "neutral"`；`"LLM" "sentiment" "primacy" "recency"`；`"large language models" "negativity bias" "sentiment"`；`"sentiment" "compositionality" "LLMs" contrast`；`"sentiment" "dilution" "ChatGPT"`；`LLM "mixed sentiment" order effect`；`"sentiment" "neutral sentences" "language models"`；`LLM "positive and negative information" judgment`；`"financial" "sentiment" "compositional" LLM`；`"LLM" "sentiment" "conjunction" "but"`；`"sentiment" "concatenation" "large language models" bias`；`"sentiment" "mixed" "order reversal" model`；以及各候选论文精确题名检索。

## Scope filter

排除“神经激活中的情绪方向是线性的”作为分数可相加的证据；线性表示与行为量表的组合函数不是同一命题。也排除多模型集成平均、金融推文流比例变化、模型生成情绪变化作为 T3 的直接重复。

## Object filter

S2 的跨项目评价历史不是一条标题内部的事实整合；S3 的摘要选择不是数值打分；S4–S5 是研究者定义的聚合；S6 是反义词替换。它们均不能单独满足“同问题、同测量”的停止条件。S1 则直接提醒：连接词引入的语义关系会改变整体情绪，不能把 `but` 的后半句主导都叫顺序偏差。T3 的 `as` 也可能表达原因或同时发生；固定分号的结果更容易解释。

## Conclusions

本分支未确认 T3 全套测量已被做过，不能据此宣布文献门失败，也不能宣布题目新颖。（S1–S6）

“平均含中性会稀释”本身是已有方法性质；若 T3 继续，可能增加的实证只是：固定提示下的生成式模型是否自发呈现该规律，以及规律能否解释独立事实组合。负面偏向、顺序效应和稀释不能笼统作为首次发现。（S1–S5）

根任务另核读的 Hämäläinen (2025), [NLP4DH 论文](https://aclanthology.org/2025.nlp4dh-1.18.pdf)，应纳入根报告：它有正负形容词列表顺序反转与独立 1–5 评分，是 T3 顺序分支更直接的先例。本笔记不将根任务转述当作本分支独立核读。

## Next steps / Risks

只有在整合其他分支后仍未发现相同测量，才进入既定小实验；不因广义“顺序偏差早已知”误杀尚未覆盖的数值整合问题。实验解释应预先区分句内组合、批次影响、连接词语义和量表压缩。

尚未取得 `Algorithmic Hesitation: Evaluating Confidence Drops in LLM Sentiment Analysis on Mixed-Emotion Text` 的原始 Zenodo 全文，只有作者发布线索；不据此判断撞车。FLUKE 的 PDF 曾超时，仅核对摘要，未用于上表结论。搜索引擎的个别日期有明显错误（ECB 页面曾显示十年前）；以原文封面的 2026 年 9 月为准。

内部证据核验：上述结论限于正文已核对的具体测量，不包含论文实验重跑或独立复现。
