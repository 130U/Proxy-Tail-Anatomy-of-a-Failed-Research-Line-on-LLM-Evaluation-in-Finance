# T2 心理物理学与数字表征查重

检索日期：2026-11-16（America/New_York）。本文件是独立文献支线；没有执行模型评分、复现作者实验或上传内容。

## Charter

- 目标：回答 Q2「T2 是否已有实质相同研究」和 Q3「剩余差异是否足够支持原题继续」。
- 范围／对象／单位：LLM 数字行为／金额与比例诱发的评分曲线／幅度、正负方向、阈值、等价单位及重复测量。
- 类型：探索式查重；将作者报告与本次重现实测严格分开。
- 判断标准：比较操纵变量、输出构念、函数形式和控制条件；论文标题相似不等于同题。

## Canonical sources

| 优先级 | 原始来源 | 日期及阅读程度 |
|---|---|---|
| 1 | Marks & Vollberg, [The psychophysics of affect in large language models](https://arxiv.org/abs/2610.40985)；[PDF](https://arxiv.org/pdf/2610.40985) | 2026-10-29 预印本；已核验正文方法、结果、Fig. 3、表 2 及补充表 S1、S4，非仅摘要 |
| 1 | Atta-Duncan, [Same Quantity, Different Answer: Numerical Representation Invariance in Language Models](https://arxiv.org/html/2609.25009v1) | 原始页面标注 2026-07-27，编号却为 2609；保留元数据差异，不自行纠正。已核验正文 §§3–5、8–9 |
| 1 | Cacioli, [Weber's Law in Transformer Magnitude Representations](https://arxiv.org/html/2603.20642v1) | 2026-03-21 预印本；已核验 §§3.3–3.4、4.2–4.3 |
| 1 | Shah et al., [Numeric Magnitude Comparison Effects in Large Language Models](https://aclanthology.org/2023.findings-acl.383/)；[PDF](https://aclanthology.org/2023.findings-acl.383.pdf) | Findings of ACL 2023，2023-07；已核验正文研究对象与方法 |
| 3 | [Marks & Vollberg 作者仓库](https://github.com/joeamarks/Psychophysics_of_Affect_in_LLMs) | 已核验仓库存在、公开、默认分支 main；未执行代码，未独立复算数据 |

## Findings ledger

| ID | 可核验发现 | 定位 | 关系 |
|---|---|---|---|
| P1 | Marks & Vollberg 的 Study 2 已测股价百分比变动到情感分数的正负曲线。其问题是第一人称预期感受，分数 −50 至 +50；与公司新闻情绪相关但构念不同。 | PDF pp.14–15，Tasks and stimuli；Fig.3 p.9 | Q2：曲线／正负方向强重合 |
| P2 | 固定 20 个幅度点覆盖 0.2–12；Study 1 用英镑，Study 2 用百分比。每模型×条件 30 个独立调用序列；比较独立提示、历史评分入上下文、同提示联合评分。股票实验只覆盖 gpt-5-nano 与 kimi-k2.5。 | PDF pp.12–16 | Q2：重复与情境控制已有先例 |
| P3 | 股票实验报告递减敏感性和收益侧较强，联合评分接近线性；其幂函数拟合并非 T2 的线性／对数／饱和三选一。论文未给出 T2 的 9.9/10.1 局部关口或等量换单位实验。 | PDF Fig.3、Table 2、pp.17–18 | Q2：部分实质覆盖；不是全部实验一致 |
| P4 | Same Quantity 用 3,600 个精确有理数数学文字题、8,600 个提示测试五族等值变换，含单位、百分比、科学记数等；评估五个开放权重系统。 | HTML §§3–4 | Q2：单位不变性方法已有强先例 |
| P5 | 该文区分解析器拒绝与数值错误；单位误差集中在特定模型和模板。主实验每提示一次 greedy 请求，不能代表 T2 的情绪分差／重测噪声比较。 | HTML §§5、8 | Q3：识别替代解释，限制外推 |
| P6 | Weber 论文拟合线性、对数、幂律的隐层几何，并做数字比较及 digit/unit-boundary 控制；作者明确指出对数几何不保证相同行为表现。 | HTML §§3.3–3.4、4.2–4.3 | Q2：非情绪曲线，不能据此判完全撞题 |
| P7 | ACL 2023 论文研究数字词／阿拉伯数字嵌入的距离、大小、比例效应，通过 linking hypothesis 对应人类反应时。 | PDF pp.1–3 | Q2：表征层前史，非金融情绪测量 |

## Scope filter

排除将“数值表征是对数的”推成“金融情绪分数必然对数”的论断（P6–P7）；表征几何、任务选择和情感评分是不同输出。排除用收益／损失选择中的 loss aversion 参数替代情绪分数的正负非对称。网页摘要仅用于定位；结论采用已打开的原始正文。

## Object filter

P1–P3 改为“核心曲线和非对称的强先例”，不表述为 T2 全部完成：第一人称感受与第三人称新闻情绪不同，固定 20 点与 25 个对数点不同，原论文未测 T2 关口及单位条件。P4–P5 改为“等值表示不变性的先例”，不把数学文字题准确率冒充情绪效应。P6–P7 仅保留为设计依据。

## Conclusions

1. **原版 T2 的宽泛贡献不足以按“首次发现幅度响应曲线／盈亏非对称”继续立项。** 2026-10-29 预印本已经在股票百分比语境画出相关曲线并操纵比较上下文（P1–P3）。这是最重要的止损证据。
2. **没有证据宣布“三个实验逐项完全相同”。** 本支线未确认金融新闻在 9.9/10.1 附近的局部跳变，或 million/billion 与 percent/basis-point 改写相对于重测噪声的效应已在同一研究完成（P3–P5）。
3. 若主任务采用“发现核心已做即止”的策略，应停止原版实验，将公司新闻构念、阈值和单位仅列为待重新立题的差异；这些差异本身还不是已验证的新颖性。若要保留新题，必须事先说明为何第三人称金融评价不同于已有 affect 评分，并提出超出“换模板再画图”的可证伪机制（P1–P7）。

## Next steps / Risks

- 以主代理的金融文本检索结果补齐整体判定；本支线的“未找到”不构成全领域不存在。
- 作者股票结果仅来自两个模型；跨模型、跨提示、跨版本不宜泛化。其 gateway 模型快照及有效温度存在作者明示的复现限制（Marks & Vollberg，Methods）。
- 固定实体规模、金融基线和合理取值域后才能解释单调性；将利润下降延伸超过 100%，或把裁员数量直接当作股东损失强度，会改变经济含义。这些是设计判断，尚非实验发现。
- 等值表示比较应对输入、解析和实际语义分别核验。单位转换导致解析失败与情绪响应改变不是同一个现象（P5）。

## 检索边界与记录

已使用网页检索并回到原始论文：

1. `large language models numerical magnitude psychophysics Weber Fechner law sentiment`
2. `large language models left digit bias price numerical magnitude`
3. `large language models unit invariance numerical framing financial sentiment`
4. `"large language models" "left-digit"`
5. `"large language models" "unit" "invariance" numbers`
6. `"language models" "loss aversion" magnitude`
7. `"language models" "numerical" "sentiment" "curve"`
8. `"LLM" "left-digit bias"`
9. `"language models" "unit invariance"`
10. `"LLM" "round numbers" bias pricing`

另外定向核验 arXiv:2610.40985、2609.25009、2603.20642 与 ACL:2023.findings-acl.383。搜索中发现的新闻转述、聚合站、rounding-output 偏好研究未作为输入阈值跳变的实证证据。没有声称完成半天或穷尽式系统综述；发现足以改变立项决策的近邻后收束检索。
