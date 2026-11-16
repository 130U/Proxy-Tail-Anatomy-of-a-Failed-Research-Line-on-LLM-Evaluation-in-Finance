# Independent randomization review

## Frozen review budget (written before execution)

- Date: 2026-11-16.
- Role: internal independent AI mathematical reviewer; not Fable, not an external referee.
- Local only: no network, no outside contact, no new empirical audit data.
- Owned outputs: `research/reports/randomization_review.md`, `research/reports/randomization_review_checks.py`.
- The checker will use Python standard library only; it must not import any author kernel, optimizer, or candidate implementation.
- Exhaustive scope: all positive integer `(d,N)` with `d*N <= 10`; all `r=1,...,d`; all audit budgets `m=0,...,d*N`; every document-level audit subset and every minimal bad set (exactly one bad document in each of exactly r distinct layers).
- Separate constructive check: explicitly enumerate the randomized whole-layer strategy support and compare its maximum payoff over all minimal bad sets with the independently enumerated average-payoff lower bound. The candidate closed-form expression is only a third diagnostic, never either oracle.
- Arithmetic: integer counts and `fractions.Fraction`; no simulation, floating optimization, or tolerance-based equality.
- Hard compute budget: at most 20,000,000 payoff intersections, 120 seconds per run, and 3 checker runs. A cap breach must be recorded as incomplete, never silently truncate scope. One initial execution plus at most two corrections is allowed.
- Theory scope: fixed-size nonadaptive minimax, adaptive zero-only hard cap, and expected-budget contracts; explicitly seek counterexamples to overly broad extensions.
- Expected-budget computation: illustrative small exact distributions only, no general LP solver or unbudgeted expansion.
- Originality scope: no novelty determination is possible from this local check; finite verification cannot replace proof.

## Status

Budget frozen before execution. Review completed locally; two checker runs used, both passed. No execution cap was reached.

## Budget amendment before author-table verification

The parent requested an additional independent check of the frozen 32-row round-9 table after the first exhaustive run completed. This amendment is recorded before that check executes. Add `--verify-results PATH` to verify the exact 20 threshold, 8 conjunction, and 4 sharpness rows; compute both reported risks and preceding-budget risks using a sequential avoidance product for whole-layer selection and an independent binomial ratio for pooled sampling. Check integer minimality at alpha=1/20 and reported summaries. Do not import or call author code. Do not reoptimize the round-8 fixed-quota costs; those remain inherited evidence. This stays inside the original limit of three checker executions and 120 seconds per execution, with at most 128 additional exact risk evaluations and no expanded document enumeration.


## 独立结论

**候选闭式在精确威胁类及强制全零出证契约下成立。** 本报告给出完整证明，并以不导入作者代码的文档级整数枚举独立验证。固定整数预算的任意随机配额、逐次审计但有硬上限的程序，以及干净世界期望成本受限的程序，需要分别表述；后两者也能得到同一值函数，但推导不同。

最重要的适用条件是：

1. 所有文档与分层事前固定；每层恰有 N 篇、单篇审计成本相同；真坏集先于审计随机种子固定，不能观察本次抽样后选坏集。
2. 威胁类恰为至少 r 个层各含一篇坏文档。每个“r 个层各恰有一坏文档”的最小坏集都必须属于可行威胁类。若这是现实模型的外包络，本结论只证明相对该外包络的极小极大最优，不证明相对真实模型最优。
3. 审计反馈是正确的二元坏/好标签，且没有额外观察通道在“全零”过程中泄露未知坏集。
4. 固定区间 I 在抽样前选好；**全部所查标签为零时必须输出 I；发现任一坏文档时输出全范围。** “仅当全零才允许输出 I”不足以定义本问题：永不输出 I 的零成本程序会有零误证风险。
5. 风险指在真值不属于 I 的坏世界输出 I 的概率。对该风险的极小极大结论不自动建立真实模型区间、真实审计标签或非空现实证书。

这几项是数学问题的定义及负载条件，不是可略去的实践脚注。随机化更便宜不等于复杂优化器更有必要；本例恰好由随机选择整层的简单策略达到最优。

