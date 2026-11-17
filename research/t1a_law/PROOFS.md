# T1A: quantitative rules and proofs in the rounding box

Date: 2026-11-16 (America/New_York). This document proves the specific form that classical error propagation takes in this task; it does not present cancellation error, interval arithmetic or the convolution of uniform distributions as new theory. The only empirical input is T1's saved `results/per_question.jsonl`; the theorems here need no empirical fitting.

## 0. Objects, assumptions and decision convention

Let the displayed centers be $a,b$, the displayed last-digit units $d_a,d_b$, and the half-widths $h_a=d_a/2,h_b=d_b/2$. The independent rounding box is

\[
A=a+u,\quad B=b+v,\qquad |u|\le h_a,\ |v|\le h_b.
\tag{D1}
\]

"Independent" in the deterministic part means that every combination of $u,v$ is allowed; random independence is added only in Section 6. Repeated references to the same source must share one variable and cannot be treated as two independent errors; accounting constraints between different financial sources are handled by T1B.

Growth rate $G=B/A-1$, displayed center $g=b/a-1$. The exact formulas below require

\[
|a|>h_a,\qquad g\ne0
\tag{A1}
\]

so that the denominator does not touch zero and the relative error about the center is defined. Unless specifically noted, **$a,b$ are not required to have the same sign**. Write $r=b/a=1+g$,

\[
\eta=h_a/|a|<1,\quad
L(u,v)=\frac{a v-b u}{a^2},\quad
R_1=\frac{|a|h_b+|b|h_a}{a^2},\quad C=R_1/|g|.
\tag{D2}
\]

Closed-interval endpoints are used to compute suprema and infima. As long as the range **strictly** crosses an acceptance boundary, continuity gives an interior witness near that endpoint; this does not depend on the convention for "rounding a 5". Exact tangency cannot be judged out of tolerance on this basis.

This section usually compares against the center band $[g-\tau|g|,g+\tau|g|]$. The actual T1 uses the band of the gold $y$, $[y-\tau|y|,y+\tau|y|]$; the two differ, and Section 3 gives the exact conversion. 1% is the audit tolerance specified by the task, not a redefinition of FinQA's official five-decimal scoring rule.

## 1. Exact range of the growth rate, first-order term and remainder

### Proposition 1: four-corner range and exact maximum error

When $|a|>h_a$, let

\[
q_{st}=\frac{b+t h_b}{a+s h_a}-1,\qquad s,t\in\{-1,1\}.
\]

Then the full range is

\[
[G_-,G_+]=[\min_{s,t}q_{st},\max_{s,t}q_{st}].
\tag{T1}
\]

The maximum absolute error and the maximum relative error about the center are, respectively,

\[
R_{\rm abs}:=\max|G-g|
=\frac{|a|h_b+|b|h_a}{|a|(|a|-h_a)}=\frac{R_1}{1-\eta},
\tag{T2}
\]
\[
R_{\rm rel}:=\max\frac{|G-g|}{|g|}
=\frac{|a|h_b+|b|h_a}{|b-a|(|a|-h_a)}=\frac{C}{1-\eta}.
\tag{T3}
\]

**Proof.** For fixed $A\ne0$, $B/A$ is monotone in $B$, so only $B=b\pm h_b$ need be considered. For each fixed $B$, the derivative is $-B/A^2$, whose sign is constant (or identically zero) over the whole denominator interval, so the extrema are at the two denominator endpoints. The real image of a continuous function on a connected rectangle is also an interval, so the four corners give the full range. Direct subtraction also gives

\[
G-g=\frac{a v-b u}{a(a+u)}.
\tag{I1}
\]

The triangle inequality and $|a+u|\ge|a|-h_a$ give the upper bound in T2. Take $u=-\operatorname{sgn}(a)h_a$, then choose $v\in\{-h_b,h_b\}$ so that $av$ and $-bu$ have the same sign; this attains the numerator upper bound and the denominator lower bound at the same time. If one of the terms is zero, either corresponding sign will do. So the upper bound is indeed attained. Dividing by $|g|=|b-a|/|a|$ gives T3. QED.

