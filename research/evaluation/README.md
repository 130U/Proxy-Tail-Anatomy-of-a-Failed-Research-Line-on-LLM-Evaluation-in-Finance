# 可复现评测入口

从仓库根目录运行，依赖 Python >=3.10 和 NumPy。研究代码不读取网络、不需要旧 checkpoint，也不修改旧 Trial。

```powershell
python -m research.evaluation.reconstruct
python -m unittest research.evaluation.test_evaluate -v
```

第一条命令重建公开汇总，覆盖 `research/experiments/wp0_1/reconstruction.json`。随机数结果在相同 NumPy 版本/seed 下可复现；运行时间和硬件字段自然会不同。

对未来新实验，先冻结模型与测试集，再导出每行预测到**本地私有目录**，一行一个 JSON 对象。例如（仅示意，不是现有真实样本）：

```json
{"id":"row-1","family_id":"family-1","event_id":"event-1","target":"A","available_at":"2024-01-01T12:00:00Z","label":"neutral","prediction":"neutral","baseline_prediction":"bullish"}
```

至少需要 id、label、prediction 和 family_id/event_id 中一个。比较系统时 baseline_prediction 必须每行都有，且来自同一行。`available_at` 和 target 用于切分/去重辅助函数；不要虚构缺失时间或把缺失 event_id 自动视为独立事件。

```powershell
python -m research.evaluation.evaluate runs/private/new_predictions.jsonl runs/private/new_metrics.json --repetitions 10000 --seed 130
```

该命令输出聚合统计和输入 SHA256，不输出文本、逐条标签或预测。仍应先检查输出是否适合公开。它可在 Kaggle/Colab 的同一仓库根目录执行，不调用云服务；仅汇总本地已有的预测。

使用 `chronological_split(records, train_end, development_end)` 获得预设时间切分；`deduplicate_events(records)` 将已审定的每个 event-target 单元保留为最早视图。选择“每个事件目标一行”会改变 estimand，必须在看测试标签之前固定。应先按完整事件族切分，再在各分区按预注册规则取代表记录；不能先删除晚到视图然后把该族当作早期可得。

簇 bootstrap 估计行加权性能：每次有放回抽取与原簇数相同的整个簇；簇大小不同则重采样行数可以不同。若目标是每事件等权，需另定统计量，不能悄悄混用。

基线执行顺序：TF-IDF 在训练分区拟合词表与分类器；FinBERT 和小 LLM 固定本地权重版本、输入任务/标签映射与 prompt；使用同一独立新测试集生成预测。此交付没有 FinBERT/LLM 实际结果，不提供伪造 baseline 表。原始 SEntFiN 情感标签与此项目的作者 stance 也不能直接当同一 gold。
