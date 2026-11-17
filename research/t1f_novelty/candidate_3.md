# 候选 3：模型知道精度，但不主动用

| 编号 | 结论 | 建议颜色 | 最接近的工作（题目、年份、链接） | 他们做了什么 | 我们多出来的是什么 | 把握 |
|---|---|---|---|---|---|---|
| 3 | 已有人做过同样的事（按任务给定的“或者报告过不问/提醒后差别”宽标准） | ⚪ | [Optimizing Human–AI Collaboration in Chemistry (2024)](https://doi.org/10.3390/chemistry6040043)；[Gauging Overprecision in LLMs (2025)](https://arxiv.org/abs/2504.12098)；[Number Cookbook (2025)](https://arxiv.org/abs/2411.03766) | 已有有效数字计算的明确提示前后对比；已有 FinQA 数值区间输出和校准评测；已有有效数字舍入基准 | 财报输入的舍入可行集、以模型自己的表达式精确传播范围为参照、自然输出位数与可支持位数的相关分析，尚未在已读正文见到同一组合 | 高：足以否定宽口号的新颖性；中：窄组合未见的判断。Chemistry 补充原始回答、Scholar/S2 内部结果未成功取得 |

这里的 ⚪ 不是说现有论文复现了本项目全部设计，而是严格使用任务事先给定的“或者”标准。不能在发现先例后把判定标准悄悄改成“必须 FinQA、必须精确区间、必须大样本”来保住颜色。更窄的设计可并入候选 1 的论文主线；单靠“提醒后会用有效数字”不宜承担一篇文章的新意。

## 最接近三篇：正文证据及差别

### 1. Vidhani & Mariappan, 2024 — Optimizing Human–AI Collaboration in Chemistry: A Case Study on Enhancing Generative AI Responses through Prompt Engineering

来源层级：**正文**。出版于 *Chemistry* 6(4):723–737；已读 §2 实验设计、§3.2 和 Fig.4、§4。[出版者全文](https://www.mdpi.com/2624-8549/6/4/43)。

原文短摘（§3.2，Fig.4E 所用提示）：

> “Round the final answer based on significant figures rules”

作者报告：多步有效数字计算中，换成另一组数值/有效位数后（Fig.4D）仅答对 2/10；加入上面一句后（E）答对 10/10。不要混同于另一个变化：原始表达式 A 的 0/10，加括号 B 后是 9/10。换运算后 F 又失稳，因而只是小案例的行为先例，不是“模型普遍知道精度”的证明。§2 说明每种修订提示测试十次，并讨论同/异上下文窗口；补充表 S6–S8 未成功下载，所以这些计数是已核正文作者报告，未独立复算原始回答。它没有财报舍入区间真值，却已覆盖“默认不落实有效数字、明确提示后能改善”的宽说法。

### 2. Bahaj, Rahimi, Chetouani & Ghogho, 2025 — Gauging Overprecision in LLMs: An Empirical Study

来源层级：**正文**。已读 §§2–5、附录 A–D。[arXiv HTML](https://arxiv.org/html/2504.12098v1)。

原文短摘（§3.3）：

> “the percentage of instances where the ground truth answers fall within the generated intervals”

它在包含 3,262 道 FinQA 题的数值问答数据上要求模型输出上下界，测试预设置信水平、vanilla/CoT、聚合与自修订。§3.3 的真值是一个点答案，衡量点覆盖率；§5 Table 4 中区间宽度与要求置信度的相关接近零。不是传播输入舍入误差，不是默认打印位数与可信位数的相关。它直接否定“既有不确定性文献只研究答对概率、没有研究数值区间”的笼统说法。它也不能支持“一问就会”：其模型仍明显过度精确。正文 §4.1 写 generation 五次，Table 4 caption 写十次，引用时应避免擅自统一这个报告差异；本报告不依赖该次数下结论。检索命中的 ICLR 2026 匿名版本未取到，不作为独立研究或已接收论文。

### 3. Yang, Hu, Kang, Lin & Zhang, 2025 — Number Cookbook: Number Understanding of Language Models and How to Improve It

来源层级：**正文**。ICLR 2025 论文，arXiv 初版 2024；已读 §2、附录 A.1.3–A.1.4、A.2、A.3。[正文及附录](https://arxiv.org/html/2411.03766v3)。

原文短摘（附录 A.2 的正式任务提示）：

> “Sig_fig: Convert the number to scientific notation: &lt;a&gt; and keep significant figures as &lt;b&gt;.”

NUPA 的 17 类任务包括把数值舍入到指定有效位数；这是正式评测，不仅是“模型数值能力差”的泛论。这里有效位数由题目指定，模型无须判断测量/舍入输入可支持多少位，亦无默认输出与提醒后的实验。故它压缩的是“首次评测有效数字”的主张，不能直接抹去本项目的精确可行集设计。

## 已知相似观点逐项核实

| 已知说法 | 核实结果 | 来源层级及位置 |
|---|---|---|
| 不确定性表达、校准、口头置信度很多，对象通常是正确概率 | 基本正确，但“只有正确概率、没有数值范围”过强。[Just Ask for Calibration (Tian et al., 2023)](https://aclanthology.org/2023.emnlp-main.330.pdf) §2、Table 1 与附录 C 提示模板确实是正确概率；Bahaj 等已直接研究 FinQA 数值区间。 | 正文 |
| 数值能力、有效数字、单位处理已有评测 | 已核实。NUPA 的 Sig_fig 是指定位数舍入；[Learning to Plan by Updating Natural Language (Guo et al., 2024)](https://aclanthology.org/2024.findings-emnlp.589.pdf) Table 2 + Fig.18（PDF p.24 / 印刷 p.10085）有197例有效位数计数任务；[BIG-bench Unit Conversion](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/unit_conversion/README.md) 测单位识别、换算与算术。 | 论文正文/附录；仓库正文 |
| 科学问答里有效数字规则评测，暂无具体文献 | 现在有明确出处：Vidhani & Mariappan 2024 §3.2/Fig.4，且有提示前后对比，已命中任务宽标准。 | 正文 |
| FinanceReasoning 提到数值精度困难 | 由同组候选4核查：§4.2 与附录B Table 9 的例子是 Black–Scholes 中间步骤过度舍入（5.44 vs 5.46），不是财报输入精度传播或模型报告区间测试。候选3不再单独增加同源引文。 | 正文，交叉核查；详见候选4附件 |

## 2026 后续工作与排除理由

- **正文**：[Yan, Miao & Huang (2026), Training Autoregressive Language Models on Rounded, Bounded, and Censored Numerical Labels via Exact Likelihood](https://arxiv.org/html/2611.02461v1)，已读 §§1–3、§6.1、附录目录/限制。它把舍入观测建模成兼容值集合，训练分布而非任意补点；实验为合成分布恢复、分子测量删失、代码延迟。故“数值标签应为集合”的总论已有直接先例，但没有本项目的提示行为对照。
- **正文**：[Piskorz, Kobalczyk & van der Schaar (2026), Eliciting Numerical Predictive Distributions of LLMs Without Autoregression](https://arxiv.org/html/2603.02913v1)，已读 §§2–3、附录 A Related Works。探针从隐藏表征恢复模型数值输出分布的分位数，不是传播显示数字的确定性舍入范围。
- **仓库正文**：[CODATA DRUM-ML](https://github.com/codata/drum-ml)，README 明确包含 GUM 不确定度与有效数字子任务，但这是实验原型的设计/示例说明。未把 README 的示例 scorecard 当成经过核实的实验结果；不能以此声称已做本项目实验。
- **摘要，未取得正文**：[Outsmarting ChatGPT in Chemistry (2026)](https://doi.org/10.1021/acs.jchemed.5c01611) 的学生出题活动包含有效数字主题；[MeasureBench (CVPR 2026)](https://openaccess.thecvf.com/content/CVPR2026/papers/Lin_Do_Vision-Language_Models_Measure_Up_Benchmarking_Visual_Measurement_Reading_with_CVPR_2026_paper.pdf) 涉及仪器读数的有效答案区间。都不能用于确认/排除“精确区间真值评估模型报告精度”的窄先例，保留为后续补查点。

## 本项目表述必须保留的限度

引用链回溯：Yan 等 §2 指向 [Spithourakis & Riedel (2018), Numeracy for Language Models](https://aclanthology.org/P18-1196.pdf)。已核其 §3.3、Fig.2、公式 (9)–(11)（印刷 p.2107）：连续数值密度在“显示值 ± 半个末位单位”的范围积分，得到数值词元概率，同时建模小数位数概率。这说明语言模型中舍入区间的概率建模并非 2026 年才出现；其目标为数值生成建模，不是本项目的输入舍入传播/提示行为实验。来源层级：正文。

**来源层级：本地初稿正文 §6（并非独立复现）。** 98.4% 对应“区间宽度在精确值的二倍因子内”，98.7% 对应“区间包含精确范围”；两者都不等于端点精确相同。因此任务摘要“98.4% 给出正确/精确区间”会夸大结果，查新不能拿这个说法制造与前人的差别。本轮只指出，不修改短文。

可继续的窄主张是：**将输入显示精度推导出的可行集作为行为评估依据，分别测自然输出精度、明确询问后的范围覆盖/宽度及可靠位数。** 要把这条发展成主贡献，需跨数据集、跨提供商和严格端点/宽度指标；与候选1合成一条计量任务会比再次宣称“提示能唤出能力”更有区分度。这是研究建议，不是查新已证明的结论。

