# 集体统计量包络：实际计算结果

所有数值来源：我们的实验（构造票矩阵，非真实模型）。实际计算耗时 0.6280 秒。

| 输入 | 方法 | 逐点accuracy | 集体accuracy | 逐点macro-F1 | 集体macro-F1 |
|---|---|---|---|---|---|
| shared_budget_strict_improvement | component | [0, 1] | [1/4, 3/4] | [0, 1] | [1/5, 11/15] |
| shared_budget_strict_improvement | exact | [0, 1] | [1/4, 3/4] | [0, 1] | [1/5, 11/15] |
| component_optima_incompatible | component | [2/3, 2/3] | [2/3, 2/3] | [4/9, 2/3] | [4/9, 2/3] |
| component_optima_incompatible | exact | [2/3, 2/3] | [2/3, 2/3] | [5/9, 5/9] | [5/9, 5/9] |
| no_contamination_perfect | component | [1, 1] | [1, 1] | [1, 1] | [1, 1] |
| no_contamination_perfect | exact | [1, 1] | [1, 1] | [1, 1] | [1, 1] |
| all_heads_change | component | [0, 1] | [0, 1] | [0, 1] | [0, 1] |
| all_heads_change | exact | [0, 1] | [0, 1] | [0, 1] | [0, 1] |

第一例证明共同受影响头约束可能严格收紧界；第二例证明逐类F1分别取极值只是外包络，不能宣称联合可达。
exact指在固定集合、选定头可自由改变所有输出这一放松模型内精确；不指真实训练过程能实现每个端点。
统计量包含固定的全部K类，零支持且零预测类贡献0，不能在每次扰动后动态删去类别。
实际部署须先另行证明可信核心和共享组件不受污染改变，再由有效审计确定影响头预算。这些输入前提没有在本实验中核实。
本轮不据此通过G0或G1，不声称集体投毒证书或macro-F1优化是新理论。
状态预算或子集预算耗尽时程序拒绝输出；当前实现的指数/组合复杂度限制了大规模使用。
