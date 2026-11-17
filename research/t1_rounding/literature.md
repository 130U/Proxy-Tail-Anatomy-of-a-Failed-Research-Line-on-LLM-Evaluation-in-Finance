# T1 查重：输入舍入精度与金融问答答案确定性

检索日期：2026-11-16（America/New_York；部分访问的 UTC 日期为 11-17）。这是并行完成的集中初筛，不声称已进行了半天壁钟时间的穷尽检索。未调用模型评分、未训练模型、未调用付费 API。

## 判定

**本轮未发现“同样问题和同样测量”的直接重复，尚未触发任务的撞题停止条件。** 这里的“直接重复”指：在 FinQA、TAT-QA 或同类现成金融 QA 基准中，由文档输入数字的报告精度构造可行区间，沿 gold program 传播，统计可能答案跨出评分接受域的题目比例。检索未找到同时覆盖这些环节的工作；这不是“此前无人做过”的证明。

**可以继续一个有明确门槛的基准审计，不能把区间算术本身、财务舍入的不确定性、不同精度重复事实处理，包装成新的数学理论。** 这些组成部分已有明确先例。若最终只有把既有方法搬到一个数据集，研究贡献可能不足；剩余价值在于可复核的发生比例、非线性运算的集中风险，以及量化精度改变的可检验预测。

## 最接近的工作