## 完整证明：固定大小随机审计

记文档集合为 D，分为 d 个同样大小的层。固定 1≤r≤d，0≤m≤dN。令最小坏集族 M 由所有 r 个不同层各取一篇文档组成，因此 |M|=C(d,r)N^r。对审计集合 A 及坏集 B，收益（误证指标）是 1{A∩B=空}。

令 n_h=|A∩层 h|、x_h=1−n_h/N。对在 M 上均匀的先验，固定 A 的平均风险为

    L(A) = [sum_{|S|=r} product_{h∈S}(N−n_h)]/[C(d,r)N^r]
         = e_r(x_1,...,x_d)/C(d,r).

这里没有假设审计集合按层独立随机；A 是任意固定的文档子集。对任意审计分布 P，

    max_{B∈M} E_P[1{A∩B=空}]
      ≥ E_P L(A)
      ≥ min_{|A|=m} L(A).

这是一个显式先验给出的下界，不需要交换 min 与 max，也不需要引用一般极小极大定理。

固定其余坐标后，对任意两个坐标 x,y，

    e_r(x,y,z) = e_r(z) + (x+y)e_{r−1}(z) + xy e_{r−2}(z),

其中 e_0=1，越界的 e_k=0。若 0<x≤y<1，令 ε=min(x,1−y)>0，用 x−ε、y+ε 替换 x,y。和不变，而乘积之差为 ε(x−y)−ε²≤0；由于 e_{r−2}(z)≥0，e_r 不增加。至少一个坐标到达边界，因此反复至多 d−1 次后，至多一个坐标位于 (0,1)。初始坐标在 1/N 网格上，每次替换仍在网格上，所以没有把整数配额问题放松为不可达的实数解。

令 q=floor(m/N)、t=m−qN。在 m<dN 时所得向量为 q 个 0、d−q−1 个 1，以及 1−t/N；t=0 时最后一个坐标就是 1。因此最低平均风险是

    V(m) = [C(d−q−1,r) + (1−t/N) C(d−q−1,r−1)]/C(d,r).

C(a,b)=0 用于 0≤a 且 b<0 或 b>a 的情形；m=dN 必须另行定义 V(dN)=0，不能直接让上式出现 C(−1,r)。

为达到该下界，均匀选 q 个层全查；当 t>0，再从剩余层均匀选一层，并在该层均匀选 t 篇。此分布在层置换及各层文档置换下不变，而这些置换对 M 传递，所以每个 B∈M 的漏检概率相同。其平均风险就是上述集中配额的 L(A)，故全部最小坏集风险均为 V(m)。对一般坏集 B，总能选一个 B0⊆B、B0∈M；逐点有 1{A∩B=空}≤1{A∩B0=空}，因此风险不超过 V(m)。下界和构造相等，定理闭合。

### 边界与非唯一性

- m=0 时 V=1；m=dN 时 V=0。
- r=1 时 V=1−m/(dN)。集中步骤的 e_{−1}=0，下降未必严格；集中策略不是唯一最优。所有固定 m 且每篇边际入样概率均为 m/(dN) 的分布均最优。
- d=1 时 V=1−m/N；N=1 时 V=C(d−m,r)/C(d,r)。
- r=d 时，只需完整查任意一层，即 m=N 时风险归零。
- 一般首次零风险预算为 N(d−r+1)。在更小预算下，每个确定审计集合都留下至少 r 个非普查层，存在完全漏过的最小坏集。随机化只能在坏集先固定时降低这个最坏概率。
- 若坏集在看到已抽中的集合之后才选，对所有 m<N(d−r+1) 都能选未审文档组成坏集，使条件误证风险为 1。故不能交换真坏集与随机种子的量词。

## 自适应硬上限：可拓展，须用全零路径证明

固定整个随机种子后，沿着所有查询都返回零的分支走到停止，得到一个确定的无重复审计集合 A0，大小不超过 m。对任意固定坏集 B，在真实运行中“没有发现”当且仅当 A0∩B=空：在首次命中之前，真实运行和该全零分支查询完全一致；若全零路径没有命中，真实运行就完整走完它。

