# 文献核验与研究差异：供 Fable 复核

日期：2026-11-15（America/New_York） · 联网：是 · 检索截止：2026-11-15 · 状态：首轮重点核验，非完整系统综述。

## Charter

目标：核查 P1/P2 的数学组件是否已有，以及剩余差异是否足以支持研究投入。范围 / 对象 / 具体单位：可认证金融语言模型 / 信息集与数字敏感度 / 原论文定理、威胁模型、输入表示和审计假设。模式：探索性，先找否决证据，不以“未检索到”认定原创。

问题：Q03、Q29 关注残余错标如何传至模型与统计量；Q10、Q13、Q31 关注硬结构保证；Q30 关注抽样审计；Q32 关注解析证书。Q01、Q02、Q12、Q14 提供必要背景，其他题本轮保留为开放项。

## Canonical sources

排序：原论文全文 / 作者正式发布资料（rank 1）；XBRL International 官方规范说明（rank 2）；导师包（待验证假设）。只使用已打开的一手来源支持下表。搜索摘要仅作为定位工具。没有向 sec.gov 请求数据；SEC 数量、字段、许可与历史可得时间未在本轮核实。

## Findings ledger

| ID | 已核实主张 | 来源、版本与定位 | 层级 | 关联 |
|---|---|---|---|---|
| L01 | 无前视可表述为 temporal non-interference；作者明确将模型权重视为黑箱，模型预训练截止日纳入证书仍属下一步 | [Fonseca, 2607.04958v1](https://arxiv.org/html/2607.04958v1)，2026-07-06，§9 limitations | 全文，rank 1；预印本 | Q03 |
| L02 | 确定性分片训练、稳定哈希与票差产生投毒鲁棒证书；原始威胁预算按集合对称差计数 | [Levine & Feizi, DPA, 2006.14768v2](https://arxiv.org/html/2006.14768v2)，2021-03-18，§3.2、Theorem 1、Appendix A；ICLR 2021 | 全文，rank 1 | Q03/Q29 |
| L03 | Finite Aggregation 使用重叠子集扩展 DPA；单条污染对多个基分类器的影响须按其设计计数 | [Wang et al., 2202.02628v1](https://arxiv.org/html/2202.02628v1)，§3；发表版本为 ICML 2022 | 全文所读为 v1，rank 1 | Q29 |
| L04 | 对 bagging 的共同投毒可写为 BILP，界同时被改变的预测数量；并有 hash bagging | [Chen et al., 2205.13176v2](https://arxiv.org/html/2205.13176v2)，2022-09-06，§3–4、Appendix B；ICML 2022 | 全文，rank 1 | Q29 |
| L05 | Lipschitz 网络加线性残差强制指定坐标单调，属于已有架构 | [Kitouni et al., 2112.00038v2](https://arxiv.org/html/2112.00038v2)，2023-03-15，§2.1–2.2 | 全文，rank 1 | Q10 |
| L06 | 更一般的可表达单调网络使用权重约束与单一残差；ICLR 2023 | [Kitouni et al., 2307.07512](https://arxiv.org/abs/2307.07512)，2023-07-14 | 摘要，rank 1 | Q10 |
| L07 | 无量纲特征实现精确单位等变；基本方法由量纲零单项式构造 | [Villar et al., 2204.00887v2](https://arxiv.org/html/2204.00887v2)，§4、Appendix；[JMLR 24(109)](https://www.jmlr.org/papers/v24/22-0680.html)，2023 | 全文，rank 1 | Q13 |
| L08 | 无放回抽样的超几何置信序列已经有 anytime-valid 构造 | [Waudby-Smith & Ramdas, 2006.04347v4](https://arxiv.org/html/2006.04347v4)，§2；NeurIPS 2020 | 全文，rank 1 | Q30 |
| L09 | 加权无放回财务审计可用 test martingale，并可纳入不可靠辅助信息 | [Shekhar et al., 2305.06884v1](https://arxiv.org/html/2305.06884v1)，2023-05-08，§2–4 | 全文，rank 1 | Q30 |
| L10 | 分布随协变量按随机序变化是已有统计对象 | [Henzi, Ziegel & Gneiting, 1909.03725v3](https://arxiv.org/html/1909.03725v3)，2021-09-28，§2；JRSSB 2021 | 全文，rank 1 | Q31 |
| L11 | xVal 把占位符 embedding 乘以数值，再送入 transformer 主干 | [Golkar et al., 2310.02989v2](https://arxiv.org/html/2310.02989v2)，2024-12-15，§2.1 | 全文，rank 1 | Q10/Q12 |
| L12 | iXBRL 的 scale 为十次幂缩放；负号通过 sign 表达，显示括号不能当作唯一依据 | [Inline XBRL Part 0: Primer 1.1](https://www.xbrl.org/WGN/inlineXBRL-part0/WGN-2026-07-14/inlineXBRL-part0-WGN-2026-07-14.html)，2026-07-14，§4、§5.9–5.10 | 官方工作组说明全文，rank 2；非完整实现规范 | Q14/Q32 |
| L13 | FiNER 的数字标签依赖上下文；数字子词碎片化影响性能 | [Loukas et al., 2203.06482v2](https://arxiv.org/abs/2203.06482)，2022-04-19；ACL 2022 | 摘要，rank 1 | Q14/Q32 |
| L14 | TAT-QA 将表格和文本中的抽取与符号计算组合 | [Zhu et al., ACL 2021](https://aclanthology.org/2021.acl-long.254/) | 摘要，rank 1；未把 QA 分数视为解析准确率 | Q32 |
| L15 | DatedGPT 采用逐年抓取日期过滤；其指令生成还使用现代模型和词汇限制 | [Yan et al., 2603.11838v2](https://arxiv.org/html/2603.11838v2)，2026-07-23，§2–3 | 全文，rank 1；预印本 | Q01/Q02/Q03 |
| L16 | Chronologically Consistent LLMs 是已有时间限制训练方向 | [He et al., 2502.21206v3](https://arxiv.org/abs/2502.21206)，2025-07-06 | 摘要，rank 1 | Q01 |
| L17 | VLM 上已有基于尺度等变的微调；其摘要报告接近等变，未给出本文需要的金融文本硬证书 | [Tan et al., 2609.00658v3](https://arxiv.org/abs/2609.00658)，2026-10-04 | 摘要，rank 1；预印本 | Q13/Q24 |

## Scope filter

删去“换到金融应用就构成理论创新”的推论：L02–L10 已覆盖各主要数学组件。删去“零发现意味着没有污染”的推论：审计只产生指定抽样模型下的置信结论。删去“概率校准证明某条预测正确”的推论。保留证书链作为组织方法，但 union bound 的组合本身不是新定理。

## Object filter

修正“P2 必须从零训练”：只要输入数值不绕过受约束通道，文本编码器可以是冻结的已有模型；它的预训练历史不影响对当前输入的数学单调性。若同时要求 P1 的历史信息约束，则必须另审训练来源。修正“xVal 可直接接上 T2.2”：L11 的主干依赖数字，所以直接使用不能满足 c 独立于 g。修正“权威时间戳就是概率为零的正确性”：需要绑定内容版本、可得时间语义、撤回/修订、提取与抓取流程，当前仍是条件假设。

## Conclusions

1. **P1 是有潜力但尚未证明新颖的组合研究。** L01 未解决模型权重污染；L02–L04 已解决投毒与集体鲁棒基本部件；L08–L09 已解决审计统计基础。剩余候选是“时间来源假设—审计预算—污染影响—固定回测统计量区间”的可计算连接与紧度，而不是首次提出任一部件。
2. **P2 的基础定理不能包装成原创。** L05–L07、L10–L11 已覆盖单调、量纲、随机序、连续数字表示。可研究的问题是金融语义规范何时合理、数值旁路如何严格隔离、解析错误如何进入端到端保证，以及相较符号/有序回归基线是否仍有必要。
3. **G1 新颖性证据只到“部分已有、差异未排尽”。** 没有证据支持“未见同类工作”的高置信度结论。也不能据此判两条主线全部失败；尚需完成更窄差异的前向/后向引文追踪。
4. **有限语料审计是成熟统计技术迁移。** L08–L09 已提供序贯和辅助信息工具；rule of three 的尺度不能独立作为新理论贡献。

## Next steps / Risks

- 优先检查 Q03/Q29 的 2023–2026 生成模型与语言模型投毒证书、unlearning/stability 路线；本轮没有穷尽。
- 用明确的 bounded statistic 定义 clean comparator，避免把反事实经验区间冒充未来总体保证。
- P2 加入“冻结文本模型 + 硬头”和“纯符号/有序回归”基线；若二者足够，就撤回从零训练的必要性叙事。
- 按用户当前离线边界，真实来源验证暂不执行；可待用户主动提供本地合法材料或改变边界后继续。当前不提供 EDGAR 年度数量、accepted 语义或许可结论，也不请求用户对外联系。
- 对解析器在独立、按公司/报告成簇的真实样本上做全元组错误审计；不能拿 FiNER 标签准确率或 TAT-QA QA 分数替代。
- 2026 年论文均按所读版本判断；不凭 preprint 的期刊模板声称已经正式接收。

## 检索记录与边界

**停止记录：** 本轮执行期间用户明确要求不联系外部、在本地自行研究。收到主代理转达后立即停止所有新增网络请求；此后的答案只引用停止前已取回的一手资料与本地推导。没有联系作者、发送邮件、发帖或向第三方投递研究材料。未核实子题继续标未完成，不通过新增联网补齐。

检索执行日 2026-11-15；关键词包括 `Deep Partition Aggregation Levine Feizi`、`Look-Ahead-Freedom as Temporal Non-Interference`、`financial language certified monotonic numeric`、`language model units equivariance`、`ordinal regression stochastic dominance cumulative link monotonic`、`Collective Robustness Certificates`、`confidence sequences sampling without replacement`、`FiNER-139`、`TAT-QA`。已从相关结果打开上表原论文；新发现 L04、L09、L10、L17 扩大了导师原始候选集。没有使用论坛或自动生成综述支持结论。

访问限制：NeurIPS 2020 PDF 一次超时，改读 arXiv 全文；JRSSB IDR 页面不可读取，改读作者 arXiv 全文；McCullagh 作者 PDF 可打开但正文未成功提取，本轮不把它列作已精读全文。JMLR 首次试探的 22-0689 是无关文章，已排除，正确来源为 22-0680。

完整问题覆盖状态见 [question_status.md](question_status.md)。已写重点答案的“部分完成”表示题内仍有未核实子项，并非整题完成。
