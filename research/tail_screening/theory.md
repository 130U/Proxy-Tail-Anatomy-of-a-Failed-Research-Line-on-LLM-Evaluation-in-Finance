# 尾部筛选：召回目标、条件极值与高斯基准

本文讨论昂贵分数A与廉价代理B之间的尾部筛选关系，不训练模型。边际变换只用于统一尾部尺度；它保持排序，却不保持均值或实际收益。下列推导不把一阶条件极值近似写成更强的乘法等价，也不把两两尾部关系自动拼成多级结果。

## 1. 要保住什么，允许怎样筛选

先将连续A、B分别变为标准Laplace边际，其上尾为 $\Pr(A>u)=\Pr(B>u)=e^{-u}/2$，$u\ge0$。原分数含离散并列时须事先规定随机化或并列处理，不能直接声称连续公式精确适用。令 $0<p<1/2$、$u_p=\log(1/(2p))$，目标是保留A最高p比例中的固定比例 $0<\gamma<1$。

本文首先限制为B的**上尾阈值筛选**。令 $v_q=F_L^{-1}(1-q)$，定义

$$
R(p,q)=\Pr(B>v_q\mid A>u_p),\qquad
q_\gamma(p)=\inf\{q\in[0,1]:R(p,q)\ge\gamma\}.
$$

在条件分布分位点唯一且连续时，$b_\gamma(u)$ 是 $B\mid A>u$ 的 $1-\gamma$ 分位点，$q_\gamma(p)=\overline F_L(b_\gamma(u_p))$。任何筛选都满足 $q_\gamma\ge\gamma p$。这里把 $q_\gamma/p$ 称为**放行倍数**；其倒数不是召回率。在精确达到召回γ时，放行样本的精确率为 $\gamma p/q_\gamma$。

若允许任意B可测筛选区域，最省放行量的方法按 $\Pr(A>u_p\mid B=b)$ 排序。只有该函数随b单调增加时，B上尾才是全局最优区域。一般条件极值假设不提供这个单调性；高斯正相关有这个性质，负相关应改用B下尾。因此“负相关上尾筛选失效”不等于代理完全没有筛选价值。

## 2. 条件极值式实际能推出多强的渐近

概率收敛必须发生在随u变化的条件分布 $\Pr(\cdot\mid A>u)$ 下。设 $\beta<1$，在这个意义下有

$$
B=\alpha A+A^\beta Z_u+o_p(A^\beta),\qquad Z_u\Rightarrow Z,
$$

其中Z为实数值的适当极限，不含无穷质量。Laplace边际给出 $A-u\mid A>u\sim\operatorname{Exp}(1)$，故 $A/u\to1$。只要残差紧，$B/u\to\alpha$。因此当 $\alpha>0$ 时，任何固定内部召回分位点满足

$$
b_\gamma(u)/u\to\alpha,\qquad
\frac{\log q_\gamma(p)}{\log p}\to\alpha.
$$

证明只需将条件概率集中在 $(\alpha-\varepsilon)u$ 与 $(\alpha+\varepsilon)u$ 之间，再夹住分位点。它给的是 $q_\gamma=p^{\alpha+o(1)}$，**不是** $q_\gamma\sim Cp^\alpha$。α=0至多给对数比为0，放行率可趋于0、常数或1；α<0时B上尾门需要放行近全部样本，$q_\gamma\to1$，不能把负α填进上述幂律。此时反而有 $\log(1-q_\gamma)/\log p\to-\alpha$。

对 $0<\beta<1$，若Z在 $z_\gamma=G^{-1}(1-\gamma)$ 附近连续、分位点可识别，则超额 $A-u=O_p(1)$ 比 $u^\beta$ 小，给出

$$
b_\gamma(u)=\alpha u+u^\beta z_\gamma+o(u^\beta),\qquad
q_\gamma(p)=2^{\alpha-1}p^\alpha
\exp\{-z_\gamma u_p^\beta+o(u_p^\beta)\}.
$$

指数中的小o仍可发散。即使 $z_\gamma=0$，也不能将它删成 $1+o(1)$。对于α>0，存在有限正C使 $q_\gamma\sim Cp^\alpha$ 的准确条件就是分位偏移收敛：

