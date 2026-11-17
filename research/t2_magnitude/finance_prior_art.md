# T2 金融文本数值扰动：查重分支记录

检索日期：2026-11-16（America/New_York）。这是主对话查重的一个独立分支，不是系统综述，也未运行新的模型评分。结论仅覆盖下列实际读取的资料；没有重新执行论文代码。

## Charter

- 目标：判断 T2 的金融数字大小—情绪分数测量，是否已有实质相同先例；将一般数字理解工作与目标响应曲线分开。
- 范围／对象／比较单位：金融文本模型行为／数字大小、表达与情绪输出／论文的输入干预、输出变量、曲线和控制条件。
- 类型：探索式查重；初始知识深度为初步了解。
- Q1：T2 测量什么？Q2：哪些部分已有直接先例？Q3：尚存的差异是否支持原题继续？
- 来源顺序：用户任务定义；原始论文全文与附录；正式出版元数据；搜索结果只作线索。

## Canonical sources

| 编号 | 原始来源与日期 | 本分支实际访问 |
|---|---|---|
| S1 | Marks & Vollberg, [The psychophysics of affect in large language models](https://arxiv.org/abs/2610.40985)，预印本 v1，2026-10-29 | 打开 [64 页 PDF](https://arxiv.org/pdf/2610.40985)，读取摘要、Methods 的 stock-trading 设计、Supplement S2 的模型比较、S8 提示；未逐页读完所有选择任务附录，未运行数据或代码 |
| S2 | Huang et al., [NASH: Numerically Aware Scoring Heuristic for Robust Semantic Similarity](https://aclanthology.org/2026.findings-acl.1119/)，ACL Findings 2026，7 月 | 打开 [15 页论文](https://aclanthology.org/2026.findings-acl.1119.pdf)，读取 §4 数值增强、§4.4 评估定义、§5.1 模型对象 |
| S3 | Yang et al., [Measuring Consistency in Text-based Financial Forecasting Models](https://aclanthology.org/2023.acl-long.769/)，ACL 2023，7 月 | 打开 [15 页论文](https://aclanthology.org/2023.acl-long.769.pdf)，读取 §3 与四类转换定义 |
| S4 | Chen et al., [Enhancing Financial Sentiment Analysis with Expert-Designed Hint](https://arxiv.org/html/2409.17448v1)，2024-09-26 | HTML 正文 §3–5、限制与参考文献；另检出 2025 workshop 版本题为 Numbers Matter，未把两版算作独立证据 |
| S5 | Zhang et al., [Instruct-FinGPT: Financial Sentiment Analysis by Instruction Tuning of General-Purpose Large Language Models](https://arxiv.org/pdf/2306.12659)，2023-06-22 | 打开 7 页 PDF，读取任务定义、分类输出与 numerical sensitivity 子集说明 |
| S6 | Chen & Guo, [Shapley in Context: Explaining Financial Language with Domain Expertise](https://arxiv.org/html/2607.00856v1)，2026-07-01 | HTML §2–3 的 FinBERT 输出和单调性定义；[Duke 出版记录](https://scholars.duke.edu/publication/1915490)列正式期刊版本 2026-08-14 |
| S7 | Jo et al., [Change the Number, Change the Answer: Assessing Rating Scale Sensitivity in LLM-Based Text Scoring](https://arxiv.org/html/2610.22187v1)，2026-10-15 | HTML 摘要、实验设计及评分尺度定义；只用于测量混杂提醒 |

以上为作者论文或正式出版渠道，按本轮等级均为 rank 1；S6 的作者所在机构出版目录只核验元数据。

## Findings ledger

| ID | 核验后的主张 | 定位 | 等级／问题 |
|---|---|---|---|
| F1 | S1 已将股票涨跌百分比作为输入幅度，将预期感受作为数值输出，并比较正负曲线与上下文条件。 | S1 Methods，PDF 第 14–15 页；S8 第 46 页 | 1／Q2 |
| F2 | S1 的 Study 2 用同一 20 点网格覆盖涨跌，输出 −50 至 +50；并比较线性、幂函数和饱和 tanh 等拟合。 | S1 Methods、S2（PDF 第 30 页）、S9（第 48 页） | 1／Q2 |
| F3 | S1 报告单独评分时边际敏感度递减及收益侧放大；共同呈现时曲线更线性。这说明幅度曲线、涨跌不对称与评分上下文并不是尚无人测量的问题。 | S1 摘要、Methods、S2 | 1／Q2、Q3 |
| F4 | NumFinE 对固定金融句中的数字做幅度变化，但评价的是语义相似度能否按数值距离排序，而非金融情绪强度。 | S2 §4.2、§4.4；PDF 第 5–6 页 | 1／Q2 |
| F5 | FinTrust 的四类测试为否定、语序对称、添加无关文本、实体替换；不能将其当作等值数字单位改写研究。 | S3 §3.1，PDF 第 4 页 | 1／Q2 |
| F6 | S4 比较数字提示是否改善金融社媒三分类，并按数字类别分组；S5 也将 numerical sensitivity 用于分类评估。两者都未建立 T2 式连续输入响应曲线。 | S4 §3–5；S5 §3–4 | 1／Q2 |
| F7 | S6 对 Shapley 归因提出单调性等公理；示例改变词语语气，不能把其理论公理等同于已测量数字大小曲线。 | S6 §3.1–3.2 | 1／Q2 |
| F8 | S7 操纵的是输出评分尺度的格式、范围、符号，包括 sentiment 任务；它不是输入金额变化实验，但说明评分尺度需固定或另设控制。 | S7 §2.1、§3 | 1／Q3 |

## 查重矩阵

“未见”仅指本分支检查的相关方法和结果，没有证明整篇不存在任何补充分析。

| 比较项 | T2 原题 | S1 psychophysics | S2 NumFinE | 其余金融研究 |
|---|---|---|---|---|
| 固定语言框架改变数字 | 是 | 是，金额／股票涨跌百分比 | 是，真实金融句反事实 | S4/S5 主要为自然数据子集分类 |
| 数字大小→连续情感评分 | 是 | **直接重叠** | 否，语义相似度 | 未见 |
| 正／负方向与曲线形状比较 | 是 | **直接重叠**，同时研究上下文 | 数值距离排序，不是正负情绪 | 未见同样曲线 |
| 公司新闻的实体情绪 | 是 | 否，持股者预期感受 | 否 | S4/S5 是金融情绪分类 |
| 10／50／100 局部关口 | 是 | 未见针对该问题的局部断点设计 | 未见 | 未见 |
| 同一金额／比例的单位表达 | 是 | 未见等价单位对照 | 幅度改变，不是等价单位不变性 | FinTrust 不做此转换 |
| 重复评分／呈现上下文控制 | 是，混合填充标题 | **已有独立／记忆／共同呈现条件** | 不是相同测量目标 | S7 提醒输出尺度混杂 |

## Scope filter

将“金融数字理解或不变性已有研究”收窄为三个不同问题：数值是否读对、语义距离是否保序、情感输出如何随幅度变化。删除“FinTrust 已做数字单位改写”的初步印象；正文并不支持它（F5）。NumFinE 不能作为情绪曲线已做完的证据（F4）。

## Object filter

S1 的输出是模型模拟持股者感受，不是 T2 的公司新闻实体情绪；因此它支持“主要实验逻辑和候选现象已有直接先例”，不支持“T2 的全部三组实验已被原样完成”。S1 的函数拟合和上下文效应对 T2 很近，但不证明现代所有模型在所有金融模板上有同样曲线（F1–F3）。

## Conclusions

1. **建议停止把原 T2 作为新的泛化行为现象题继续投入。** 最关键的数字幅度→情感响应曲线、边际敏感度和正负不对称，已在 S1 的金融场景中测量；只换成利润／罚款标题或平移评分量表，尚不足以说明新贡献。T2 原文件尚未指定量表。这是基于 F1–F3 的研究定位判断，不是“完整逐项撞题”的事实宣称。
2. **保留“局部关口×等价表示×实体情绪”的精确残余问题，但本分支没有证据认证其新颖性。** 它需要结合其他分支对左位数效应、单位不变性的核查；不能从本分支的未检出推出没人做过。
3. **若后续另立窄题，必须区分测量目标。** 实体语义情绪、模拟投资者感受、价格预测、embedding 相似度不应混合；同时固定输出评分尺度，并在独立输入与混合批次之间加入对照（F4–F8）。

## Next steps / Risks

- 本轮按用户“查到相近实质工作当天停”的研究优先级，不建议进入原 T2 的正式评分；由主对话整合各分支作最终判断。
- 对数线性不是天然的正确性标准。若事件风险、有限评分上界或提示尺度导致饱和，不能仅凭不服从某个曲线就判定数值理解错误。这是本报告的设计分析，而非既有实验结果。
- 部分检索线索无法全文访问：Battle of transformers（期刊页及 SSRN 403）；ConFIT（OpenReview 验证页）。它们不作为停止原题的决定性证据。NASH 的 OpenReview 旧页也受验证阻挡，但已用正式 ACL 全文完成核验。
- 未检索所有学位论文、付费全文或每个作者代码仓库；未做引文数据库的穷尽前向追踪。没有声称“半天已实际用满”或穷尽查重。
- 自查结果：关键事实有原始全文定位；结论已限定“核心逻辑重叠”而非完整重复。未重新执行论文代码；未把来源中的作者解释当成我们已复现的结果。

## 检索记录

使用公开网页检索，在结果中优先打开 arXiv、ACL Anthology 和论文出版页。实际查询包括：

1. financial sentiment analysis numerical perturbation numbers magnitude large language models
2. "financial" "sentiment" "numerical" "sensitivity"
3. "language models" "sentiment" "magnitude" numbers
4. "9,227" "numerical" "financial"
5. "financial sentences" "controlled numerical"
6. "financial sentiment" "perturbations" numbers
7. "Battle of transformers" Leippold pdf
8. "NumFinE"
9. "Battle of Transformers" "Leippold"（排除部分二手目录）
10. financial sentiment numerical perturbation magnitude monotonicity benchmark
11. LLM financial sentiment "numbers" "change" "monotonic"
12. language model "profit" "sentiment" "magnitude"
13. financial sentiment "unit" "invariance" language models
14. "NASH: Numerically Aware" ACL 2026
15. "Shapley in Context" financial language
16. "financial sentiment" "numerical perturbation"
17. "sentiment" "magnitude" "psychophysics" language models
18. "financial sentiment" "numbers" "counterfactual"
19. "numerical sensitivity" "sentiment" language models

S1 的具体 arXiv 标识来自并行分支转介；本分支随后独立打开 PDF 核验上述重叠。单位不变性来源 2609.25009 已转交对应分支，未重复写成此分支结论。
