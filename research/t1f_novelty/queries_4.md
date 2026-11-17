# 候选4检索词与访问记录

执行日期：2026-11-17（America/New_York）。以下为真实执行的检索；共 45 组网页检索，另有 GitHub connector 检索和数据库直接访问。查询按实际字符串保留。网页排序结果无稳定总命中数，未把返回片段数当作数据库总数；也未以搜索“无结果”证明无人做过。

| ID | 平台/方式 | 实际检索词 | 筛选/跟进结果 |
|---|---|---|---|
| 4-01 | web搜索 | `FinanceReasoning ACL 2025 financial numerical reasoning revised 15.6 FinQA` | FinanceReasoning 正式PDF、arXiv、官方仓库；发现2023 Mavi错误分析 |
| 4-02 | web搜索 | `FinQA benchmark errors annotation errors 2024 2025` | 同组召回FinanceReasoning及FinQA评测文献 |
| 4-03 | web搜索 | `FinQA 数据集 错误 标注 清洗` | 中文二手解读，继而回到FinanceReasoning原文 |
| 4-04 | web搜索（域名限定） | `site:aclanthology.org FinQA "annotation errors"` | ACL正文定位，未获得穷尽被引集合 |
| 4-05 | web搜索（域名限定） | `site:arxiv.org FinQA "error analysis" benchmark` | FinQAPT、Confidently Wrong及新近金融研究线索 |
| 4-06 | web搜索（域名限定） | `site:semanticscholar.org FinanceReasoning FinQA` | Semantic Scholar域名限检结果有限，非直接数据库检索 |
| 4-07 | web搜索（域名限定） | `site:scholar.google.com FinQA errors benchmark` | 仅出现Scholar帮助页面，无可用学术结果；随后直接查询失败 |
| 4-08 | web搜索 | `FinQA "annotation error"` | Mavi 2023错误分类；后续读取Appendix D.2 |
| 4-09 | web搜索 | `FinQA "incorrect" "ground truth"` | FinQA相关原文及公开仓库错误诊断线索 |
| 4-10 | web搜索 | `DocMath-Eval FinQA annotation errors` | DocMath-Eval原文§3.3 |
| 4-11 | web搜索 | `BizBench CodeFinQA cleaning answer` | BizBench原文Appendix A.2与§4.1 |
| 4-12 | web搜索 | `"Positive and Negative Chain-of-Thoughts" FinQA` | FinQA-fix二手线索；转期刊原文取回失败 |
| 4-13 | web搜索 | `"FinQA-fix"` | FinQA-fix二手线索 |
| 4-14 | web搜索 | `FinQA "cross-model" errors` | BizBench与跨模型评测线索；读§4.1 |
| 4-15 | web搜索（域名限定） | `site:github.com/czyssrs/FinQA/issues wrong answer` | 官方FinQA issues页及#15错误个案 |
| 4-16 | web搜索 | `"基于正负例思维链"` | SinoMed摘要索引与中文期刊题录 |
| 4-17 | web搜索 | `"FinQA-fix" 李希` | 未取回FinQA-fix一手正文 |
| 4-18 | web搜索 | `"FinQA" "近20%"` | 未核实近20%数字的一手来源 |
| 4-19 | web搜索 | `"FinanceMath" FinQA dataset annotation` | FinanceMath官方数据及原文；发现并非FinQA重标 |
| 4-20 | web搜索 | `"Retrieval-Augmented Chain-of-Thought in Semi-structured Domains" arxiv` | Mavi原文arXiv2310.14435 |
| 4-21 | web搜索 | `FinQA expert 91.16 2021` | FinQA原文91.16%专家均值 |
| 4-22 | web搜索 | `Northcutt 2021 pervasive label errors test sets 10` | Northcutt原文arXiv2103.14749 |
| 4-23 | web搜索 | `Are We Done with MMLU MMLU Redux Platinum benchmarks` | MMLU-Redux原文与Platinum线索 |
| 4-24 | web搜索 | `Platinum Benchmarks LLM simple tasks 2025 arxiv` | Platinum arXiv2502.03461 |
| 4-25 | web搜索 | `"基于正负例思维链" pdf` | 中文期刊仍未取回正文 |
| 4-26 | web搜索 | `"FinQA" "91.16"` | FinQA原论文PDF§4.3 |
| 4-27 | web搜索 | `"Platinum Benchmarks" arxiv [domain arxiv.org]` | Platinum原论文；其他同名不相关结果剔除 |
| 4-28 | web搜索 | `"基于正负例思维链的表格" "pdf"` | 未新增可核验全文 |
| 4-29 | web搜索 | `"FinQA-fix" github` | 未获得可核验FinQA-fix官方代码 |
| 4-30 | web搜索 | `"Platinum" "Vendrow" ICML 2025` | Platinum原文及2024 workshop题名变体 |
| 4-31 | web搜索 | `"Are We Done with MMLU" "NAACL"` | NAACL2025正式MMLU-Redux元数据 |
| 4-32 | web搜索 | `基于正负例思维链 表格 文本 金融 李希 中文信息学报 2025 7` | SinoMed题录；未获得全文 |
| 4-33 | web搜索（域名限定） | `site:jcip.cipsc.org.cn "FinQA"` | 域名限定未新增有效FinQA一手正文 |
| 4-34 | web搜索 | `"FinQA-fix" "20"` | 未核实20%数字 |
| 4-35 | web搜索 | `"zwxxxb_3951"` | 未取回期刊页面有效正文 |
| 4-36 | web搜索 | `"FinQA" "label errors" 2026` | 2026 Confidently Wrong、公共仓库错误分析 |
| 4-37 | web搜索 | `"FinQA" "benchmark" "saturation"` | 饱和观点线索；不将聚合榜单当原文证据 |
| 4-38 | web搜索 | `"FinQA" "same" "errors" models` | 模型同错与模型自身错误线索 |
| 4-39 | web搜索 | `"TAT-QA" "ConvFinQA" "annotation errors"` | 派生数据集及引用链扩展 |
| 4-40 | web搜索 | `"Collaborative LLM Numerical Reasoning with Local Data Protection" arxiv` | Collaborative LLM原文arXiv2504.00299 |
| 4-41 | web搜索 | `"FinQA" "annotation" "23.3"` | 检索命中23.3%，读原文后确认为MultiHiertt而非FinQA |
| 4-42 | web搜索（域名限定） | `"BizBench" site:aclanthology.org 2024` | 核实正式会议为ACL2024、元数据及共同一作排序差异 |
| 4-43 | web搜索 | `"FinQA-fix" "李希" 2025` | 仍仅有二手线索，无新增可用全文 |
| 4-44 | web搜索 | `"FINESSE-Bench" arxiv` | 根代理引用链发现后追原文，命中arXiv2605.15482v2；剔除另一篇同名FINESSE模拟器 |
| 4-45 | web搜索 | `"FINESSE-Bench" "9.33"` | 找到Table8线索，继而核作者HTML及PDF p.16 |

