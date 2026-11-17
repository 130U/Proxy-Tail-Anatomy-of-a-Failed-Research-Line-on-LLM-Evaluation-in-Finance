# T1 输入来源与可解析性

核查日期：2026-11-16（America/New_York）。本文件仅记录数据准备与结构检查；此阶段未执行答案区间、越界率或继续／放弃的假设测量。

## 固定输入

| 数据 | 固定上游版本 | 本地位置 | 实际读取条数 |
|---|---|---|---:|
| FinQA train | `0f16e2867befa6840783e58be38c9efb9229d742` | `data/finqa/train.json` | 6,251 |
| FinQA dev | 同上 | `data/finqa/dev.json` | 883 |
| FinQA public test | 同上 | `data/finqa/test.json` | 1,147 |
| TAT-QA dev | `870accc41953dcde885aabeb963d94aabdc0fbc3` | `data/tatqa/dev.json` | 278 文档组、1,668 问 |

FinQA 合计 8,281 问；没有下载不提供 gold program 的 private test。以上数量来自对下载文件的 JSON 结构读取，不是研究结果。固定版本分别由官方 [FinQA commit](https://github.com/czyssrs/FinQA/commit/0f16e2867befa6840783e58be38c9efb9229d742) 和 [TAT-QA commit](https://github.com/NExTplusplus/TAT-QA/commit/870accc41953dcde885aabeb963d94aabdc0fbc3) 确认。

两者官方仓库根目录均提供 MIT License：FinQA 为 Copyright (c) 2021 Zhiyu Chen；TAT-QA 为 Copyright (c) 2021 Fengbin Zhu。原文已随下载保存在各数据目录的 `LICENSE`，对应 [FinQA LICENSE](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/LICENSE)、[TAT-QA LICENSE](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/LICENSE)。本交付提交下载器及派生分析，原始下载文件由本目录 `.gitignore` 排除。

在仓库根目录执行 `python research/t1_rounding/download_inputs.py` 可重新取得上述固定版本及官方评测源文件。下载器只用 Python 标准库，先完整下载、校验 JSON 可读取再写盘；已存在文件跳过。没有模型调用或付费 API。FinQA 文件较大，使用官方 raw 固定提交地址下载；首次 TAT-QA 连接中断后重新下载成功，没有保留不完整文件。

## FinQA：可以做，但数字必须绑定到来源

每条记录含 `pre_text`、`post_text`、`table_ori`、`table`、`filename`、`id` 和 `qa`。`qa` 含 `question`、`answer`、`program`、`program_re`、`steps`、`gold_inds`、`ann_table_rows`、`ann_text_rows`、`exe_ans`。另有检索结果，不能当作新的源披露。[官方数据](https://github.com/czyssrs/FinQA/tree/0f16e2867befa6840783e58be38c9efb9229d742/dataset)

- `qa.answer` 在三个 split 中全为字符串，能保留人工答案的 `127.40`、`93.5%` 等格式；`qa.exe_ans` 多为 float，少量为 `yes` / `no`。人工答案格式与执行尺度须分别处理。
- `table_ori` 保留原始表格字符串，包括逗号、括号负数、HTML、`5.0` 等末尾零；`table` 是预处理表示。`pre_text` / `post_text` 已经是提取和预处理后的文本，并非原 PDF 的逐字排版。因此此数据准备支持的是“基准提供的文档表示中显示的精度”，不能保证恢复原始 PDF 的全部版面、末尾零或全文信息。
- `gold_inds` 和 `ann_table_rows` 标出支持行，但没有为每个 program operand 提供唯一 cell 坐标。同一数值在不同年份、行、列多次出现时，不能仅凭值相等断言是同一变量，也不能把同一来源的多次引用视为独立扰动。
- `const_*` 是 DSL 编码，不能一概解释为数学上精确的常量。下面第一例 `const_5` 实际代表报告显示的 `5.0`。相反，比例换算 `const_100`、求平均的计数常量等应保持精确，须按用途分类。
- 不应利用 `steps[*].res` 的显示小数位重建中间误差：官方执行器不在每一步舍入，只在最终结果处调用 `round(this_res, 5)`。`steps` 的人工中间答案与程序执行是不同层次。

### 具体陷阱

1. **数据编码常量不等于精确数学常量。** `V/2008/page_17.pdf-1` 问 American Express 每笔交易平均支付量。程序 `divide(637, const_5)`；`table_ori` 对应行中 Payments Volume 为 `637`（billions）、Total Transactions 为 `5.0`（billions），人工答案为 `127.40`，执行答案为 `127.4`。若把 `const_5` 固定不动，会漏掉输入分母的舍入不确定性。[dev 数据](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/dataset/dev.json)
2. **百分数程序尺度不统一。** `C/2017/page_328.pdf-1` 的答案 `93.5%` 对应 `subtract(193.5, const_100), divide(#0, const_100)`，执行答案为 `0.935`。`DVN/2007/page_58.pdf-2` 的答案 `24.69%` 对应 `divide(60, 243), multiply(#0, const_100)`，执行答案为 `24.69136`。不能对所有含 `%` 的人工答案统一除以 100 后直接和执行结果比较。[dev 数据](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/dataset/dev.json)
3. **预处理伪数字。** `DVN/2007/page_58.pdf-2` 中 International 的 NGLs 原单元格为 em dash `—`，`table` 把它编码成 `2014`。年份、脚注、缺失符号和 HTML 编码必须排除出可扰动财务量。[dev 数据](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/dataset/dev.json)
4. **括号和表操作。** `AES/2016/page_191.pdf-3` 使用 `table_average(settlements, none)`；预处理行是 `-13 ( 13 )`、`-19 ( 19 )`、`-2 ( 2 )`。官方 `process_row` 去掉 `$` 并截去 `(` 及之后部分，得到负数。应在与官方中心值对齐后，用 `table_ori` 的原显示位数建区间，而不是把括号里的数当成额外独立输入。[dev 数据及官方执行器](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py)

官方 DSL 支持 `add`、`subtract`、`multiply`、`divide`、`exp`、`greater` 以及 `table_max`、`table_min`、`table_sum`、`table_average`。`#k` 引用前面第 k 步；table 操作第一个参数是行名，第二个通常为 `none`。最终执行值保留五位小数后，直接与 `qa.exe_ans` 判等，**不是 1% 相对容差，也不是按 `qa.answer` 小数位舍入**。T1 的两套判分规则应命名为额外审计口径。[官方 evaluate.py](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py)

## TAT-QA：可选扩展的实际成本

开发集共 1,668 问，其中 `answer_type=arithmetic` 718 问，`span` 701，`multi-span` 217，`count` 32。每个文档组含 `table`、`paragraphs`、`questions`；题目有 `derivation`、`scale`、`rel_paragraphs` 等字段。算术题的 `derivation` 是中缀表达式，例如 `44.1-56.7`，并非 FinQA 的 DSL。[固定开发集](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/dataset_raw/tatqa_dataset_dev.json)

具体例：`eb787966-fa02-401f-bfaf-ccabf3828b23` 问 Other 在 2019 相比 2018 的变化，`derivation=44.1-56.7`，`answer=-12.6`，`scale=million`；来源表格保留字符串 `44.1` 和 `56.7`。但算术答案通常是 JSON float/int，不能由 Python `str(float)` 可靠恢复作者原先希望显示的末尾零。若做 TAT-QA 扩展，需要独立安全中缀解析器、scale 规范化、来源绑定，并将“gold 显示位数”无法恢复的题单列，不能伪造精度。

官方 TAT-QA metric 与数值处理代码也已本地保存，以便分析时核对，不应假设其评分和 FinQA 一致：[tatqa_metric.py](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_metric.py)、[tatqa_utils.py](https://github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/tatqa_utils.py)。
