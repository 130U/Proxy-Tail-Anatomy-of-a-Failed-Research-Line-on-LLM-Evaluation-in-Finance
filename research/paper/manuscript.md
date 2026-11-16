# Audit Budgets for Conditional Financial-Model Certificates

Prepared for Theodore and Fable, internal working draft  
16 November 2026

## Abstract

We study a mathematical component of a proposed certificate chain for financial text models: the fixed stratified audit needed to certify a prescribed interval for a fixed evaluation statistic. Document contamination affects a declared set of prediction heads. We express the worst probability of issuing an incorrect zero-finding certificate through an antichain of minimally harmful contamination profiles. We compare direct certification of the final statistic with the strongest rectangular count-certificate procedure that reports only after jointly observing zero findings. Its exact risk is a maximum of stratum risks, rather than their Bonferroni sum. A threshold influence family admits exact optimization by symmetry and an asymptotic separation between these two procedure classes. A simple total-count certificate already attains the balanced separation; general nonrectangular count sets reproduce direct testing. Constructed experiments include a case requiring 88 rather than 114 audits, but nine of twenty frozen cases improve, eleven do not, and the full-grid median saving is zero. Separate real-text sentiment baselines provide research context, not validation of the audit theorem. Historical provenance, meaningful task utility, and natural-language semantic coverage remain external obligations. No real historical certificate is established. Novelty is unresolved: this offline working report combines established robustness and finite-population testing ideas, and the available literature review is incomplete.

## 1. Research question and claim boundary

The motivating objective is an interval containing the evaluation statistic of a clean comparator model. Such a comparator deletes ineligible document versions and reruns a fixed training procedure. The desired interval resembles a verified price bound in financial mathematics, but its endpoints depend on a chain of obligations: provenance, contamination assessment, dependence tracking, and propagation to the statistic. A correct last step does not repair an unsupported first step.

This report isolates one question. Given fixed document-to-head influences, observed votes, evaluation labels, and a target interval, how much fixed stratified auditing suffices when the audit finds no contaminated documents? The question concerns a finite evaluation statistic, not expected investment returns, future population accuracy, or the conditional probability that a particular document is clean. All probabilities below concern the specified random audit, with the contamination configuration held fixed.

Two output contracts differ. A direct procedure promises only that the final statistic lies in its announced interval. A rectangular procedure additionally promises that every stratum's contamination count lies in a simultaneous rectangular confidence set. The latter may certify information unnecessary for the final conclusion. We characterize this additional cost within a precise procedure class, including a family in which the ratio grows with the number of heads.

These results are mathematical components and constructed examples. They do not establish that the distinction is new, that financial corpora exhibit the favorable structures, or that training a language model from random initialization is necessary. The main optimization excludes adaptive audits, unequal inclusion probabilities within strata, and randomized allocations. A broader audit method may outperform both procedures considered here.

## 2. Relationship to existing methods

Deep Partition Aggregation (DPA; L02) already connects deterministic partitions and vote margins to poisoning robustness. Finite Aggregation (L03) extends the dependence structure through overlapping training subsets. Collective bagging certificates (L04) explicitly exploit the fact that the same poisoning action affects multiple predictions. Our influence relation and shared-head relaxation belong to this existing line of reasoning. A domain change to financial documents does not itself create a new robustness principle.

The audit component also has substantial precedent. L08 constructs confidence sequences for sampling without replacement. L09 studies weighted financial auditing with test martingales and auxiliary information. This report uses the simpler fixed-allocation, zero-finding setting. It neither introduces sequential validity nor claims that direct tests of composite harmful hypotheses are a new statistical idea.

The available local review inspected the full texts recorded under L02--L04 and L08--L09, but did not exhaust later citations or establish priority for the specific optimization developed here. Bibliographic entries retain those ledger identifiers; incomplete metadata are explicitly marked. The contribution claimed in this draft is a self-contained interface, proofs, exact implementations, and an explicit comparison boundary. Originality remains a research question requiring a more complete comparison with auditing and robustness literature.

