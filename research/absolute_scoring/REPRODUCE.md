# 复算绝对评分实验

这是用户在文献门之后授权继续的复现与压力测试。问题、范围和预先判断规则见 [protocol.md](protocol.md)，题目见 [TASK.md](../../TASK.md)。[progress.md](progress.md) 记录采集状态；不要把冻结的计划数量当成已完成数量。分析器要求所有预定原始文件到齐才计算正式结果。

在仓库根目录，使用 Python 3.12 及根目录 [requirements-analysis.txt](../../requirements-analysis.txt) 中记录的数值依赖，运行：

```powershell
python research/absolute_scoring/test_analysis.py
python research/absolute_scoring/analyze_scores.py
```

本机实际 Python 为 `../130U-FinLLM/.venv/Scripts/python.exe`。绘图依赖在本机相邻 `../tmp/tail_plot_deps` 时程序会使用该目录；其他机器可在自己的环境安装所列版本，不依赖这个本机目录。最终分析默认执行 5,000 次标题配对 bootstrap，分别固定主分析和对照的种子。运行后输出到 `results/`：完整 JSON、方向性统计与边界数据 CSV，以及 `stability.png` / `stability.pdf` 六面板图。`--no-figure` 可只复算统计；不要把减少 bootstrap 次数的调试输出作为冻结协议的最终结果。

`raw_scores/{call_id}.json` 保存每次实际返回的原始 ID/整数分数。主调用 `r01_b01` 至 `r08_b25` 各含 40 个分数；对照 `c1_b01` 至 `c2_b25` 对应首轮完整批次的两次新调用。每轮 ID 覆盖、重复 JSON 键、分值范围和对照完整性均由分析器检查。`calls.jsonl` 记录配置、代理任务标识和时间；`schedule.csv` 冻结顺序，`batches.csv` 冻结批内 ID 及位置，`sample.csv` 保存来源 ID 和词法族对应关系，`control_ids.csv` 固定 100 个对照目标。

全部完成时主数据应为 8,000 个分数，对照伴随数据为 2,000 个分数。其中只有预定 100 个目标的 200 个对照分数进入主要控制比较；其余 1,800 个伴随分数保留但不扩充主样本。重复调用不会增加独立标题数。

重建输入使用 `prepare_inputs.py`、[prompt.txt](prompt.txt) 与已保存的来源测试划分。程序只使用 ID、词法族、来源 ID 和文本进行固定种子选择，不按已有标签或预测筛选；输出文本只写到仓库外相邻 `proxy-tail-absolute-inputs/`。程序拒绝覆盖已有样本和输入目录；新的完整复现实验应在新的副本中执行。输入原文没有随本轮提交，合成锚点则保存在提示中。

再次评分需要按 [agent_task_template.txt](agent_task_template.txt) 在宿主中逐次创建全新上下文代理，固定 `gpt-6-sol`、`reasoning_effort=low`、`fork_turns=none`。脚本不会自行生成任何模型分数，也不调用付费 API。宿主没有暴露温度、随机种子和精确底层模型快照，因此可以完整复算已保存结果，但不能承诺新一轮生成逐分相同。

本次实际使用的调用记录与格式校验帮助文件原样保存在 [execution/record_call.py](execution/record_call.py)。运行时它位于仓库相邻的 `proxy-tail-absolute-inputs/` 根目录，其相对路径按那个位置设计；仓库中的副本用于保留实际执行代码，不应直接在此位置运行。该文件只记录调用、保留原始字节和检查输出，不生成分数或创建评分代理。

`interim_round1.json` 是首轮完成后保存的分值分辨率阶段结果，不是八轮重测结论。它的边界统计可由主分析的首轮 `boundary_diagnostics` 重新取得。13 项合成测试验证了并列、方向、完整分数组放行、配对重采样、输入完整性与高斯边界；插值误差仅为数值检验结果，不作为严格误差证书。

`interim_m1.json` 和 `interim_m2.json` 分别是第五、六轮完成时保存的预定比较点估计，不含正式区间或公式判定；最终分析 `estimands` 中相应 m 的原始点估计应与它们一致。阶段结果没有反馈给评分代理，也没有用于更改提示或判定规则。
