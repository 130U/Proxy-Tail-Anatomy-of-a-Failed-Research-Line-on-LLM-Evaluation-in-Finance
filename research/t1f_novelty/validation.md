# 交付核验记录

日期：2026-11-17。

| 检查 | 结果与限度 |
|---|---|
| 任务范围 | 一页结论以指定7列表格开头；五条均使用指定三选一结论并给颜色、近邻、增量和把握 |
| 最接近来源 | 每条列三项原始资料及短引、章节/页码；候选5明确包含PR与issue，未冒充三篇独立论文 |
| 检索日志 | 每条均超过10组实际检索；含中文和英文；site限定、原生数据库失败、GitHub搜索与REST枚举分别记录 |
| 正文阅读 | 分组清单逐项列范围和来源层级；未取回全文单列；未将摘要或二手内容当正文 |
| 关键交叉核读 | 根代理复核XBRL§5.5、Chemistry§3.2、Gauging Overprecision的点真值、FinQAPT§4.5.1、FinanceReasoning Table1；另一个代理独立核读候选2的宽边界 |
| 版本 | FinanceReasoning正式ACL PDF仍保留1420/1330矛盾；FINESSE使用作者arXiv v2；XBRL使用2024勘误版；EnvCommons PR4固定合并SHA |
| FINESSE题目对应 | 见[data_identity_check.json](data_identity_check.json)：作者1147题与原始FinQA test同序全部匹配；参考全部匹配exe_ans。此核查只证实数据身份，未复算53模型的共同错误率 |
| 本地材料口径 | 98.4%指标已按初稿§6纠正为宽度二倍因子；未重跑本项目实验；README和论文初稿不在修改范围 |
| 引文身份 | 通过ACL、出版者、arXiv和官方规范元数据核对主要来源；短引控制在单一来源25英文词内，共用来源尽量不重复摘录 |
| DOI脚本 | 按技能运行verify_citations.py。首次中文标点抽取/Windows编码报错，改用明确DOI列表与UTF-8重跑。4个DOI注册请求均因本地代理连接被沙箱拒绝而无结果；[JSON记录](citation_verification.json)保持inconclusive，原始网页元数据人工核对另记；不把请求失败解释为DOI不存在 |
| 附件链接 | 交付前检查所有本目录Markdown相对链接；检查结果存[validation_manifest.json](validation_manifest.json) |
| 发布内容 | 仅新增research/t1f_novelty目录下的自撰报告与验证摘要；不上传他人整篇PDF、网页全文缓存、数据集副本或工作区环境日志 |

公开网页与GitHub代码是可变资源，优先提供正式论文标识、规范版本、arXiv版本和合并提交。未穷尽Google Scholar/Semantic Scholar的被引文献，也未取得FinQA-fix期刊全文；这些是查新的实质覆盖限制，不应被“颜色”掩盖。