## 3. Model, audit, and comparator assumptions

Let a finite set of document versions be partitioned into disjoint strata:
$$
W=\bigsqcup_{h=1}^{d}W_h,\qquad |W_h|=N_h\ge1.
$$
The unknown contamination set is a fixed subset $C^*\subseteq W$. Before sampling, choose integers $0\le n_h\le N_h$. Independently across strata, sample $n_h$ documents uniformly without replacement. Every sampled document must be correctly classified as contaminated or clean. An unresolvable historical version is not a verified clean observation. Costs are fixed positive values $c_h$ per audited document, giving total cost $\sum_h c_hn_h$.

There are $m$ prediction heads and $J\ge1$ fixed evaluation points. For $K\ge2$ classes numbered $0,\ldots,K-1$, the observed vote matrix is $V\in\{0,\ldots,K-1\}^{J\times m}$ and the fixed truth vector is $y$. Equal-weight plurality selects the smallest class index on a tie. Each document $i$ has a declared influence set $H_i\subseteq\{1,\ldots,m\}$, and
$$
B(C)=\bigcup_{i\in C}H_i.
$$

The essential structural assumption is simultaneous: for every allowed deletion set $C$, rerunning the fixed procedure with fixed randomness leaves all heads outside $B(C)$ unchanged. Single-document ablations cannot establish it. For example, an output equal to the OR of two present-document indicators survives either single deletion but changes after both deletions.

A sufficient construction is a fixed directed acyclic dependency graph. Inputs corresponding to deleted documents may change; every other node is a fixed function of its parents and fixed external randomness. Topological induction shows that nodes not reachable from the changed inputs retain their values. Thus $H_i$ may contain all heads reachable from document $i$. Shared tokenizers, normalization, model selection, and mutable partition identities must appear in this graph. A contaminated shared encoder may affect every head.

For certification, allow every head in $B$ to output arbitrary classes independently at each evaluation point, including retaining its original output. Heads outside $B$ remain fixed. This relaxation contains the actual clean comparator under the structural assumption. It may admit prediction tables that no retrained model can realize, including inconsistent outputs on duplicate inputs.

Let $\mathcal Z(B)$ be this finite prediction set and let $S:\mathcal Z\to[0,1]$ be a fixed statistic. Define
$$
A(B)=\left[\min_{z\in\mathcal Z(B)}S(z),\ \max_{z\in\mathcal Z(B)}S(z)\right].
$$
Freeze a target closed interval $I=[\ell,u]$, an audit error level $\alpha\in(0,1)$, the data identities, votes, labels, influences, and costs before auditing. They may depend on information available before sampling, provided the stated sampling distribution remains valid conditional on that information.

## 4. Exact statistic envelopes and harmful configurations

For a fixed affected set $B$, let $b=|B|$ and let $u_{jk}(B)$ count unchanged votes for class $k$ at point $j$. The reachable classes are exactly
$$
R_j(B)=\left\{k:\ u_{jk}(B)+b\ge u_{ja}(B)+\mathbf1\{a<k\}
\quad\text{for every }a\ne k\right\}.
$$

To prove necessity, a candidate winner receives at most $u_{jk}+b$ votes, while a rival receives at least its unchanged count. A lower-index rival requires a strict integer advantage. For sufficiency, assign every affected vote to the candidate winner. Across points, the relaxation permits these assignments simultaneously.

Consequently, fixed-set accuracy has exact endpoints
$$
L_{\rm acc}(B)=\frac1J\sum_j\mathbf1\{R_j(B)=\{y_j\}\},\qquad
U_{\rm acc}(B)=\frac1J\sum_j\mathbf1\{y_j\in R_j(B)\}.
$$
Each point can attain its worst or best correctness value simultaneously. This argument is specific to an additive statistic. Macro-F1 requires joint confusion-count optimization or a separately proved outer bound; summing individually optimal class contributions need not be jointly attainable.

