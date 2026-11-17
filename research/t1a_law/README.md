# T1A：显示精度与答案精度

任务：[T1a_law.md](../../tasks/T1a_law.md)。结论入口：[一页结论](ONE_PAGE.md)。分支 `task/t1a`。代码和交付均在本目录，T1 文件保持其 `task/t1` 基线内容不变；没有重新绑定输入、训练模型或调用付费 API。

## 结果与范围

输入只读取 `research/t1_rounding/results/per_question.jsonl` 的 8,281 行；其中 5,337 行可分析，2,944 行排除。后者没有被赋为稳定或零概率。由于结果在本任务之前已被观察，本次称复核与扩展，不声称新的预注册确认性实验。

| 增长率口径 | 题数 | 用途 |
|---|---:|---|
| T1 的 growth 标签 | 1,458 | 保持原类别，全量混淆表 |
| 上述标签且两个输入 | 1,434 | 包括 9 个原未定项 |
| 上述且 T1 已判定 | 1,425 | 原 97.8% 与四组表格复现；Δ 对原输入直接算 |
| 代数上等于 ±1 或 ±100 倍 `(b/a−1)`，单位统一 | 1,427 | 精确增长率规则、位数预算、Benford |
| 原 T1 严格 `subtract(b,a), divide(#0,a)` 结构 | 1,307 | 解释与早先 growth_summary 的分母差别 |

1,427 条标准增长率全部同号且非零；Benford 模型排除 31 条不属于该结构的 growth 标签题。其 1% 实测为 578/1,427=40.5046%。原复现和标准化规则的逐条误判分别是 31 与 29，不能混用。

主零参数规则为 `abs(center-gold)+sum(abs(gradient_i)*halfwidth_i)>tau*abs(gold)`。重复变量先合并偏导系数，再取绝对值。该规则在 1% 下与原 5,322 个已判定标签、以及独立重算的全部 5,337 个标签均一致；原 15 个未定项全部变为 inside。忽略 gold 偏移会错 1 题。

新值域认证使用有理数：5,330 题由导数区间同号证明极值在角点，7 题由每个变量分别线性分式的性质证明。始终检查原程序分母在盒内有定义；未将外包络越界当成实际越界。边界恰相切算 inside，严格越界可用连续性取得内部见证。

一阶规则没有普遍的 100% 保证。例如 `a=100,b=300,h_a=h_b=0.5,gold=2,tau=0.01`，一阶半径恰为 0.02，预测 inside；真实上端 `300.5/99.5−1≈2.0201005` 超出 2.02。在本数据的 0.1%、0.5%、1%、2%、5% 容差下，误判次数为 **2、0、0、2、1**，见 [逐条记录](results/first_order_tau_mismatches.csv)。

## 分布预测与概率

Benford 主模型独立抽取经验增长率边际和经验 `(k_a,k_b)` 位数对，再独立抽取 `log10(M_a)~Uniform[0,1)`。令 `a=M_a,b=(1+g)M_a`，按各自有效位数构造末位单位。预测器不读取原题 mantissa、gold 或确定性标签；结果对照部分才使用原值域标签。通过 mantissa 的十进制边界分段，对精确阈值作解析积分，无参数拟合。

这比“首位数字服从 Benford”更强，也假设增长率与位数独立。主预测 41.5192%，联合经验分布敏感性 42.0971%，首位内均匀敏感性 41.3635%；实测 40.5046%。仅给首位概率、保留上述其他独立性时，数值识别范围为 38.6904%–44.5891%。其中取值端点由双精度分段计算。test 单独分布代入的预测/实测为 40.0984%/40.3587%，仍非在 train 拟合后对 test 的外推。1% 下中心带与 gold 带的实测计数相同，其他容差在 JSON 中分别保留。

概率定义是每题在输入盒中独立均匀取值时，原程序输出超出 gold 接受带的概率。**4,787 题由双变量以内线性分式的闭式 CDF 计算（双精度），550 题用每题 262,144 个独立伪随机样本。** 种子由固定前缀、split 和 ID 决定；同来源引用共享样本。不要求题目之间的真实误差独立才能对概率求和，题间独立随机数只用于控制计算误差。

