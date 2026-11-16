# 便宜模型在尾部漏掉什么：文献排重与可保留的问题

2026-11-16。针对 Fable 同日第二版方向的独立文献核查。

**当前结论是缩小主张后继续验证，尚不能宣布新颖。** 已经存在以 copula 建模不同档 LLM 置信度并优化级联的论文，也已经存在把预测分数与目标的尾依赖直接解释为极端事件预测能力的理论。SUPG 与后续语义过滤工作则已经解决了“便宜代理筛选、少量昂贵标注、达到召回目标”的阈值设计问题。因此，“把依赖引入 LLM 级联”“用尾依赖解释极端漏检”“有召回约束的代理筛选”都不能单独作为贡献。

本次已打开的相关原文中，尚未发现把**金融文本中不同档 LLM 的连续语义分数**作为对象，同时研究**固定召回率下随目标尾部比例收缩而变化的放行比例**、正负两端差异及样本外预测的完整工作。这只是有边界的检索结果；不是不存在该工作的证明。尤其是 1984 年的代理排序选拔论文尚未取得全文，排重没有完全关闭。

## 一、检索后重排：候选集大小和两个阶段的相互作用早已是研究对象

Zamani、Bendersky、Metzler、Zhuang、Wang 的 *Stochastic Retrieval-Conditioned Reranking*（ICTIR 2022）在 §3.1 描述低成本检索产生候选集、昂贵重排处理候选集的标准结构；§4 的 ECR 目标直接条件于第一阶段检索结果，分析重排噪声与候选池的关系；后续提出随机化采样和可学习截断。其关键区别是优化最终排名指标，重排器存在误差时扩大候选池还可能引入干扰，不能仅靠第一阶段 recall 判断整体收益。它没有在本文所检查的建模与方法部分提出 Laplace 条件极值下的固定召回加宽指数。我们的工作若继续，应明确只研究“参考模型的头部能否到达下一阶段”；最终答案质量、收益和重排错误是另外的对象。[作者全文，§§3–4](https://maroo.cs.umass.edu/getpdf.php?id=1452)，[DOI](https://doi.org/10.1145/3539813.3545141)。

这一分支还需要承认一个更老的数学入口：按代理排序后观察目标的 **concomitants of order statistics**。Yeo 与 David 的 *Selection through an Associated Characteristic, with Applications to the Random Effects Model*（JASA 79, 399–405, 1984）是直接排重对象。其原刊书目信息已核实；出版社正文此次返回 403，所以本文不声称已经排除它包含相同的选拔规模渐近式。不能只搜 “LLM tail dependence” 后便绕过这支文献。[原刊目录](https://www.tandfonline.com/toc/uasa20/79/386)，[原文 DOI](https://doi.org/10.1080/01621459.1984.10478063)。

同日做了最后一次定向补查：精确题名加 PDF、Iowa State 机构库及作者所属机构组合，共四个查询；另直接检查出版社公开 PDF／全文入口和 [JSTOR 原文记录](https://www.jstor.org/stable/2288282)。仍未找到可直接读取的作者／机构全文，原刊入口也没有返回正文。本次到此停止，未联系作者或绕过访问限制。**全文未取得，因而不能判断该文是否已给固定 recall 的 rare-tail screening-width law；也不能把检索到的引用或摘要视为完成排重。**

Khorrami Chokami 与 Kratz 的 *On the relation between extremal dependence and concomitants*（2023，arXiv:2301.08856）则已将极端依赖与代理排序选拔联系起来：§1 定义按一维次序配对的另一维观测，§§2–4 分析被选与未选 concomitants 的最大值，并专门研究 Gaussian 情形。其目标是两个子集最大值的联合极限，不等于固定份额召回下的最小放行比例；但它否定了“极端依赖用于代理排序”这一宽泛的新颖性说法。[原文 PDF](https://arxiv.org/pdf/2301.08856)。

## 二、人事选拔：高斯基准是旧工具，非高斯扩展也不是空白

Taylor–Russell（1939）在双变量正态模型中联系总体合格率、选拔比例、相关系数与入选者合格率。Thomas–Owen–Gunst（1977）将其扩到多个门槛。用户给出的 CRAN 页面可以核对相应双变量／多变量正态积分及反解阈值的实现；它是软件作者的说明，不能替代对原始论文的阅读。这些结果足以说明，Gaussian overlap 曲线与阈值数值反解应当作为基准复现，而不是新理论。[CRAN 作者说明](https://cran.r-project.org/web/packages/personnelSelectionUtility/vignettes/taylor-russell-and-thomas-owen-gunst.html)，[Taylor–Russell DOI](https://doi.org/10.1037/h0057079)，[Thomas–Owen–Gunst DOI](https://doi.org/10.3102/10769986002001055)。

Raju、Steinhaus、Edwards、DeLessio 的 *A Logistic Regression Model for Personnel Selection*（Applied Psychological Measurement 15(2), 139–152, 1991）已经以 logistic 回归描述成功概率并处理选拔、范围截断与效用问题，不能把“放弃双变量正态假设”本身当创新。本次出版社摘要和大学存档首页可读，完整正文获取不稳定；其模型并不能据此直接认定与尾部指数定律重复。[原刊摘要](https://journals.sagepub.com/doi/10.1177/014662169101500204)，[大学存档](https://conservancy.umn.edu/bitstream/handle/11299/114330/v15n2p139.pdf)。

这一分支对新工作的要求是：给出**随稀有度变化的规模关系和可检验误差**，而非再写一次“相关不够”或一个非高斯选拔表。还需区分总体概率中的固定召回与有限总体中 top-k 全部入选的概率，两者不应混用。

## 三、极值预测与 LLM 分数依赖：最需要收紧的新颖性边界

Heffernan–Tawn 的 *A conditional approach for multivariate extreme values*（JRSS B 66(3), 497–546, 2004）建立条件极值的规范化模型；§8.6、原刊 pp.527–528 明确推导 Gaussian 情形，在正相关条件下位置规范化为 \(\rho^2 x\)、尺度为 \(x^{1/2}\)。因此 \(\alpha=\rho^2\) 是已有结果，不是本项目发现。原文采用 Gumbel 边际；Laplace 版本的有符号表达 \(\alpha=\rho^2\operatorname{sign}(\rho)\)、\(\beta=1/2\) 可在 Kereszturi–Tawn–Jonathan（2016）的作者稿 p.10 核对。[HT 原刊 PDF，§8.6](https://www.d.umn.edu/~yqi/mydownload/heffemantawn.pdf)，[Laplace 表达作者稿](https://www.lancaster.ac.uk/~jonathan/KrsTwnJnt15.pdf)。

由这一条件分布转成放行概率，是本项目对既有模型的推论与解释。假设允许的结论究竟是 \(q_\gamma(p)=p^{\alpha+o(1)}\)、比例等价，还是带有可控余项的有限阈值公式，必须另行证明；不能将三者都写成“约等于”。Lugrin–Tawn–Davison 的 *Sub-asymptotic motivation for new conditional multivariate extreme models*（Stat 10, e401, 2021）§3.1、Theorem 1 及公式(12)–(13) 已研究 Gaussian 的有限阈值规范化修正，含 \(\log(u)/u\) 项，并展示慢收敛。笼统声称“首次给二阶修正”也不成立。[原刊全文](https://onlinelibrary.wiley.com/doi/full/10.1002/sta4.401)。

Verma–Stoev–Chen 的 *On the Optimal Prediction of Extreme Events in Heavy-Tailed Time Series With Applications to Solar Flare Forecasting*（2025 online；JTSA 47(1), 25–42）§2.1 允许报警比例与事件比例不同，§2.2、Corollary 2.1 给 Gaussian copula 的最优预测，§2.3 则将等比例报警的极限 precision 明确等同于尾依赖系数。Bobbia–Stoev 的 *On the optimal prediction of extreme events*（arXiv:2606.26270v2, 2026）§§2.2–2.3 又给出 Archimedean/Gumbel copula 下的结果，§3 在正则变差框架中研究最优极端预测。两者的主要渐近对象是等比例预测的极限 precision；这与固定 recall、可变放行比例的反问题有区别，但已经覆盖“尾依赖是极端预测能力”这一核心解释。[前者全文，§§2.1–2.3](https://arxiv.org/html/2407.11887v2)，[后者全文，§§2–3](https://arxiv.org/html/2606.26270v2)。

最接近 LLM 的已有论文是 Zellinger–Thomson 的 *Rational Tuning of LLM Cascades via Probabilistic Modeling*（arXiv:2501.09345v3, 2025）。§3.1 用 Markov 结构建模各档模型的联合置信度；§3.2 使用含原子的边际和 Gumbel copula；§4.3.2 检验 OpenAI 等模型之间的 copula 拟合。它已经做了“依赖建模→LLM 级联阈值优化”。其对象主要是回答正确性置信度，不是金融文本语义得分的极端排序；本文未在这些章节找到固定召回的稀有尾部加宽曲线。该文还报告 GPT-4o-mini 在 MMLU 验证集上有 45.7% 原始置信度恰为 1，说明 **API 提供 logprob 并不自动保证头部可严格排序**；这一数值不能外推为当前模型或金融任务的并列率。[原文，§§3.1–3.2、4.3.2及表1](https://arxiv.org/html/2501.09345v3)。

多级链条也已有条件极值理论：Papastathopoulos–Casey–Tawn 的 *Hidden tail chains and recurrence equations for dependence parameters associated with extremes of stationary higher-order Markov chains*（2024 online；Advances in Applied Probability 57(2), 407–452, 2025）研究极端状态下的规范化与依赖参数递推，§5 的 Gaussian 例子再次给出 \(\alpha_i=\rho_i^2\)。这里的平稳时间 Markov 链不自动等于非同质模型档位，但“沿链传播极端依赖”本身已有理论；跨模型乘法关系必须说明结构假设和筛选造成的条件分布变化。[原刊全文，尤其§§3–5](https://doi.org/10.1017/apr.2024.47)。

## 四、数据库代理筛选：召回目标与便宜／贵模型组合已经做过

Kang、Gan、Bailis、Hashimoto、Zaharia 的 *Approximate Selection with Guarantees using Proxies*（SUPG，PVLDB 13(11), 1990–2003, 2020）§3.2 直接给出昂贵二值 oracle、连续代理分数、抽样预算以及 precision/recall 目标；§§3.3–4 通过抽样选择代理阈值。这已经是有限总体下“网撒多宽才能达到召回”的问题，论文还讨论稀有阳性。它主要提供阈值估计算法和概率保证，并非两个连续模型分数的条件极值指数。因此可把其阈值选取思路作为直接比较对象，但不能把它改名成 LLM 筛选后算新问题。[作者原文，§§3–4](https://ddkang.github.io/papers/2020/supg-paper.pdf)，[DOI](https://doi.org/10.14778/3407790.3407804)。

Zeighami–Shankar–Parameswaran 的 *Cut Costs, Not Accuracy: LLM-Powered Data Processing with Guarantees*（BARGAIN，arXiv:2509.02896v1, 2025）将这类问题用于 LLM 数据处理。§4.2 的 recall-target 查询直接选取满足召回目标的最大代理阈值；§4.2.2 指出少阳性时均匀抽样不足，并采用 positive density 与自适应抽样。因此“低尾部样本量使召回估计困难”和“用 OpenAI 廉价/昂贵模型验证代理召回”也不是未开发领域。其二值任务设定尚不等同于随着参考模型分位数变化的连续尾部研究。[原文，§4.2、§6](https://arxiv.org/html/2509.02896v1)。

Kim–Catheland–Ailamaki 的 *Fast LLM-Based Semantic Filtering: From a Unified Framework to an Adaptive Two-Phase Method*（arXiv:2606.08090v1, 2026）§§3–6 研究 semantic predicate 的准确率约束、oracle soft confidence、代理校准与分阶段过滤；§7 给出其 oracle 概率模型下 Bayes error rate 对 oracle 调用的限制。它与预算节省和难例升级高度相关，但其二值谓词准确率目标并非贵模型最高 \(p\) 分位集合的固定召回问题。用户列出的 *Is Escalation Worth It?*（2605.06350）在 2026-10-05 的 v2 已改题为 *Is Escalation Worth It? On the Depth of LLM Cascades*：§3 研究联合分数下的级联阈值、成本和期望准确率收益，重点也不是稀有语义头部。引用时应注明所用版本。[Semantic Filtering 全文](https://arxiv.org/html/2606.08090v1)，[Cascade Depth v2 全文](https://arxiv.org/html/2605.06350v2)。

## 对 Fable 的判断

现有证据已经否决宽泛的新颖性叙述，但尚未触发“已发现同一定律与同样 LLM 测量”的完整否决条件。值得留下的最小问题是：**在预先固定的金融语义打分任务上，便宜模型筛回参考模型极端集合所需的放行率，能否由条件极值模型在独立样本上预测；两端是否有稳定且具有成本意义的差异？** 贵模型在这里是参考排序，不能称客观真值；参考排序的一致性也不能直接推出投资收益。

在数学上，仅把已有条件极值模型反演为 \(p\) 的幂次，大概率不足以独立支撑理论论文。更有分量但尚未完成的目标，是证明足够弱且可核查的条件、明确有限阈值误差如何影响固定召回预算，并展示这种预测在新数据上优于精确 Gaussian 基准及直接经验阈值。需要特别防止将 \(\alpha\) 与 Ledford–Tawn 的 \(\eta\) 或等阈值尾依赖系数 \(\chi\) 混为同一个量。

下一项最有判别力的实际工作仍是小样本分数分辨率测试和有限 \(p\) 的直接加宽曲线。若分数可用，却只有既有 Gaussian 关系的复现，就应按 Fable 的要求收束为经验规则；若出现稳定偏离，也应先检验并列、提示词、题材混合和参考模型误差，再讨论极端依赖机制。

本次检索以四支文献的原刊、作者稿和 arXiv 正文为主；重点使用 “tail dependence / conditional extremes / concomitants / retrieval-conditioned reranking / recall-target proxy selection / copula LLM cascade”等组合，并追溯最接近工作的引用。没有声称完成穷尽性系统综述。Yeo–David 原文、Taylor–Russell 原始全文以及部分大学存档的访问缺口均保留为限制，不能被“搜索未见”替代。