Define the harmful configuration family
$$
\mathcal H_I=\{C\subseteq W:A(B(C))\not\subseteq I\}.
$$
It is upward closed. Indeed, enlarging $C$ enlarges $B(C)$, and newly affected heads can retain their old votes. The feasible prediction set therefore expands. Any previously feasible statistic outside $I$ remains feasible.

A sound but nonmonotone numerical outer envelope does not automatically support this pruning argument. One must use a proven monotone envelope, take its monotone hull, or avoid monotonicity-based pruning. Throughout the exact results, harmfulness refers to the stated relaxed output set, not an unverified claim about all actual retraining outcomes.

## 5. Direct zero-finding certification and antichain reduction

Write $q_h(C)=|C\cap W_h|$ and adopt $\binom ab=0$ when $b>a$. Define
$$
p_h(q;n_h)=\frac{\binom{N_h-q}{n_h}}{\binom{N_h}{n_h}},
\qquad
p_n(q)=\prod_{h=1}^{d}p_h(q_h;n_h).
$$
The probability of finding no contaminated document is exactly $p_n(q(C))$. The numerator counts samples avoiding contamination; independence gives the product. This probability is nonincreasing in each contamination count and each sample size.

**Theorem 1: exact harmful-profile risk.** Let $\mathcal M_I$ be the inclusion-minimal elements of $\mathcal H_I$. Form their count vectors, remove duplicates, and retain only the coordinatewise minimal vectors, denoted $Q_{\min}$. Then
$$
R_I(n):=\max_{C\in\mathcal H_I}p_n(q(C))
=\max_{M\in\mathcal M_I}p_n(q(M))
=\max_{q\in Q_{\min}}p_n(q).
$$
The maximum over an empty harmful family is zero. If $R_I(n)\le\alpha$, the procedure reporting $I$ after jointly observing zero findings, and otherwise reporting $[0,1]$, covers the actual clean-comparator statistic with probability at least $1-\alpha$.

**Proof.** Every harmful finite set contains an inclusion-minimal harmful subset. Its count vector is coordinatewise no larger, hence its miss probability is no smaller. Conversely, minimal harmful sets are members of the original family. This proves the first reduction. Every vector in the finite count family dominates a coordinatewise minimal vector; the same probability monotonicity proves the second.

Fix the actual contamination set. If its clean statistic lies outside $I$, the structural relaxation implies that this set belongs to $\mathcal H_I$. Incorrect reporting then requires the all-zero event, whose probability is at most $R_I(n)$. Otherwise neither possible reported interval misses the statistic. The statement holds for every fixed contamination set. This is unconditional coverage over audit sampling, not a posterior probability given observed zero findings. End of proof.

The reduction of the maximum itself only needs finiteness and probability monotonicity. Upward closure additionally permits identifying minimal harmful sets by checking their single-element deletions. A count vector records that at least one harmful location configuration has those counts; it does not assert that every arrangement with those counts is harmful.

If every document in a stratum has the same influence set, only contamination presence in that stratum matters. A minimal harmful configuration then contains at most one document per stratum. Enumerating $2^d$ presence patterns replaces enumerating $2^{|W|}$ document subsets. If the empty configuration is harmful, no design can pass for $\alpha<1$: its zero-finding probability is one.

## 6. The strongest joint-zero rectangular comparator

A rectangular procedure has an additional obligation. On the all-zero event it reports a count box
$$
[0,b]=\{q:0\le q_h\le b_h\},\qquad b_h\in\{0,\ldots,N_h\},
$$
and otherwise reports the full count space. The box is safe when every document configuration with counts in it has its statistic envelope inside $I$. By Theorem 1, safety is equivalent to the absence of $q\in Q_{\min}$ satisfying $q\le b$.

**Theorem 2: exact box risk.** The worst probability that the reported box excludes the true count vector is
$$
R_{\rm box}(n,b)=\max_{h:b_h<N_h}p_h(b_h+1;n_h),
$$
with value zero if the index set is empty.

