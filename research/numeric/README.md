# 有限语义候选的严格有理数包络检查器

本组件对应 [运行前协议](PROTOCOL.md)。它计算给定语义候选和固定 affine ordered-logit 模型的输出包络，使用 Python 标准库与 Fraction；没有真实文本解析器、金标审计、模型训练、网络访问或部署错误率。基础区间运算、有序 logit 和有限候选 min/max 均不据此声称原创。

本轮所有数值区间、斜率、偏移、阈值和候选集合均为预先手选的数学构造；这里没有从语料训练出的权重。手选参数示例的通过不证明某个现实金融模型满足相同前提。

## 输入与目标

`SemanticBranch(semantic_id,g_interval,slope,offset,thresholds,target_id=...,class_labels=...)` 声明一个固定语义解释：无量纲值 g 位于闭区间，`η=slope*g+offset`，阈值为固定严格递增的有理数。至少一个阈值，即 K≥2。斜率可以为正、负或零；其符号说明这个**给定模型**的方向，不证明经济语义的方向正确。不同分支可以有不同的基准、方向和模型参数。

联合分支必须声明同一 `target_id` 和完全相同次序的 `class_labels`；仅 K 相同不足够。默认 target 是明确的示例标识，默认标签为 `class_0,...`，不是金融语义。检查器能拒绝不同声明，**不能证明相同声明真的描述同一语义目标**。`semantic_id` 必须唯一；它标识解释，不携带解释的概率。

区间端点、斜率、偏移、阈值、容差、宽度阈值和单位比例只接受精确 int/Fraction；float、bool 和未经解析的字符串被拒绝。预算的 max_terms 也拒绝 bool。所有区间必须有序；概率计算超出声明数值预算时抛出 `BudgetExceeded`，不返回部分分支或未经证明的窄区间。

```python
from fractions import Fraction as F
from research.numeric.semantic_envelope import (
    Interval, Budget, SemanticBranch, relative_change_interval,
    semantic_envelope, width_gate,
)

g = relative_change_interval(Interval(9,11), Interval(8,10))
branch = SemanticBranch("baseline-A", g, F(1), F(0), (F(-1),F(1)),
                        target_id="declared-comparison",
                        class_labels=("below","near","above"))
result = semantic_envelope([branch], Budget())
serializable = result.to_json()  # 有理数端点写成字符串，不转成float。
decision = width_gate(result, F(1,10)).to_json()
```

## 比值、单位与符号基线

`ratio_interval(x,b)` 返回 x/b 的四角极值；`relative_change_interval(x,b)` 返回 x/b−1，两个接口不混用。要求 b.lower>0，允许 x 为负。分母含零或全为负均在这个受限支持域之外，直接拒绝。

在独立矩形 `x∈[l,u],b∈[v,w],v>0` 下，四角给出真实极值；连续映射的像为区间。若真实 x 与 b 共享依赖，矩形仍是安全外放松，但可能不紧。例如真实 x=b∈[1,2] 时比值恰为 1，而只给两个独立区间会得到 [1/2,2]。不能将丢失依赖造成的宽度称为自然语义不可识别。

`rescale_interval` 只接受正有理比例。把 x 与 b 同时乘同一比例时，ratio 和 relative_change 的 Fraction 结果精确不变，之后相同参数的概率包络也相同。这里只验证已给元组的单位变换；不认证文本单位、币种、汇率时点或解析器不变性。

`difference_interval(x,b)` 给 x−b 的区间。`label_set` 对数值区间返回可能的 `below/equal/above`；默认零容差为 0，equal 指恰为 0；非零容差时 equal 指位于所声明的闭容差带。`robust_label` 只有在所有候选共同只允许一个标签时返回该标签，否则返回 None。这些是比较关系，不能改名为投资立场或市场方向。若任务就是该比较关系，符号基线已经给出了直接答案，不需要保留一个学习头来制造研究必要性。

## 超越函数的严格外包络

核心没有使用 `math.exp`、浮点 sigmoid、nextafter 或将中心值伪装成证明。对于有理 x≥0，令 `S_n=Σ_{k=0}^n x^k/k!`。在 `x<n+2` 时，从下一项开始，后续项之间的比例不超过 `r=x/(n+2)<1`，故：

```text
S_n ≤ exp(x) ≤ S_n + [x^(n+1)/(n+1)!] / [1−x/(n+2)]。
```

程序用精确 Fraction 递推，只有尾界不超过所请求容差才返回。`max_terms` 计入 k=0 项，默认 1,000；默认最大绝对参数为 50。这是实现预算，不是数学定义域；达到上限而未满足尾界则失败。负参数使用正 exp 区间的倒数 `[1/U,1/L]`，且 L≥1，因此倒数不放大该绝对宽度。

