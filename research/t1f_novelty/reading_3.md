# 候选 3 正文阅读台账

日期：2026-11-17。只把实际读到的节列入“已读”；未取到的补充材料不算已读。来源层级“正文”包含正式论文正文、附录或作者仓库正文，后两者明确注明。

| 题目 | 年份 | 链接 | 实际阅读部分 | 关联与处理 |
|---|---|---|---|---|
| Optimizing Human–AI Collaboration in Chemistry: A Case Study on Enhancing Generative AI Responses through Prompt Engineering | 2024 | https://doi.org/10.3390/chemistry6040043 | §2、§3.2、Fig.4、§4；补充S6–S8未取到 | 3，决定性宽标准先例 |
| Gauging Overprecision in LLMs: An Empirical Study | 2025 | https://arxiv.org/html/2504.12098v1 | §§2–5；附录A–D，重点§3.3真值、§4数据、Table4 | 3，FinQA数值区间输出；点真值而非舍入可行集 |
| Number Cookbook: Number Understanding of Language Models and How to Improve It | 2024初版 / 2025 ICLR | https://arxiv.org/html/2411.03766v3 | §2；附录A.1.3–A.1.4、A.2、A.3 | 3，有效数字舍入正式任务 |
| Learning to Plan by Updating Natural Language | 2024 | https://aclanthology.org/2024.findings-emnlp.589.pdf | §3方法段、§4/Table2；附录Fig.18 (p.10085) | 3，有效数字计数与提示计划效果；非区间真值 |
| Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback | 2023 | https://aclanthology.org/2023.emnlp-main.330.pdf | §§1–2，Table1，附录B温度拟合及C提示模板 | 3，正确概率口头校准背景 |
| Training Autoregressive Language Models on Rounded, Bounded, and Censored Numerical Labels via Exact Likelihood | 2026 | https://arxiv.org/html/2611.02461v1 | §§1–3、§6.1；附录结构/限制，未逐项核实验附录 | 1/3，区间数值标签与训练；非FinQA行为审计 |
| Eliciting Numerical Predictive Distributions of LLMs Without Autoregression | 2026 | https://arxiv.org/html/2603.02913v1 | §§2–3；附录A Related Works | 3，模型输出分布的数值不确定性探针 |
| BIG-bench Unit Conversion | 项目文档，2026-11-17访问 | https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/unit_conversion/README.md | 仓库README全文，重点Subtasks、Behavior、Limitations | 3，单位处理评测，非舍入区间传播 |
| CODATA DRUM-ML | 项目文档，2026-11-17访问 | https://github.com/codata/drum-ml | 仓库README，benchmark/uncertainty与scorecard上下文 | 3，实验原型设计；没有核实其示例scorecard为实测 |
| Numeracy for Language Models: Evaluating and Improving their Ability to Predict Numbers | 2018 | https://aclanthology.org/P18-1196.pdf | §3.3、Fig.2、公式(9)–(11)，§3.5–4、§5.2–6相关段 | 3，沿Yan 2026引用链核实舍入区间积分与小数位数建模；非提示行为审计 |

未取得正文（不计入以上正文阅读数量）：Outsmarting ChatGPT in Chemistry (2026), doi:10.1021/acs.jchemed.5c01611；MeasureBench (CVPR 2026)；Gauging Overprecision 的检索命中匿名 OpenReview 版本（404）。

已知观点中 FinanceReasoning 的精度例子由同组候选4正文核查，本台账不冒领该全文阅读。