In particular, the half-widths may differ, and the interval of $b$ may cross zero; neither breaks T1–T3. **The symmetric envelope of the maximum error, $[g-R_{\rm abs},g+R_{\rm abs}]$, is in general not the full range**: the deviations on the two sides are usually unequal.

### Proposition 2: full first-order expansion and uniform remainder

\[
G-g=L(u,v)+E(u,v),\qquad
E(u,v)=-\frac{u}{a+u}L(u,v).
\tag{T4}
\]

Therefore

\[
|E(u,v)|\le\frac{\eta}{1-\eta}R_1,
\qquad
R_{\rm rel}=C+\frac{C\eta}{1-\eta}.
\tag{T5}
\]

More specifically, pointwise,

\[
\frac{|L(u,v)|}{1+\eta}\le|G-g|
\le\frac{|L(u,v)|}{1-\eta}.
\tag{T6}
\]

**Proof.** I1 equals $L(u,v)/(1+u/a)$. Subtracting $L$ gives T4; then $|u/(a+u)|\le h_a/(|a|-h_a)$ and $|L|\le R_1$ give the remainder bound. The algebraic identity of T3 gives the second part of T5. $1-\eta\le|1+u/a|\le1+\eta$ gives T6. QED.

So $C$ is the first-order worst-case relative radius, not a strict upper bound; with non-zero rounding, $C\le R_{\rm rel}$, and the difference is explicitly controlled but cannot be omitted unconditionally.

### Two-sided exact bounds for same-sign positive quantities

If $a>h_a$ and $b\ge h_b$, then

\[
G_-=\frac{b-h_b}{a+h_a}-1,
\quad G_+=\frac{b+h_b}{a-h_a}-1,
\tag{T7}
\]
\[
g-G_-=\frac{a h_b+b h_a}{a(a+h_a)},
\quad G_+-g=\frac{a h_b+b h_a}{a(a-h_a)}.
\tag{T8}
\]

The proof is the monotonicity in T1: with a non-negative numerator, the value increases as the denominator decreases; subtract the center. When both are negative and neither rounding interval crosses zero, multiply $A,B$ both by (-1) and replace the centers by $|a|,|b|$; T7–T8 continue to hold. For opposite signs use T1; T7 cannot be applied directly.

## 2. How far "a difference of 100 last-digit units" actually holds

### Exact version with equal precision

If $d_a=d_b=d>0$, define

\[
\Delta=|b-a|/d.
\]

Then T3 gives

\[
R_{\rm rel}=\frac{1+|r|}{2\Delta(1-\eta)},
\qquad \eta=\frac{|g|}{2\Delta}.
\tag{T9}
\]

If the centers have the same sign, $r=1+g>0$, and further

\[
\boxed{R_{\rm rel}=\frac{1+g/2}{\Delta-|g|/2}},
\tag{T10}
\]
\[
\boxed{R_{\rm rel}\le\tau\ \Longleftrightarrow
\Delta\ge\frac{1+g/2}{\tau}+\frac{|g|}{2}}.
\tag{T11}
\]

**Proof.** Substitute $h_a=h_b=d/2$ and $|r|=1+g$, then multiply by the positive $\Delta-|g|/2$. QED.

Only for a small growth rate $|g|\ll1$ and a sufficiently small relative rounding of the denominator $\eta\ll1$ is T9 approximately $1/\Delta$. With the same sign, the relative approximation error can be quantified exactly:

\[
\left|\frac{R_{\rm rel}}{1/\Delta}-1\right|
=\left|\frac{g/2+\eta}{1-\eta}\right|
\le\frac{|g|/2+\eta}{1-\eta}.
\tag{T12}
\]

**"If $\Delta<100$ then 1% can certainly not be met" is not an unconditional theorem.** Example $a=100,b=10,d=1$: $g=-0.9,\Delta=90$, but T10 gives $R_{\rm rel}=0.55/89.55\approx0.6142\%<1\%$. It also fails in the other direction: $a=1000,b=1100,d=1$, $\Delta=100$, while $R_{\rm rel}=1.05/99.95\approx1.0505\%>1\%$. T11 is the corrected rule for the case of the center band, equal last-digit precision and same sign.

