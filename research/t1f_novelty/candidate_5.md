# 候选 5：人工答案与程序执行值不一致

**判定：已有人做过同样的事；建议 ⚪；把握高。** 截至 2026-11-17。这里按任务的“报告不一致率，或据此筛过数据”标准判断；无需先例得到完全相同的 508/7,952。

## 决定性证据（正文：公开 PR、代码、发布文档）

izarov，2026-10-08，[Serve only FinQA tasks whose reference agrees with the written answer，EnvCommons/FinQA PR #4](https://github.com/EnvCommons/FinQA/pull/4)，当日 14:38:46 UTC 合并。已读 PR 的 Problem、Fix、Decisions、Tests，以及三个文件的完整补丁；核对合并版本 [`finqa.py` L27–74](https://github.com/EnvCommons/FinQA/blob/b0e5f907abda069f0915e93e006c4ba55658360e/finqa.py#L27)。

作者直接比较 `qa.answer` 和 `qa.exe_ans`，报告：

| 切分 | 原始题数 | yes/no | 数值字段不一致 | 保留 |
|---|---:|---:|---:|---:|
| train | 6,251 | 124 | 455 | 5,672 |
| dev | 883 | 10 | 58 | 815 |
| test | 1,147 | 20 | 80 | 1,047 |

训练集 455 个冲突中，作者列出 64 个反号、51 个其他单位、340 个其他。三个切分共 593 个数值冲突；593/8,127 = 7.30% 是本报告按其数字计算，分母为去掉 yes/no 的题数，**不是作者报告的我们的口径不一致率**。该 PR 明确对全部三个切分启用筛选；[当前发布页 Tasks](https://openreward.ai/GeneralReasoning/FinQA)也显示这些保留数。

过滤器在以下任一条件下判一致：1% 相对差；落在人工答案末位的半单位舍入带；同号截断误差小于一个末位单位；并对程序值尝试原值、乘100、除100。无可解析人工数字时保留。它不同于本项目只按显示精度、单列符号冲突、限定可解析分母的统计。因此 593 与 508 不构成互相否定；**也不能凭数字不同宣称方法新颖**。

PR 举 STT/2006/page_92.pdf-4：人工答案35.72%，程序反向相除得0.73684；16次训练会话给出约35.72均得0。这同时是基准造成稳定判错的已有公开个案。它不是多模型全测试集研究，不能扩张为候选4全部结论。

## 最接近的三项原始资料与短引

本条的直接先例是软件维护工作。以下明确标出资料类型，不把三个资料冒充三篇独立学术论文。

1. **PR #4（2026，直接先例）。** 原文 Fix：> “a task is served only if `exe_ans` is a number that agrees with the written answer.”
   已报告分切分计数、反号子类并实现过滤，满足任务的已有标准。来源层级：**正文／代码**。剩余增量是更严格解析规则、精确分母、与模型判错逐题关联，可作复现及证据，难独立撑文章。
2. **[Description for the attributes in the data file，czyssrs/FinQA issue #6](https://github.com/czyssrs/FinQA/issues/6)（2022-05-17，官方仓库公开讨论）。** 原文问题第3项：> “`answer` and `exe_ans` are different for Sample 1”
   给出380与3.8；已读全文，并通过API核查当时可见评论为空。来源层级：**正文（issue）**。只是个案且正好相差100倍，按本项目允许百分比缩放的规则未必算矛盾；不能单靠它降白或说已知6.4%。
3. **[FinQAPT: Empowering Financial Decisions with End-to-End LLM-driven Question Answering Pipeline](https://arxiv.org/html/2410.13959)（Singh、Kaur、Smiley，ICAIF 2024）。** §4.5.1 FinReader 段：> “disparities between the execution answer and the provided answer”
   已读 §§4.1–4.5，尤其4.5.1；论文直接指出执行答案与给定答案的差异，以及问数值却给百分比的口径问题。来源层级：**正文**。它未单独给两个字段的总体不一致率，也未说明按字段一致性筛题，故仅凭该论文尚不足完全命中任务的候选5标准；PR #4则已明确满足。FinQAPT在4.5.1报告其他错误类别的比例，但不能把那些比例转当字段矛盾率。

## 已知说法核实

- “导师没检索到”：现已补上2022 issue线索与2026-10已合并PR；不能继续用作首次发现主张。
- “官方判分用的是 `exe_ans`”：已读[官方 evaluate.py](https://github.com/czyssrs/FinQA/blob/main/code/evaluate/evaluate.py) 的 str_to_num、eval_program、evaluate_result，L188预测执行值舍入到5位，L418取exe_ans，L444比较相等；官方不是统一1%自由文本容差。
- [PR #2](https://github.com/EnvCommons/FinQA/pull/2)与[PR #3](https://github.com/EnvCommons/FinQA/pull/3)均于2026-10-07合并：前者按输出显示位数配1%上限，后者改为固定1%并提示至少3有效数字。讨论和实验针对**输出比较规则**，不是财报输入舍入所诱导的可行区间，不能拿来直接否定候选1。
- [PR #5](https://github.com/EnvCommons/FinQA/pull/5)于2026-10-09合并，增加文档单位感知的量级词处理。它说明单位与格式仍影响评分，不等于本项目独立重算已完成。

## 局限

已直接读取官方仓库全部可见 issues/PR（15条，含PR）及 EnvCommons全部6个PR，并核对高相关补丁。GitHub搜索接口曾对EnvCommons空查询返回0，但列举REST端点成功返回6条；因此本报告采用枚举结果，不把搜索零命中当零先例。Google Scholar和Semantic Scholar直接检索端点无法通过本轮浏览工具访问；见检索日志。未重跑PR的593条计数，本文报告的是作者的原始公开结果与已读实现，用户任务中的508条亦未在本轮复算。
