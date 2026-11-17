# 任务记录

原研究路线已于 2026-11-17 收尾。下表是做过的工作及其材料入口，不是待执行路线图。各任务文件保留布置时的原文，最终判断见[首页复盘](../README.md)。

| 任务 | 实际状态 | 原任务与材料 |
|---|---|---|
| 尾部排序与成对比较 | 完成；128 条确认未通过全部预定门槛 | [完整报告](../research/tail_screening/FABLE_CURRENT_REPORT.md) |
| 绝对评分 | 完成 250 次调用；触发并列门，正式无法判断 | [原任务](absolute_scoring.md) · [报告与原始分数](../research/absolute_scoring/) |
| T1 舍入输入 | 完成范围计算与见证检查 | [任务](T1_rounding.md) · [材料](../research/t1_rounding/) |
| T1a 精度规则 | 完成推导、逐题复核及条件概率计算 | [任务](T1a_law.md) · [材料](../research/t1a_law/) |
| T1b 文档约束 | 完成加总、重复披露约束及语义筛查 | [任务](T1b_tighten.md) · [材料](../research/t1b_tighten/) |
| T1c 模型判分 | 完成 392 题独立会话与评分审计；未支持预想的判分影响 | [任务](T1c_models.md) · [材料](../research/t1c_models/) |
| T1d 精度问答 | 完成条件比较、独立复跑和第二轮语义复核 | [任务](T1d_precision.md) · [材料](../research/t1d_precision/) |
| T1e 扩展测试 | 未整体完成；前三部分暂缓，第二数据集审计转入 T1g | [原计划](T1e_full_test.md) |
| T1f 查新 | 完成五项候选的查新；保留检索边界 | [任务](T1f_novelty.md) · [材料](../research/t1f_novelty/) |
| T1g 实际后果 | 四部分审计完成；未达进入模型答题的门槛 | [任务](T1g_consequence.md) · [材料](../research/t1g_consequence/) |
| T2 数字大小 | 查重和设计审查后停止；新增评分 0 次 | [任务](T2_magnitude.md) · [记录](../research/t2_magnitude/) |
| T3 消息组合 | 评分完成；原 λ 门通过，后续因机制解释不足收束 | [任务](T3_combination.md) · [材料](../research/t3_combination/) |
| T4 跨模型尾部 | 未执行 | [原计划](T4_cross_model.md) |

跨厂商复现和真人抽查未完成。任务原文中的“并行开展”“继续”“写短文”都是当时安排，不代表项目仍在运行。原任务目录首页完整保存在[历史版本](../archive/tasks-before-closeout.md)。