**Proof.** Any count vector outside the box exceeds at least one coordinate bound. Its all-zero probability is at most the miss probability for $b_h+1$ contaminated documents in that coordinate, and hence at most the displayed maximum. Conversely, choose a maximizing coordinate, place exactly $b_h+1$ contaminated documents there, and place none elsewhere. This configuration attains that probability and lies outside the box. It need not be harmful for the final statistic, because the comparator promises coverage of the count box itself. End of proof.

The strongest comparator in this class optimizes both a safe $b$ and the fixed allocation $n$, subject to $R_{\rm box}\le\alpha$. Using a Bonferroni sum instead would impose an unnecessarily weak baseline. Optimizing a continuous allocation of individual error budgets does not remove that difference: it still requires the sum of the individual risks to be at most $\alpha$.

Every safe box places all harmful configurations outside it. Therefore $R_I(n)\le R_{\rm box}(n,b)$, and the optimal direct cost cannot exceed the optimal box cost. If a proposed rectangle method abandons coverage of its intermediate box and calibrates only the final interval, it belongs to the broader direct-testing contract. The theorem does not claim superiority over that larger class.

**Proposition: general count sets reproduce direct testing.** Define the safe downset
$$
D=\left\{q\in\prod_h\{0,\ldots,N_h\}:\ \text{no }a\in Q_{\min}\text{ satisfies }a\le q\right\}.
$$
Reporting $D$ on zero findings and the full count space otherwise has exact count-coverage error $R_I(n)$.

**Proof.** For counts in $D$, every location configuration is safe, by Theorem 1. Outside $D$, a minimal harmful profile $a$ satisfies $a\le q$. Extend a realizing harmful set within each stratum until its counts equal $q$; upward closure preserves harmfulness. Thus every outside vector is realized by a harmful configuration, and the worst count-coverage error is $\max_{q\notin D}p_n(q)=R_I(n)$. End of proof.

The distinction is therefore a restriction to a single predetermined safe rectangle, not superiority over general count-confidence sets. The downset can still require exponential representation or optimization.

## 7. A threshold family with a growing cost separation

Take $r\ge2$, $d=m=2r-1$, and $N$ documents in every stratum. Every document in stratum $h$ affects only head $h$. At every evaluation point all heads initially predict its true class. Any number of evaluation points is allowed; the executed construction uses one point with label zero. Costs equal one and $I=[9/10,1]$.

**Theorem 3: threshold structure and costs.** A configuration is harmful exactly when at least $r$ strata contain contamination. Thus
$$
R_I(n)=\max_{|T|=r}\prod_{h\in T}(1-n_h/N).
$$
A balanced allocation is feasible with
$$
n_h=n_\star=\left\lceil N(1-\alpha^{1/r})\right\rceil.
$$
The exact optimal joint-zero safe-box cost is
$$
C_{\rm box}^*=r\left\lceil N(1-\alpha)\right\rceil.
$$

**Proof.** With at most $r-1$ affected heads, at least $r$ unchanged heads still vote correctly, so every point remains correct. With at least $r$ affected heads, their votes can all become an incorrect class, or remain unchanged. Accuracy therefore ranges from zero to one. Minimal harmful profiles contain one contaminated document in each of exactly $r$ strata, yielding the risk formula and balanced feasibility.

A safe box can allow a positive contamination bound in at most $r-1$ strata. At least $r$ coordinates must therefore have bound zero. Theorem 2 requires each such coordinate to satisfy $1-n_h/N\le\alpha$, giving the stated cost lower bound. It is attained by imposing bound zero and auditing the required amount in exactly $r$ strata, while assigning bound $N$ and no sampling to the rest. End of proof.

For comparison, the optimal Bonferroni-box cost is $rN-\lfloor N\alpha\rfloor$. The zero-bound coordinates must have total sampling at least $N(r-\alpha)$. Auditing $r-1$ of them completely and the last to $N-\lfloor N\alpha\rfloor$ attains the integer lower bound. Our main comparison nevertheless uses the stronger maximum-risk box.

