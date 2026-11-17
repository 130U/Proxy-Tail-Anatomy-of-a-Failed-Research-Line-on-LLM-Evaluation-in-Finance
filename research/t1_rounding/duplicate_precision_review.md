# 同量不同精度：来源核验与计算示例

日期：2026-11-16（America/New_York）。这是补充审计，不替代主实验舍入盒下的越界率。来源为 `sources.md` 记录的固定版本 FinQA；位置均为原始 JSON 的零基索引。语义确认由本次 AI 阅读题目、完整页面表示、表头、脚注及 gold 支持行完成，不是外部专家标注。

## 扫描范围和结果应怎样读

`find_duplicate_precision.py` 已扫描全部公开 test 页面。启发式只提名：表格中正数、叙述中明确带 thousand/million/billion 的数字、不同末位精度、统一候选单位后舍入区间重叠、并共享至少一个指标词。它不自动判定年份、指标范围或事实同一性，也不覆盖所有百分数、负数、无单位叙述、表表重复和跨页披露。

完整 test 候选在 `duplicate_precision_test_candidates.csv`：**54 个候选位置对、24 页、54 个表格单元格**，没有截断。另一个 `duplicate_precision_candidates.csv` 是跨 train/dev/test 故意截到 100 条的演示集合，不能作为任何总体分母。

本文件作者负责 test 候选第 1–27 对，逐项结果在 `duplicate_precision_test_review_part1.csv`。其中 **14 对确认同一事实、10 对否定、3 对保留待定**；确认者涉及 9 页。确认同量不一定意味着这道问题实际使用该量；进一步核对 question / gold program / gold_inds 后，本批有 **11 个问题**确实使用了其中一处来源。

对这 11 问，只改变已确认同一事实的出现位置中心值，并在统一单位后原样运行 gold program，得到 **2 问从 1% 容差内移到容差外，6 问从人工答案显示单元内移到单元外**。1% 以 `qa.exe_ans` 为目标；显示单元沿用主分析的 `display_acceptance`。表平均例使用与原表行逐项相等的显式加法／除法展开，并检查原中心与官方执行标签相差不超过 0.000005。逐问原值、新值、替换方向、分数和判定见 `duplicate_precision_test_substitutions_part1.csv`，由 `review_duplicate_part1.py` 复算。第 28–54 对由另一位执行者负责，未纳入本段数字。

主解析器补充前导小数点支持后，本批已重跑：BLL/2010/page_35.pdf-1 的 gold `.635` 可正确解析，原值 0.635 与替换后的 0.6349 都在显示单元内。11 问的显示口径现均可判定，以上 2 问和 6 问的跨界计数不变。

这些是已读候选范围内的确认数量；**11 不是整个 test 的完整重复披露题数，2 和 6 也不是总体边界跨越率**。尤其不能把“候选 54”直接称作“54 道题答案不确定”。同一页可有多题、同一道题可涉及多次披露。

## 五个可复核实例

| 例子 | 同一事实的精细显示与粗显示 | 题目计算与实际变化 |
|---|---|---|
| AAL/2015/page_114.pdf-1（test） | 2013 labor-related deemed claim；`table_ori[1][1]` 为 1,733 million，`post_text[2]` 为 1.7 billion。`post_text[0]` 的脚注 (1) 将叙述明确绑定到表格该项。 | `1733/2655` 得 65.2731%；改用 1700 million 得 64.0301%。相对变化约 1.9042%；原人工答案为 65.3%，两种口径均跨界。 |
| ADBE/1999/page_64.pdf-2 与 -3（test） | 1999-12-03 剩余 restructuring accrual；`table_ori[1][5]` 为 772 thousand，`post_text[0]` 为 0.8 million。`post_text[10]` 说明更早合并项目已无余额。 | -2 原 gold 使用粗叙述 `0.4/0.8=50%`；换成精细 `0.4/0.772≈51.8135%`，两种口径均跨界。-3 原为 `772−8867=−8095`，换成 800 得 −8067；1% 内但整数显示不同。 |
| DXC/2018/page_56.pdf-3（test） | 2018 cost of services，均排除折旧摊销及重组；`table_ori[2][1]` 为 17,944 million，`post_text[5]` 为 17.9 billion。 | `17944/22885` 得 78.4094%；改用 17900 得 78.2172%。仍在 1% 容差内，按 gold `78.41%` 的两位小数则变成 78.22%。同页 -1 只有整数 `78%`，替换后仍通过，说明显示口径影响结论。 |
| GS/2013/page_63.pdf-2（test） | 2013 年 12 月 total assets；`table_ori[2][1]` 为 911,507 million，`pre_text[0]` 为 911.51 billion。 | `911507−938555=−27048`；换成 911510 得 −27045。1% 内，gold 整数显示不同。同页 -1 的平均资产也从 925031 变为 925032.5。 |
| GIS/2006/page_43.pdf-1（train，演示，不混入 test 数） | 2006 current portion of long-term debt；`table_ori[2][1]` 为 2,131 million，`post_text[0]` 为 2.1 billion，叙述说明是未来 12 个月到期并列为流动部分的债务。 | `2131/6049` 得 35.2290%；改用 2100 得 34.7165%。相对变化约 1.4547%；原人工答案 35.2%，两种口径均跨界。 |

对应原始数据：[test.json](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/dataset/test.json)、[train.json](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/dataset/train.json)。表中计算是本次派生结果；论文或数据作者没有提供这些跨界统计。

## 为什么相近数值不够

- **ABMD/2008/page_86.pdf：**表格 168 thousand 明确 *excluding accrued interest*，叙述 0.2 million 明确 *including accrued interest*。虽然数值接近、年份相同，但不是同一量，必须拒绝。
- **BLK/2017/page_121.pdf：**表格 5,225 million fair value 是 2017 年，叙述 5.2 billion 是 2016 年；另有 principal、carrying value、fair value 之间的误匹配。不能只按表中最接近的数绑定。
- **DXC/2018/page_56.pdf：**折旧摊销 1,964 million 和 SG&A 2.0 billion 的区间虽重叠，叙述还提到 depreciation，但它实际是在明确排除折旧。关键词相似也不保证同一指标。
- **AMT/2010/page_99.pdf：**原始发行金额与两三年后的未偿本金数值相等，仍不能在没有其间变动证据时把它们自动当作同一时期的事实。

## 正确的解释与合并

这五个实例中，精细来源的舍入区间落在粗来源的区间内。它们通常是**相容的重复披露**，不是财报自相矛盾。例如 GIS 的表格支持 `[2130.5, 2131.5]` million，叙述支持 `[2050, 2150]` million；共同使用文档时应取交集，得到前者。把两个显示中心分别塞进程序，展示的是“来源选择会改变判分”，不是证明原始财报真实值能在两个显示中心之间自由变化。

反过来，ADBE 的 gold 已使用较粗叙述 0.8 million；精细表格将可行值收窄到 0.772 million 附近，导致另一中心计算跨界。这支持对来源选择和 gold 计算口径做审计，但不能单凭一个例子宣布该基准所有答案都以未舍入真实量为目标。

上述区间都条件于四舍五入假设。合同本金、定义数值与明确精确的整数，应另外审查；同量不同显示位数本身不证明存在随机或未知误差。