### Version with unequal precision

If the last-digit units differ, there is no unique "number of last-digit units". When $h_a+h_b>0$, the natural definitions are

\[
\Delta_{\rm eff}=\frac{|b-a|}{h_a+h_b},\qquad
w=\frac{h_a}{h_a+h_b}.
\]

Then

\[
C=\frac{1+(|r|-1)w}{\Delta_{\rm eff}},\qquad
R_{\rm rel}=\frac{1+(|r|-1)w}{\Delta_{\rm eff}(1-\eta)}.
\tag{T13}
\]

With the same sign, the numerator is $1+gw$. The proof factors $h_a+h_b$ out of $h_b+|r|h_a$. If a coarse rule is built from the largest, smallest or average last-digit unit instead, this must be stated, and replication counts under different definitions must not be mixed together.

## 3. From center uncertainty to the gold acceptance interval

Let the final answer be $Z=sG$, where $s\ne0$ is an exact constant (for example, multiplying by 100 for a percentage output), the center is $z_0=sg$, and the gold is $y$. The actual acceptance band is

\[
[\ell,u]=[y-\tau|y|,y+\tau|y|].
\]

The exact decision given by T1 is

\[
\min(sG_-,sG_+)\ge\ell\quad\text{and}\quad
\max(sG_-,sG_+)\le u.
\tag{T14}
\]

The center-gold offset $e=z_0-y$ should not be dropped. The first-order symmetric approximation uses radius $|s|R_1$, and the condition for judging stable is

\[
|e|+|s|R_1\le\tau|y|.
\tag{T15}
\]

Replacing $R_1$ with $R_{\rm abs}$ gives a **sufficient condition**, but in general not a necessary one, because the exact range is asymmetric. Only T14 is the exact necessary and sufficient condition. If the center is already outside the acceptance band, no input perturbation is needed; it should be listed separately as center-incompatible and not attributed to rounding.

If $g=0$, the relative error about the center is undefined; if $y=0$, the task's relative acceptance band is a single point. Neither can be patched by adding an arbitrarily small constant to the denominator. The absolute range must be compared directly with the original acceptance band. If the whole denominator interval touches zero, the growth rate is usually unbounded or undefined, and it should be marked as a domain failure; T1–T15 do not apply.

## 4. One-line rules for differences, ratios and sums

The expressions below are all about the displayed center; comparison with the gold must also add the offset as in Section 3.

- **Difference** $D=B-A$, $b-a\ne0$: exact relative radius $(h_a+h_b)/|b-a|$. The difference must be at least $1/\tau$ times the total half-width; with the same last-digit unit, $\Delta\ge1/\tau$.
- **Ratio** $Q=B/A$, $b\ne0$, $|a|>h_a$: exact relative radius $(h_b/|b|+h_a/|a|)/(1-h_a/|a|)$. The sum of the inputs' relative half-widths must be smaller than the tolerance, with the denominator's $1/(1-\eta)$ factor added.
- **Sum** $S=\sum_i c_i X_i$, $s_0\ne0$: exact relative radius $\sum_i|c_i|h_i/|s_0|$. The total rounding half-width must not exceed $\tau$ times the total; a same-sign sum has no cancellation amplification, while cancellation between opposite signs still amplifies.
- **General differentiable program** $f$: first-order relative radius $\sum_i|\partial_i f|h_i/|f(x)|$. Propagate the first-order sensitivity of each independent source; this by itself does not guarantee that the higher-order remainder is small.

**Proof.** The range of the difference error $v-u$ is exactly $[-(h_a+h_b),h_a+h_b]$, so the difference rule is an equality. Ratio and growth rate differ only by the constant 1 and have the same absolute error; dividing T2 by $|b/a|$ gives the ratio rule. The error of a linear sum is $\sum c_i\epsilon_i$; the triangle inequality gives the upper bound $\sum|c_i|h_i$, attained at $\epsilon_i=\operatorname{sgn}(c_i)h_i$, and the opposite choice attains the lower bound. The general program follows from the first-order multivariate Taylor term; if the second derivatives in each input direction exist and are bounded within the box, the integral remainder gives

