# T1d：模型知不知道自己的答案有几位是可信的

最后一轮。做完之后导师写短文。分支 `task/t1d`，目录 `research/t1d_precision/`。只读 T1、T1a、T1b、T1c 的结果，不改它们的文件。不训练模型，不调用付费 API。

## 为什么做这一轮

T1c 的结论是：输入的舍入精度不改变现有的判分。原因很简单，标准答案和模型用的是同一批显示数字。但 T1c 同时看到，模型报出 12 到 16 位有效数字，其中有意义的只有 1 到 3 位。

现有基准测不了这件事。我们手里有每道题的精确答案区间，所以能测。问题只有一个：

> 直接问模型"你的答案有几位是可信的"，它答得对不对？教它一句规则之后呢？

本轮还有第二件事：T1b 和 T1c 的语义复核都是一个 AI 做的，需要另一个 AI 独立再做一遍。

---

## 第一部分：精度实验

### 题目

沿用 T1c 的 392 道题（196 道见证题，196 道按运算类型匹配的稳定题）和同样的文档文本。不重新抽样。

### 三个条件

| 条件 | 做法 | 新增调用 |
|---|---|---:|
| A 不问 | 直接用 T1c 已有的 392 个回答 | 0 |
| B 问，不教 | 下面的提示 B | 392 |
| C 问，并教规则 | 下面的提示 C | 392 |

每次调用是全新会话，只给提示、文档和问题。答题的 agent 不能访问本仓库，不能用代码或工具。提示逐字使用，定稿后不改。

调用预算不够时，条件 B 必须做满 392 道；条件 C 可以只做固定随机的一半（按配对抽 98 对，种子 20261117）。

条件允许时，用另一档模型把条件 B 再做一遍。做不到就写明。

### 提示 B

```
Solve the financial question using only the document below. Do not use external sources, code or tools.

Figures in the document are rounded to the precision shown: a displayed figure may stand for any value that rounds to it. Counts, years, dates and contractual terms are exact.

Give a final numerical answer, its unit, and a brief arithmetic expression showing your calculation. Your expression must use the figures exactly as displayed, with arithmetic operators (+, -, *, /, parentheses), and evaluate to your answer in the stated unit.

Then state how precisely the document determines your answer:
- "low" and "high": the smallest and largest values your answer could take, given the rounding of the figures you used.
- "reliable_digits": how many significant digits of your answer you would report as reliable (an integer; 0 if not even the first digit is reliable).

Do not include prose outside the JSON. Return JSON with exactly these fields:
{"answer": "numerical value as a string", "unit": "unit, or percent, ratio, times, years, etc.", "expression": "arithmetic expression", "low": "numerical value as a string", "high": "numerical value as a string", "reliable_digits": "integer as a string", "explanation": "one brief sentence"}

DOCUMENT
{document}

QUESTION
{question}
```

### 提示 C

与提示 B 完全相同，只在第二段（"Figures in the document are rounded…"）之后插入下面这一段：

```
How to work it out: a figure shown to a last digit of size u may be any value within u/2 of the displayed figure. The smallest and largest values of your answer are reached at extreme values of the inputs. For a difference b - a, or a growth rate (b - a)/a, of two figures with the same last-digit unit u, the result is uncertain by about u/|b - a| in relative terms; the two figures must differ by about 100 units for the result to be reliable to 1%.
```

### 真值怎么算

真值按**模型自己写的算式**来算，不按标准解法。这样测的是"模型是否知道自己这个算法的精度"，与它的算式是否和标准答案一致无关。

1. 把算式里的每个数字绑定到文档里的显示数字。绑定上的，按文档里显示的小数位给半个末位单位的舍入区间。同一个事实出现多次，用同一个变量。
2. 绑定不上、且明显是常数的（100、12、换算用的 1000 等），当作精确值。
3. 在舍入盒上求算式的精确取值范围 [L*, U*]，沿用 T1c 的有理数角点方法。
4. 记中心值 c 为算式在显示数字上的值，半宽 h* = (U* − L*)/2，**真实可信位数** d* = log10(|c| / h*)。
5. 算式解析不了，或者有数字既绑定不上又不是常数：该回答不参加精度打分，单独计数。h* = 0（输入全是精确值）和 c = 0 的题也单独计数。

对条件 A：模型没有报区间，只统计它打印了几位有效数字。

### 指标

对条件 B 和 C 的每个回答：

1. **区间宽度比** r = (high − low) / (U* − L*)。分三类：
   - 准确：0.5 ≤ r ≤ 2；
   - 报得过窄（夸大精度）：r < 0.5；
   - 报得过宽：r > 2。
2. **是否包住**：low ≤ L* 且 high ≥ U*，允许真实宽度 5% 的误差。
3. **位数误差** e = reliable_digits − d*。报告中位数、|e| ≤ 1 的比例、e > 1（多报一位以上）的比例。
4. **1% 判断**。模型的区间如果满足 max(|high − answer|, |answer − low|) ≤ 1% × |answer|，就算它认为"答案确定到 1%"。真值用 [L*, U*] 和 c 按同样的式子算。报告准确率，并分开报告：真不确定的题里它认出了多少，真确定的题里它认对了多少。
5. **自相矛盾**：模型自己的区间对应的位数是 log10(|answer| / 半宽)。reliable_digits 比它多一位以上的比例。