$$
b_\gamma(u)-\alpha u\to c\in\mathbb R,
\qquad C=2^{\alpha-1}e^{-c}.
$$

常用的充分情形为β=0，且联合极限 $(A-u,Z_u)\mid A>u\Rightarrow(E,Z)$ 存在。若 $\alpha E+Z$ 的目标分位点c唯一，则上式成立；若采用HT型极限中的超额—残差独立性，应明确它是联合假设。β<0且残差紧时 $B-\alpha u\Rightarrow\alpha E$，从而α>0下 $q_\gamma\sim2^{\alpha-1}\gamma^\alpha p^\alpha$。β>0也可能有乘法等价，但须另证明目标分位误差为 $c+o(1)$，不能只依赖一阶归一化。

**无穷质量不能忽略。** 以概率π令B=A、其余概率令A与B独立，仍有Laplace边际。给定A极端，$B-A$的极限有 $1-\pi$ 质量逃向负无穷。若γ<π，则 $q_\gamma\sim(\gamma/\pi)p$；若γ>π，则 $q_\gamma\to(\gamma-\pi)/(1-\pi)$。所以拟合出α=1而不检查目标分位是否落在有限残差部分，甚至可能连相同的对数指数都无法用于所有召回目标。

### α=1、β>0仍可有无界放行倍数

固定 $0<\beta<1$，取 $S\sim\operatorname{Exp}(1)$ 及独立的 $U,V\sim\operatorname{Uniform}[0,1]$，令

$$
X=S+S^\beta U,\qquad Y=S+S^\beta V.
$$

X、Y同边际且连续。用其共同CDF变换成精确Laplace变量 $A=T(X),B=T(Y)$，其中正尾上 $T(x)=-\log(2\Pr(X>x))$。有

$$
T(x)=x-x^\beta+o(x^\beta).
$$

证明：令 $r+r^\beta=x$，则 $\Pr(X>x)\le e^{-r}$。固定任意ε>0，在 $U\ge1-\varepsilon$ 上有 $\Pr(X>x)\ge\varepsilon e^{-r_\varepsilon}$，其中 $r_\varepsilon+(1-\varepsilon)r_\varepsilon^\beta=x$。两根分别为 $x-x^\beta+o(x^\beta)$ 与 $x-(1-\varepsilon)x^\beta+o(x^\beta)$；先令x趋于无穷，再令ε趋于0，夹出该等价。

在 $A>u$ 下，$X>T^{-1}(u)=u+u^\beta+o(u^\beta)$，因此 $S\ge u+o(u^\beta)$；另一方面对任意δ>0，

$$
\Pr(S>u+\delta u^\beta\mid A>u)\le2e^{-\delta u^\beta}\to0.
$$

所以 $S=u+o_p(u^\beta)$。V不受条件事件影响，代入Y及T得到 $B=u+u^\beta(V-1)+o_p(u^\beta)$。又因 $A-u=O_p(1)$，有

$$
\frac{B-A}{A^\beta}\mid A>u\Rightarrow V-1,
\qquad
q_\gamma(p)/p=\exp\{\gamma u_p^\beta+o(u_p^\beta)\}\to\infty.
$$

这是具有真实Laplace边际、有限非退化残差的反例，不是任意拼出的不相容条件模型。α=1仅说明对数尺度相同。还需注意：α=1、β>0时Laplace边际迫使Z没有正值质量，因为 $\Pr(B>A+\varepsilon A^\beta\mid A>u)\le e^{-\varepsilon u^\beta}$；但Z完全在非正半轴上仍允许上述无界放行倍数。

## 3. 高斯copula：完整召回积分与次阶修正

令 $(X,Y)$ 为标准二元正态，相关系数ρ，A、B是各自的Laplace边际变换。**ρ是正态分数变换后的latent correlation，不是任意原始有界分数的Pearson相关。** 对连续边际，正态分数是 $\Phi^{-1}(F_A(A))$ 与 $\Phi^{-1}(F_B(B))$。以原始Pearson相关匹配的一条曲线失配，并不足以拒绝Gaussian copula。