\[
|f(x+\epsilon)-f(x)-\nabla f(x)^T\epsilon|
\le\frac12\sum_{i,j}h_i h_j\sup_{z\in B}|\partial_{ij}f(z)|.
\tag{T16}
\]

Proof of T16: along the segment let $\phi(t)=f(x+t\epsilon)$; the integral Taylor remainder is $\int_0^1(1-t)\epsilon^TH_f(x+t\epsilon)\epsilon\,dt$; take absolute values, bound term by term, and use $\int_0^1(1-t)dt=1/2$. If the same source appears several times, its derivative coefficients must be combined before taking absolute values; for example, the true error of $X-X$ is zero.

## 5. Significant-digit budget: an exact statement, not "guaranteed correct digits"

For non-zero displayed centers write

\[
|a|=m_a10^{e_a},\quad |b|=m_b10^{e_b},\qquad 1\le m_a,m_b<10.
\]

If they display $k_a,k_b$ significant digits respectively, counting meaningful trailing zeros, then

\[
d_a=10^{e_a-k_a+1},\quad d_b=10^{e_b-k_b+1},\quad
\epsilon_a=\frac{h_a}{|a|}=\frac{10^{1-k_a}}{2m_a},\quad
\epsilon_b=\frac{10^{1-k_b}}{2m_b}.
\tag{D3}
\]

### Proposition 3: exact digit budget

Under A1 and $b\ne0$, T3 is equivalent to

\[
\boxed{R_{\rm rel}
=\frac{|r|(\epsilon_a+\epsilon_b)}{|g|(1-\epsilon_a)}}.
\tag{T17}
\]

So the necessary and sufficient condition for meeting the center relative tolerance $\tau$ is

\[
|r|(\epsilon_a+\epsilon_b)\le\tau|g|(1-\epsilon_a).
\tag{T18}
\]

If both inputs display $k$ significant digits, and the displayed precision is raised or lowered uniformly with the centers $a,b$ held fixed, the necessary and sufficient condition can be written as

\[
\boxed{
k\ge1+\log_{10}\!\left[
\frac{|r|(m_a^{-1}+m_b^{-1})+\tau|g|m_a^{-1}}
{2\tau|g|}\right]}
\tag{T19}
\]

together with the requirement $10^{1-k}<2m_a$ (the denominator does not touch zero). The integer number of digits is the right-hand side rounded up, and at least 1.

**Proof.** Substituting $h_a=|a|\epsilon_a,h_b=|b|\epsilon_b$ into T3 gives T17. The denominator is positive; cross-multiplying gives T18. Let $q=10^{1-k}$; T18 is equivalent to

\[
q\{ |r|(m_a^{-1}+m_b^{-1})+\tau|g|m_a^{-1}\}\le2\tau|g|,
\]

and taking base-10 logarithms and rearranging gives T19. QED.

To avoid confusing an error bound with correct rounding of a numeric string, define the "relative precision digit budget"

\[
p:=-\log_{10}R_{\rm rel}.
\]

This is an error-magnitude indicator: $p\ge j$ means the error is at most $10^{-j}$; **it does not unconditionally guarantee that the first $j$ decimal characters of the output are unchanged**. Right next to a rounding boundary, an arbitrarily small error can change the last digit.

For equal $k$ digits, T17 gives the exact expression

\[
p=k-1+\log_{10}|g|
 +\log_{10}\frac{2}{|r|(m_a^{-1}+m_b^{-1})}
 +\log_{10}(1-\epsilon_a).
\tag{T20}
\]