Fix $\alpha$ and let $a=\log(1/\alpha)$ and $N=r^2$. Since $1-e^{-a/r}\le a/r$,
$$
0<C_I^*\le (2r-1)(Na/r+1)\le2Na+2r,\qquad
C_{\rm box}^*\ge rN(1-\alpha).
$$
Consequently,
$$
\frac{C_{\rm box}^*}{C_I^*}\ge
\frac{rN(1-\alpha)}{2Na+2r}=\Omega(r).
$$
This is a separation caused by the intermediate box-coverage obligation. It is not a lower bound against all auditing procedures, and the total population grows as $(2r-1)r^2$.

**Proposition: a simple total-count certificate attains balanced risk.** Under balanced sampling $n_h=n$, the confidence set $\sum_hq_h\le r-1$ is safe and has exact zero-finding error $(1-n/N)^r$.

**Proof.** Its configurations activate at most $r-1$ heads, establishing safety. A stratum miss probability is the product of $q$ factors $(N-n-j)/(N-j)$, each at most $1-n/N$, or is zero if too many documents are contaminated. Total contamination at least $r$ therefore gives product risk at most $(1-n/N)^r$. One contaminated document in each of $r$ different strata attains equality. End of proof.

Thus the balanced 88-versus-114 example and the asymptotic separation are already achieved by a simple nonrectangular total-count gate. They do not establish that location-aware optimization is necessary.

There need not be a strict saving. In a two-stratum construction harmful only when both strata contain contamination, risk is $(1-n_1/N)(1-n_2/N)$. For total sampling $s\le N$, this equals $1-s/N+n_1n_2/N^2\ge1-s/N$. Concentrating the samples in one stratum attains the minimum. Both direct and box optima equal $\lceil N(1-\alpha)\rceil$.

**A separate location-sensitive comparison.** For $r=2,N=20,d=3,\alpha=1/20$, allocation $(0,19,19)$ is directly feasible at cost 38: its largest product over two contaminated strata is $1/20$. Every fixed design certifying total contamination at most one costs at least 48. If any stratum samples at most 15, two contaminations there have miss probability at least $20/380>1/20$. Each stratum must therefore sample at least 16. Sampling 16 everywhere attains cost 48: two contaminations in one stratum have probability $12/380$, while one in each of two strata has probability $1/25$. Higher counts only reduce miss probability.

This analytical comparison was added after review, not preregistered as a new experiment. It isolates a location advantage over this specific total-count gate, while general count sets remain equivalent to direct testing. It is not an originality claim or evidence that the original empirical decision threshold passed.

## 8. Exact optimization and computational scope

For a general finite instance, enumerate all fixed integer allocations and retain those satisfying Theorem 1. Taking their least cost gives the global minimum within this specified design class. Exhaustiveness proves optimality; an interrupted search gives only a feasible upper bound when a certified allocation has been found. Finding nothing before interruption is not proof of infeasibility.

Antichains can be exponentially large. After their construction, a straightforward risk scan costs on the order of $d|Q_{\min}|\prod_h(N_h+1)$ operations, apart from exact-integer arithmetic costs. Influence-oracle calls and Pareto filtering also require accounting. The implementation imposes explicit configuration, state, and allocation budgets and refuses unsupported computations.

**Theorem 4: symmetric exact search.** In the threshold family, it suffices to enumerate
$$
0\le a_1\le\cdots\le a_r\le N,\qquad
\prod_{i=1}^{r}(N-a_i)\le\alpha N^r,
$$
minimizing $\sum_{i=1}^{r-1}a_i+ra_r$. The corresponding allocation consists of the displayed prefix followed by $r-1$ additional copies of $a_r$.

**Proof.** Symmetry permits sorting any allocation increasingly. Its worst miss probability uses the first $r$ entries, whose miss factors are largest. Lower every subsequent entry to the $r$th entry. The largest $r$ factors and feasibility remain unchanged, while cost weakly decreases. Hence an optimum has the claimed form, and every enumerated form is a legal design. There are $\binom{N+r}{r}$ such tuples. End of proof.