| 一手来源 | 已经做了什么 | 与 T1 的边界 |
|---|---|---|
| [XBRL Calculations 1.1，2023 推荐标准、2024 勘误](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22%2Bcorrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22%2Bcorrected-errata-2024-02-14.html)，§5.2–5.7 | 报告值及 decimals 定义半末位舍入区间；区间加总后与已报告总数的区间比较；一致重复事实取区间交集。 | 舍入区间、区间加总和重复精度处理均有明确规范先例。该规范主要处理财务合计一致性，未测量 QA gold program 的答案跨评分边界比例，也未给增长率审计结果。 |
| [VeriFin，arXiv:2608.10213](https://arxiv.org/html/2608.10213)，§3.6 | 用 XBRL 事实和授权公式验证候选答案；操作数约束为 `x_i=m_i*`，输出差值容差取报告精度的半个末位单位。 | **输出容差不是输入区间传播**。其公式把操作数固定，再检查候选值；未测量 FinQA/TAT-QA 的潜在原值区间。不是直接重复，但半末位容差早已用于金融 QA 验证。 |
| [FinVerBench，arXiv:2605.29586](https://arxiv.org/html/2605.29586)，§3.4、5.4、6.1、6.5 | 对财报注入数值错误；指出接近报告舍入单位的误差会形成不可判别区域；比较未舍入与按原精度舍入后的 LLM 检出表现。 | 已有“显示舍入影响金融验证”和欠确定性讨论；测量对象是注入误差检出、格式线索消融，不是 QA 输入区间经 gold program 的像集。未发现同一测量。 |
| [Characterizing Ambiguity in Financial Document Question Answering，FinNLP 2026](https://aclanthology.org/2026.finnlp-1.37.pdf)，§3–5、附录 A | 人工标注 200 个 MultiHiertt 问题，区分问题/文档来源及歧义程度；另分析数值判分容差的影响。 | 文档歧义、单一答案局限和容差敏感性均非新问题。其类别及示例主要涉及语义、范围与数据缺失，未给输入舍入区间传播或条件数审计。 |
| [FinInteract，arXiv:2609.24002](https://arxiv.org/html/2609.24002)，§2–3 | 以实体、指标、时期、申报版本、政策口径的歧义构造默认/意图两种答案，测量澄清行为。 | 语义口径对应多个答案，与固定语义下的输入量化不确定性不同。 |
| [Gauging Overprecision in LLMs，arXiv:2504.12098v2](https://arxiv.org/html/2504.12098v2)，§3–4 | 让 LLM 在指定置信水平下直接生成答案区间，并在 FinQA 等任务上评价区间校准与聚合。 | 区间来自模型表达的置信，不是财报舍入所确定的可行输入集合；不能据“FinQA + interval”判为同题。 |
| [XFinBench，arXiv:2508.15861](https://arxiv.org/html/2508.15861)，§4.4、标注附录 | 检查金融计算回答中的中间步骤舍入错误与公式误用。 | 模型在计算中损失精度，与源文档已经舍入而丢失信息不同。 |

2021 年的 [XBRL Calculations 1.1 需求文档](https://www.xbrl.org/REQ/calculation-requirements-1.1/REQ-2021-11-08/calculation-requirements-1.1-2021-11-08.html) 已明确说明：同一事实可在表格中按千报告、在文字中按百万概括，并要求采用区间算术。这进一步排除了“首次注意到文本/表格精度不同”这样的贡献表述。

## 官方判分规则核验

FinQA 原论文的目标是根据财报回答数值推理问题，并发布专家写的 gold reasoning programs。[原论文及项目入口](https://aclanthology.org/2021.emnlp-main.300/)

本次核验的 FinQA 仓库 `main` 指向 `0f16e2867befa6840783e58be38c9efb9229d742`。官方 `eval_program` 在运算结束后把数值结果 `round(..., 5)`；`evaluate_result` 将该结果与 `qa.exe_ans` 直接比较，另有程序符号等价判分。**官方程序执行正确率不是“1% 相对容差”，也不是“按 qa.answer 字符串显示位数取整”。** 因此 T1 的两套规则应称“预设审计容差”，与官方执行规则分列。[固定版本 evaluator](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py)

TAT-QA 官方 `get_answer_str` 对一般数值先 `round(ans_num, 2)`、乘 scale，再格式化四位；含 `%` 字符串走另一条归一化分支。算术题的 F1 等于 EM。它也不是简单的按原始 gold 字符串末位舍入。因此，若扩展到 TAT-QA，必须保持百分数、scale 和官方归一化的区别。[官方 scorer](https://github.com/NExTplusplus/TAT-QA/blob/master/tatqa_metric.py)；[原论文](https://aclanthology.org/2021.acl-long.254/)

1% 并非凭空提出：例如 OpenEnv 的 FinQA 环境文档声明使用 1% 相对或 0.01 绝对容差。但这是基于 Snorkel AI FinQABenchmark 的 290 题环境，**不能借它证明原始 FinQA 的官方判分就是 1%**。[OpenEnv 官方环境文档](https://huggingface.co/docs/openenv/v0.4.2/environments/finqa)

## 对本次测量的限制

以下是据上述来源作出的研究设计判断，不是这些论文已经报告的 T1 结果。

1. **研究对象必须说准。** 以文档显示数字为算术输入，基准答案可能完全确定；把显示数字理解为潜在未舍入事实的约束后，真实量的函数值才可能跨出容差。后者不自动证明基准标错或模型不可能完成原任务。
2. **“外包区间越界”只是候选。** 普通区间算术可能因同一操作数重复使用而过宽。若要宣称确有多个合法潜在答案，应给出可行输入见证，或使用精确值域/有证书的界；不能仅以松的外包界越界计入已证实比例。
3. **精度应追溯到出现位置和量的身份。** 金额、比例、单位换算常量、年份、计数不能一律附加半单位误差；同数值不等于同一财务事实。只有同实体、同口径、同时期、同单位的重复才适合合并约束。
4. **充分使用文档证据。** 同一事实多处出现时，分别代入不同显示值可测“计算出处敏感性”；但宣称整个文档仍不确定时，应合并这些证据。已知财务恒等式也可能缩小可行集合。单独输入盒上的比例必须标明所用信息集。
5. **单位与信息精度不同。** 仅把 12 百万写成 12,000 千，原信息没有增加。只有实际提供千位精度的额外有效数字，才对应缩窄区间的反事实；若没有更精细真实数据，不能说已实证验证报告单位改写的效果。

## 检索记录

本子任务共提交 31 个检索式，另读取官方源码与相关全文。搜索使用可访问网页索引，优先核对 ACL Anthology、arXiv、作者论文与 XBRL 原规范；搜索摘要、聚合站与商业榜单只作线索，不作为关键结论依据。以下按批次记录原始查询；每批返回的是合并结果，未伪造单条检索命中数。

| 批次 | 原始查询 | 主要处理 |
|---|---|---|
| 1 | `FinQA "interval arithmetic"`；`"financial question answering" "rounding" uncertainty`；`"TAT-QA" "precision" rounding`；`"FinQA" "condition number"` | 发现官方 TAT-QA scorer、容差讨论及 VeriFin 线索。 |
| 2 | `"FinQA" "rounding" "interval"`；`"TAT-QA" "rounding" "interval"`；`"financial question answering" "condition" "rounding"`；`"VeriFin" rounding uncertainty precision` | 精读 VeriFin §3.6，区分固定输入加输出容差。 |
| 3 | `"financial" "rounding uncertainty" "question"`；`"FinQA" "uncertainty propagation"`；`"financial question answering" "interval" arithmetic rounding`；`"TAT-QA" "numerical precision"` | 未检出 T1 测量；得到其他数值推理、事实验证邻近线索。 |
| 4 | `XBRL calculations 1.1 rounded values intervals duplicate facts consistency`；`"FinQA" "rounding errors" benchmark tolerance`；`"financial" "question answering" "interval arithmetic"`；`"financial benchmarks" "rounding" uncertainty` | 找到 XBRL 区间规范和 FinVerBench，核验正式规范与论文相关段落。 |
| 5 | `"FinQA" "1%" "tolerance"`；`"FinQA" "rounding" "ill-conditioned"`；`"question answering" "rounding uncertainty"`；`"FinQA" "significant digits"` | 核验 1% 只是一种下游采用的规则；未找到源精度确定性审计。 |
| 6 | `"Gauging Overprecision in LLMs"`；`"XFINBENCH" rounding`；`"financial question answering" "conditioning"`；`"FinQA" "uncertainty" "rounded"` | 获取两篇 arXiv 正文；分别判定为预测校准、中间计算舍入。 |
| 7 | `"FinQA" ("perturbation" OR "quantization") "precision"`；`"financial question answering" ("determinacy" OR "roundoff" OR "ill-conditioned")`；`"TAT-QA" ("round-off" OR "interval propagation" OR "error propagation")`；`"FinQA" ("input uncertainty" OR "answer uncertainty" OR "measurement error")` | 扩展术语查重；未发现直接重复。 |
| 8 | `"Characterizing Ambiguity in Financial Document Question Answering"`；`"Characterizing Ambiguity" "rounding"`；`"FinInteract" "rounding"` | 精读 MultiHiertt 歧义论文及 FinInteract，排除语义歧义研究的表面重合。 |

主代理另外报告已使用 `"FinQA" "input uncertainty"`、`"FinQA" "significant digits"`、`"TAT-QA" "interval arithmetic"`、`"financial question answering" "precision" "ambiguity"` 查找，并提供 MultiHiertt 歧义论文线索；本报告已独立打开该论文核验。

访问限制：最初的 Gauging OpenReview PDF 链接返回 404，XFinBench 的 OpenReview 链接触发浏览器验证；均改用相应 arXiv 正文核验，没有把不可读链接当作已读证据。一次 FinNLP 全卷页面超时，随后直接读取文章 PDF。

## 可提交的研究定位

建议表述为：**在固定问题语义、证据集合及舍入模型下，对金融 QA 参考计算的输入量化敏感性进行可复核审计，并检验哪些运算类型和报告精度导致潜在结果跨出预设接受域。**

不应表述为“发现一种新的区间理论”“首次发现财报有舍入误差”“证明 FinQA 标准答案错误”或“已证明没有任何同题文献”。若后续检索找到相同问题和测量，应按任务规则当天停止扩展，保留证据说明。
