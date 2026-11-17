# 候选 1–2 阅读清单与证据层级

检索/阅读日：2026-11-17。“正文”只说明所列章节已阅读，不把摘要、网页搜索片段或未打开的引文自动升级。每项事实的解释见 candidate_1_2.md；这里记录范围，避免重复引文。

| 题目 / 年份 | 链接 | 已读范围 | 层级 | 对应候选 |
|---|---|---|---|---|
| Gittings, Rounding errors and index numbers / 1991 | [Chicago Fed](https://www.chicagofed.org/-/media/publications/economic-perspectives/1991/ep-may-jun1991-part1-gittings-pdf.pdf) | pp.2–10，实际指数例及模拟部分 | 正文 | 1 |
| XBRL Calculations 1.1 / 2023，2024修正 | [官方规范](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22+corrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22+corrected-errata-2024-02-14.html) | §§3–5.7；重点§§5.2.3、5.5及数值例子，版本元数据与errata | 规范正文 | 1、2 |
| Hamscher & Wallis, Precision, Decimals and Units 1.0 / 2008 public working draft | [XBRL RFC](https://www.xbrl.org/rfc/pdu/pwd-2008-10-09/pdu-rfc-pwd-2008-10-09.html) | §§6–9、Appendix A部分；非全文逐段核验 | 规范讨论稿正文 | 1、2 |
| Higham, The Mathematics of Floating-Point Arithmetic / 2021 | [作者PDF](https://nhigham.com/wp-content/uploads/2021/04/high21m.pdf) | pp.35–41，尤其p.37 Theorem5和输入不确定性段 | 正文 | 1 |
| Dandekar, (In)Effectiveness of Independent Rounding of Discrete Tabular Data as Statistical Disclosure Control Strategy / 2010 | [ASA SRMS](http://www.asasrms.org/Proceedings/y2010/Files/306584_56766.pdf) | pp.1158–1164全文，附后演示页1165–1167；视觉核对p.1163 LP min/max和Table6 | 正文 | 2 |
| Salazar-González, A Unified Mathematical Programming Framework for Different Statistical Disclosure Limitation Methods / 2005 | [大学托管期刊PDF](https://www.cs.utep.edu/vladik/cs5354.10/819.pdf) | §§1–2（pp.819–821）、§5（pp.825–826）、§6；未宣称其余证明逐行审查 | 正文 | 2 |
| Zhang, Cao & Liao, XFinBench: Benchmarking LLMs in Complex Financial Problem Solving and Reasoning / 2025 | [ACL全文](https://aclanthology.org/anthology-files/pdf/findings/2025.findings-acl.457.pdf) | §§2–3、§4.4 pp.8721–8722，Figure6b及AppendixF.1 p.8735 | 正文、附录 | 1 |
| Mavi et al., Retrieval-Augmented Chain-of-Thought in Semi-structured Domains / 2023 | [ACL全文](https://aclanthology.org/anthology-files/pdf/nllp/2023.nllp-1.18.pdf) | §§3–5，尤其§5.1 p.181；AppendixA/B部分，参考文献；未完整读D.2 | 正文、附录部分 | 1 |
| Tang et al., FinanceReasoning: Benchmarking Financial Numerical Reasoning More Credible, Comprehensive and Challenging / 2025 | [arXiv HTML v1](https://arxiv.org/html/2506.05828v1) | §§2.1、4.2、AppendixB Table9；候选4分组另核数据、错误分析和附录 | 正文、附录 | 1（并与4交叉） |
| Yan, Miao & Huang, Training Autoregressive Language Models on Rounded, Bounded, and Censored Numerical Labels via Exact Likelihood / 2026-11-02 | [arXiv HTML](https://arxiv.org/html/2611.02461) | §§1–6、AppendixD/E；重点§3.2和Table1；全文内查FinQA/TAT未命中，但结论还基于实验内容阅读 | 预印本正文、附录 | 1（并与3交叉） |
| Hall, Shome & Eiers, VeriFin: A Neurosymbolic Framework for Verifying LLM-Generated Financial Claims / 2026，v3 2026-10-23 | [arXiv HTML v3](https://arxiv.org/html/2608.10213v3) | §§1–6，重点§3.6定义式、§4.1样本、§4.3 repair；没有附录 | 预印本正文 | 1、2 |
| EnvCommons/FinQA PR #2/#3 / 2026 | [PR#3](https://github.com/EnvCommons/FinQA/pull/3) | 根代理读取正文、合并状态和grader讨论，本分工不冒称独立复核全部评论 | 一手PR正文（根代理核验） | 1 |
| whileai-sdk #255, audit_grades for program verifiers / 2026检索时可见 | [Issue正文](https://github.com/LMikeH/whileai-sdk/issues/255) | connector返回整个简短issue body；没有取得其所称570任务实验的独立产物 | 一手issue中的作者自报，非已复核实验 | 1外围（与4交叉） |

## 未读正文 / 限制记录

- Higham, *Accuracy and Stability of Numerical Algorithms* 第二版（2002）：书目及“Cancellation”章节定位已查，未成功取得并读完出版社全文；数值原理核验使用上表作者2021公开原文。
- 陆骥、周莉（2010）《会计电算化报表数据自动调整方法的研究》，《中国管理信息化》4:11–15，DOI 10.3969/j.issn.1673-0194.2010.04.004：检索到转载摘要/开头，未取得完整原文。描述的是舍入报表的自动调整使其平衡，不能据此认定它计算了舍入前真值的可行域。证据层级：摘要/二手转载。
- Scholar、Semantic Scholar 原生搜索页面访问未取得结果；仅完成了站点限定网页检索。全文查新结论保留此覆盖缺口。
- FinQA、TAT-QA、ConvFinQA 的所有2023年后被引文献没有穷尽。已读后续工作只是可追溯的命中集合。
- Dandekar原站HTTPS访问超时/证书不匹配；公开原站HTTP下载成功。保存本地阅读副本和两张页图只是审读证据，不需要随GitHub报告发布整篇他人PDF。
- 这次是新颖性审查，未重跑项目的数学判定、5337题一致性或1/196恢复结果；报告中的本项目结果仍以现有任务/初稿为来源。