| ID | 其他真实操作 | 结果 |
|---|---|---|
| 4-GH1 | GitHub connector `search_issues`: `repo:czyssrs/FinQA error`, topn=30 | 返回#15参考程序错误个案及#12运行问题；未见系统不一致率。 |
| 4-GS1 | 直接打开 `https://scholar.google.com/scholar?q=FinQA+benchmark+errors` | 工具返回URL不可访问；不宣称完成Google Scholar原生检索或被引遍历。 |
| 4-SS1 | 直接打开 `https://www.semanticscholar.org/search?q=FinQA%20errors&sort=relevance` | 工具返回URL不可访问；域名限检只补充发现，不替代数据库完整检索。 |
| 4-GH2 | GitHub connector fetch作者 `data/finqa` 和官方FinQA `dataset`目录，并尝试fetch作者question.jsonl | 目录成功；4.79MB文件过大返回400，改用只读HTTP下载。逐行验证作者1147题与官方test问题同序、参考值全部等于exe_ans字符串；记录在data_identity_check.json。 |

引用链路径：FinQA→Mavi2023、BizBench、FinQAPT、Confidently Wrong；FinQA/TAT-QA→DocMath-Eval；BizBench/FinanceMath→FinanceReasoning；ConvFinQA→BizBench中的抽取任务；根代理沿ConvFinQA链发现FINESSE-Bench，本代理核原文Table8及公开题目。已跟进原文相关节和附录，不宣称穷尽三篇种子论文的全部2023年后被引文献。

正文访问与恢复：FinanceReasoning和Mavi ACL PDF首轮超时，先读作者arXiv HTML；最终通过HTTP客户端下载两份正式PDF成功，直接核对页码及版本。FinanceReasoning正式版仍列CodeFinQA795，表1合计1330/修订208，引言及附录A仍写1420。Mavi正式Table7确为印刷p.186。BizBench正式元数据为ACL2024、pp.8309–8332。FinQA-fix期刊HTTPS和HTTP都未获得正文，访问详情见candidate_4.md。Google Scholar/Semantic Scholar原生界面受限，是本轮覆盖的明确缺口。

