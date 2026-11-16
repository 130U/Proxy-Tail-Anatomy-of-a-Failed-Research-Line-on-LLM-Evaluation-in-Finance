# 固定审计量的精确前沿规划

从仓库根目录运行，只有Python标准库依赖，无网络、无训练：

```powershell
python -m research.planning.audit_frontier
python -m unittest research.planning.test_audit_frontier -v
```

第一条写出 `frontier_results.json`，全部N、m和票数均是假设设计值。重复运行会更新实际用时。`source_hashes.json`记录本次检查所用源码字节。

程序接口：

```python
from research.planning.audit_frontier import minimum_zero_audit, coverage_plan
n = minimum_zero_audit(N=1000, B=3, alpha="1/20")
plan = coverage_plan(1000, [[11,0,0],[8,2,1],[6,5,0]], q="2/3", alpha="1/20")
```

`votes[j][c]`是第j个固定测试点收到的c类票数；所有测试点必须有相同分片数与类别数。平局选最小类编号。alpha与q接受Fraction、整数或精确十进制/分数字符串，拒绝float，以避免隐含二进制近似改变严格边界。

重要契约：

- 模型、共享核心、总体内容版本、分片映射、测试点和票差、审计数量及抽样机制在审计前固定。
- 均匀无放回抽样，审计真实判定可靠；每篇污染只触及一片，共享核心不变。
- 这是**未来审计恰好发现零错标时**达到目标覆盖的最小固定n。它既不保证观察到零错标，也不预测其概率；实际总体污染数未知，不能用门概率代替成功概率。
- 若x>0，调用 `research.local.audit.audit_upper(N,n,x,alpha)` 并按实际上界重新计算覆盖；若未通过，报告失败。不得反复抽样或追加审计直到固定时点区间好看，然后仍称同一alpha保证。
- 输出覆盖是对指定投票更改机制的标签稳定比例，不是准确率，也不是统计区间一定有用。原始文档ID变更可能触及两片，必须换算片预算，不能直接调用此删除预算接口。
