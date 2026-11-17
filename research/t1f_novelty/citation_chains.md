# 引用链与排除判断

检索日：2026-11-17。以下记录本轮实际追踪的相关链路，箭头表示后文引用/使用前文数据或由其参考文献追踪，**不是取得完整cited-by导出**。原生Scholar/S2访问受限的请求已记入queries文件。

| 种子／链路 | 核读的2023年后工作及位置 | 查新作用 |
|---|---|---|
| FinQA → BizBench/CodeFinQA → FinanceReasoning | BizBench §4.1、A.2；FinanceReasoning §2.1、Table1、C.1 | 派生清洗、跨模型互补、标签质量与饱和；不混淆795与1147 |
| TAT-QA → BizBench/CodeTAT-QA → FinanceReasoning | 同上；FinanceReasoning中的288题切分 | 纠错机制并非FinQA独有；未见输入舍入可行性比例 |
| FinQA/TAT-QA → DocMath-Eval | §3.2–3.3及附录 | 确认重标与去除问题题，不能捏造原始两字段冲突率 |
| FinQA/TAT-QA/ConvFinQA → Evaluating LLMs’ Mathematical Reasoning in Financial Document Question Answering（EEDP，2024） | [§§2、4、A.3–A.4](https://aclanthology.org/2024.findings-acl.231.pdf) | 完整FinQA test、ConvFinQA dev与TAT-QA部分dev的元注释、错因；C2是数值计算偏差，不是输入舍入的不确定性 |
| FinQA/ConvFinQA → Are ChatGPT and GPT-4 General-Purpose Solvers for Financial Text Analytics?（2023） | [§3.5/Table8、Appendix B](https://aclanthology.org/2023.emnlp-industry.39.pdf) | 明确模型算术、上下文指代错误；说明共同错不能自动归于标签 |
| FinQA/ConvFinQA/TAT-QA → FINESSE-Bench（2026） | [§5.3、§7.4/Table8](https://arxiv.org/html/2605.15482v2) | 原始FinQA 1147题的多模型共同错已报告；裁判式判分与本项目官方程序判分需区分 |
| FinQA → Mavi等2023；FinQAPT2024 | 前者D.2 Table7；后者§4.5.1 | FinQA错误归因及两种答案差异的直接先例 |
| FinQA → Gauging Overprecision2025 | §§3.3–5、附录提示 | 同基准的数值区间回答已有人评估，但真值为点 |
| 有效数字提示 → Chemistry2024；Number Cookbook2025 | §3.2/Fig4；NUPA Sig_fig任务附录 | “提醒后会用”及有效数字基础评测不是首次 |
| 显示精度 → Gittings1991、XBRL2023/2024 → VeriFin2026 | 增长率全文；XBRL§§5.2–5.7；VeriFin§3.6 | 区分输入误差传播、区间一致性和最终答案容差 |
| 约束恢复 → Dandekar2010 → Salazar-González2005 | pp.1161–1163；§§2、5 | 线性关系+界+逐变量极值规划已有技术先例 |
| 舍入标签 → Yan等2026 → Spithourakis/Riedel2018 | Yan§2–3；早期数值LM模型部分，详见3组阅读清单 | 集合标签/舍入区间似然已有思想，不能占为本项目总论 |

高相关但未取回：FinQA-fix中文期刊全文、Chemistry补充表原始回答；另有MeasureBench、Outsmarting ChatGPT摘要线索，见3/4附件。未取得不表示无关，报告没有用它们支撑“无人做过”的确定性结论。