强制全零出证契约因此把风险精确变为 P(A0∩B=空)。将 A0 任意填补为大小 m 的集合 A+，其漏检指标逐点不大于原指标。固定大小定理给

    sup_B P(A0∩B=空) ≥ sup_B P(A+∩B=空) ≥ V(m).

非自适应构造本就属于自适应类，故极小极大值仍是 V(m)。无需枚举完整决策树。该论证允许正发现后立即停止；若允许全零后拒绝出证，结论再次退化。

本轮没有枚举所有自适应策略树；这里给出的是数学归约。将它写成“数值验证了全部自适应策略”是不真实的。

## 期望预算：两个不同问题

对实数 b∈[0,dN]，把 V 延拓为相邻整数点间的线性插值。它实际上在每段 [qN,(q+1)N] 上线性，斜率为

    −C(d−q−1,r−1)/[N C(d,r)].

这些斜率随 q 非降，故 V 非增且凸；最后为零的区间斜率为零。

若非自适应审计集合的大小 T 随机且 E T≤b，对均匀最小坏集先验，平均风险至少 E V(T)≥V(E T)≥V(b)。对自适应程序，令 T0 是其全零路径长度。如果预算规定 E[T0]≤b，也就是完全干净世界的期望成本受限，同一归约与 Jensen 不等式给出 V(b) 下界。若预算对全部真值统一成立，它当然包含干净世界，结论也成立。

反向按适当概率混合 floor(b)、ceil(b) 两个整数预算的最优非自适应策略，期望成本正好 b，每个最小坏集风险都是 V(b)。这也满足对每个真值都相同的期望成本预算。因此干净世界预算或全真值统一预算下，允许提前停止并不改进该极小极大风险。

**不能把这一结论扩展为仅在坏世界约束期望成本。** 反例：d=1,N=2,r=1，均匀随机排序两篇，查到第一篇坏文档便停止，否则查完。任意单坏文档世界期望成本为 3/2，两篇都坏时成本为 1，所有坏世界误证风险为 0；干净世界则成本为 2。于是仅坏世界的期望预算 b=3/2 可以达到风险 0，而上面的 V(3/2)=1/4。该反例在独立脚本中逐个排列及坏集精确枚举。

## 验证范围及执行证据

独立脚本只导入 Python 标准库，不导入作者内核、优化器或风险实现。两个主要数值对象分别是：

1. 对每个 m，枚举每个文档级 A 和每个最小坏集 B，直接计数 A∩B=空，取固定 A 的均匀坏集平均风险的最小值。
2. 显式列出随机整层策略的文档集合支持，对每个最小坏集计数漏检，取最大值。

只有二者相等后，才将候选闭式作为第三个诊断值比较。没有用两个调用同一闭式的函数彼此“验证”。

首跑实际范围：所有正整数 (d,N) 满足 dN≤10，共 27 组；各组全部 r=1,...,d、m=0,...,dN，共 **87 张风险表、709 个预算问题**。生成了 7,306 个审计 mask（每个 (d,N) 只计一次）、2,583 个最小坏集 mask（跨 (d,N,r) 累计）、22,542 个构造支持动作（跨 (d,N,r,m) 累计），共执行 **3,239,464 次精确收益交叉**。709 格均有先验下界=构造最坏风险=闭式，所有 87 张独立风险表的离散斜率非降。没有触及预算上限。

附加期望预算例 d=3,N=2,r=2，等概率混合预算 2 和 3，直接枚举所得每个最小坏集风险均为 1/4、期望成本为 5/2。仅坏世界预算的反例亦按原始查询顺序枚举，不调用候选公式。

首跑观察用时 0.184557 秒；这是本机执行观察，不是算法复杂度或跨机器性能保证。未测峰值内存，未做模型训练、数据审计或现实成本测量。

复现命令（从此 worktree 根目录）：

    & '..\130U-FinLLM\.venv\Scripts\python.exe' 'research\reports\randomization_review_checks.py'

完整 709 格的规范化记录 SHA256：

    acb8af54ed68e6121e70966d099ff895200258643d7e183139b61dcd1cbc484a

