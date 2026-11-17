# T1g 查新与两处引文核实

核实日期：2026-11-17。本文只写查新结论和来源证据，不代替本轮实验。

## Charter

目标是判定是否已有与 T1g 第一、二部分相同的测量，并核实两处待确认的论文。研究范围为金融与表格问答评测；对象为财报披露精度所引起的答案分歧；具体研究单元为印出变化与重算变化、比较结论的可确定性。类型为有明确停止条件的定向文献查新。知识起点为已有任务说明和 T1f 报告；T1f 只作为检索线索，以下实质判断重新回到原始来源。

问题为：Q1 是否已有 QA 基准中的自然变化差异统计；Q2 是否已有由输入显示精度判定比较标签不确定性的统计；Q3 FINESSE 的共同判错数字是否确有原文；Q4 2611.02461 是否存在、研究边界在哪里。

## Canonical sources

第一顺位为论文作者原文、正式出版物及作者托管全文；第二顺位为 XBRL 官方规范；第三顺位为本仓库既有研究，只用于寻找来源。检索结果摘要、聚合站和博客仅用于定位，不单独支持技术结论。阅读情况与证据层级逐行写在下表。

本轮执行 36 条定向搜索查询，覆盖 FinQA/TAT-QA、printed/reported/recomputed change、rounding/precision/interval/uncertainty propagation/comparison、financial consistency checking、table fact verification，并沿近邻文献回溯。实际完成的是本次会话内的有边界查新，**没有经过半天墙钟时间，也没有完成全库被引穷尽检索**。直接读取了 2611.02461 的全文及附录 A–F；其余来源的阅读范围如下。

## Findings ledger

