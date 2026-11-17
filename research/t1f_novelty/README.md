| 编号 | 结论 | 建议颜色 | 最接近的工作（题目、年份、链接） | 他们做了什么 | 我们多出来的是什么 | 把握 |
|---|---|---|---|---|---|---|
| 1 舍入定律与精确计数 | 读了正文仍未见 | **可条件升 🟢**，证据完整性由导师另判 | [Rounding errors and index numbers，1991](https://www.chicagofed.org/-/media/publications/economic-perspectives/1991/ep-may-jun1991-part1-gittings-pdf.pdf)；[VeriFin，2026](https://arxiv.org/html/2608.10213v3) | 已研究增长率舍入失真、披露精度下的声明验证；后者固定输入点值后设置输出容差【正文】 | **从财报输入显示精度传播答案可行范围，在金融QA统计不可辨识率并检验增长率阈值**。数学基础不是新意 | **中**：未找到满足此边界的正文；Scholar/S2原生检索及完整被引图未取回 |
| 2 冗余信息救不回来 | 已有人做过同样的事 | **⚪** | [XBRL Calculations 1.1 §5.5，2023/2024](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22+corrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22+corrected-errata-2024-02-14.html) | 重复披露区间取交，给出数值收紧效果并用于计算；舍入界+加总LP亦有先例【规范/论文正文】 | **FinQA中仅救回1/196**的负面实证仍新增，适合作为1的稳健性证据；难单独撑文 | **高**（按任务宽标准）；未见相同FinQA总体恢复率，不能把规范例子说成该负结果已发表 |
| 3 知道精度但不主动用 | 已有人做过同样的事 | **⚪** | [Optimizing Human–AI Collaboration in Chemistry，2024](https://doi.org/10.3390/chemistry6040043)；[Gauging Overprecision in LLMs，2025](https://arxiv.org/abs/2504.12098) | 有效数字题加明确提示后2/10→10/10；已有FinQA数值区间评测【正文】 | 以**输入舍入的精确可行集**测自然输出与提示后的精度仍有区别，可并入1；提示唤出能力的口号不足撑文 | **高**（宽模式有先例），窄设计未见为中；化学补充原始回答未取回 |
| 4 判错的是同一批题 | 已有人做过同样的事 | **⚪** | [FINESSE-Bench，2026，§7.4](https://arxiv.org/html/2605.15482v2)；[FinanceReasoning，ACL 2025](https://aclanthology.org/2025.acl-long.766/) | FINESSE在1,147题、53模型上统计共同错；FinanceReasoning修订CodeFinQA等并讨论标注质量【正文】 | 新模型样本的**基准侧逐题归因**可作新增审计；同错本身不证明基准错 | **高**；未见前人得到我们55/68的同一归因；FinQA-fix中文全文未取回 |
| 5 answer与exe_ans矛盾 | 已有人做过同样的事 | **⚪** | [Serve only FinQA tasks whose reference agrees with the written answer，2026，PR #4](https://github.com/EnvCommons/FinQA/pull/4)；[FinQAPT，2024](https://arxiv.org/html/2410.13959) | 已比较两字段、报告train/dev/test数值冲突455/58/80并筛题；论文更早提及冲突【PR正文/代码/论文正文】 | 我们的解析口径、508/7,952及模型对齐案例可作复现/量化补充；计数不同不构成新的问题 | **高**：PR于2026-10-08已合并；原文、代码、发布计数相符 |

**T1f一页结论 · 检索截至2026-11-17。** 严格采用任务预先给定的“或”标准；⚪表示该宽主张已有先例，**不表示前人做过本项目全部实验**。🟢仅是查新侧的有条件建议，不是“已证明无人做过”或“论文必然成立”。本轮不改项目首页和短文。

**建议主线：集中做候选1，将2、3作为区间审计的验证与行为结果，4、5作为评测背景和修复证据。** 应把贡献定位为输入级可辨识性的基准实证，避免宣称首次发现舍入误差、首次把数值标签视为集合、首次统计共同错或首次发现两个字段冲突。“舍入标签对应集合”本身也已有[2026年的直接研究](https://arxiv.org/html/2611.02461)。候选1尚需T1e证据与第二数据集支持，查新不替代实验验收。

**两项必须修正的写法：** 初稿§6的98.4%是“区间宽度在精确宽度二倍因子内”，不是端点精确正确率；FinanceReasoning修订的是795题CodeFinQA，不是原始1147题全test。专家91.16%也不能直接推成基准硬上限。

**附件入口：** [1–2原文证据及逐项核实](candidate_1_2.md) · [3](candidate_3.md) · [4](candidate_4.md) · [5](candidate_5.md)；全部检索词：[1–2](queries_1_2.md) / [3](queries_3.md) / [4](queries_4.md) / [5及补充](queries_5.md)；正文阅读清单：[1–2](reading_1_2.md) / [3](reading_3.md) / [4](reading_4.md) / [5及补读](reading_5.md)；[引用链](citation_chains.md)、[方法与覆盖缺口](methodology.md)、[验证记录](validation.md)。