对照行：在同样的题上，T1a 的一阶规则做第 4 项的准确率；以及"永远回答确定"的准确率。

每个数都给按页面成簇的 bootstrap 95% 区间（沿用 T1c 的 237 个页面簇）。条件 C 减条件 B 的差用同题配对。

所有指标报两遍：全部可打分的回答；以及其中算式按官方规则与标准答案一致的子集。再按见证题 / 稳定题、按运算类型分开各报一遍。

### 怎么下结论

主要看三个数：第 1 项的"准确"比例、第 3 项的"多报一位以上"比例、第 4 项的准确率。结论只有三种，执行前就定好：

| 结论 | 条件 |
|---|---|
| 模型本来就知道 | 条件 B：准确比例 ≥ 80%，且 1% 判断准确率 ≥ 90% |
| 教一句就会 | 条件 B 不满足，条件 C 满足同样两条 |
| 教了也不会 | 条件 C 也不满足 |

压线时照实写数字，按上表归类。不要因为差一点就写"无法判断"。只有一种情况例外：不能参加打分的回答超过 10%，这时先报告原因。

三种结论都能写进短文，没有哪一种算失败。

---

## 第二部分：让另一个 AI 把语义复核重做一遍

### 复核 T1b 的判断

1. 对象：T1b 的 196 道见证题，再加 60 道从稳定题里固定随机抽出的题（种子 20261117）。共 256 道，打乱顺序。加入稳定题有两个用处：复核者不能假设每道题都有问题；顺便得到稳定题里语义问题的比例。
2. 复核者是全新会话，尽量用与第一次不同的模型档位。它只看到：文档、问题、标准解法、每个输入绑定到的位置。**看不到**第一次的判断和理由，看不到区间和见证值，看不到题目属于哪一组。
3. 判断标准沿用 T1b：输入绑定对不对；这个量是不是舍入过的金额（而不是精确的计数、合同条款、定义值）；标准解法是否符合题意。输出 valid / invalid / uncertain 和一句理由。
4. 两次判断不一致的题，交给第三个全新会话。它看到两条理由，但不知道哪条是先做的。三次判断全部保留。

报告：

- 两次复核的一致率和 Cohen's κ，以及 3 × 3 的对照表。
- "保留"的题数，按三种口径各报一个：第一次复核（139）；两次都判 valid；三次里多数判 valid。**短文用最严的口径（两次都判 valid）做主数字。**
- 稳定题里被判 invalid 或 uncertain 的比例，与见证题比较。

### 复核 T1c 的归因

1. 对象：T1c 里 68 个被官方规则判错的回答。
2. 同样由全新会话独立重判，沿用 T1c 的 `REVIEW_RUBRIC.md`，看不到第一次的归因。不一致的交给第三个会话。
3. 报告一致率、κ，以及两次都同意的条件下，"参考答案有问题"和"合理的口径差异"各占多少。

---

## 交付

- **一张图**，三幅：
  1. 条件 A、B、C 下，模型声称的位数对真实可信位数的散点或箱线图；
  2. 条件 B、C 的区间宽度比分布（对数刻度），标出 0.5 和 2；
  3. 1% 判断的准确率：条件 B、条件 C、一阶规则、"永远回答确定"。
- **一页结论**，开头填好这张表：

| | 条件 A 不问 | 条件 B 问 | 条件 C 问并教 |
|---|---:|---:|---:|
| 可打分的回答数 | | | |
| 声称位数的中位数 | | | |
| 真实可信位数的中位数 | | | |
| 多报一位以上的比例 | | | |
| 区间"准确"的比例 | — | | |
| 区间"过窄"的比例 | — | | |
| 1% 判断准确率 | — | | |

  接着写：属于三种结论里的哪一种；语义复核后 139 这个数变成多少。
- `results.json`：上表的全部数字和区间，以及第二部分的全部计数。
- 逐题表 `per_response.csv`：题号、组别、运算类型、条件、是否可打分、算式是否与标准答案一致、L*、U*、d*、low、high、reliable_digits、r、是否包住、e、模型的 1% 判断、真实的 1% 判断。
- 全部原始回答、两份提示原文、打分和分析代码。

不要清单、哈希表、打包脚本、对复核的复核。

## 要注意

- 提示里不提本研究、不提 T1、不提组别。
- 不根据答得对不对重试。格式坏掉的回答保留并计数。
- 正式运行前可以用 10 道题检查 JSON 能否解析。这 10 道从训练集取，不得来自这 392 道。看过正式结果之后不改提示、不改指标定义。
- 条件 B 的提示本身已经告诉模型"数字是舍入过的"。这是任务定义的一部分，写结论时要说明：条件 B 测的是"被提醒之后会不会算"，不是"会不会主动想到"。主动想到与否由条件 A 回答。
- FinQA 是公开数据，模型可能见过题目和答案。这对精度问题的影响应当很小，因为基准里没有区间的标准答案。照实写这条限制。