| 编号 | 可核实事实及本轮关系 | 证据、阅读范围、来源层级 | 回答 |
|---|---|---|---|
| F1 | FINESSE-Bench 确实报告 53 个模型在 1,147 道 FinQA 上共同失败 9.33%，共同成功 22.41%。这是论文报告值，本轮未重跑模型。 | [作者 v2 全文](https://arxiv.org/html/2605.15482v2)，§§5.1–5.3、7.4 Table 8；另读 [PDF 第 16 页](https://arxiv.org/pdf/2605.15482v2#page=16)。**正文** | Q3 |
| F2 | 2611.02461 确实存在；将舍入、区间与删失标签作为相容值集合，以事件概率训练数字 token 模型。 | [arXiv 原始记录](https://arxiv.org/abs/2611.02461)、[v1 全文](https://arxiv.org/html/2611.02461v1)，全文和附录 A–F。**正文** | Q4 |
| F3 | 财报内印出比例与表格重算比例不一致，早已有直接例子及公司文件层面的统计；不能把“财报存在可见矛盾”本身作为首次发现。 | Cao、Li、Luo、Yao，*Towards Automatic Numerical Cross-Checking: Extracting Formulas from Text*，WWW 2018，[作者托管 PDF](https://ping-luo.github.io/files/2018_Towards%20Automatic%20Numerical%20Cross-Checking%20Extracting%20Formulas%20from%20Text.pdf)，§1、Figs.1–2 及方法/实验。**正文** | Q1 |
| F4 | 已有系统跨正文和表格匹配相同 KPI，标注时考虑单位、量级和舍入。这是重复披露匹配，并非“两个水平值与另印的变化”的自然差异率或 QA 判分后果。 | Hillebrand 等，*Towards automating Numerical Consistency Checks in Financial Reports*，2022，[原文](https://arxiv.org/pdf/2211.06112)，§§I、III–IV，Fig.1。**正文** | Q1 |
| F5 | 已有德国财务文件的正文—表格 KPI 一致性分类研究；测量对象是 KPI 配对及一致性分类表现。 | Ali 等，*Automatic Consistency Checking of Table and Text in Financial Documents*，2023，[全文](https://d-nb.info/1280398930/34)，§§3–5。**正文** | Q1 |
| F6 | XBRL 已按半个末位单位构造舍入区间，使用区间相交判断加总一致性；因此“点值不相等”与“舍入模型不相容”必须区分。 | [Calculations 1.1 官方规范](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22+corrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22+corrected-errata-2024-02-14.html)，§§5.2–5.7。**正文／规范** | Q1、Q2 |
| F7 | VeriFin 把操作数绑定为披露点值，再按披露精度设置输出容差；未将所有输入作为舍入前变量求目标的可行集合。 | Hall、Shome、Eiers，*VeriFin: A Neurosymbolic Framework for Verifying LLM-Generated Financial Claims*，2026，[v3](https://arxiv.org/html/2608.10213v3)，§§3.5–3.6、4、6。**正文** | Q1、Q2 |
| F8 | TabVer 已提出数字、量词与近似的集合逻辑，并在 FEVEROUS 做数字扰动/舍入探针；运算接受点值并输出单一数值，再处理声明的语义。未见由每个输入末位单位传播出比较结论可翻转性的统计。 | Aly、Vlachos，*TabVer: Tabular Fact Verification with Natural Logic*，TACL 2024，[作者全文](https://arxiv.org/html/2411.01093)，§§3、5、Appendix D。**正文** | Q2 |
| F9 | CLEARFACTS/GRAYFACTS 已把数值精度及舍入列为标签歧义，并比较清洗前后的模型排名；例子是 197.9 与“约 198”的判断口径。不是两个派生量在同一舍入盒上的比较翻转审计。 | Seo 等，*Verifying the Verifiers: Unveiling Pitfalls and Potentials in Fact Verifiers*，COLM 2025；[已读 arXiv v2](https://arxiv.org/html/2506.13342)（2026-02-05），§§2–4、Appendix D.2 Table 17。**正文** | Q2 |
| F10 | FinVerBench 已测量将人工注入错误舍入到报表精度后的性能下降；Claude Sonnet 4 在 105 个可观察样例上召回由 100% 降至 79%。研究的是去掉注入错误的小数格式线索。 | Panda，*FinVerBench: Benchmark Validity and Calibration in Large Language Model Financial Statement Verification*，2026，[原文](https://arxiv.org/html/2605.29586)，§§3.3–3.4、5.4、6.4–6.6、Table 11。**正文** | Q1、Q2 |
| F11 | 更早的数字语言模型已将连续密度在数字的舍入区间积分；“数字表示一个区间”并非始于 2026 年论文。 | Spithourakis、Riedel，*Numeracy for Language Models: Evaluating and Improving their Ability to Predict Numbers*，ACL 2018，[正式 PDF](https://aclanthology.org/P18-1196.pdf)，p.2107 Fig.2、Eq.(9)。**正文** | Q4 |

## Scope filter

保留上述近邻，排除将“模型中间步骤过度舍入”“最后答案容差”“权重量化”“注入数值错误”视为同一测量的解释。它们可说明舍入、数值歧义或金融文件错误已有研究，不能直接替代本轮两个预注册分母上的统计。尤其 F3 已直接展示文档内算术分歧，F8–F9 已研究数值近似造成的判定歧义；不能把这些宽泛主张重新当新意。

## Object filter

保留 F1 的共同失败数据，但将其限定为作者的 GPT-5.2 裁判协议，不能称为 FinQA 官方执行准确率，也不能将共同失败率称作标签错误率。保留 F2 的集合标签观点，但不把标签事件似然训练等同于本项目的输入区间传播。F3 的 1,000 份招股书结果不是金融 QA 样本的舍入影响比例。F10 是受控人工扰动，不是对未经改动的财报自然舍入残差的统计。

## Conclusions

**本轮查新结论（一段话）：**在上述 36 条查询与近邻原文范围内，尚未找到在金融／表格 QA 基准上统计“表里另印的变化与显示水平值重算结果不一致，并关联到该题判分”的同样测量；也未找到按输入显示精度构造共同可行输入、统计派生量比较标签是否可翻转的同样测量。因此第一、二部分均不触发任务的停止条件。这个结论只支持继续实测，不构成全球首创证明。已有文献覆盖文档内算术差异（F3）、财报一致性与舍入区间（F4–F7）、近似数值的集合语义及歧义对排名的影响（F8–F9）、舍入渲染对检测的后果（F10），以及集合标签学习（F2、F11）；剩余候选必须收窄到**原始 QA 数据中的输入精度可确定性及具体后果**。

### FINESSE-Bench：已核实

题名为 *FINESSE-Bench: A Hierarchical Benchmark Suite for Financial Domain Knowledge and Technical Analysis in Large Language Models*。作者为 Dmitry Stanishevskii、Nini Kamkia、Alexey Khoroshilov、Dmitry Zmitrovich、Denis Kokosinskii、Zhirayr Hayrapetyan、Andrei Kalmykov。arXiv 2605.15482，v1 2026-05-14，所核 v2 为 2026-05-21。[原始书目记录](https://arxiv.org/abs/2605.15482)

**原文定位：§7.4 “Discriminative Power and Benchmark Saturation”，PDF 第 16 页，Table 8。**正文对共同失败的短引为：

> “the share of questions that no model solves (unanimous fail)”

同页 FinQA 行依列顺序为 **53；1147；9.33；22.41；24.15**，分别是模型数、题数、共同失败百分比、共同成功百分比及 10%–90% 模型答对的中间带比例。[原文 Table 8](https://arxiv.org/pdf/2605.15482v2#page=16)

§5.3 明确使用 GPT-5.2 对问题、参考答案和模型回复作二元评分。因此“53 模型、1147 题、共同失败统计”的说法成立；“这些都是 gold 错误”或“9.33% 是官方判错率”均不由此成立。**来源层级：正文。**

### arXiv 2611.02461：存在，且概念直接相关

题名为 *Training Autoregressive Language Models on Rounded, Bounded, and Censored Numerical Labels via Exact Likelihood*。作者为 Jingquan Yan、Yuwei Miao、Junzhou Huang，University of Texas at Arlington；v1 提交日期为 2026-11-02。[原始记录](https://arxiv.org/abs/2611.02461)

§1 的原文短引明确给出舍入标签含义：

> “A measurement rounded to one decimal place and reported as 1.2 represents the interval [1.15,1.25).”

§3.2、Table 1 将观察写成相容网格集合；§3.3 的目标为该集合的负对数概率。§4 用数字前缀树的至多两条边界路径精确求事件质量与梯度；§5 还给出分位数、尾概率与 CRPS 计算。实验是合成分布恢复、自然删失 hERG 分子测量与构造超时的代码时延，使用两种 Qwen 主干；全文及附录未出现 FinQA/TAT-QA 审计。Appendix A 和 B.3 限定了有限网格、可忽略报告机制及可识别性：粗标签并不自动识别区间内部的真实分布。[全文 §§3–6、附录 A–F](https://arxiv.org/html/2611.02461v1)

**关系判断（我们的推论）：**不能再主张“舍入标签应是集合”为独有贡献；该文没有完成本任务的财报操作数区间传播、变化差异统计、比较翻转见证或 QA 评分后果测量。它也不为独立均匀舍入假设提供实证保证。**来源层级：正文；与本项目的界线为我们的分析。**

### 最需写清的近邻：Cao 等 2018

Fig.2 已将表格重算占比 **91.13%** 与正文印出 **93.88%** 并置；§1 称其系统在 1,000 份已发布中国招股书中发现 68.92% 含数值不一致，并经专业人员复查。论文核心是公式抽取和数值交叉检查，未把这一总体比例分解为舍入可相容差异，更没有 QA gold 判分分母。[作者原文 §§1、4–5](https://ping-luo.github.io/files/2018_Towards%20Automatic%20Numerical%20Cross-Checking%20Extracting%20Formulas%20from%20Text.pdf)

这一来源足以否定“此前无人比较财报文字数字与表格重算值”的宽泛说法，**但尚不满足任务文件限定的金融／表格 QA 基准上的相同测量停止标准**。是否有后果仍应由本轮预注册数字决定。

## Next steps / Risks

两部分可按原任务继续，门槛不变。检索使用网络搜索及主源全文，没有完整导出 Scholar、Semantic Scholar 或全部被引集合；未读到的后续工作仍可能构成先例。本文不声称已用满“半天”。阅读中遇到 DOI 403、机构 PDF 超时及 PDF 截图缓存缺失，已改用作者 HTML 或作者／图书馆托管 PDF；两处待核实论文的核心证据均来自实际打开的原文。
