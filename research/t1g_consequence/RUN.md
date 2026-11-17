# 复现 T1g

本目录在 `task/t1g` 分支，以任务提交 `ff30d61` 为起点。预测单独提交 `0c68d8a`；不要改写它或用测量结果重新校准预测。

Python 3.13 环境使用 numpy 2.5.5、scipy 1.18.1、sympy 1.14.0、matplotlib 3.11.2、tqdm 4.70.1。当前解释器位于本目录 `.venv/Scripts/python.exe`，环境和原始下载数据未提交。

只读依赖是同父目录已有工作区：`proxy-tail`（T1 `30acb8d`）、`proxy-tail-t1a`（`3b29bfe`）、`proxy-tail-t1b`（`3e6e626`）、`proxy-tail-t1c`（`c3d2a91`）、`proxy-tail-t1d`（`67569c2`）。代码使用它们的精确区间引擎、原始数据和已保存结果，没有修改前轮研究文件。其他机器须先取得这些版本与数据；T1d 尚未公开推送时，已有回答交集重算依赖其本地结果。其余四部分计算不调用任何付费 API 或模型。

TAT-QA 原始输入是 [固定官方提交](https://github.com/NExTplusplus/TAT-QA/tree/870accc41953dcde885aabeb963d94aabdc0fbc3/dataset_raw) 的 `tatqa_dataset_train.json`、`tatqa_dataset_dev.json`、`tatqa_dataset_test_gold.json`，分别放在本目录 `data/tatqa/train.json`、`dev.json`、`test.json`。FinQA 原始数据与官方评测源码在 T1 工作区 `research/t1_rounding/data/`；其下载器固定了官方提交。

从当前仓库根目录运行（令 `P` 为上面的 Python，`D` 为 `research/t1g_consequence`）：

```text
P D/tatqa_prepare.py
# 新研究必须在此单独提交预测；复现本次则检查与 0c68d8a 相同。
P D/tatqa_measure.py
P D/tatqa_binding_sensitivity.py
P D/tatqa_validate.py
P D/part1_changes.py --dataset all
P D/part1_questions.py
P D/part1_existing_responses.py
P D/part1_support.py
P D/part1_validate.py
P D/part2_comparisons.py inventory
P D/part2_comparisons.py finqa
P D/part2_comparisons.py tatqa
P D/part2_summarize.py
P D/plot_results.py
```

第四部分依次运行 `part4_duplicates.py` 和 `part4_measure.py`；扫描与语义标签说明见 `part4_report.md`。最宽词重叠候选池保存为约 2 MB 的 `part4_candidates.jsonl.gz`，可由扫描代码重建；确认的对子、实际替换、语义排除和逐项结果随分支保存。gzip 仅压缩逐行候选数据，不把未审的宽候选算作同量证据。

实测验证覆盖第一部分全部 2,839 行极值和角点、FinQA 官方评分，以及第三部分全部 5,661 程序中心与 2,339 个完整联合见证；第二部分的内点翻转见证由其汇总代码重新代入。报告中的“人工”检查均明确标为 AI 语义阅读。
