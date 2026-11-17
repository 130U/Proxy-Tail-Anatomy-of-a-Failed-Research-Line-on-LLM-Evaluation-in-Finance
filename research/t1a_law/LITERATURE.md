# T1A 定向查重与贡献边界

检索日期：2026-11-16（America/New_York）。这是有限范围的定向检索，不是系统综述，也没有声称用满半天。只将原论文、官方标准、官方数据说明及官方源码作为下述结论的依据；搜索中的镜像、聚合站和一般教程只用来发现线索。

## 结论

本轮未检出同时完成“财报输入舍入盒 → 增长率精度阈值 → 金融 QA 基准逐题判定与零参数验证”的完整先例，可以继续完成 T1A。但“舍入使经济增长率失真，并在真实经济数据上验证”已有明确的 1991 年先例；不能把这一层表述为新发现。相消、条件数、区间运算及均匀误差传播也不能作为新数学贡献。

可争取的贡献应限定为：对已固定的 FinQA 程序及输入绑定，证明并检验一个带适用条件的显示精度规则，明确近似规则的失败类型，并把最坏情形发生比例与指定概率模型下的期望比例区分开。是否说明模型被不公平判错，需要 T1C；是否在融合全文披露后仍然成立，需要 T1B。

## 核验过的主要先例