All audit probabilities, costs, and interval comparisons in these experiments use exact rational or integer arithmetic. The balanced formula involving a root is implemented by integer inequalities rather than floating-point rounding. Equal costs and equal stratum sizes are essential for the symmetry reduction.

## 9. Constructed evidence and separate real-text context

The frozen mathematical grid contains all twenty combinations of $r\in\{2,3,4,5,6\}$ and $N\in\{2,5,10,20\}$, with $\alpha=1/20$ and the interval in Section 7. Its complete results are stored in [threshold_results.json](../planning/threshold_results.json). These are artificial vote structures; no document audit or trained language model generated them.

| Threshold example: r=6, N=20 | Audit count | Qualification |
|---|---:|---|
| Direct fixed allocation | 88 | Exact optimum in stated class |
| Joint-zero rectangle | 114 | Exact optimum for box coverage |
| Balanced total-count gate | 88 | Feasible; matches direct optimum |

For this threshold case, eight samples in each of eleven strata give risk $(3/5)^6=0.046656$. Exact optimization confirms cost 88; the stronger box costs 114 and the Bonferroni box 119. Across the entire grid, nine cases show strict savings and eleven show none. The maximum saving is $4/15$, occurring at $r=6$ with $N=5,10$. The grid median is zero. Accordingly, the full frozen family did not meet the proposed median-saving threshold of 20 percent. Selecting only the favorable value of $r$ afterward would not satisfy that rule.

A separate, newly trained SEntFiN experiment concerns source-native entity sentiment, with negative, neutral, and positive labels. It uses a non-temporal lexical-component split and development-only selection of regularization. Its 2,107 test entity rows form 1,570 lexical components.

| System | Test macro-F1 | Role |
|---|---:|---|
| Word TF-IDF and logistic regression | 0.7920 | Prespecified baseline |
| Character TF-IDF and logistic regression | 0.7548 | Prespecified comparison |
| Entity-only logistic regression | 0.5336 | Diagnostic |

The prespecified character-minus-word difference is $-0.03723$, with a nominal 95 percent paired lexical-cluster bootstrap interval approximately $[-0.05306,-0.02156]$, using 10,000 draws. This is conditional approximate uncertainty for fixed training and development choices, not a certificate. Lexical components need not be independent semantic events. Entity-only performance cannot be divided by full-model performance to obtain an explained proportion. These results are not directly comparable to the old 0.6549 score, do not replace absent FinBERT or zero-shot LLM comparisons, and do not validate any audit theorem. Their purpose is to establish a reproducible simple-model starting point and sharpen the burden of proving that more complex language components are necessary.

## 10. Limitations and research decisions

The most important missing object is a real model, real contamination assessment, and useful statistic interval connected under one verified assumption ledger. Accurate sentiment predictions do not establish an influence graph or historical admissibility. Conversely, a mathematically valid interval around an uninformative constant classifier would not establish task value.

The rectangular comparison measures an additional confidence-set restriction. General safe count sets reproduce direct testing, and a simple total-count gate already realizes the balanced separation. The separate location example distinguishes a direct allocation from that specific total-count gate, not from all count-based audits. These distinctions may already be fully explained by existing composite-hypothesis testing or risk-limiting audit methods. A useful next result would identify a realistic influence class, establish what information the audit genuinely needs, and compare against the strongest applicable existing procedure. Extending the current formula to adaptively chosen samples without a valid sequential construction would be an error.

The manuscript is therefore a working technical report, not the completed research objective. The central mathematical interface is explicit, but originality, complete mainline experiments, and a real historical certificate remain unresolved. The project's G0 and G1 gates have not automatically passed. No material has been sent to Fable, and no Fable approval or feedback is represented here.

## Appendix A. Historical non-interference is a separate obligation

Represent a finite version log by immutable events with knowledge times. The historical projection $H_t(L)$ retains only events known by cutoff $t$ and orders them canonically. For fixed external configuration and seed, a pipeline $F$ is historically non-interfering exactly when
$$
H_t(L)=H_t(L')\ \Longrightarrow\ F(L)=F(L').
$$
This is equivalent to a factorization $F=G\circ H_t$: define $G$ by the common output on each history fiber. On countable canonical byte histories the measurable factor is straightforward. In general measurable spaces, a set-theoretic factor alone does not ensure a measurable one.

