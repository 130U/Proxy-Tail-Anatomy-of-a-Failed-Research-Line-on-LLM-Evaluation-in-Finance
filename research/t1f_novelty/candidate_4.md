# 候选 4：判错的是同一批题

检索截止：2026-11-17。判定采用任务文件的三个「或者」标准，不把标准临时收窄成必须同时有原始测试集、最新模型、交集矩阵和大规模人工审计。

**结论：已有人做过同样的事；建议 ⚪；把握高。** FINESSE-Bench 已报告完整 1,147 道 FinQA test 上 53 个模型的共同失败率；另有 FinQA 判错归因分类、金融派生基准修订前后对比及 CodeFinQA 逐题跨模型互补分析。具体的“四运行共同错误 63 题、Jaccard 0.89–0.93、55/68 归于基准侧”仍可构成新的实证结果，但不能再以“原始完整测试集上的跨模型共同判错”保留首次性。尚未找到把大多数共同错误独立人工归因于基准侧的同样强结论；这是剩余增量的边界。

## 最接近的三项工作与原文短引

### 4A. FinanceReasoning（Tang 等，ACL 2025）

[正式论文](https://aclanthology.org/2025.acl-long.766/)；[正式PDF](https://aclanthology.org/2025.acl-long.766.pdf)；[正文与附录HTML](https://arxiv.org/html/2506.05828v1)。位置：§1、§2.1、Table 1、Appendix C.1（Tables 10–14）；正式版 Table 1 和引言在印刷 p.15722，Appendix A/C.1 在 p.15734。来源层级：**正文**。已直接下载正式PDF复核关键数字，并非只依据arXiv v1。

> “are saturated due to annotation quality”

其重标范围是 **CodeFinQA test 795**，不是原始 FinQA test 1,147；其余为 CodeTAT-QA test 288、FinCode test 47、FinanceMath validation 200。Table 1 的 CodeFinQA 修订为答案 55（6.92%）、消歧 58（7.30%），合计 113（14.21%）。四项修订合计 208/1,330≈15.6%，范围 9.72%–30%。**正式ACL版**引言（p.15722）及Appendix A（p.15734）仍把来源题数写成 1,420，与表中合计及 2,238−908=1,330 不一致；引用应以表格分母为准，不能照抄 1,420。这一不一致并未在正式版修正。

更新动作包括消歧、补充解题步骤及纠错；附录另区分不可解、表述歧义、步骤过简、错误答案、宽松判分。它比较两个 DeepSeek 模型修订前后准确率，但未见逐题共同判错矩阵。另同时改变判分约定，故分数增幅不能全归于标签修订。

**剩余新意判断：**细粒度错误原因及独立人工裁决可作增量审计；“标注质量限制旧金融基准”已明确提出，完整原始测试集的共同错误也已有下一项先例。

### 4B. FINESSE-Bench: A Hierarchical Benchmark Suite for Financial Domain Knowledge and Technical Analysis in Large Language Models（Stanishevskii 等，2026）

[作者原文v2](https://arxiv.org/html/2605.15482v2)；[PDF](https://arxiv.org/pdf/2605.15482v2)；[作者数据](https://github.com/LimexAILab/FINESSE-Bench/blob/main/data/finqa/question.jsonl)。位置：§5.1–5.3、§7.4 Table 8（PDF p.16）；v2日期2026-05-21。来源层级：**正文及原始公开数据**。

> “the share of questions that no model solves (unanimous fail)”

Table 8：FinQA **53模型、1,147题，共同失败9.33%、共同成功22.41%、10%–90%模型答对的中间带24.15%**。本轮另将作者question.jsonl与官方FinQA test.json逐行比对：1,147条问题均同序匹配，作者参考答案全部等于原始qa.exe_ans的字符串；因此完整测试题目的对应已核实，不是仅凭数量推断。校验摘要见 [数据身份核验摘要](data_identity_check.json)。其格式经过转换，统一使用GPT-5.2裁判，不能把分数直接等同官方执行准确率。

这直接满足“FinQA逐题跨模型比较、共同判错集合”标准。论文将该结果用于区分度与饱和分析，**并未证明9.33%是标签错误率**，也未提供多数共同错归于基准侧的人工因果审计。我们的Jaccard及具体归因仍有增量空间，但完整test、近期多厂商模型及共同失败现象本身已不是空白。

### 4C. Retrieval-Augmented Chain-of-Thought in Semi-structured Domains（Mavi、Saparov、Zhao，NLLP 2023）

[正式论文](https://aclanthology.org/2023.nllp-1.18/)；[正式PDF](https://aclanthology.org/2023.nllp-1.18.pdf)；[正文与附录HTML](https://arxiv.org/html/2310.14435)。位置：Appendix D.2，Table 7；已下载正式PDF核实第9页即印刷 p.186。来源层级：**正文**。

> “Error analysis of the incorrect examples on 40 samples from FinQA.”

40 道构建的验证样本中 30 道正确，余 10 道人工分类为算术 3、逻辑 2、标注 2、检索 3。因此已有明确的 FinQA 判错归因和数量（标注错误占此批错例 2/10）；样本小，且不是完整原始测试集。它满足任务的第二个先例标准，却不支持“多数剩余错误都来自基准”。我们的更强比例若获独立人工验证，属于结论强度上的增量。

## 额外的直接相关工作

### BizBench: A Quantitative Reasoning Benchmark for Business and Finance（Krumdick、Koncel-Kedziorski 等，ACL 2024；预印本 2023）

[正式记录](https://aclanthology.org/2024.acl-long.452/)；[正式PDF](https://aclanthology.org/2024.acl-long.452.pdf)；[正文HTML](https://arxiv.org/html/2311.06602)。位置：§4.1（逐题互补段落在印刷 p.8315）、Appendix A.2、Appendix B Table 5。来源层级：**正文**。正式会议确为ACL2024，全文pp.8309–8332；书目按ACL记录，PDF和arXiv中两位共同一作排序不同。

> “Models pretrained on language-only versus code solve different sets of questions.”

CodeFinQA 上，Llama-2-70B 答对 CodeLlama-34B 错题的 33%，反向为 25%，两者 oracle 组合达 68%。这已经是逐题跨模型错误重合/互补分析，只是对象是派生版本。其 50+25+25 个错输出还按抽取、公式、生成和问题歧义分类；类别允许重叠，不能把列相加当独立样本。正文讨论 gain/loss 正负号语义困难。A.2 将 FinQA 方程转 Python 并检查执行答案，不能据此断言审计了原始 answer/exe_ans 冲突率。

**剩余新意判断：**模型错误结构随时间的变化仍可比较，但近期模型共同失败也已有FINESSE先例；新增价值须落在更细的原因审计。

### 其他已读论文

- **FinQAPT（Singh、Kaur、Smiley，ICAIF 2024）**：[§4.5.1](https://arxiv.org/html/2410.13959)。来源层级：**正文**。它已经给出 FinQA 的问题、上下文、计算等错误分析及近似比例，并讨论百分比/数值口径和执行答案与给定答案差异。唯一短引为 “disparities between the execution answer and the provided answer”。这也是候选 5 的直接相关先例；未见两字段总不一致率或据此过滤的数据流程。
- **Do Large Language Model Benchmarks Test Reliability?（Vendrow 等，2025；Platinum）**：[§2.1–2.2、Appendix B](https://arxiv.org/html/2502.03461)。来源层级：**正文**。15 个基准不含 FinQA。其清洗方法让多个模型作答并人工检查至少一模型出错的题，以区分错标签和不良题目。方法上高度接近；它也强调修复后仍存在模型失败，因此“多模型共同错”本身不能证明标签错。
- **Confidently Wrong（Wang，2026，v2 2026-10-13）**：[§3、§5.2、§6](https://arxiv.org/html/2607.11414)。来源层级：**正文**。使用 FLARE 分发的 FinQA **训练集**和 TAT-QA；校验判分器时报告约 4%–6% 残余标签噪声及口径歧义，研究八次采样同答仍被判错。不是原始 test 跨模型共同错审计，也没有证明大部分剩余错误来自基准。
- **Collaborative LLM Numerical Reasoning with Local Data Protection（Zhang 等，预印本 2025 / AAAI 2026）**：[Error Analysis / Table 4](https://arxiv.org/html/2504.00299v2)。来源层级：**正文**。搜索摘要容易令人误以为其 23.3% 标注错误/歧义率属于 FinQA；正文明确为 **MultiHiertt、Phi3、30 个错例**，故不拿它作为 FinQA 的直接证据。

## 任务给定的相似观点逐项核实

| 给定说法 | 核查结果（均依据正文，例外明确列出） |
|---|---|
| FinanceReasoning 修订四数据集 15.6%，9.72%–30% | 成立；准确范围、分母及非原始 FinQA test 见 4A。它明确谈标注质量与饱和，但不能扩大为“原始完整 FinQA 剩余错误主要归于基准”。 |
| Northcutt 等 2021 十个测试集标签错误 | 成立。[§3 Table 1、§4–5、Appendix A](https://arxiv.org/html/2103.14749) 覆盖图像、文本、音频十数据集，平均至少3.3%；没有 FinQA。是一般方法和动机先例。 |
| MMLU-Redux 与 Platinum 清洗工作 | 成立。[Gema 等 NAACL 2025 正式记录](https://aclanthology.org/2025.naacl-long.262/)；[§2–3、Appendix F 正文](https://arxiv.org/html/2406.04127) 重标5,700题，区分歧义、无正确选项、多正确答案、错误真值等。Platinum 的范围与方法见上。二者均非 FinQA 审计。 |
| DocMath-Eval 对 FinQA 派生题筛选/重标 | 成立。[§3.2–3.3、附录](https://arxiv.org/html/2311.09805) 明确重标 FinQA、TAT-QA 等，删除错误或非数值题、增加尺度说明、改正题目、重写Python解及核验证据。未见按原始 FinQA 分母报告错误率。 |
| BizBench 对 FinQA 派生题筛选/重标 | 部分成立；代码改写及执行结果验证成立，见上文BizBench段。论文并未完整人工重审所有数据（Limitations）。 |
| FinanceMath 也对 FinQA 派生题清洗 | **不成立/原文未支持。** [§2.2–2.4](https://arxiv.org/html/2311.09797) 是专家依金融概念写新题或改教材/网络题，1,200题中674改编；没有将 FinQA 派生清洗作为构建步骤。 |
| FinQA 专家约91%，暗示上限 | 数字为91.16%，成立；“因此存在约9%的标签噪声上限”不成立。[FinQA §4.3、Table 2](https://aclanthology.org/2021.emnlp-main.300.pdf) 是两名外部专家在随机200题的执行准确率均值，不能区分专家失误、标注错误和歧义。 |

## 高度相关但尚未取回正文的线索

**李希等（2025），《基于正负例思维链的表格-文本混合金融数据自动问答方法》，《中文信息学报》39(7)。** [期刊页面](http://jcip.cipsc.org.cn/article/id/zwxxxb_3951)，[期刊PDF](https://jcip.cipsc.org.cn/cn/article/pdf/preview/zwxxxb_3951.pdf)。**本轮仅取得摘要索引及二手介绍**：[SinoMed](https://www.sinomed.ac.cn/article.do?ui=2025477889)、[二手线索](https://research.elamur.ai/free/en/papers/li-2025-positive-negative-chain/)。二手称作者构建 FinQA-fix，修订近20%答案并列七类错误，包括符号；这些数字尚未原文核实，不进入确定性判断。期刊 web 请求超时，shell HTTPS 连接重置、HTTP 返回网络错误 HTML。仍应优先人工取回全文，尤其核对修订分母、测试集范围和符号类别。即使此线索最终不成立，上述已读正文也足以判候选4为⚪。

## 对本项目的含义（本轮判断，不是文献事实）

保留该结果作为动机与数据审计附件，主张应收窄为“在指定模型、提示和样本上，残余判错高度集中，并经审查归于若干参考或口径问题”。不能仅凭同错就推出模型没有共同弱点；现有392题分层样本、同提供商模型和AI裁判不足以外推完整测试集。是否还能独立支撑短文，要看全测试集、异厂商与人工复核后的新增发现；目前不宜单靠候选4担任新颖性中心。
