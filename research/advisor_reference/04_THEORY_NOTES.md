# Theory draft: definitions, propositions and open problems

**Status of this file:** these are the advisor's **drafts**, not theorems. Each proposition is labeled with a status:

- **Draft**: the idea is clear; the constants and conditions need checking.
- **To verify**: depends on literature results from the advisor's memory.
- **Open**: the answer is not yet known.

The task of the derivation questions is to make the drafts rigorous and complete the proofs, or to give counterexamples and correct the statements. **If you find that a draft is wrong, say so directly.**

**Notation:**

- Label set $\mathcal Y=\{1,\dots,K\}$, ordered in P2.
- The model's output distribution is written $q(\cdot\mid x)$.
- $\sigma$ is the logistic function and $\Phi$ is the standard normal distribution function.

---

## T0 Certificates: definition and composition

**Definition T0.1 (certificate).** A certificate is a 4-tuple $(\varphi, A, E, V)$:

- $\varphi$: the conclusion to be proven;
- $A$: all assumptions, listed explicitly;
- $E$: the evidence (code, data, computed results);
- $V$: the checker, an executable program.

Requirement: if $V(E)=\text{accept}$, then $A\Rightarrow\varphi$ (deterministic certificate), or $\Pr[\varphi]\ge 1-\alpha$ (statistical certificate).

**Three types of certificate:**

- **Constructive certificate:** the property is guaranteed exactly by the construction of the architecture or pipeline. $E$ is code plus a proof, and $V$ is tests.
- **Bound certificate:** $E$ is a computed numerical bound, and $V$ recomputes it.
- **Statistical certificate:** $E$ is data plus a test, and the conclusion holds with probability at least $1-\alpha$.

**Proposition T0.2 (composition of a certificate chain).** Suppose the conclusion $\varphi_i$ of link $i$ holds with probability at least $1-\alpha_i$ (take $\alpha_i=0$ for deterministic links), and $\bigwedge_i\varphi_i\Rightarrow\varphi$. Then $\varphi$ holds with probability at least $1-\sum_i\alpha_i$.

*Proof:* union bound.

**Open:** when the links are correlated, is there a tighter way to compose them than the union bound? (Q30)

---

## T1 Information set (P1)

### T1.1 Definition: F_t-measurable pipeline (draft)

**Corpus.** The corpus is $\mathcal D=\{(d_i,\tau_i,\tau_i^*)\}$, where:

- $d_i$: the document content (one specific version);
- $\tau_i$: the recorded timestamp;
- $\tau_i^*$: the true availability time of this content version (unknown).

**Mislabeled set.** At cutoff $t$, the mislabeled set is

$$C_t=\{i:\ \tau_i\le t<\tau_i^*\}.$$

That is: the timestamp says before t, but the content actually became available only after t. A revised document is a new content version with its own $\tau^*$.

**Pipeline.** The pipeline $\Pi$ maps the corpus, the cutoff and independent randomness $\omega$ to parameters $\theta$. It includes **all** components: the tokenizer, data filtering and dedup models, hyperparameter selection, instruction data, label definitions, early stopping and so on.

**Definition (F_t-measurable).** $\Pi$ is called F_t-measurable at $t$ if, for any two corpora $\mathcal D_1,\mathcal D_2$ that agree on $\{i:\tau_i^*\le t\}$,

$$\Pi(\mathcal D_1,t,\omega)=\Pi(\mathcal D_2,t,\omega).$$

**Implementable version.** The true availability time $\tau^*$ is not observable, so an actual pipeline can only filter by the recorded timestamp $\tau$. A pipeline is called **measurable by record** if it depends only on $\{i:\tau_i\le t\}$.

**Proposition T1.1.** If a pipeline is measurable by record, then its difference from an F_t-measurable pipeline is exactly that it additionally uses the documents in $C_t$. It also omits documents whose timestamps are "too late", but this only loses information and causes no leakage.