So the task's $k-\log_{10}(1/|g|)$ is an order-of-magnitude approximation that omits the mantissa constant and the denominator remainder. For small growth rates and close mantissas, $p\approx k-1+\log_{10}(m_a|g|)$; since $m_a\in[1,10)$, the same $k,g$ can differ by nearly one digit of precision. "At least about $\log_{10}(1/(|g|\tau))$ digits are needed" has the same constant band. With actually unequal precision, T18 should be used; the average of the two significant-digit counts cannot stand in for it.

## 6. Exact probabilities under uniform rounding errors

The new probabilistic assumption is $U\sim\operatorname{Unif}[-h_a,h_a]$, $V\sim\operatorname{Unif}[-h_b,h_b]$, independent. Real filing rounding errors need not satisfy it; this is not an empirical distribution derived from worst-case witnesses.

First make a negative denominator positive: use $a'=|a|$, $b'=\operatorname{sgn}(a)b$, and multiply both perturbations by $\operatorname{sgn}(a)$ as well. The symmetric uniform distributions are unchanged, and $B/A$ is unchanged. The primes are dropped below, so $a>h_a$.

### Lemma 4: sum of two symmetric uniform variables

Let $X\sim\operatorname{Unif}[-p,p]$ and $Y\sim\operatorname{Unif}[-q,q]$ be independent with $p,q>0$. The CDF of their sum is

\[
H(z;p,q)=\frac{(z+p+q)_+^2-(z+p-q)_+^2
 -(z-p+q)_+^2+(z-p-q)_+^2}{8pq},
\tag{T21}
\]

where $x_+=\max(x,0)$.

**Proof.** Shift the variables to $X'=X+p\in[0,2p]$ and $Y'=Y+q\in[0,2q]$; the probability equals the area of $X'+Y'\le w=z+p+q$ inside the rectangle divided by $4pq$. Unrestricted by the rectangle in the first quadrant, this triangle has area $w_+^2/2$; subtract the two shifted triangles beyond $X'>2p$ and $Y'>2q$, then add back the doubly subtracted corner area, giving half of the numerator. Dividing by the rectangle's area gives T21. QED.

A numerical implementation should use the following equivalent piecewise form, which avoids cancellation of large numbers. Write $M=\max(p,q),m=\min(p,q)$:

\[
H(z)=\begin{cases}
0,&z\le-M-m,\\
(z+M+m)^2/(8Mm),&-M-m<z<-M+m,\\
(z+M)/(2M),&-M+m\le z\le M-m,\\
1-(M+m-z)^2/(8Mm),&M-m<z<M+m,\\
1,&z\ge M+m.
\end{cases}
\tag{T22}
\]

If exactly one half-width is zero, use the CDF of the other symmetric uniform variable; if both are zero, use the CDF of a point mass at zero.

### Proposition 5: closed-form CDF of the growth rate and the out-of-tolerance probability

For any real $t$,

\[
\boxed{F_G(t)=P(G\le t)
=H((1+t)a-b;h_b,|1+t|h_a).}
\tag{T23}
\]

**Proof.** Since $A>0$, the event $G\le t$ is equivalent to

\[
B\le(1+t)A
\iff V-(1+t)U\le(1+t)a-b.
\]

The variable $-(1+t)U$ is a symmetric uniform variable with half-width $|1+t|h_a$, and is still independent of $V$. Substituting into Lemma 4, including the limiting cases of degenerate widths, gives T23. QED.

If the acceptance band of the unscaled growth rate is $[\ell,u]$, the exact out-of-tolerance probability is

\[
P_{\rm out}=P(G<\ell)+P(G>u)=F_G(\ell^-)+1-F_G(u).
\tag{T24}
\]

When $h_b>0$, the ratio has a continuous distribution conditional on any denominator, so $F_G(\ell^-)=F_G(\ell)$. If $h_b=0,b\ne0,h_a>0$, the strictly monotone transformation of the denominator also gives a continuous distribution. If $h_b=b=0$, then $G=-1$ is constant; if both half-widths are zero, it is also constant. For a point mass one must directly check whether it lies in the closed acceptance band; mass on the boundary must not be counted as out of tolerance.