脚本会打印当前自身 SHA256、计数、边界例和全部范围，便于防止把不同版本混为一份执行证据。第一次运行版本的 SHA256 为 1aacf4eab89e903784d9055c1ba995ff26884bfb8a1120bc923d3b42236d82b1；随后应父代理要求新增作者表核对接口，该旧 hash 不代表最终脚本。

## 作者 32 格结果表的独立检查

状态：最终整合后的作者表 **32/32 通过**，128 个当前/前一预算精确风险全部匹配，所有整数最小性条件通过；第二次运行同时重跑了完整709格独立文档枚举。总观察用时 0.230907 秒。实际命令：

    & '..\130U-FinLLM\.venv\Scripts\python.exe' 'research\reports\randomization_review_checks.py' --verify-results 'research\planning\randomization_results.json'

随机策略风险采用按顺序抽整层的回避乘积，再乘余下层中部分审计的条件漏检概率；pooled 风险使用原始二项系数比。逐格复核当前预算、少一篇预算和 alpha=1/20 的严格跨阈值关系。由于两种风险随预算非增，当前可行、前一预算不可行即证明整数最小性。圆整展示小数不参与判断。

此处不重新枚举第八轮固定配额最优成本。相关“收益”只独立核对表内数字的算术、范围和汇总；其固定成本本身的证据仍是第八轮报告及已有独立审查。32 格均为探索性人工结构，不能作为新确认集。

| 人工结构族 | 格数 | 比 pooled 严格节省 | 相对 pooled 的节省中位数 | 严格低于继承的 fixed-direct 下界 |
|---|---:|---:|---:|---:|
| threshold | 20 | 20 | 64/315 | 18 |
| and | 8 | 8 | 1/2 | 0 |
| sharpness bounds | 4 | 4 | 1069/4324 | 3 |

这些汇总由独立程序重新计算。必须同时保留比较器：8个 and 行虽然全部胜过 pooled，却都与“固定普查一层”的成本2打平；只报告胜过 pooled 会掩盖已知简单基线已经最优。4个 sharpness 行的固定成本仍是区间，不能把上界称为精确最优，也不能将 N=4 行的相等下界推断为真实打平。原16个 star 行不满足对称阈值结构，未被暗中计入本定理。

最大 N=32 行独立核对为：随机方案最小预算141，风险28239839/570148863；前一预算140的风险9598421/190049621，严格大于1/20。构造是4层普查加另1层抽13篇。pooled的整数最小预算是190；第八轮的192仅为可行预算，不能继续称为本轮最优值。

执行时的版本证据如下；作者结果记录的全部5个源hash与本地文件重新计算均相等。hash相等只证明版本对应，不证明数学正确。

| 文件或记录 | SHA256 |
|---|---|
| 最终独立检查脚本 | 1b6dfed3c880f0eb587327a91a37f173bc932da5deb3ef689a2de0f54e1f5cd3 |
| randomization_results.json | 90c3feb577533f39d69be92b687f0f77db3ff3cd38eb6f617a7785899c690616 |
| run_randomization.py | 702312f54f5defa628458d4c4538143eb9821995771c679d0e212168882b051d |
| randomized_audit.py | bbe16b1637e1cc805c9c81f53aca261bd3a8347076312efa7f8fde77adebfd6d |
| test_randomized_audit.py | 985595a14a716ea284b5bc40520b1704b63b90ca2d23b7a3719208e36aa125cd |
| RANDOMIZATION_PROTOCOL.md | 0dc929118dfbde182c49493201e0c34dff74dc762ac1e246f1ff4740f2e831a8 |
| 继承的 localization_results.json | 9b7f81cd51d6724838afa7b08707363c988bb4b361c64e9cac1b20d2a3f2c1d0 |

阅读作者主表生成脚本还确认：32格ID集合有完整范围检查；失败不会被当作已完成；每行保留前一预算风险；sharpness固定成本标记为非精确；两边成本的范围定义清楚。该语义阅读不包括对作者随机风险内核的逐行审计，核心正确性由本报告独立数学证明和无导入的计算比较支持。

## 证明闭合及研究地位