sigmoid 使用 `E=exp(|z|)` 的严格包络。z≥0 时用 `E/(1+E)`，z<0 时用 `1/(1+E)`；这两种函数在 E≥1 上的导数幅值不超过 1/4，所以返回宽度不超过所请求容差。缓存只复用相同精确参数与相同预算的已证结果，不改变数值；预算耗尽没有近似兜底。

## 每分支真实极值与数值误差分别保存

仿射映射的 η 区间通过两个端点得到，负斜率时自动交换端点。首类 `q₀=σ(θ₀−η)` 随 η 下降，尾类 `q_last=σ(η−θ_last)` 随 η 上升。中间类为：

```text
q_i(η) = σ(θ_i−η) − σ(θ_(i−1)−η)。
```

其峰在相邻阈值中点 `(θ_i+θ_(i−1))/2`；最小值在 η 区间端点。因此程序为每类计算两端，对内部类再加入落在区间内的中点，不能只查两端。真实连续范围的这条极值刻画来自模型结构；有限网格只是实现检查。

每次 sigmoid 的请求容差取公开 tolerance 的 1/4。两个 sigmoid 相减使用 `[L_hi−U_lo,U_hi−L_lo]`，再与 [0,1] 相交；其数值不确定宽度不超过 tolerance/2。每个候选真实值都被严格包含。对若干候选值取最小值，其包络为 `[min L,min U]`，取最大值为 `[max L,max U]`；这些操作不会将各候选最大数值宽度累加。因此每个真实极值的数值不确定宽度至多为公开 tolerance，单侧误差也至多为 tolerance。

`branch_probability_extrema` 返回每类的 `RangeCertificate(minimum,maximum)`，分别包住真实最小值和最大值；`branch_probability_ranges` 返回 `[minimum.lower,maximum.upper]`。这是严格的**数值外包络**，不是声称超越函数端点本身已化为精确有理数。真实范围的外扩总宽度可达两个端点数值误差之和，不能把 tolerance 当成真实语义范围宽度。

## 有限语义联合与宽度三态门

`semantic_envelope` 对所有候选的最小值取 min、最大值取 max，不假设或估计分支权重。`Envelope.class_intervals` 是最终逐坐标外包络；`extrema` 保留联合真极值的数值不确定性，`branch_intervals` 保留各分支计算范围。理论上的逐坐标 hull 对声明的候选集合最紧，机器计算是它的有理外包络。

这不表示 box 里每个点都可达到：不同坐标的极值可能来自不同 η 或不同分支，甚至 box 的某些角点之和大于 1，不是概率向量。它也不证明真实解析解释在候选集合中，更不证明候选都是现实可行的；遗漏候选会破坏覆盖，误报候选会增加保守性。

`width_gate` 判断真实最大坐标范围宽度 `D=max_i(max q_i−min q_i)` 是否不超过阈值 w。若真最小值位于 [a,b]、真最大值位于 [c,d]，则该坐标真宽度位于 `[max(0,c−b),d−a]`。再对各坐标分别取最大下界／最大上界，得到 D 的区间 [L_D,U_D]：

- `pass`：U_D≤w，已证宽度通过。
- `fail`：L_D>w，已证对当前要求全覆盖的候选集合超宽。
- `undetermined`：其余情况，当前数值精度不能区分，应细化预算或保留未定。

仅 outer width>w 不构成 fail；这是本组件需要避免的关键误用。即使 fail，也只针对当前候选集合和模型，不是未经语义审计的自然文本不可能性证明，更不是金融部署风险验收。

`width_gate` 的入口契约是消费当前检查器 `semantic_envelope` 成功生成、未被改写的 Envelope 对象。Python 类型检查并不能证明一个手工构造的对象具有正确极值；该函数**不是读取外来 JSON 后独立验证数学证书或签名的验签器**。同样，`target_id/class_labels` 仅检查声明一致，无法验证声明背后的自然语言语义；外部 JSON、解析器或传输链需要另设验证接口，本轮未实现。

## 已执行的有限检查

```powershell
& '..\130U-FinLLM\.venv\Scripts\python.exe' -X utf8 -m unittest research.numeric.test_semantic_envelope -v
```

2026-11-16 首次 14 项测试通过，约 0.099 秒。测试包括正负 exp 和 sigmoid、预算失败、正尺度精确单位不变、零／负基准拒绝、负斜率、内部峰、逐分支包络、共同目标/schema、符号拒绝、宽度三态和严格类型。网格检查使用 100 个比值点与 39 个 η 点，均为人工有理构造，不是自然文本数据。

测试另使用独立的有理 Lagrange 余项 oracle：96 次 Taylor 部分和配合 `exp(x)≤3^ceil(x)`（x≥0，x=0 时为等号）上界构成更窄参考区间；这与实现使用的几何尾界不同，也不依赖浮点指数作真值。参考区间被实现包络包含，只提供这些有限点的数值交叉检查；全域有效性来自余项推导和极值证明。父任务 runner 与独立审查的更广构造记录另行保存，本文不预填其结果。