For the output $Z=sG$, first divide both endpoints of the gold band by $s$, sort to get $\ell,u$, then use T24. This exactly preserves the gold offset, negative output scales and unequal input precisions. Similarly, for a ratio just replace $1+t$ in T23 with $t$; the CDF of a two-input difference is $H(t-(b-a);h_a,h_b)$. Over any number of questions, the expected number of out-of-tolerance questions is $\sum_i P_{{\rm out},i}$; this relies only on linearity of expectation and **does not require independence between questions**; only the rounding assumption within each question needs to be explicit.

## 7. What the Benford prediction can test

"The leading digit follows Benford" only specifies $P(D=j)=\log_{10}(1+1/j)$; it specifies neither the distribution within $[j,j+1)$ nor the dependence on growth rate/displayed digits. This assumption alone cannot uniquely determine the out-of-tolerance rate.

A reproducible main model with explicit extra assumptions: independently draw from the empirical marginal of the growth rate $g$ and the empirical joint distribution of digit pairs $(k_a,k_b)$; independently take $\log_{10}M_a\sim\operatorname{Unif}[0,1)$. Normalize $a=M_a$, let $b=(1+g)M_a$, generate $d_b$ from $b$'s own decimal exponent and $k_b$, generate $d_a$ from $a,k_a$, and then use T3/T18 to decide center-band stability. This reads no per-question mantissa, fits no threshold, and keeps the ratio of the two inputs consistent. The half-width ratio of the original question should not additionally be held fixed, because it could bring back the original question's mantissa/decimal-boundary-crossing information.

This model is stronger than leading-digit Benford: it uses a full log-uniform mantissa and assumes it is independent of the empirical growth rate/digit counts. The main model draws growth rate and digit counts independently; keeping the empirical joint distribution of $(g,k_a,k_b)$ is a sensitivity analysis. The two give different results and should be clearly distinguished. What it tests is the conditional population prediction under these distributional assumptions, **not an external a priori validation independent of this data**. $(g,k_a,k_b)$ alone cannot recover each question's gold offset, so the main model naturally predicts the center band; when compared with observations on the gold band, this difference in convention must be listed separately. Degenerate items such as $g=0,b=0$, denominators crossing zero and shared sources need explicit denominators and exclusion counts.

### Independent derivation of the piecewise integral

Restrict to $r=1+g>0$, $g\ne0$, $k_a,k_b\ge1$. Let $M=a\in[1,10)$; then $h_a=10^{1-k_a}/2\le1/2<M$. On a subinterval that does not cross $rM=10^e$, $h_b=10^{e-k_b+1}/2$ is constant, and T3 becomes

\[
R_{\rm rel}(M)=\frac{h_b+r h_a}{|g|(M-h_a)}.
\]

So the question is out of tolerance if and only if

\[
M<h_a+\frac{h_b+r h_a}{\tau|g|}=:M_*.
\tag{T25}
\]

For any segment $[L,U)$, let $V=\min(U,\max(L,M_*))$. Under the log-uniform model, the out-of-tolerance mass of the segment is exactly $\log_{10}(V/L)$, because the density is $1/(M\ln10)$. The segment endpoints are given by $1,10$ and all $10^e/r$ inside the interval; adding the integer leading-digit boundaries as well, one can also compute the within-leading-digit uniform model: within leading digit $j$, the out-of-tolerance length of each segment is multiplied by $\log_{10}(1+1/j)$. This is exactly the piecewise integral in benford.py::mantissa_prediction, not a fit to observed labels. When numerically computing the identification interval for a variable within-leading-digit distribution, the tolerance for floating-point "empty/full interval" decisions should be stated, and floating-point approximate bounds should not be called symbolically certified bounds.

## 8. Limits of the conclusions in this document

The conclusions above are theorems of the rounding-box model; whether the full document can narrow the box, whether the gold program is faithful to the question, and whether models are marked wrong because of it are not things these formulas can prove. The empirical 95% agreement rate and the 5-percentage-point prediction error are T1A's data acceptance criteria and cannot be guaranteed by the formulas themselves. The probabilistic expectation and the existential worst case are different quantities of study; they should be reported side by side and cannot substitute for each other.
