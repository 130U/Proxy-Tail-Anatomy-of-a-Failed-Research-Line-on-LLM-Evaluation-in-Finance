# T3 信息整合与稀释效应：定向查重笔记

检索截至 2026-11-16（用户时区）。本笔记只回答文献门；没有生成模型分数，也没有声称已用满半天或完成系统综述。

## Charter

- 目标：核验是否已有与 T3 相同的问题与测量，区分理论先例、邻近行为研究和直接重复。
- 范围 / 对象 / 单位：LLM 判断行为 / 正负与中性信息的整合 / 单条消息基准与组合消息评分之间的函数关系。
- 类型：探索性。任务设计已知，文献覆盖待查。
- Q1：Anderson 相加/平均框架是否已有 LLM 同类应用？Q2：中性信息稀释是否已被直接测量？Q3：负面信息占优已有何种测量？Q4：哪些结果真正覆盖 T3？
- 来源：原始论文及作者/出版机构全文为第一层；检索摘要只作线索，不用它们作“没有做过”的证明。

## Canonical sources

| 来源 | 核读范围 | 用途 |
| --- | --- | --- |
| Norman H. Anderson (1971), *Integration Theory and Attitude Change*, Psychological Review 78, 171–206：[原文 PDF](https://fsnagle.org/files/anderson1971integration.pdf) | 全文可访问；重点 pp.175–176、181–182、188 | 相加/平均、初始印象、量表与权重的理论先例 |
| Mavillonio et al. (2026), *Measuring sentiment news with transformer-based language models*, ECB WP 3283：[机构 PDF](https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3283~df0633dfd3.de.pdf?495f4d0ec675f3cbda625976eb20dff3=) | §3.2、pp.11–12、Appendix A pp.34–38；45 页全文可访问 | 金融情绪汇总与中性稀释的最近邻 |
| Julien Benchek (2025-01-08), *Large Language Models Exhibit Cognitive Biases in Interactive Stock Trading Scenarios*：[大学托管原稿](https://bpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/9/3887/files/2025/01/Benchek_SRF24_Final_Paper.pdf) | §2.1–2.6、§3–4；10 页全文可访问 | 金融情境负面/正面锚定的行为先例；不将此原稿称为已同行评审 |
| Acerbi & Stubbersfield (2023), *Large language models show human-like content biases in transmission chain experiments*, PNAS 120(44), e2313790120：[原文 PDF](https://www.pnas.org/doi/pdf/10.1073/pnas.2313790120) | Results 实验 2、4，Methods；5 页全文可访问 | 正负与中性信息在摘要中的保留差异 |
| Park, Schoenegger & Zhu (2024), *Diminished diversity-of-thought in a standard large language model*, Behavior Research Methods 56, 5754–5770：[出版方全文](https://link.springer.com/article/10.3758/s13428-023-02307-x) | Methods、Results、Table 1 对应描述 | less-is-better 与顺序问题的邻近心理测量 |

以上均为原始研究/作者理论论文；全文存在不等于所有附录与代码均已复核。

## Findings ledger

| 编号 | 证据支持的主张 | 精确出处 | 层级 / 问题 |
| --- | --- | --- | --- |
| I1 | 人类信息整合中的相加与平均比较、加入较温和信息降低极端程度，早已是明确的实验范式。 | Anderson (1971), p.181，“Averaging versus Adding” | 原始理论，Q1 |
| I2 | “同值信息越多，判断越极端”也可由包含初始意见的平均模型解释。简单二项平均并不代表完整 Anderson 框架。 | Anderson (1971), pp.181–182，“Averaging versus Adding / Averaging Assumptions” | 原始理论，Q1/Q4 |
| I3 | 金融新闻已有基于 FinBERT 单句分类、再由研究者显式汇总的情绪指标；包含中性句的平均指标会稀释极性，排除中性句的指标则不同。 | ECB WP 3283, §3.2；Appendix A pp.34–38：`index_stat=(pos-neg)/(pos+neg+neu)` | 原始研究，Q2/Q4 |
| I4 | GPT-4o mini 交易研究已比较正/负市场消息以及无关天气/心情锚点造成的卖出价变化，并报告若干负面锚点影响较大。 | Benchek (2025), §2.4、§3 pp.7–8 | 原始研究，Q3/Q4 |
| I5 | ChatGPT 的迭代摘要中已有负面内容较正面内容更易保留的实测；另有威胁、负面、中性内容的保留比较。 | Acerbi & Stubbersfield (2023), Results 实验 2、4；Fig.2B/2E | 原始研究，Q3/Q4 |
| I6 | GPT-3.5 已被用于复现 less-is-better 心理实验，但该实验比较不同类别礼物的慷慨程度，不是把单条正负消息合并后预测情绪分。 | Park et al. (2024), Methods、Results；Table 1 研究 12 | 原始研究，Q1/Q4 |

开放项：本次定向检索尚未核实一篇同时具备“同实体单事实基准 + 正负/同向/中性配对 + 组合标题直接评分 + 相加/平均/负面系数比较”的 LLM 论文。此句描述检索结果，不能升级为已证明首创。

## Scope filter

排除了把 Anderson 的 **information integration theory** 与意识研究的 **integrated information theory** 混同的结果；后者不回答本题。也排除了注意力随长上下文扩散、训练数据稀释、版权市场稀释、多模型投票平均等同名但不同对象的工作。

人类的稀释效应提供假设和识别方法，不证明 LLM 已呈现同一机制。负面摘要保留、卖出价格和直接情绪评分是不同结果变量；不能相互代替。

## Object filter

- **I3 最接近领域，但不是直接撞车。** ECB 论文的合成函数由研究者指定；T3 要反推模型自己读组合文本时的合成函数。看到外置平均公式会被中性句稀释，不等于测到了 LLM 内生平均。
- **I4 最接近金融负面偏向，但测量不同。** 它比较交易决定在不同单个锚点下的变化，没有用单条情绪分预测双条情绪分，也没有估 T3 的组合系数 λ。
- **I5 已否决“LLM 会偏向负面信息是新发现”的泛化表述。** 它未识别金融标题情绪合成权重。
- **I6 不能用来宣称中性消息稀释已被做过。** 礼物类别的可评价性操纵与本题中性句添加不同。

## Conclusions

1. 在本分支的已核读来源中，**没有达到“相同问题且相同测量”的停止证据**；相加/平均模型及稀释概念本身早已有之（I1–I3）。这不是新颖性保证。
2. 若继续，贡献只能是特定模型、提示与金融组合标题上的可复现实测，而不能称“首次发现信息平均”或“首次发现 LLM 负面偏向”（I1、I4、I5）。
3. 应把 T3 三式明确叫作受限候选基准。即使同向组合更极端，也不能据此排除所有平均模型；带初始意见的平均是必须承认的竞争解释（I2）。
4. 中性添加造成回归 50，最多先支持这个评分任务下的稀释现象。没有给定决策目标与正确聚合规则，不能直接宣布它是金融漏洞；外置金融指标本就有不同的中性处理口径（I3，本条为研究判断）。

## Next steps / Risks

检索边界：英文公开 web 检索，组合使用 `large language models information integration theory Anderson`、`LLM averaging model judgments`、`ChatGPT dilution effect`、`LLM impression formation`、`LLM less-is-better effect`、`language models negativity dominance`、`LLM negative information positive information averaging`、`sentiment neutral sentences dilution` 等词，并追到最近原文。未做覆盖全部数据库的系统综述，未读全部引用链，未核对作者代码。

受限线索：Tak, Bolourani, Shank & Gratch 的 COLM 2025 [*Impact of LLM Alignment on Impression Formation in Social Interactions*](https://openreview.net/pdf?id=R135tO3SJJ) 搜索索引显示其比较 ACT 与 LLM 社会互动印象，但 OpenReview 正文读取遇到浏览器验证。本次只看到原始来源的摘要，不据此断言全文没有相关实验。原摘要的对象是性别化社会互动，而非金融标题。ACL 2026 *HumanLLM* PDF 因文件过大未成功打开，不能把其中 bias 名称清单当已核验实验。

本笔记的内部证据检查结果：上述 I1–I6 的窄主张有可读原文支撑；“尚未发现精确重复”需保留检索边界；T3 是否产生效应仍待实验，本文不填入任何估计值或区间。