Future-append invariance implies this property only when equal-history logs are connected by legal future extensions and deletions, for example through a legal historical prefix. Versions must be projected by knowledge time before selecting the latest visible version. A future correction can retain an old event date; selecting the global latest version first can either import the correction or discard a formerly available version.

All shared choices must factor through the history: vocabulary, deduplication, sampling, validation, hyperparameters, and core roles. Stable artifacts cannot include the final whole-log hash or future document count. Those belong in a separate audit envelope that does not feed model decisions.

Even perfect record non-interference does not authenticate knowledge times. The same observed log can be compatible with a genuinely early document or an incorrectly backdated future document, producing clean-comparator statistics zero and one under a fixed comparison rule. Any closed interval uniformly covering both compatible worlds must contain $[0,1]$. Mathematical measurability is also insufficient by itself: a retrospectively fixed checkpoint is a constant random variable. Historical constructibility requires a prospectively specified procedure and a truthful, replayable provenance contract. External randomness must not introduce future information conditional on the historical information set; marginal independence from future data alone is insufficient.

## Appendix B. Semantic envelopes bound a different weak link

A numeric text branch fixes the task, context, direction, and ordered-logit thresholds. For independent intervals in $x$ and positive baseline $b$, the exact range of $g=x/b-1$ is obtained from four corners. An affine latent score then has an exact interval $[L,U]$. All branches must share the same output target and class meanings.

For middle ordered-logit class $i$,
$$
q_i(\eta)=\sigma(\theta_i-\eta)-\sigma(\theta_{i-1}-\eta).
$$
Its minimum on $[L,U]$ is the smaller endpoint value. Its maximum occurs at the projection of $(\theta_{i-1}+\theta_i)/2$ onto the interval. To verify this, write the derivative as the difference of sigmoid derivatives at the two thresholds; that derivative kernel is even and decreases with distance from zero. The class probability increases up to the midpoint and decreases afterward. Endpoint-only evaluation would miss its maximum.

Taking each coordinate's minimum and maximum across branches gives the smallest covering coordinate box, although its corners need not be jointly attainable. If a scalar candidate range has diameter $D$, every all-candidate interval has width at least $D$, and the minimax absolute error of a point report is $D/2$. On frozen tasks with weights $w_i$, the largest possible robust acceptance mass at width limit $w$ is $\sum_iw_i\mathbf1\{D_i\le w\}$. This is relative to the specified candidate sets, not proof that extra branches emitted by a parser reflect intrinsic textual ambiguity.

When the target is exactly $\operatorname{sign}(x-b)$ and all branches agree, a symbolic rule solves the downstream task completely. Learning an ordered head is then unnecessary. With a fixed accepted set, sound numeric propagation gives output failure risk at most the conditional parse-set miss rate. An unconditional miss bound $\varepsilon$ only yields a conditional bound $\min(1,\varepsilon/P(A))$. Audit confidence error $\alpha$ is a different quantity. These observations identify the semantic coverage obligation; they do not supply natural-text gold labels or calibrate model probabilities.

## Appendix C. Complete frozen threshold grid

All rows use $\alpha=1/20$, $d=2r-1$, and unit costs. Direct and Box columns are exact optima in their respective fixed-allocation classes. Balanced is the least-cost balanced design; by Section 7 it also certifies total contamination at most $r-1$. It is not claimed to optimize arbitrary unbalanced total-count designs. Saving is $(\text{Box}-\text{Direct})/\text{Box}$. The balanced total-count interpretation was made explicit during review; the allocations themselves are from the frozen twenty-case experiment.