设 $-1<\rho<1$，$\sigma=\sqrt{1-\rho^2}$，$x=\overline\Phi^{-1}(p)$、$y=\overline\Phi^{-1}(q)$。两份上尾名单的重合概率和召回率精确为

$$
J_\rho(p,q)=\int_x^\infty\phi(s)\overline\Phi\!\left(\frac{y-\rho s}{\sigma}\right)ds,
\qquad R_\rho(p,q)=J_\rho(p,q)/p.
$$

精确率为 $J_\rho(p,q)/q$；$q_\gamma$通过 $J_\rho(p,q)=\gamma p$ 唯一反解。ρ>0时，$\Pr(X>x\mid Y=y)=\overline\Phi((x-\rho y)/\sigma)$ 随y增，因此该阈值也在所有仅使用B的筛选区域中最优。

若两份名单都只取p比例，则对固定 $-1<\rho<1$，角点积分给出

$$
J_\rho(p,p)\sim\frac{(1+\rho)^2}{2\pi x^2\sqrt{1-\rho^2}}
\exp\!\left(-\frac{x^2}{1+\rho}\right).
$$

例如在二元正态密度中代入 $(s,t)=(x+a/x,x+b/x)$，主指数增量为 $-(a+b)/(1+\rho)$，积分常数为 $(1+\rho)^2$。故任何固定ρ<1的同预算上尾召回 $J(p,p)/p\to0$；高相关不等于极深尾部名单重合。

### 固定召回的完整乘法渐近，0<ρ<1

令 $z=\Phi^{-1}(1-\gamma)$，$L=\log(1/p)$。门槛在正态尺度上满足

$$
y_\gamma(p)=\rho x+\sigma z+\frac\rho x+O(x^{-2}).
$$

理由是 $D=X-x\mid X>x$ 满足 $\mathbb ED=x^{-1}+O(x^{-3})$、$\mathbb ED^2=O(x^{-2})$。条件CDF为 $\mathbb E\Phi((y-\rho x-\rho D)/\sigma)$；在 $y=\rho x+\sigma z+\rho/x$ 展开，误差为 $O(x^{-2})$，且该处密度趋于 $\phi(z)/\sigma>0$，故分位误差亦为 $O(x^{-2})$。

再用Mills比率，平方中的常数项为 $\sigma^2z^2/2+\rho^2$，得到

$$
q_\gamma(p)\sim
\frac{e^{-\rho^2-\sigma^2z^2/2}}{\rho}
(4\pi L)^{-\sigma^2/2}\,p^{\rho^2}
\exp\{-\rho\sigma z\sqrt{2L}\}.
$$

等价地，保留正态分位x时，次阶因子为 $(2\pi)^{-\sigma^2/2}x^{-\sigma^2}\exp(-\rho\sigma zx)$。$e^{-\rho^2}$ 来自条件 $X>x$ 的平均超额；把它误替成 $X=x$ 会漏掉这个常数。用 $x=\sqrt{2L}+O(\log L/\sqrt L)$ 替换线性指数只造成 $1+o(1)$ 的相对误差。

因此高斯copula确有 $\log q_\gamma/\log p\to\rho^2$，但一般没有有限正C使 $q_\gamma\sim Cp^{\rho^2}$。γ>1/2时z<0，存在增大的 $\exp(c\sqrt L)$ 修正；γ=1/2时该修正消失，仍有 $L^{-\sigma^2/2}$。对于任何固定 $0<\rho<1$，$q_\gamma/p\to\infty$：幂项 $p^{-(1-\rho^2)}$ 最终压过这些次阶项。“接近高斯且高相关就只需固定倍数”至多是有限p窗口内的经验近似。

HT2004原文§8.6及表1给出正相关高斯的中心项 $\rho^2u$、尺度 $u^{1/2}$；其原文使用Gumbel边际。Laplace正尾与Gumbel只差常数，故这里仍有α=ρ²、β=1/2，并且

$$
\frac{B-\rho^2A}{\sqrt A}\mid A>u
\Rightarrow N\bigl(0,2\rho^2(1-\rho^2)\bigr).
$$