| 单元或风险 | 初始状态 | 独立审查结果 |
|---|---|---|
| 固定大小主张 | 提供了证明梗概 | 已在本报告展开完整下界、整数集中化及达到下界的构造；条件成立 |
| 全零只允许出证的歧义 | S1：会产生永不出证的退化程序 | 必须改为全零必须出证；本报告已显式采用该定义 |
| 整数及边界 | r=1、t=0、m=dN 需说明 | 已分别处理；不宣称唯一最优 |
| 自适应硬上限 | 不能直接把自适应集合视作事前分布 | 全零种子路径及填补归约闭合 |
| 期望成本无真值范围 | S1：不同预算契约结论不同 | 干净或全真值预算有完整凸性证明；仅坏世界预算有明确反例 |
| 实际模型只被包络 | S1：可能误称实际模型最优 | 最优性只在完整可行威胁类成立，外包络不能升级 |
| 新颖性与实用性 | 未核验 | 无网络、无外部评审；不作原创性或现实价值判断 |

证明梗概 1 处，已展开 1 处，未展开 0 处。审查状态是“给定明确契约及威胁类下，局部数学闭合”，不是形式化证明或人类外部审稿认可。本报告由内部独立 AI 审稿人撰写，**不是 Fable 的意见**。

有限检查不排除检查脚本自身错误，也不代替一般证明。精确最小坏集族的可达性、真实影响图、可靠审计真值、实际 interval 语义仍须另行建立。没有查阅外部文献，不能认定该有限对称组合结果具有新颖性；没有证明 G0/G1、实际非空证书或复杂算法必要性。


## 冻结作者全文与第九轮叙事的最终复核

在独立枚举及主表完成之后，另读作者最终完整稿 `research/theory/randomized_audit.md` 和 `research/reports/2026-11-16-round9.md`。这是文本和版本复核，没有重跑已通过的计算，没有扩大数值案例集。

- 作者理论稿 SHA256：`4fd7808a87e1712aaf1ee6f4c1f40fce2dd83f5b7f7c5ea559675cc7b981977d`。
- 第九轮报告 SHA256：`1add400b39f8a738b8766208315b58c9ac32ef9018f522829b1bf502911e96b3`。

RA1、RA2、RA3 的威胁族、全零必出证、随机种子与真值顺序、自适应反馈限制和期望预算世界均与本报告审查的命题一致。没有发现作者将外包络最优升级为真实模型最优，或把仅坏世界的期望成本例子混入主定理。

新增 RA4 的总数门最优性也成立：对所有 r 元文档坏集作均匀平均，任意固定 m 元审计集的漏检平均都是 C(dN−m,r)/C(dN,r)；全总体 SRS 对每个这样的坏集均达到该值。因而把 pooled 称为“相同随机设计能力下、总数覆盖契约的最优”有匹配下界支撑。两类程序承诺排除的坏集合不同，稿件已作区分；这不意味着对一切简单审计的优势。

第6节新增渐近附注已逐步核对：固定 alpha=1/20、r=N²、d=2r−1 时，4N 与5N的极限风险分别为1/16与1/32，线性块的交点满足余数/N趋于2/5，故结构预算/N趋于22/5。总数门的对数乘积使用 z_max=O(N⁻²)，r z_max²/(1−z_max)=O(N⁻²)趋零，风险趋于exp(−lambda/2)；再用阈值两侧的严格极限和单调性夹逼最小整数预算，得到预算/N趋于2log20。节省极限1−11/(5log20)是同一允许设计类内、不同覆盖承诺之间的常数差；作者没有将其冒称阶数收益或自然数据实证。该附注证明完整，不依赖新增数值扫描。

第九轮报告的32格范围、18/20与0/8的固定direct严格改善计数、N=32的141/190、49/190与883/1024均与已核对记录一致；合取族的零新增收益、sharp固定成本仍为界、原192仅可行、G0/G1未达、无新颖性核验和未发送Fable等边界明确保留。文中的125项测试与13条复现命令属于作者集成执行记录，本审查没有将它们冒称为自身重复执行。未发现需要修改的实质数学或科学叙事问题。