| r | N | Direct | Box | Balanced | Saving |
|---:|---:|---:|---:|---:|---:|
| 2 | 2 | 4 | 4 | 6 | 0 |
| 2 | 5 | 10 | 10 | 12 | 0 |
| 2 | 10 | 20 | 20 | 24 | 0 |
| 2 | 20 | 38 | 38 | 48 | 0 |
| 3 | 2 | 6 | 6 | 10 | 0 |
| 3 | 5 | 15 | 15 | 20 | 0 |
| 3 | 10 | 30 | 30 | 35 | 0 |
| 3 | 20 | 57 | 57 | 65 | 0 |
| 4 | 2 | 8 | 8 | 14 | 0 |
| 4 | 5 | 20 | 20 | 21 | 0 |
| 4 | 10 | 39 | 40 | 42 | 1/40 |
| 4 | 20 | 76 | 76 | 77 | 0 |
| 5 | 2 | 9 | 10 | 9 | 1/10 |
| 5 | 5 | 23 | 25 | 27 | 2/25 |
| 5 | 10 | 42 | 50 | 45 | 4/25 |
| 5 | 20 | 84 | 95 | 90 | 11/95 |
| 6 | 2 | 10 | 12 | 11 | 1/6 |
| 6 | 5 | 22 | 30 | 22 | 4/15 |
| 6 | 10 | 44 | 60 | 44 | 4/15 |
| 6 | 20 | 88 | 114 | 88 | 13/57 |

## Reproducibility and source status

This draft reuses recorded local experiments and finite exact arithmetic review checks; manuscript preparation performs no new model training or confirmatory experiment. The main proof sources are the internal impact-audit and collective-metric notes; implementation identities, budgets, and full numerical outputs are preserved alongside the code. The real-text context comes from the public aggregate baseline and bootstrap summaries; private text, labels, weights, and individual predictions are excluded from the handoff. Markdown and LaTeX versions share the same body. PDF production is separate from mathematical validation.

## References and metadata verification

The identifiers below match the existing seventeen-source literature ledger. Entries reproduce only locally recorded information; full titles where unavailable, complete author lists, and publication metadata were not revalidated for this offline draft. These are source pointers, not a claim of an exhaustive or submission-ready bibliography.

L01. Fonseca. Temporal non-interference and look-ahead freedom; full title not revalidated. [arXiv:2607.04958v1](https://arxiv.org/html/2607.04958v1). Local review: full text.

L02. Levine and Feizi. Deep Partition Aggregation (DPA); complete title metadata not revalidated. [arXiv:2006.14768v2](https://arxiv.org/html/2006.14768v2). Local review: full text, Theorem 1 and Appendix A.

L03. Wang et al. Finite Aggregation; complete title and author list not revalidated. [arXiv:2202.02628v1](https://arxiv.org/html/2202.02628v1). Local review: full text, Section 3.

L04. Chen et al. Collective bagging robustness certificates; descriptive topic, full title not revalidated. [arXiv:2205.13176v2](https://arxiv.org/html/2205.13176v2). Local review: full text, Sections 3--4 and Appendix B.

L08. Waudby-Smith and Ramdas. Confidence sequences for sampling without replacement; descriptive topic, full title not revalidated. [arXiv:2006.04347v4](https://arxiv.org/html/2006.04347v4). Local review: full text, Section 2.

L09. Shekhar et al. Weighted financial auditing with test martingales; descriptive topic, full title and author list not revalidated. [arXiv:2305.06884v1](https://arxiv.org/html/2305.06884v1). Local review: full text, Sections 2--4.

L05. Kitouni et al. Lipschitz networks with monotonic residuals; descriptive topic, complete metadata not revalidated. [arXiv:2112.00038v2](https://arxiv.org/html/2112.00038v2). Local review: full text, Sections 2.1--2.2.

L07. Villar et al. Dimensionless machine learning. [JMLR source page](https://www.jmlr.org/papers/v24/22-0680.html). Local review: full text; complete author list not revalidated.

L10. Henzi, Ziegel, and Gneiting. Isotonic distributional regression. [arXiv:1909.03725v3](https://arxiv.org/html/1909.03725v3). Local review: full text, Section 2.