残差尺度含 $\sqrt2$，不能遗漏；α也不是同阈值联合尾指数中的 $\eta=(1+\rho)/2$。[HT2004原文§8.6](https://www.d.umn.edu/~yqi/mydownload/heffemantawn.pdf)

有限阈值修正已有明确先例：Lugrin、Tawn与Davison（2021）§3.1定理1直接研究Laplace边际高斯copula，给出有符号中心 $\operatorname{sign}(\rho)\rho^2x$、上述残差方差及更精细的归一化，式（12）—（13）讨论有限阈值下的有效参数偏移。本文固定召回的分位展开服务于筛选问题，不能仅因改写成放行成本就宣称新的条件极值理论；有限范围的斜率也不自动等于结构α。[原文§3.1](https://onlinelibrary.wiley.com/doi/full/10.1002/sta4.401)

### 零相关、负相关与完美相关

ρ=0时独立，所有p都有 $q_\gamma=\gamma$。固定 $-1<\rho<0$ 时仍有同一 $y_\gamma=\rho x+\sigma z+\rho/x+O(x^{-2})$，但它趋于负无穷，所以B上尾放行 $q_\gamma\to1$。更精确地，令 $a=|\rho|$，则

$$
1-q_\gamma(p)\sim
\frac{e^{-a^2-\sigma^2z^2/2}}{a}
(4\pi L)^{-\sigma^2/2}p^{a^2}
\exp\{a\sigma z\sqrt{2L}\}.
$$

负相关的Laplace条件中心为 $-\rho^2A$，不是 $+\rho^2A$。改用−B筛选后，其成本就是正相关|ρ|的情形。端点须单列：ρ=1时 $q_\gamma=\gamma p$；ρ=−1时对于B上尾 $q_\gamma=1-(1-\gamma)p$。这些端点不能从固定 $0<|\rho|<1$ 的式子直接代入，两个极限不一致。

## 4. 多级筛选：α相乘需要共同条件结构

假设昂贵到廉价的变量为 $A_0,A_1,\ldots,A_k$。两两拟合 $A_j\approx\alpha_jA_{j-1}$ 不足以推出端点指数 $\prod_j\alpha_j$，因为 $A_0$ 极端挑出的中间样本，可能不同于单独令 $A_{j-1}$ 极端时的样本。

反例已存在于三元高斯：$\rho_{01}=\rho_{12}=1/2$、$\rho_{02}=0$ 的相关矩阵正定。相邻两对Laplace α均为1/4，乘积为1/16，但端点独立，α为0。在这个例子里并非估计误差，而是两两结构本来就没有指定三元关系。

一个足够的联合条件是，在同一个 $A_0>u$ 条件下，对所有j都有

$$
A_j-\alpha_jA_{j-1}=o_p(u),\qquad \alpha_j>0.
$$

有限次递推立即给 $A_k/u\to\prod_j\alpha_j$，再由端点分位夹逼得到对数筛选指数。更可解释的充分条件是Markov链 $A_0\to A_1\to\cdots\to A_k$，各转移核在 $y\to\infty$ 时满足 $\Pr(|A_j/y-\alpha_j|>\varepsilon\mid A_{j-1}=y)\to0$，并对所用大y版本有效。Markov性使选中 $A_0>u$ 不再改变给定中间值的转移核，才能逐步传递。高斯Markov链有 $\rho_{02}=\rho_{01}\rho_{12}$，所以正相关时才对应α相乘。

这仍只给端点的对数阶。乘法常数、次阶损失和每级门槛需要共同残差极限及足够精细的分位误差控制。串联门的总召回精确等于各级**条件于真正A高尾且之前已通过**的召回之积；把每对变量单独测得的召回相乘，通常没有这种含义。整体放行量同样是门事件交集概率，不能无条件相乘。

## 5. MES与“代理行权为负”必须对应不同payoff

此处回到实际效用/收益分数 $\widetilde A,\widetilde B$，假设期望存在。Laplace化只保持排序，不能用其均值代替原量纲收益。按上尾约定定义

$$
\operatorname{MES}_{A\mid B}(q)=\mathbb E[\widetilde A\mid\widetilde B>b_q].
$$

这不是 $\mathbb E[\widetilde B\mid\widetilde A>a_p]$；二者条件方向不同。金融损失或负收益文献可能采用下尾及相反符号，应先声明约定。MES衡量入选样本的平均价值，不等同于目标高尾的召回率。

若代理超过门槛就必须付K换取实际收益，策略价值可定义为

$$
V_{\rm proxy}(K,b)=\mathbb E[(\widetilde A-K)\mathbf1\{\widetilde B>b\}]
=\Pr(\widetilde B>b)\{\operatorname{MES}_{A\mid B}-K\}.
$$

这个强制代理决策价值可以为负。真正看见A后才行权的价值为 $V_{\rm oracle}(K)=\mathbb E[(\widetilde A-K)_+]\ge0$，而

$$
V_{\rm oracle}-V_{\rm proxy}
=\mathbb E[(\widetilde A-K)_+\mathbf1\{\widetilde B\le b\}]
+\mathbb E[(K-\widetilde A)_+\mathbf1\{\widetilde B>b\}]\ge0.
$$

两个非负项分别是漏掉高价值和误选低价值的损失。$\mathbb E[(\widetilde A-K)_+]$、$(\mathbb E\widetilde A-K)_+$ 及 $\mathbb E[(\mathbb E[\widetilde A\mid\widetilde B]-K)_+]$ 本身都不会为负；扣除价格或评估成本之后的净收益则另当别论。不能把负代理策略价值写成“真实期权价值为负”。

原始标准正态X、Y下，$\mathbb E[X\mid Y>y]=\rho\phi(y)/\overline\Phi(y)$。例如K=x且B也只取top-p，$V_{\rm proxy}=\rho\phi(x)-xp$；Mills比率使它为 $p\{(\rho-1)x+\rho/x+O(x^{-3})\}$，对任何固定ρ<1最终为负。这说明代理触发的买入规则可能赔钱，不违反正部payoff的非负性，也不证明所有按B最优决策都无价值。

## 来源与本文推导的边界

- Heffernan, J. E. & Tawn, J. A. (2004), *A conditional approach for multivariate extreme values*, JRSS B 66(3), 497–546。已读取原文§8.6、表1及条件模型部分；高斯α、β及残差协方差据此核对。[原文PDF](https://www.d.umn.edu/~yqi/mydownload/heffemantawn.pdf)；[DOI](https://doi.org/10.1111/j.1467-9868.2004.02050.x)。
- Keef, C., Papastathopoulos, I. & Tawn, J. A. (2013), *Estimation of the conditional distribution of a multivariate variable given that one of its components is large: Additional constraints for the Heffernan and Tawn model*, Journal of Multivariate Analysis 115, 396–404。[DOI](https://doi.org/10.1016/j.jmva.2012.10.012)；[作者机构条目](https://research.lancaster-university.uk/en/publications/estimation-of-the-conditional-distribution-of-a-vector-variable-g/)。本次核对了元数据及摘要；出版社全文请求403，未声称已读该文全部约束。
- Rohrbeck, C. & Tawn, J. A., *Some benefits of standardisation for conditional extremes*，作者公开稿§1–2明确重述Keef的Laplace框架及联合超额极限，也提醒标准化与条件模型的限制。[作者稿](https://eprints.lancs.ac.uk/id/document/119955)。这是作者原稿中的说明，不冒充Keef原文已获取。
- Lugrin, T., Tawn, J. A. & Davison, A. C. (2021), *Sub-asymptotic motivation for new conditional multivariate extreme models*, Stat 10(1), e401。已读取开放原文§3.1及定理1，核对高斯的Laplace归一化与有限阈值修正。[原文与DOI](https://onlinelibrary.wiley.com/doi/full/10.1002/sta4.401)。

本报告的固定召回完整高斯展开、反例和多级条件均在正文给出推导；不据此宣称首次发现。实证上应检验的是预定p与γ范围内的实际重合、召回、放行成本和效用，而不是仅凭总体相关系数或一个拟合α宣布廉价代理可靠。
