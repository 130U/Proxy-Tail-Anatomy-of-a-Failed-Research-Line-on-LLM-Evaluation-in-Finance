# Fable：从这里阅读本次完整交付

2026-11-16。当前方向：便宜模型在尾部漏掉什么。第一阶段和新128条确认均已真实执行完成，结果支持停止按原规则扩大到512条；四次聚合改善明显，但确认门七项通过、一项略未过。

先读[一页结论](tail_screening/FABLE_ONE_PAGE.md)，再读[完整报告](tail_screening/FABLE_CURRENT_REPORT.md)。阅读版PDF位于`tail_screening/output/pdf/`。报告明确区分原始判断、数学假设、检索判断、历史研究和未完成目标。

实际稳定性对比与判定：

- [32条第一阶段](tail_screening/stage1_conclusion.md)：成对与聚合，两模型完整比较。
- [新128条确认](tail_screening/stage2_report.md)：选中Sol四次聚合，八次新会话；结果为接近门槛的未通过。
- [独立内部AI复核](tail_screening/measurement_peer_review.md)：另一套实现重算，结果一致；不是Fable已审阅。
- [复算入口](tail_screening/REPRODUCE_CURRENT.md)：读取保存判断即可重建统计，无API或训练。

数学与先例请看[完整推导](tail_screening/theory.md)及[四支文献核验](tail_screening/literature.md)；[词法复算](tail_screening/one_page.md)与[旧agent开发结果](tail_screening/agent_result_one_page.md)保留为此前阶段。历史API计划未执行，API密钥不是本次agent测量的前置条件。

此前所有调研也保留： [九轮历史总报告](FABLE_FULL_REPORT.md)、[五条路径比较](paths/COMPARATIVE_ANALYSIS.md)及各路径全文、理论、历史实验与内部审查。旧报告中的停止状态、工作计划和原方向只适用于其当时范围，当前结论以本入口链接的报告为准。旧合并阅读版、哈希清单及打包脚本是历史材料，不覆盖本次新增内容；本轮没有新增这些流程。

本次本地交付包含64份已完成的评分输出、全部对应输入/提示/映射、两次无输出尝试的记录、机器结果、图和分析源码。保存的词法预测及源样本供复算使用。未包含虚构的20,000条或100,000条LLM实验，未估计渐近α、真实金融收益或API成本。

材料由Theodore自行转交；未发送给Fable或其他外部联系人。数学原创性、目标的经济含义及是否另立研究协议，仍需要Fable裁定。
