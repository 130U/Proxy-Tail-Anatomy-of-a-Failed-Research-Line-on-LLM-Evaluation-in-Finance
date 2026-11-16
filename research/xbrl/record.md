# 实验 WP0.4-offline：受限数值与单位解析

## 要检验的问题

只验证本地人工synthetic fixture的单位、scale、sign、decimals、context转换与失败时拒绝行为；不回答真实SEC语料是否足够支撑可信核心。

## 预算

运行前记录见 [budget.md](budget.md)：CPU，预计10秒内，0显存、0训练token，无网络。

## 配置

- 基线commit：8e4dd0b33c95ac2ac1a6015eba6f2dfafe5c1254；新增代码在research/xbrl/，运行时未提交。
- Python 3.12.14，Windows AMD64 CPU，标准库；不需要随机seed。
- 数据：`synthetic_fixture.xml`，SHA256见 [example_result.json](example_result.json)。事实结构由本轮手工指定。
- 实际测试：8项unittest全部通过；测试框架计时0.006秒，解析+测试工具调用耗时约1.35秒（包含进程启动）。来源层级：**我们的实验 WP0.4-offline**。

## 结果

| 条件 | 输出 | 解释 |
|---|---|---|
| 123.40 × 10^6 USD | 123400000 | scale精确换算 |
| 5.2 × 10^3 USD，sign=- | -5200 | sign与scale分别应用 |
| ratio=0.125，decimals=3 | 声明舍入区间[0.1245,0.1255] | 条件于准确度声明，不是真实值验证 |
| unknown accounting transformation | 拒绝，保留reason | 不把(1,234)猜成可支持输入 |
| missing unit/context、continuation、反向period、超域scale、缺decimals | 相应事实拒绝 | 不返回看似有效但无前提的数值 |
| duplicate ID / DTD | 整文档拒绝 | 不选择含糊绑定 |

完整JSON见 `example_result.json`，包含3条已解析事实、1条格式拒绝、`status=partial`及`timestamp_certificate=null`。这些计数是特定手工案例的确定性检查，不是随机样本，因此没有95%真实误差率区间。

## 结论和限制

本地文件→受限结构化数值的接口已可运行。真实SEC统计、calc覆盖、accepted精度、修正申报、inline文本对齐、每年监督规模均未测。原型不能证明真实无前视或单位解析在开放文本上正确，也不构成完整WP0.4验收。按用户要求没有新增外部访问。
