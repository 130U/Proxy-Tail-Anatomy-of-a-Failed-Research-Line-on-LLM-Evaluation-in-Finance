# 32条新样本：排序方法阶段结果

本次分析范围：`all`。只读取已存输出；未调用模型、训练或联网。

所有名义尾部包含边界全部同分。gate 使用名义 p=25%；JSON 同时记录实际 A 人数、实际比例与 B/A 倍数。12.5% 仅为四条名义样本的诊断。

## pair

完整总体工作 gate：**FAIL**；全部输出可判断：True。

- luna 的两个方向、上下尾合并判定：FAIL。
- sol 的两个方向、上下尾合并判定：FAIL。

未满足的工作项：

- luna_p1__to__luna_p2，upper：q90_over_nominal_p_at_most_1_5, B_tie_expansion_at_most_0_2。
- luna_p1__to__luna_p2，lower：same_budget_recall_at_least_0_8, q90_over_nominal_p_at_most_1_5。
- luna_p2__to__luna_p1，upper：same_budget_recall_at_least_0_8, q90_over_nominal_p_at_most_1_5, A_tie_expansion_at_most_0_2。
- luna_p2__to__luna_p1，lower：same_budget_recall_at_least_0_8, q90_over_nominal_p_at_most_1_5。
- sol_p1__to__sol_p2，upper：q90_over_nominal_p_at_most_1_5。
- sol_p2__to__sol_p1，upper：q90_over_nominal_p_at_most_1_5。

| 模型/panel | 换位不一致/可比较对 | 合并零边/496 | 严格三边循环/严格三角 | U判断 |
|---|---:|---:|---:|---:|
| luna_p1 | 248/496 | 272/496 | 8/508 | 0 |
| luna_p2 | 230/496 | 266/496 | 7/543 | 0 |
| sol_p1 | 56/496 | 149/496 | 0/1964 | 0 |
| sol_p2 | 63/496 | 135/496 | 0/2125 | 0 |

## rank

完整总体工作 gate：**FAIL**；全部输出可判断：True。

- luna 的两个方向、上下尾合并判定：FAIL。
- sol 的两个方向、上下尾合并判定：PASS。

未满足的工作项：

- luna_p1__to__luna_p2，upper：q90_over_nominal_p_at_most_1_5。
- luna_p2__to__luna_p1，upper：q90_over_nominal_p_at_most_1_5。

m=1、2、4 的全部前缀结果均保留于 JSON；仅 m=4 决定本方法 gate，未挑选最有利的 m。

组合范围不是置信区间；同批判断共享上下文，重复排序不增加独立金融样本。pair 的 U 若进入零边诊断，始终保留失败身份；rank 的 U 不补造完整名次。

结果：[methods_stage1_all.json](methods_stage1_all.json)；[图](methods_stage1_all.png)。原始输入/输出在 `research/private/agent_tail_methods/stage1_n32/`。

实际 CPU 2.547 秒；wall 3.264 秒；未测峰值内存。