| 来源 | 已做什么 | 与 T1A 的交集及差异 |
|---|---|---|
| Thomas A. Gittings，1991，*Rounding errors and index numbers*，Federal Reserve Bank of Chicago，Economic Perspectives 15(3), pp. 2–10。[官方介绍](https://www.chicagofed.org/publications/economic-perspectives/1991/06mayjun1991-part1-gittings)、[官方全文](https://www.chicagofed.org/-/media/publications/economic-perspectives/1991/ep-may-jun1991-part1-gittings-pdf.pdf) | 比较 CPI-W 原始与重定基期后的水平值和月增长率；用 Monte Carlo 研究舍入对时间序列估计的影响；指出较低信号与显示有效位数减少会加重问题。正文 pp. 3–5、7–10；末页脚注明确区分重定基期与固定显示精度。 | 这是本轮新找到的实质性经济数据先例，覆盖“舍入精度损失 → 增长率扭曲 → 实证/模拟后果”。未见以末位单位差值 Δ 与相对容差 τ 构造金融 QA 逐题阈值检验。它限制宽泛新颖性，不构成该狭窄基准审计的直接重复。 |
| XBRL International，*Calculations 1.1*，2023-02-22 Recommendation，2024-02-14 勘误版。[规范](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22%2Bcorrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22%2Bcorrected-errata-2024-02-14.html) | §5.2.3 规定最近舍入事实对应半末位区间；§5.5 对一致重复事实取区间交集；§5.7 用区间加法与已知权重乘法作一致性检查。 | 财务输入区间及重复披露收紧已有正式标准。规范所列计算关系是求和关系；未给本任务的增长率 Δ 阈值、FinQA 发生比例或概率版本。T1A 不能称“首次将区间运算引入财报”。 |
| Silu Panda，2026-05-28，*FinVerBench: Benchmark Validity and Calibration in Large Language Model Financial Statement Verification*，arXiv:2605.29586v1。[原文](https://arxiv.org/html/2605.29586v1) | §3.4 与 §6.5 对比未舍入错误注入和按财报精度舍入的变体，研究显示方式及可观测性如何影响错误检出。舍入变体在其可观测子集上使所报告模型的 recall 从 100% 下降至 79%。 | 已有“财务 AI 基准结果受显示精度影响”的强近邻。任务是检验财务报表一致性/注入错误；未见以 FinQA gold program 推导输入舍入盒下答案范围、Δ 阈值或相应零参数混淆表。不能把所有“舍入影响金融 LLM 评测”的主张据为首创。 |
| Bethel Hall、Sachi Shome、William Eiers，2026-08-10，*VeriFin: A Neurosymbolic Framework for Verifying LLM-Generated Financial Claims*，arXiv:2608.10213v1。[原文 §3.6](https://arxiv.org/html/2608.10213v1#S3.SS6) | 验证器把操作数绑定到已披露的固定值，执行被授权公式，再以披露末位的半单位作为候选输出容差。其公式明确使用等式约束将每个操作数固定。 | 与 T1A 都涉及可验证财务数值及精度，但这里核验的是固定输入下的候选输出；不能把输出容差误读为输入区间传播。未见本任务的 Δ 法则验证。 |
| Federal Reserve Bank of St. Louis，FRED Help，*What Formulas are Used to Calculate Growth Rates?*。[官方说明](https://fred.stlouisfed.org/help/data/understanding-the-data/formulas-calculate-growth-rates) | 官方提示：由已公布的舍入水平数据重新计算百分比变化或增长率，可能与原始发布不同。 | 增长率对舍入数据敏感早已是公开的数据使用注意事项；此页面没有给出本任务阈值和基准检验。 |
| FinQA 官方固定提交 `0f16e2867befa6840783e58be38c9efb9229d742` 的执行器。[源码](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py) | `eval_program` 最终将数值 `round(this_res, 5)`；`evaluate_result` 与 `qa.exe_ans` 比较。 | T1A 的相对 1% 是指定的敏感性审计口径，不是这个版本官方 FinQA 的原始容差。输入盒内存在越界输出，也不等于“按显示数字作算术”的任务无定义。 |

上述文献中的经验数字属于各自设置；不移植为本项目的效果大小。本轮没有把未检出结果解释为不存在先例，也没有进行付费数据库的穷尽检索。

## 搜索记录

以下为实际发送的完整检索式（通用网络检索）；随后打开上述官方原文及其相关章节。没有筛掉与预想结论不利的命中。

1. `"FinQA" "rounding" "uncertainty"`
2. `"financial statements" "growth rate" "rounding" precision`
3. `"FinQA" "significant digits"`
4. `"financial question answering" "condition number"`
5. `"FinVerBench" rounding`
6. `"VeriFin" "rounding"`
7. `site:xbrl.org "Calculations 1.1" "interval"`
8. `"rounded data" "growth rates" uncertainty`
9. `"financial ratio" "rounding errors" interval`
10. `"growth rate" "significant figures" error rounding`
11. `"FinQA" "interval arithmetic"`
12. `"financial statements" "condition number" rounding`
13. `"rounding" "financial ratios" uncertainty bounds`
14. `"rounding error" "percentage change" bounds`
15. `"growth rate" "rounding" "interval" precision financial`
16. `Thomas Gittings "Rounding errors and index numbers"`
17. `"Rounding errors and index numbers" Chicago Fed`
18. `"FinQA" "rounding interval"`
19. `"financial ratios" "interval arithmetic" rounding`
20. `"rounding errors" "growth rates" "bounds"`
21. `"rounding errors" "financial statements" "precision"`
22. `"FinQA" "rounding" "Benford"`
23. `"growth rate" "rounding" "100" uncertainty`

其他发现与处理：搜索命中 CPI 舍入精度的诉讼专家意见、银行效率分析中的区间比率、商业财报工具对舍入加总差异的说明，以及大量有效数字教材。它们可作扩展检索线索，但本结论没有依赖镜像教程或未充分核验的专家意见；本轮也未从这些命中发现完整的 FinQA 精度法则验证。

## 可用的论文定位表述

“我们不提出新的相消理论或财报区间标准。我们研究已披露精度与金融问答审计容差之间的匹配：在固定程序和输入绑定的前提下，将经典误差传播转化为可复算的精度规则，在 FinQA 上检验其预测能力，并报告最坏情形与均匀舍入模型下概率结果的区别。”

这仍然是条件性的基准审计贡献；不能仅凭本次检索写成‘首个’、‘唯一’或‘已证明无先例’。
