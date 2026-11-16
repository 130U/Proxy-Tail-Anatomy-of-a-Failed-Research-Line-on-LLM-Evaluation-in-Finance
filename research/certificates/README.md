# 固定测试统计量检查器

离线实现P1中“共同受污染分片 → accuracy和macro-F1区间”。不训练模型、不下载数据。

```powershell
python -m research.certificates.collective research/experiments/collective_metrics/audit_example.json research/experiments/collective_metrics/audit_certificate.json --method exact
python -m research.certificates.run_examples
python -m unittest research.certificates.test_collective -v
```

`audit_example.json` 明确是人工数学例子，其审计零发现不是实测数据。输出中的概率语句**条件于**随机抽样、正确审计和历史可信核心等前提；程序只核算这些前提下的界。

## 输入

- `input_kind` 必须是 `head_predictions`。
- `votes_by_example_and_head` 是每行一个测试点、每列同一个分片头的**类别预测**，不是每类票数。列身份必须跨所有点相同。规划器 `research/planning/` 接收的是每类票数，两者不可互换。
- `labels` 是固定测试真值；`classes` 固定且至少2；平局按最小编号。
- 二选一：`budget` 是最多可改变的头数；或 `audit` 提供有限总体大小、固定抽样量、发现数与alpha，转换为文档污染上界。

完整可信核心/本地训练/稳定ID条件下，污染文档删除数可上界受影响头数。共享骨干被污染或一个修改跨两个ID时不能直接这样转换。

## 两种计算

`component`：对每个共同头集合，逐类界TP/FP，再对F1分量作保守包络。它不保证各类端点同时可达。

`exact`：动态规划联合TP与预测计数，得到所声明“选中头可自由改变全部输出”放松模型内的精确极值。它不证明某训练集能实现端点。完全精确的计数模型仍是实际重训的外放松。

两者枚举共同受影响的头集合，保留跨测试点共享约束。超过 `--max-subsets` 或 `--max-states` 时失败，不能把未搜索部分丢掉并继续出证。

数值端点同时给出精确分数与向外舍入浮点显示。全K类参与macro-F1；真支持和预测支持都为0的类贡献0。这不是按观察到的类别动态取平均。

## 统计语义

审计包装器给的是固定有限语料上、对审计随机性的覆盖率。accuracy与macro-F1由同一事件 `K_true <= K_upper` 同时得到，无需把alpha再分两份。它不是未来总体置信区间，也不是随意提前停止仍有效的审计方法。

没有在此证明真实语料权利、时间戳、解析准确性、无未来选择信息、训练确定性或主干来源。输出明确列出这些未验证前提，不能因JSON显示conditional certificate就对外声称真实无泄漏。
