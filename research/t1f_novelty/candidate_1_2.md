# T1f 候选 1–2 查新结论

检索截止：2026-11-17。以下按任务文件原定边界判定；“读了正文仍未见”只描述本次证据，不等于证明全球无人做过。项目中的 10.7%、5,337、1/196 等数字来自本地任务及初稿，本轮没有重跑核验。

| 编号 | 结论 | 建议颜色 | 最接近的工作（题目、年份、链接） | 他们做了什么 | 我们多出来的是什么 | 把握 |
|---|---|---|---|---|---|---|
| 1 | 读了正文仍未见 | 可条件升 🟢，由导师另判证据完整性 | [Gittings, Rounding errors and index numbers, 1991](https://www.chicagofed.org/-/media/publications/economic-perspectives/1991/ep-may-jun1991-part1-gittings-pdf.pdf)；[XBRL Calculations 1.1, 2023/2024](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22+corrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22+corrected-errata-2024-02-14.html)；[VeriFin, 2026 v3](https://arxiv.org/html/2608.10213v3) | 分别是指数增长率的舍入扭曲、财报区间验证、固定输入值后按披露精度设置答案容差；均已读正文 | 在金融 QA 上从**输入显示精度**计算答案可辨识性，统计规模，并检验具体增长率阈值。方法基础和“舍入会影响答案”不是新意 | **中**。未见满足候选1完整边界的正文；Google Scholar / S2 原生检索未成功，未穷尽被引图 |
| 2 | 已有人做过同样的事 | ⚪ | [XBRL Calculations 1.1 §5.5, 2023/2024](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22+corrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22+corrected-errata-2024-02-14.html)；[Dandekar, 2010](http://www.asasrms.org/Proceedings/y2010/Files/306584_56766.pdf)；[Salazar-González, 2005](https://www.cs.utep.edu/vladik/cs5354.10/819.pdf) | XBRL 已用重复披露交集收紧舍入范围并给出收紧效果的数字例子；后两篇已用加总约束和 LP/ILP 研究舍入表格的可恢复性 | 196 道 FinQA 中仅恢复 1 道是特定语料的负面结果，可支撑候选1；不能把它包装为首次发现约束恢复或首次做区间收紧 | **高**（宽边界已有先例）；**中**（FinQA 特定负面计数是否已有）。不能把原边界事后缩成“在 FinQA 上报告总体恢复率” |

候选 2 降为 ⚪ 并不要求先例也得到“几乎救不回来”的结论。任务明定只要重复披露或会计关系收紧舍入范围并报告效果即可；XBRL 的数字例子已经满足这一边界。LP 的精确实现、更大的约束集和本项目的恢复率仍可有工程与实证价值，但单凭这些不足以声称独立的新方法贡献。

## 最接近工作及原文证据

以下短引为核对定位所需，单一来源总英文引文不超过 25 词。XBRL 是两个候选共用的近邻，只在下方摘录一次。

### 候选 1：三项近邻

**1A. Thomas A. Gittings, 1991, Rounding errors and index numbers。来源层级：正文。** Chicago Fed *Economic Perspectives* May/June，印刷页 2–10，已读全文。

> “Rounding of historical index numbers can distort the pattern of monthly growth rates” （p.2）

研究对象是重定基后的 CPI-W 等指数：较早期数值小、末位单位相对粗，月度增长率会受舍入显著扭曲；正文含实际指数与模拟时间序列例子。它证实了增长率舍入风险早已研究，未给出 FinQA 一类基准的输入精度审计，也未见“相差约 100 个末位单位”在公司报告数据上验证。不可说本文首次发现增长率受舍入影响。[正文](https://www.chicagofed.org/-/media/publications/economic-perspectives/1991/ep-may-jun1991-part1-gittings-pdf.pdf)

**1B/2A. XBRL International, Calculations 1.1，Recommendation 2023-02-22，修正版本 2024-02-14。来源层级：规范正文。** 已读 §§3–5.7。

> “the calculation is performed using the intersection of fact value intervals for all facts within the set.” （§5.5）

§5.2.3 给出显示值两侧各半个末位单位的闭区间；§5.7 给出区间加法和与权重相乘；§5.2 用加总区间与总计区间是否相交检验一致性。§5.5 的两次披露是 5000（decimals=-3）、5500（decimals=-2），各自区间 [4500,5500]、[5450,5550]，交集 [5450,5500]，展示了定量收紧效果。没有金融 QA 整体不可辨识率或增长率阈值实验，但**已满足候选 2 的宽边界**。[规范](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22+corrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22+corrected-errata-2024-02-14.html)

**1C. Bethel Hall, Sachi Shome, William Eiers, 2026, VeriFin: A Neurosymbolic Framework for Verifying LLM-Generated Financial Claims。来源层级：预印本正文，v3（2026-10-23）。** 已读 §§1–6，尤其 §§3.5–3.6、4.1–4.3。

> “The tolerance τ is half a unit in the last place reported by the filing” （§3.6）

其公式将每个输入绑定为已披露的点值，计算预期结果，再与候选答案比较，使用末位半单位容差。评估含 XBRLFiling 600 题、FinanceBench 67 题、TAT-DQA 403 题；结果量度是声明验证的正确性和覆盖率。该设计未将每个输入作为未知舍入前变量，也未传播输入区间来统计目标不可辨识性。它非常接近“披露精度决定验证容差”的应用，必须讨论，不能泛称金融 QA 尚无人处理报告精度。[正文](https://arxiv.org/html/2608.10213v3)

### 候选 2：另两项近邻（第一项为上面的 2A）

**2B. Ramesh A. Dandekar, 2010, (In)Effectiveness of Independent Rounding of Discrete Tabular Data as Statistical Disclosure Control Strategy。来源层级：会议论文正文。** ASA JSM Survey Research Methods，pp.1158–1164；已读正文及附后演示页。

> “The LP setup uses publicly available rounding rules in combination with additive properties associated with the table structure.” （p.1161）

正文用 5×4 假设计数表和公开 CTPP 舍入规则构造上下界与行列加总约束（pp.1159–1162）；p.1163 通过逐个变量最小化和最大化，求舍入前数值的可能范围，并以界相等判断精确恢复。Table 6 展示 LP 重构例。此为统计披露保护，不是公司财报或 FinQA，不能把示例说成真实公司总体恢复率；但它直接覆盖“舍入界 + 线性冗余 + LP 恢复”的方法骨架。[会议原文](http://www.asasrms.org/Proceedings/y2010/Files/306584_56766.pdf)

**2C. Juan-José Salazar-González, 2005, A Unified Mathematical Programming Framework for Different Statistical Disclosure Limitation Methods。来源层级：期刊论文正文（大学网站托管的排版版）。** *Operations Research* 53(5):819–829，DOI 10.1287/opre.1040.0202；已读 §§1–2、5–6。

> “Otherwise, yi is a continuous variable and the models are linear programs (LP).” （p.821, §2；变量排版转为纯文本）

§2 用线性加总关系及单元格上下界求被隐藏数值的最小/最大可能值，区分连续 LP 与整数 ILP；§5 专论 controlled rounding，允许由发布值及舍入规则形成界。Fig.1 是按地区/活动分类的企业投资表，不等于上市公司问答审计。它说明把约束和极值规划用于信息恢复已有成熟框架。[正文](https://www.cs.utep.edu/vladik/cs5354.10/819.pdf)

## “已知的相似观点”逐项核实

| 原说法 | 核实结果与限定 | 来源层级及位置 |
|---|---|---|
| 相近数相减损失有效数字是教材知识 | 原理正确，但要区分输入原有误差被放大与浮点减法本身舍入。Higham 解释满足 Sterbenz 条件的浮点减法甚至可精确，仍会放大输入不确定性。不能把项目的显示精度问题写成新浮点误差定理 | **正文**：[Higham, The Mathematics of Floating-Point Arithmetic, 2021](https://nhigham.com/wp-content/uploads/2021/04/high21m.pdf)，p.37 Theorem 5 及后段。2002 二版书目及 §1.7 信息已定位，但未将未读全书当作全文核验 |
| Gittings 1991 讨论经济增长率舍入 | 年份、机构正确；准确题名是 *Rounding errors and index numbers*。主要是指数重定基后月度增长率失真及时间序列影响，不是 FinQA/公司财报特定统计 | **正文**，1A |
| XBRL Calculations 1.1 处理舍入区间与运算 | 正确，而且明确区分最近舍入/截断、闭区间边界、重复事实交集和加总一致性。规范并未宣称任意非线性比率的全局精确范围 | **规范正文**，1B/2A，§§5.2–5.7 |
| EnvCommons/FinQA 有 1% 与显示位数的评分争论 | 根代理已读 PR #2/#3 原文；对应最终答案 grader 及容差，不是从所有输入显示精度传播区间。此分工检索得到的 issues 搜索空结果不能否定已直接找到的 PR | **一手 PR 正文（根代理核验）**：[PR #3](https://github.com/EnvCommons/FinQA/pull/3)。合并记录与具体比较由总报告提供 |
| FinanceReasoning 2025 说模型数值精度有困难 | 正确，但 §4.2、Appendix B Table 9 是计算步骤过度舍入。例子为 Black–Scholes put 定价 gold 5.46、模型 5.44；并非披露输入本身不足以确定答案。§2.1 采用 0.2% 评分容差、规范单位/符号/小数位，不是输入可辨识性审计 | **正文及附录**：[FinanceReasoning](https://arxiv.org/html/2506.05828v1)，§§2.1、4.2、Appendix B Table 9 |
| XBRL 重复事实交集、计算一致性 | 已核实；§5.5 的数值例子直接显示收紧，因此是候选 2 的正面先例，不能只写成“相关但没做过” | **规范正文**，2A |
| 会计关系还原舍入前数值，导师未了解 | 已找到规范内的财务重复披露例子；又向统计披露领域追到完整 LP/ILP 恢复先例。会计论文的中文检索发现“报表数据自动调整”线索，但未获取完整正文，不能把调整报表凑平当作推断真实数值 | **正文** 2A–2C；中文线索为**摘要/转载摘录**，见阅读清单 |

## 额外近邻及写作限制

[Yan, Miao & Huang 2026, Training Autoregressive Language Models on Rounded, Bounded, and Censored Numerical Labels via Exact Likelihood](https://arxiv.org/html/2611.02461) 的正文 §3.2、Table 1 已将舍入标签作为相容区间，并对整个集合训练精确似然。实验为合成数据、hERG 和代码时延，未见 FinQA/TAT-QA 或由财报操作数传播得到 gold 集合。**“舍入标签应当是一个集合”不能作为本项目独有概念**；候选1剩余空间是输入级可辨识性审计与具体实证结论。来源层级：正文（包括 Appendix D/E）。

[XFinBench](https://aclanthology.org/anthology-files/pdf/findings/2025.findings-acl.457.pdf)（2025）§4.4/F.1 分析模型中间步骤舍入；[Retrieval-Augmented Chain-of-Thought in Semi-structured Domains](https://aclanthology.org/anthology-files/pdf/nllp/2023.nllp-1.18.pdf)（2023）§5.1 讨论评分如何忽略精度和舍入差别。已读相关正文和附录段落；均不能用来证明或否定输入可辨识性主张。精度、舍入、rounding 关键词命中不等于同一个研究对象。

更早的 [XBRL Precision, Decimals and Units RFC, 2008](https://www.xbrl.org/rfc/pdu/pwd-2008-10-09/pdu-rfc-pwd-2008-10-09.html) §§6–9 已讨论区间一致性，并在 §9 提及为保持加总平衡而调整显示数字的实务。故半末位区间应明示为舍入模型假设；不能未经核验把所有财报数字都断言为独立最近舍入。来源层级：规范讨论稿正文。

本轮没有证明“全球没有候选1”。Scholar/S2 原生页面访问失败、搜索引擎的站内限定命中并不等于这两个库的原生查询；没有完整导出 FinQA/TAT-QA/ConvFinQA 被引集合。检索过程、未成功访问及正文阅读范围另附，足以支持有边界的查新意见，不足以支持无条件的首创声明。