So: **leakage = the effect of the mislabeled set $C_t$.** The premise is that all components are measurable by record. This premise is a constructive link, guaranteed by code audit and tests (WP1.2).

### T1.2 DP route (draft, to verify)

**Setting.** Suppose the training algorithm satisfies $(\varepsilon,\delta)$-DP with respect to adding or removing a single document. Let $\mathcal D'=\mathcal D\cup C$ with $|C|\le k$. Let the backtest statistic be $S\in[0,1]$.

**Conclusion (draft).** By group privacy,

$$\big|\mathbb E\,S(\Pi(\mathcal D'))-\mathbb E\,S(\Pi(\mathcal D))\big|\le e^{k\varepsilon}-1+k\,e^{(k-1)\varepsilon}\delta.$$

**GDP version.** If the algorithm satisfies $\mu$-GDP, then a group of $k$ documents is $k\mu$-GDP, so

$$\big|\Delta\,\mathbb E\,S\big|\le \mathrm{TV}\le 2\Phi(k\mu/2)-1.$$

**Advisor's expectation:** for this bound not to exceed 0.05, one needs $k\mu\lesssim0.125$. In pretraining a 24M-scale language model, such a $\mu$ would leave the model able to learn almost nothing. So the role of the DP route is to serve as a **baseline**.

**To verify:**

- the exact form of the $\delta$ term in group privacy;
- the derivation of the TV bound under GDP;
- the $\varepsilon$ or $\mu$ that DP language-model pretraining can actually reach on small models (Q3c).

### T1.3 Shard-aggregation certificate (draft, to verify)

**Setting (trust tiers).**

- **Trusted core** $\mathcal D_{\text{core}}$: assume $C_t\cap\mathcal D_{\text{core}}=\varnothing$. Use it to train the backbone $\theta_0$ and the tokenizer.
- **Suspect window** $W$: a hash function $h$ splits the documents into $m$ shards, $S_1,\dots,S_m$. $h$ depends only on the document id and is independent of both content and timestamp.
- **Shard heads:** $f_l=\mathcal A(\theta_0,S_l)$, where $\mathcal A$ is required to be a **deterministic** function of its input (fixed seed, deterministic operators).
- **Aggregation:** for input $z$, let $n_c(z)=\#\{l: f_l(z)=c\}$. $F(z)=\arg\max_c n_c(z)$, with ties broken toward the class with the smaller index.

**Observation.** Adding, deleting or modifying at most $k$ documents changes the heads of at most $k$ shards.

**Pointwise certificate (Levine–Feizi type).** Let $\hat c=F(z)$. If for all $c\ne\hat c$

$$n_{\hat c}(z)-n_c(z)\ \ge\ 2k+\mathbf 1[c<\hat c],$$

then $F(z)$ is unchanged under contamination of at most $k$ documents.

**Collective certificate (the form we need).** The backtest statistic is $S=\frac1n\sum_j s_j(F(z_j))$, where $s_j\in[0,1]$.

Let $R_j(k)$ be "the set of labels $z_j$ can receive after the votes of at most $k$ shards are changed". Then there is a **naive lower bound**:

$$S_{\text{low}}(k)=\frac1n\sum_j\min_{c\in R_j(k)} s_j(c).$$

It holds because the real contamination is a change to one and the same set of $k$ shards **common** to all test points, which is a special case of the pointwise worst case. The upper bound $S_{\text{high}}(k)$ is analogous.

**Tighter collective bound:** take the minimum over shard sets $K$ ($|K|\le k$). This is a combinatorial optimization that can be solved with ILP. See collective robustness certificates.

**The key direction (please check carefully).** What we want to bound is the statistic of the **leakage-free** model. The training data of the observed model $F_{\text{obs}}$ and of the leakage-free model $F_{\text{clean}}$ differ by $|C_t\cap W|$ documents, so they differ in at most that many shards. Therefore the interval $[S_{\text{low}},S_{\text{high}}]$ computed from the votes of $F_{\text{obs}}$ contains $S(F_{\text{clean}})$.

**To verify:** the exact conditions and tie rules of DPA / Finite Aggregation; the computational complexity of the collective certificate (Q29).

### T1.4 Audit resolution limit (draft; the most important and shortest derivation question)

**Setting.** From the suspect window $W$ ($|W|=N$), draw $n$ documents uniformly without replacement and manually verify their true availability times. $X$ mislabels are observed. Let the true number of mislabels in $W$ be $K^*$.

**Exact upper bound.** From the hypergeometric distribution, the one-sided $(1-\alpha)$ confidence upper bound is

$$K_u=\max\{K:\ \Pr_{\text{Hyp}(N,K,n)}[X\le x]>\alpha\}.$$

**Approximation with zero mislabels.** When $x=0$, $\Pr[X=0]=\binom{N-K}{n}/\binom Nn\approx(1-K/N)^n$, so

$$K_u\approx N\big(1-\alpha^{1/n}\big)\approx \frac{N\ln(1/\alpha)}{n}.$$

**Proposition T1.4 (draft).** To obtain any certified prediction with T1.3 at the audit upper bound $K_u$, at least $m\ge 2K_u+1$ shards are needed. So a **necessary condition** for a non-vacuous certificate is

$$n\ \gtrsim\ \frac{2N\ln(1/\alpha)}{m-1}.$$

**Numerical example ($\alpha=0.05$):**

| Suspect window size N | Audit size n | Certifiable k ≈ | Minimum number of shards m | Documents per shard |
|---:|---:|---:|---:|---:|
| 100,000 | 1,000 | 300 | 601 | about 166 |
| 10,000 | 1,000 | 30 | 61 | about 164 |
| 1,000 | 500 | 6 | 13 | about 77 |

**Corollary:** non-vacuity is determined by $N/n$. Either increase the audit size or shrink the suspect window with authoritative timestamps. The latter is the only approach that scales.

**Please complete:**

1. Write a rigorous statement, including the case $x>0$.
2. Determine whether a sequential audit (early stopping with an e-process) can improve the constant.
3. Discuss stratified sampling: stratify by source, with different mislabel rates in each stratum.
4. Fill in a table with real EDGAR counts (together with WP1.1).

### T1.5 Certificate-chain theorem (draft)

**Assumptions:**

- (A1) All components of the pipeline are measurable by record (constructive link);
- (A2) $C_t\cap\mathcal D_{\text{core}}=\varnothing$;
- (A3) Shard training is deterministic, and the hash is independent of content;
- (A4) The audit sample is drawn uniformly from $W$.

**Conclusion (draft).** With probability at least $1-\alpha$ (with respect to the audit sampling),

$$S(F_{\text{clean}})\in\big[S_{\text{low}}(K_u),\ S_{\text{high}}(K_u)\big].$$

**Optional second statistical link.** To extend "the statistic on the test set" to "the population statistic", attach a sampling confidence interval and add the failure probabilities.

**Please complete:**

1. Make it rigorous, especially the step "$F_{\text{obs}}$ and $F_{\text{clean}}$ differ in at most $K^*$ shards".
2. Explain how (A2) can be tested, or how it can also be turned into a statistical link.

### T1.6 Open problems

- If the tokenizer is trained only on the trusted core, how much compression rate is lost?
- Is choosing hyperparameters only on a validation set from before t enough for the certificate?
- Can $\mathcal D_{\text{core}}$ itself also be audited, so that assumption (A2) can be dropped?
- Can multiple cutoffs $t_1<t_2<\dots$ share computation and give certificates that are valid simultaneously?

---

## T2 Sensitivity (P2)

### T2.1 Writing permissions as specifications (draft)

**Edits.** An edit is a map $g:\mathcal X\to\mathcal X$ with a permission type $\pi(g)$. The specification for each type:

| Permission type | Specification |
|---|---|
| INV$(\eta)$: distribution-preserving | $\mathrm{TV}\big(q(\cdot\mid x),q(\cdot\mid gx)\big)\le\eta$ |
| LBL: label-preserving | $\arg\max q(\cdot\mid gx)=\arg\max q(\cdot\mid x)$ |
| REL$(a\to b,\gamma)$: relabel | $D(x,gx)\ge\gamma$, where $D$ is the log-odds difference defined in the repository |
| **UP (new)** | $q(\cdot\mid gx)\succeq_{\text{FOSD}} q(\cdot\mid x)$, i.e. for all $i$, $\sum_{j\ge i}q(j\mid gx)\ge\sum_{j\ge i}q(j\mid x)$ |
| FREE | No constraint |

**Note.** UP formalizes the repository's idea that "the label stays the same, but the confidence may change": when evidence in the same direction increases, the output distribution shifts up in first-order stochastic dominance.

**Open:** can UP + LBL fully characterize "more evidence in the same direction"? How should the neutral class be handled here? (Q9, Q31)

### T2.2 Ordered monotone head and "the model's Greeks" (draft)

**Model.** Cumulative link model:

$$\Pr(Y\le i\mid x)=\sigma(\theta_i-\eta(x)),\qquad \theta_1<\dots<\theta_{K-1}.$$

**Latent variable.**

$$\eta(x)=h(g,c)+\lambda\sum_{r\in M}g_r,$$

where:

- $g\in\mathbb R^{d}$: the features of the numeric channel (dimensionless groups); $M$ is the set of coordinates designated as monotone;
- $c$: the text-context representation, **which does not depend on the value of $g$**;
- $h$ is $\lambda$-Lipschitz in $g$ under the $\ell_1$ norm.

**Proposition T2.2 (draft).** For all $r\in M$:

1. $\partial\eta/\partial g_r\in[0,2\lambda]$.
2. If $g'\ge g$ (coordinatewise), then $q(\cdot\mid g',c)\succeq_{\text{FOSD}}q(\cdot\mid g,c)$.
3. $0\le\partial P(Y=K)/\partial g_r\le\lambda/2$ and $-\lambda/2\le\partial P(Y=1)/\partial g_r\le0$; for each intermediate class, $|\partial P(Y=i)/\partial g_r|\le\lambda/2$.

**Proof sketch.**

- (1): $h$ being $\lambda$-Lipschitz under $\ell_1$ means that the absolute value of each partial derivative is at most $\lambda$.
- (2): by (1), $\eta$ is non-decreasing in $g$; since $\sigma$ is monotone, each $\Pr(Y\le i)$ is non-increasing.
- (3): $\sigma'\le1/4$; the probability of an intermediate class is the difference of two $\sigma$ terms, so its derivative is the difference of two $\sigma'$ terms times $\partial\eta/\partial g_r$, and $\sigma'(a)-\sigma'(b)\in[-1/4,1/4]$.

**Key engineering premise:** $c$ must not depend on $g$. So the numbers in the text stream must be replaced by placeholders, and the values can enter the model only through $g$.

**Version without monotonicity.** Drop the term $\lambda\sum g_r$ and keep only the Lipschitz constraint; this gives certificates of the type "the output change caused by a numerical error $\delta$ is at most $\lambda\|\delta\|_1/4$". This applies to rounding or misparsed scale.

### T2.3 Dimensionless inputs and unit invariance (draft)

**Setting.** Numbers carry dimensions. The base dimensions include currency, time, share count and count. The group of unit transformations acts on the values: each base unit is multiplied by a positive factor, for example currency conversion or converting thousands of yuan to millions of yuan.

**Proposition.** If the numeric channel receives only dimensionless groups (monomials whose dimension exponents are all zero, such as the ratio of two quantities with the same unit), then the whole model is **exactly invariant** under unit transformations.

By the Buckingham Pi theorem (Villar et al.), every unit-invariant function can be written as a function of dimensionless groups. So within the class of "unit-invariant functions", doing this **loses no expressive power**.

**Note:**

1. **Absolute scale sometimes matters** (for example in judging materiality). In that case, normalize by a reference quantity in the same unit (total assets, market capitalization); the result is still dimensionless.
2. **Conversion between different currencies** is not a pure scale symmetry, because exchange rates vary over time. Only scale changes within one currency are exact symmetries.
3. **It must be made explicit** which quantities are treated as having the same dimension; this is itself part of the specification.

### T2.4 Entity-slot invariance (draft)

**Setting.** An anonymization map $a$ replaces the entities in the text with slots: the target entity becomes `[TGT]`, and other entities become `[E1]`, `[E2]`, .... The model is written $F=G\circ a$.

**Proposition.** For any entity renaming $\pi$ with $a(\pi x)=a(x)$, $F(\pi x)=F(x)$.

This follows directly from the construction; the proposition itself is trivial. **The research content is in two places:**

- Cost: how much accuracy is lost (compare with the anonymization literature in Q11).
- Alias recognition: $a$ must recognize all aliases of the same entity. This is a statistical link.

### T2.5 Lipschitz bound in embedding space (expected to be vacuous)

**Setting.** For length-preserving edits, write the embedding distance $r=\|E(x)-E(gx)\|$. If the logit map is $L$-Lipschitz, then $|\Delta\text{logit}|\le Lr$. For length-changing edits, this bound is undefined.

**Advisor's expectation:** on a 24M model, even with a Lipschitz transformer, the certified radius for real rewrites will be smaller than the actual distance of the rewrites. Please measure this, confirm that it is vacuous, and write down the reason clearly (Q7).

### T2.6 Open problem: whether the monotonicity specification is reasonable

**Question 1:** when the numbers have been fully extracted, metric direction degenerates into a threshold on $g$. What are the meaningful application scenarios? The advisor's candidates:

- the comparison baseline is implicit in the wording;
- the text contains only some of the numbers;
- the numbers are only one piece of evidence for a stance judgment.

**Question 2:** is "stance is monotone in numeric evidence" a reasonable specification? Counterexamples include contrarian investors and "already priced in".

Please argue under which tasks and specifications monotonicity is right, and under which it is not.

---

## T3 Deployment risk (P3)

### T3.1 Worst case for the number of errors under unknown within-cluster dependence (draft, to verify)

**Setting.**

- A batch of new samples is partitioned into clusters $c=1,\dots,C$, for example multiple views of the same event. Clusters are independent of each other.
- The error indicator of sample $i$ is $e_i\sim\text{Bernoulli}(p_i)$, with $p_i$ from the calibrated model.
- The joint distribution within a cluster is unknown.
- The total number of errors is $E=\sum_i e_i$.

**Conclusion (draft):**

1. For each cluster, with fixed marginals, the comonotone coupling $e_i=\mathbf 1\{U_c\le p_i\}$ makes the within-cluster error count $E_c$ maximal in convex order (Dhaene et al. 2002).
2. Convex order is preserved under sums of independent variables, so $E^{\text{com}}$, "comonotone within clusters and independent across clusters", is maximal in convex order.
3. Therefore, for any convex function $\phi$, the worst value of $\mathbb E\phi(E)$ is attained by $E^{\text{com}}$. In particular, the worst values of the variance, the stop-loss and $\mathrm{ES}_\beta$ (ES is consistent with convex order) can all be computed exactly by convolution.
4. VaR is **not** consistent with convex order, so the worst-case VaR is not necessarily attained by the comonotone coupling and needs separate treatment (T3.2).

**Scope.** This is **forward-looking risk at deployment time**: how large is the tail of the number of errors among the next batch of n events?

When estimating overall accuracy on a test set, if the clusters are known and there are enough of them, the cluster bootstrap already handles the unknown within-cluster dependence. WP0.1 uses the cluster bootstrap.

### T3.2 Open problems

- Is there a closed form for the worst-case VaR of a sum of Bernoullis under dependence uncertainty? What is its relation to joint mixability? (Q20)
- If $p_i$ is itself estimated, how can the estimation error also be put into the certificate?
- How should correlation between clusters (for example from the same macro event) be handled?
