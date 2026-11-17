# 候选5及补充检索日志

执行日期：2026-11-17（America/New_York）。Web为通用搜索工具；带site限定不等于直接检索数据库。结果为本轮可见返回，未提供全库命中总量时不杜撰计数。下列均实际执行。

| ID | 渠道 | 完整检索词或请求 | 结果／用途 |
|---|---|---|---|
| 5-01 | Web | FinQA "answer" "exe_ans" inconsistent | 发现OpenReward一致性筛选文档 |
| 5-02 | Web | FinQA "answer" "exe_ans" cleaning | 同上，及数据schema |
| 5-03 | Web中文 | FinQA 答案 程序执行 不一致 数据清洗 | 大量无关清洗资料；不据此判不存在 |
| 5-04 | Web | FinQA "annotation errors" answer | 发现FinQA-fix二手线索，转交4组核原文 |
| 5-05 | Web | "FinQA" "exe_ans" "inconsistent" | 官方实现等邻近结果 |
| 5-06 | Web | "FinQA" "written answer" "program" | 指向EnvCommons/OpenReward |
| 5-07 | Web | "FinQA-fix" | 二手线索；原文获取由4组记录 |
| 5-08 | Web/ACL域 | site:aclanthology.org FinQA "answer" "exe_ans" | ViNumQA等字段说明，不是冲突率先例 |
| 5-09 | Web/arXiv域 | site:arxiv.org FinQA "inconsistent" "annotation" | 获得评测相关候选，非穷尽 |
| 5-10 | Web/S2域 | site:semanticscholar.org FinQA answer inconsistency cleaning | 混合无关结果，不当数据库零命中 |
| 5-11 | Web/Scholar域 | site:scholar.google.com FinQA "annotation errors" | 未获得可用数据库导出 |
| 5-12 | Web中文 | FinQA 人工答案 程序结果 矛盾 清洗 | 邻近资料与噪声 |
| 5-13 | Web | FinQA "written answer" "consistency" | EnvCommons字段一致性 |
| 5-14 | Web | FinQA "exe_ans" "filter" | OpenReward过滤规则 |
| 5-15 | Web中文 | "FinQA" "FinQA-fix" "错误" | 清洗和新近评测线索 |
| 5-16 | GitHub search_issues | repo=czyssrs/FinQA; query=answer exe_ans; topn=100 | 1条：issue #6 |
| 5-17 | GitHub search_issues | repo=czyssrs/FinQA; query=wrong OR incorrect OR inconsistency OR rounding; topn=100 | 1条：issue #15 |
| 1-PR-01 | Web | site:github.com/EnvCommons/FinQA pull rounding | 补查1的已知容差讨论，随后枚举PR |
| 1/5-PR-02 | GitHub search_prs | repo=EnvCommons/FinQA; query=""; topn=100 | 搜索返回0；随后REST枚举6个，搜索结果不能用作不存在证据 |
| 5-18 | Google Scholar直接入口 | https://scholar.google.com/scholar?q=FinQA+answer+exe_ans+inconsistency | 工具返回不可访问 |
| 5-19 | Semantic Scholar直接入口 | https://www.semanticscholar.org/search?q=FinQA%20answer%20inconsistency&sort=relevance | 工具返回不可访问 |
| 5-20 | GitHub REST完整枚举 | https://api.github.com/repos/czyssrs/FinQA/issues?state=all&per_page=100 | 15条可见issue/PR，逐条筛题；重点读6、13、15 |
| 5-21 | GitHub REST完整枚举 | https://api.github.com/repos/EnvCommons/FinQA/pulls?state=all&per_page=100 | 6个PR，重点读2、3、4、5及4的全部补丁 |
| 5-22 | GitHub REST交叉核对 | https://api.github.com/repos/EnvCommons/FinQA/issues?state=all&per_page=100 | 同6个PR，与PR枚举去重 |

扩展读取：OpenReward Tasks/Reward；EnvCommons PR4 files、merge b0e5f907abda069f0915e93e006c4ba55658360e；官方evaluate.py；FinQAPT 2410.13959（由候选4引用链发现）；Gauging Overprecision 2504.12098与Chemistry 2024（由候选3发现，根代理交叉核读）；技能来源2609.00065元数据。首次误用Chemistry ISSN路径2673-7167，未获取；纠正为2624-8549后成功，不将失败路径当来源。


## 根代理的补充引用链检索

以下实际于2026-11-17执行，不计入候选5的最低10组要求。

| 渠道 | 查询／请求 | 结果 |
|---|---|---|
| Web | `"TAT-QA" "rounding" "uncertainty"` | 多为评分约定、系统评测，未发现输入舍入审计直接先例 |
| Web | `"ConvFinQA" "annotation errors" "2024"` | 金融推理评测、数据构建方向，结合4组追引 |
| Web | `"FinQA" "condition number"` | 未定位直接先例，不作不存在证明 |
| Web | `"FinQA" "rounding" "determinacy"` | 未定位直接先例，不作不存在证明 |
| Semantic Scholar API | `/graph/v1/paper/ARXIV:2109.00122/citations?fields=title,year,url&limit=1000` | 工具不可访问；FinQA被引全集未取回 |
| Semantic Scholar API | `/graph/v1/paper/ARXIV:2105.07624/citations?fields=title,year,url&limit=1000` | 工具不可访问；TAT-QA被引全集未取回 |
| Semantic Scholar API | `/graph/v1/paper/ARXIV:2210.03849/citations?fields=title,year,url&limit=1000` | 工具不可访问；ConvFinQA被引全集未取回 |

另根代理为复核已定位原文执行find：Chemistry正文 `3.2.`、`2 out`、`10 out`；后两者不命中字面，但3.2节原文有“2 correct answers over 10 trials”及随后全10次正确。find不是独立文献检索组。

追加实际关键词：`"EEDP" "FinQA" "ConvFinQA"`；`"ConvFinQA" "TAT-QA" "error analysis" benchmark 2023 2024`。发现EEDP正式论文及FINESSE-Bench（交4组读原文）。EEDP正文find键：Precision errors、A Metadata、missing information、rounding；后两类匹配/不匹配均通过上下文阅读解释。