全体可分析题在 1% 下的期望越界数为 731.4699/5,337=13.7056%，最坏情形为 1,469/5,337=27.5248%。test 对应为 98.6177/731=13.4908%，最坏情形为 196/731=26.8126%。test 期望比例的估计 Monte Carlo 标准误约 0.00038 个百分点；这仅是模型内计算误差，不包含来源绑定、均匀假设或真实财报分布的不确定性。每题 Wilson 区间在输出内，MC 零命中不等于严格零概率。

| 容差 | test 最坏情形 / 731 | test 均匀模型期望 / 731 | 期望题数 |
|---|---:|---:|---:|
| 0.1% | 55.68% | 38.35% | 280.32 |
| 0.5% | 34.88% | 19.70% | 144.00 |
| 1% | 26.81% | 13.49% | 98.62 |
| 2% | 18.88% | 8.12% | 59.32 |
| 5% | 9.71% | 3.10% | 22.68 |

原来的 17.09% 使用全部 test 的 1,147 题分母。相同分母下，均匀模型已分析部分贡献为 8.60%，但排除的 416 题概率未知，因此整个 test 的覆盖界为 8.60%–44.87%，不是完整总体概率估计。存在性与概率版本都依赖输入盒；T1B 收紧全文约束后必须另算。

## 复现

已验证 Python 3.12.14、NumPy 2.5.3、SymPy 1.14.0；绘图使用 Matplotlib 3.11.2。使用正常 Python 环境，从仓库根运行：

```powershell
python -m pip install -r research/t1a_law/requirements.txt
python research/t1a_law/analyze.py
python research/t1a_law/benford.py
python research/t1a_law/probability.py
python research/t1a_law/plot_results.py
python -m unittest discover -s research/t1a_law -p "test_*.py"
python research/t1a_law/theory_checks.py
python research/t1a_law/test_benford.py
```

前三个分析脚本支持 `--input` 与 `--output-dir`；概率默认 `--samples 262144`。所有默认经验输入均是原 T1 JSONL，不读取或导入 T1 分析代码。标准输出重跑即可替换本目录派生结果；不改输入。科学计数与浮点文本可能随依赖版本有末位差异。

核心公式的有理测试覆盖增长率角点、同异号、不等精度、余项和位数预算。独立概率测试用有理多边形裁剪面积作 oracle，240 个合成接受带和 114 个真实题接受带均通过。独立数值复核执行 24,674 个角点，与全部保存极值一致；另用符号导数核验 240 题。这些是本任务的实现验证，未宣称外部人工审稿或形式化证明。

## 文件

| 内容 | 文件 |
|---|---|
| 一页结论、证明、查重 | [ONE_PAGE.md](ONE_PAGE.md)、[PROOFS.md](PROOFS.md)、[LITERATURE.md](LITERATURE.md) |
| 一张三面板图 | [PNG](results/t1a_law.png)、[PDF](results/t1a_law.pdf) |
| 每题精确值域、规则和各容差标签 | [per_question.jsonl](results/per_question.jsonl) |
| 全量混淆表与原复现 | [summary.json](results/summary.json)、[mentor_replication.csv](results/mentor_replication.csv) |
| 原口诀误判、单位统一后误判、其他容差一阶误判 | [simple_rule_mismatches.csv](results/simple_rule_mismatches.csv)、[canonical_simple_mismatches.csv](results/canonical_simple_mismatches.csv)、[first_order_tau_mismatches.csv](results/first_order_tau_mismatches.csv) |
| 1% 一阶误判（零行，保留表头） | [first_order_mismatches.csv](results/first_order_mismatches.csv) |
| Benford 分布输入和对照 | [benford_summary.json](results/benford_summary.json)、[benford_inputs_and_outcomes.csv](results/benford_inputs_and_outcomes.csv) |
| 每题概率、数值误差和汇总 | [probabilities.jsonl](results/probabilities.jsonl)、[probability_summary.json](results/probability_summary.json) |
| 各 split 容差曲线 | [tolerance_curve.csv](results/tolerance_curve.csv) |

相消和有效数字理论是经典结果；经济增长率舍入失真也已有 [1991 年 Chicago Fed 研究](https://www.chicagofed.org/-/media/publications/economic-perspectives/1991/ep-may-jun1991-part1-gittings-pdf.pdf)。本项目的可用主张是条件性基准精度审计，不能由本次查重推出“首个”或“无先例”。FinQA 官方固定版本使用 [五位小数执行结果比较](https://github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/code/evaluate/evaluate.py)；本目录没有把 1% 审计口径称为官方评分规则。
