# 给Fable的集中技术报告

最新补充请先读[第九轮报告](../reports/2026-11-16-round9.md)与[任意随机审计证明](../theory/randomized_audit.md)：固定层配额限制已放宽，并得到简单策略的匹配下界。以下第七轮PDF与源稿保留原历史版本，不包含第八/九轮新结果；不能仅据旧稿判断最新方法必要性。

**后续第八轮补充请先读[最新研究判断](../reports/2026-11-16-round8.md)。** 它进一步比较最强固定总数门、简单组合和更广随机抽样，缩小了本稿候选贡献的适用范围。下列PDF及两份源稿保留第七轮被审版本，没有把后续结论默默合并进旧稿。

先读中文[决策短笺](FABLE_DECISION_NOTE.md)，再读10页[英文PDF](output/pdf/audit_budgets_working_report.pdf)及[独立论文审查](../reports/paper_review.md)。完整五条路径在[比较入口](../paths/COMPARATIVE_ANALYSIS.md)。本地交付，尚未对外发送。

核心问题是固定分层审计下，认证最终统计量、单个矩形计数盒和更一般计数区域的成本有何区别。稿件纳入了能削弱原主张的简单总污染数对照，并保留全20格中位改善0的负结果。它是可反驳、可复查的内部技术稿，不是已确认原创或完成真实证书的论文。

源稿为[manuscript.md](manuscript.md)及[manuscript.tex](manuscript.tex)。[构建记录](BUILD_RECORD.md)说明源稿一致性、10页视觉检查与本地复现；PDF采用原生MathML排版，LaTeX未编译。项目G0/G1仍保持未通过，详见[完整验收审计](../reports/completion_audit.md)。
