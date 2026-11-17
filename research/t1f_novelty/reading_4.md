# 候选4正文阅读清单

日期：2026-11-17。此表的「已读」指工具实际返回并审阅的指定节段，不冒称逐字通读所有页。重复的arXiv和正式论文属于同一项研究，不重复计数。

| ID | 题目、年份、正式/全文链接 | 实际阅读位置 | 来源层级 | 相关候选与用途 |
|---|---|---|---|---|
| B01 | [FinanceReasoning: Benchmarking Financial Numerical Reasoning More Credible, Comprehensive and Challenging](https://aclanthology.org/2025.acl-long.766/), 2025；[HTML](https://arxiv.org/html/2506.05828v1) | §1、§2.1、Tables1–4、§4.2、Appendix B Table9、Appendix C.1 Tables10–14；浏览构建、实验与附录目录；另下载正式ACL PDF核对印刷pp.15722、15734、15739 | 正文 | 4：来源数据、修订类型/比例、饱和论述；1/3：precision为中间计算舍入；正式版仍有1420与1330不一致 |
| B02 | [Retrieval-Augmented Chain-of-Thought in Semi-structured Domains](https://aclanthology.org/2023.nllp-1.18/), 2023；[HTML](https://arxiv.org/html/2310.14435) | 引言、§3.2、§5目录及设置、Appendix A.1、D.2 Table7、E提示说明；另下载正式PDF核对第9页/印刷p.186 | 正文 | 4：FinQA40验证样本的10错例分类 |
| B03 | [BizBench: A Quantitative Reasoning Benchmark for Business and Finance](https://aclanthology.org/2024.acl-long.452/), 2023预印本/ACL2024正式；[HTML](https://arxiv.org/html/2311.06602) | §1、§4.1、Limitations、Appendix A.2/A.3、B Table5及Fig9–10、D任务例；正式ACL元数据、PDF印刷p.8315互补段 | 正文 | 4：CodeFinQA跨模型互补、错误类别；5：代码执行验证≠两字段冲突审计 |
| B04 | [FinQAPT: Empowering Financial Decisions with End-to-End LLM-driven Question Answering Pipeline](https://arxiv.org/html/2410.13959), ICAIF2024 | §1、§4.4.1 Table3、§4.4.2、§4.5.1–4.5.2、结论 | 正文 | 4：错误分析；5：已明示执行答案/给定答案差异 |
| B05 | [DocMath-Eval: Evaluating Math Reasoning Capabilities of LLMs in Understanding Long and Specialized Documents](https://arxiv.org/html/2311.09805), ACL2024 | §1、§3.2–3.3（含两个re-annotation小节）、Appendix评测表与Limits片段 | 正文 | 4/5：确有FinQA重标，但无原始全量两字段冲突率 |
| B06 | [FinanceMath: Knowledge-Intensive Math Reasoning in Finance Domains](https://arxiv.org/html/2311.09797), ACL2024 | 引言/任务概览、§2.2–2.4，相关附录目录 | 正文 | 4：核实其为新写/改编题，纠正“清洗FinQA派生题”的归因 |
| B07 | [Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks](https://arxiv.org/html/2103.14749), NeurIPS Datasets and Benchmarks2021 | §1、§3 Table1、§4–5相关论述、Appendix A数据集清单 | 正文 | 4：一般标签错误先例，无FinQA |
| B08 | [Are We Done with MMLU?](https://aclanthology.org/2025.naacl-long.262/), NAACL2025；[HTML](https://arxiv.org/html/2406.04127) | §1、§2.1–2.2、§3.1–3.3关键结果、Limitations、Appendix F Table5 | 正文 | 4：错误协议及重标，非FinQA |
| B09 | [Do Large Language Model Benchmarks Test Reliability?](https://arxiv.org/html/2502.03461), 2025（2024 workshop早期题名不同） | §1、§2.1–2.2、Table2、Appendix B内容结构 | 正文 | 4：多模型分歧辅助人工清洗；15基准不含FinQA |
| B10 | [FinQA: A Dataset of Numerical Reasoning over Financial Data](https://aclanthology.org/2021.emnlp-main.300.pdf), EMNLP2021 | PDF pp1–4，§3、§4.3；p7 Table2及评测论述 | 正文 | 4：两专家200题、91.16%均值，不可直接转为基准上限 |
| B11 | [Confidently Wrong: Detecting Hallucinations in Financial Question Answering from LLM Internal States](https://arxiv.org/html/2607.11414), 2026 | §1、§3全部（data/labels/grading）、§5.2及§6相关讨论 | 正文 | 4/5：训练集的判分歧义与噪声；不是完整test审计 |
| B12 | [Collaborative LLM Numerical Reasoning with Local Data Protection](https://arxiv.org/html/2504.00299v2), 2025预印本/AAAI2026 | 引言、Results的Ablation、Error Analysis Table4；附录结构 | 正文 | 4：23.3%是MultiHiertt，不是FinQA，排除错用数字 |
| B13 | [FINESSE-Bench: A Hierarchical Benchmark Suite for Financial Domain Knowledge and Technical Analysis in Large Language Models](https://arxiv.org/html/2605.15482v2), 2026-05-21 v2 | §1–3、§4.10、§5、§6主要结果表、§7.1–7.5、§8–9；PDF p.16 Table8；作者FinQA question.jsonl与官方test.json逐题匹配 | 正文及公开数据 | 4：53模型/完整1147题共同失败9.33%，直接跨模型逐题先例；不代表标签错误率 |

## 未取回全文与非论文材料

| 材料 | 层级 | 本轮处理 |
|---|---|---|
| 李希等《基于正负例思维链的表格-文本混合金融数据自动问答方法》，2025，[期刊页面](http://jcip.cipsc.org.cn/article/id/zwxxxb_3951) | 摘要索引/二手 | 标为高优先未取回，FinQA-fix近20%和七类不计入已核实事实 |
| [FinQA issue #15](https://github.com/czyssrs/FinQA/issues/15) | 原始公开讨论正文 | 一道平均值分母4/5的争议个案，无系统比例；读取GitHub connector结果 |
| FinQA-error-diagnosis等个人公开仓库搜索结果 | 搜索片段 | 未深读，不纳入三项最接近证据或确定性判定 |

## 本轮筛选规则

直接匹配：FinQA判错归因/比例、原始或派生FinQA逐题跨模型错题对比、金融数值基准标注修订与分数影响。一般背景：其他基准标签审计。排除：纯模型能力排行榜、无原文二手总结、将MultiHiertt比例误当FinQA、把代码改写验证误当字段冲突统计。未能访问的正文保留为缺口，不能拿来作确定性反证。
