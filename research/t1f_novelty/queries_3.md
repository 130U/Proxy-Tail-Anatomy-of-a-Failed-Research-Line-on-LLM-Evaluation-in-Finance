# 候选 3 检索日志

日期：2026-11-17。以下 39 组检索全部实际执行；每批 web 搜索最多 4 组。网页搜索不等于检索数据库全部记录；本轮不报告虚假的总命中数。

| ID | 检索词（原样） | 通道 | 返回批次 |
|---|---|---|---|
| C3-01 | "large language models" "significant figures" | general | q1 |
| C3-02 | "language models" "rounding" "uncertainty" "interval" | general | q1 |
| C3-03 | "ChatGPT" "significant digits" physics | general | q1 |
| C3-04 | "LLM" "numerical precision" "prompting" | general | q1 |
| C3-05 | site:aclanthology.org "significant figures" language | ACL site search | q2 |
| C3-06 | site:arxiv.org "significant figures" ChatGPT | arXiv site search | q2 |
| C3-07 | site:semanticscholar.org "language models" "precision" uncertainty | Semantic Scholar site search | q2 |
| C3-08 | site:scholar.google.com "large language models" "significant figures" | Google Scholar site search | q2 |
| C3-09 | "large language model" "significant figures" benchmark | general | q3 |
| C3-10 | "ChatGPT" "uncertainty propagation" assessment | general | q3 |
| C3-11 | "大语言模型" "有效数字" 评测 | general Chinese | q3 |
| C3-12 | "语言模型" "舍入" "区间" 精度 | general Chinese | q3 |
| C3-13 | site:github.com "issues" "significant figures" "LLM" | GitHub site search | q4 |
| C3-14 | "ChatGPT" "significant figures" physics education | general | q4 |
| C3-15 | "large language models" "measurement uncertainty" | general | q4 |
| C3-16 | "Training Autoregressive Language Models on Rounded" | general | q4 |
| C3-17 | "ChatGPT" "significant figures" chemistry assessment prompting | general | q5 |
| C3-18 | "language models" "error propagation" "rounded" | general | q5 |
| C3-19 | "language models" "uncertainty" "rounded inputs" | general | q5 |
| C3-20 | "ChatGPT" "significant figures" "prompt" study | general | q5 |
| C3-21 | "Optimizing Human–AI Collaboration in Chemistry" Wang | general identity check | q6 |
| C3-22 | "Gauging Overprecision" 2026 | general citation followup | q6 |
| C3-23 | "large language models" "significant digits" "uncertainty" | general | q6 |
| C3-24 | "large language models" "numerical uncertainty" precision | general | q6 |
| C3-25 | "significant figures" "LLM" | GitHub issue API; topn=20 | platform0 |
| C3-26 | "FinQA" "precision" | GitHub issue API; topn=20 | platform1 |
| C3-27 | "chemistry-06-00043" "s001" | supplement discovery | q7 |
| C3-28 | "Optimizing Human" "Table S8" | supplement discovery | q7 |
| C3-29 | "LLM" "interval arithmetic" benchmark | general | q7 |
| C3-30 | "language models" "rounding error" "FinQA" | general | q7 |
| C3-31 | Number Cookbook number understanding processing NUPA 2025 | general | q8 |
| C3-32 | Just Ask for Calibration Strategies for Eliciting Calibrated Confidence Scores from Language Models | general | q8 |
| C3-33 | "FinQA" "interval" "overprecision" | general citation chain | q8 |
| C3-34 | "TAT-QA" "significant" precision language | general citation chain | q8 |
| C3-35 | LLM benchmark unit conversion measurement units UnitBench | general | q9 |
| C3-36 | "large language models" "significant figures" "uncertainty propagation" | general | q9 |
| C3-37 | "language models" "precision" "rounded measurements" | general | q9 |
| C3-38 | "模型" "有效数字" "不确定度" ChatGPT | general Chinese | q9 |
| C3-39 | Spithourakis Riedel 2018 numeracy language models rounding precision interval | backward citation chain | q10 |

直接平台补检：

- Google Scholar：`https://scholar.google.com/scholar?q=%22large+language+models%22+%22significant+figures%22`，工具返回不可访问；site 检索已执行，但不能替代 Scholar 内部检索。
- Semantic Scholar：`https://www.semanticscholar.org/search?q=language%20models%20numerical%20precision&sort=relevance`，工具返回不可访问；site 检索仅作为补充。
- GitHub：通过连接器执行 C3-25、C3-26，各返回 20 条，筛查标题和正文；结果多数为实现问题/自动论文摘要，未当作已核论文。C3-25 中 LitXBench issue #19 是显示精度影响数值评分的公开个案，但并未做模型主动/被动精度行为实验。
- ACL、arXiv：检索命中后直接读 Anthology PDF / arXiv HTML 正文及相关附录。

检索发现路径：C3-01–04 → Bahaj 等 (2025) → 文内 FinQA 引用与提示附录；C3-17–20 → Vidhani & Mariappan (2024) → §3.2/Fig.4 及补充材料链接；C3-05 → Guo 等 (2024) → AMPS Task 6；中文检索 → NUPA → arXiv 正文/附录；C3-16 → Yan 等 (2026)。

访问失败的原文/附件：

- Chemistry 2024 补充材料 `/article/10.3390/chemistry6040043/s1`：cache miss；正文 PDF `/2624-8549/6/4/43/pdf` 同样失败。尝试 mdpi-res 的 s001.pdf 路径也失败。公开正文 §3.2 可完整读取，故将 2/10→10/10 标为正文作者报告，未假称复核 S6–S8 原始回答。
- ACS 2026 `10.1021/acs.jchemed.5c01611`：摘要可读，全文不可访问，因此不作为降色决定性证据。
- Gauging Overprecision 的 ICLR 2026 匿名 OpenReview PDF 检索命中，但直连返回 404；不与已读 arXiv 版本重复计数，也不声称其已获 ICLR 接收。
- MeasureBench 的 CVPR 2026 官方 PDF 返回 403；保留为待补读线索。

`sources/precision_search_log.json` 保留返回结果标题、URL、工具引用标识和返回长度；为避免重复传播大段来源文本，没有把完整抓取正文放入交付。

