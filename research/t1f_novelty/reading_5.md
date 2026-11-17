# 候选5与根代理交叉核读清单

日期：2026-11-17。每行区分正文读取、元数据与未获取；同一作品不同链接不算独立研究。

| 题目／来源 | 年 | 链接 | 已读范围 | 关联 | 层级与用途 |
|---|---|---|---|---|---|
| Serve only FinQA tasks whose reference agrees with the written answer | 2026 | [PR4](https://github.com/EnvCommons/FinQA/pull/4) | Problem、Fix、Decisions、Tests、全部3文件补丁、合并代码has_consistent_reference及load_finqa_data | 5、4 | 正文／代码；直接先例 |
| Grade FinQA answers at their stated precision and accept percent forms | 2026 | [PR2](https://github.com/EnvCommons/FinQA/pull/2) | 全部PR正文 | 1、5 | 正文；输出评分规则 |
| Grade FinQA answers by a fixed 1% relative tolerance and state the required precision | 2026 | [PR3](https://github.com/EnvCommons/FinQA/pull/3) | Problem、Fix、规则比较表、Tests | 1、3、5 | 正文；非输入区间 |
| Credit FinQA amounts written with a scale word in the document's units | 2026 | [PR5](https://github.com/EnvCommons/FinQA/pull/5) | Problem、Fix、Numbers、Tests、Decisions | 5 | 正文；单位解析 |
| Description for the attributes in the data file | 2022 | [issue6](https://github.com/czyssrs/FinQA/issues/6) | 全文；评论API返回空 | 5 | 正文；380/3.8个案 |
| Possible incorrect gold answer/program for ANSS/2008/page_89.pdf-1 | 2026 | [issue15](https://github.com/czyssrs/FinQA/issues/15) | 全文 | 4、5 | 正文；平均数分母个案 |
| FinQA官方evaluate.py | 2021项目／当前文件 | [实现](https://github.com/czyssrs/FinQA/blob/main/code/evaluate/evaluate.py) | str_to_num、eval_program、equal_program、evaluate_result | 1、5 | 代码；官方评分规则 |
| GeneralReasoning/FinQA | 2026 | [环境](https://openreward.ai/GeneralReasoning/FinQA) | Tasks、Reward Structure、Data、Repository | 5 | 正文；PR4现已部署的文档旁证，非独立研究 |
| FinQAPT: Empowering Financial Decisions with End-to-End LLM-driven Question Answering Pipeline | 2024 | [正文](https://arxiv.org/html/2410.13959) | §§4.1–4.5，重点§4.5.1 | 4、5 | 正文；字段冲突已有论文描述 |
| Gauging Overprecision in LLMs: An Empirical Study | 2025 | [正文](https://arxiv.org/html/2504.12098) | §§3.1、3.3、4、5表4（根代理复核） | 3 | 正文；3,262来自各split，点真值覆盖 |
| Optimizing Human–AI Collaboration in Chemistry: A Case Study on Enhancing Generative AI Responses through Prompt Engineering | 2024 | [正文](https://www.mdpi.com/2624-8549/6/4/43) | §3.2（根代理复核）、出版元数据 | 3 | 正文；提示有效数字小案例 |
| Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents | 2026 | [记录](https://arxiv.org/abs/2609.00065) | 标题、作者、日期、版本 | 方法归属 | 摘要／元数据；不充当查新证据 |


## 引用链补读

| 题目 | 年 | 链接 | 实际阅读位置 | 层级与判断 |
|---|---|---|---|---|
| Evaluating LLMs’ Mathematical Reasoning in Financial Document Question Answering（Srivastava等） | 2024 | [ACL](https://aclanthology.org/2024.findings-acl.231.pdf) | §§2、4/Table3，附录A.3相关分析、A.4元数据覆盖与引用关系 | 正文；覆盖FinQA完整test、ConvFinQA dev、TAT-QA部分dev；精度错误指数值计算偏差，与输入可辨识性不同 |
| Are ChatGPT and GPT-4 General-Purpose Solvers for Financial Text Analytics? A Study on Several Typical Tasks（Li等） | 2023 | [ACL](https://aclanthology.org/2023.emnlp-industry.39.pdf) | §3.5/Table8、Appendix B中ConvFinQA与FinQA、参考文献 | 正文；后续评测及模型算术/指代错误，不报告输入区间或原始字段不一致率 |
