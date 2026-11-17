# 新 SEntFiN Phase 0：独立实施与证据审查

日期：2026-11-16。角色：内部 AI 反方审查员；不代表 Fable、导师或外部同行。全程离线，未联系任何外部人员。依据本地“学术研究-组织反方研究审查”技能及 reviewer 模板开展。

**结论：在所审查范围内，来源原任务的准备、训练和配对评估设计可以形成新的、范围受限的 Phase 0 基线证据。没有发现仍会改变本轮模型选择的 critical 实现错误；发现的 important 模型名称接口错误已修复并复测。这个判断不等于人工标签、完整事件独立性、历史可得性或旧 G0/G1 已通过。** 最终公开区间及归档复核见文末增量记录。

## 审查范围与证据边界

实际读取了 [PROTOCOL](../real_baseline/PROTOCOL.md)、[DESIGN_REVIEW](../real_baseline/DESIGN_REVIEW.md)、prepare/train/bootstrap 三套代码及构造测试、[评估实现](../evaluation/evaluate.py)及测试、[打包代码](https://github.com/130U/proxy-tail/blob/closeout-2026-11-17/research/package_handoff.py)及测试，以及匿名 [准备清单](../real_baseline/aggregate_manifest.json)和[训练汇总](../experiments/real_baseline/baseline_summary.json)。也查阅了本机 threadpoolctl 实现，核对线程枚举 fallback 的行为。

没有读取原始 CSV、`research/private/` 下的新闻文本、逐行标签、分区、预测或模型权重；没有人工重标标签，没有检查实际语义事件成员，没有重新训练真实模型。构造测试中的人工字符串与标签不属于真实私有语料。真实数据处理的字节验证和行级不变量由所审代码执行并记录；本审查独立检查代码、公开汇总的内部一致性及公开文件哈希，不能将其写成审查员逐条复核了真实数据。

本轮协议按执行记录在真实准备/训练前写定。最终主比较为运行前 PROTOCOL 的 **char−word test macro-F1**；DESIGN_REVIEW 建议的“开发集赢家−majority”没有被采纳。保留不同意见是合理的，不能在结果出来后把两者混成同一个事先指定分析。求解器 `lbfgs` 在训练前代码/config 中固定，原协议文字未逐项展开这个字段；本地文件摘要和执行记录并非外部可信时间戳。

## 逐项核验

| 项目 | 核验内容与结论 | 仍不能推出的结论 |
|---|---|---|
| 标签与目标输入 | 三类保持 negative/neutral/positive；同标题多实体不同标签合法。两主模型共用目标前缀及有词边界的字面替换，raw `input_text` 不作为特征。 | 不证明目标实体语义绑定、上市证券身份或投资立场真值。 |
| 严格解析与冲突 | AST 检查在 literal_eval 前拒绝重复原始键及规范化碰撞；跨行冲突键为规范标题＋规范实体，整键隔离；相同标签重复合并。 | 不证明来源标签正确或隔离后总体具有代表性。 |
| 近重复完整性 | 同一全局 token 顺序下，prefix 长度为 `|X|−ceil(.8|X|)+1`；合格对有足够公共 token，最早公共 token 必在双方 prefix 中。再用整数 Jaccard 判定及完整传递闭包。 | 只覆盖定义的词法关系，不能覆盖全部同一事件或跨来源依赖。 |
| 分组与分区 | 有效标题先于标签清理建图；隔离标题仍可作为桥，避免标签决定图拆分。组件内容摘要与 seed 决定分区，组身份不依赖 union-find 根序号。空 token 标题没有被全部合并。 | 不是时间划分、未见实体划分，也不是从未接触过的外部确认集。 |
| 拟合与选择 | 词表、IDF、最大特征截断及 LR 只拟合 train；每系统三个 C 只用 dev 固定三类 macro-F1 选择，精确平局取小 C；全部系统完成选择后才 test predict；不做 train+dev refit。 | 三种特征各自开发选择仍不使 bootstrap 包含整个研究搜索过程的不确定性。 |
| 输入与身份绑定 | 真实 CLI 强制 manifest；在任何 fit 前比较 prepared rows 的 SHA256 及类 schema。拒绝覆盖已有真实输出；新模型没有加载旧 checkpoint。 | 不能恢复旧 24M 权重或旧逐行分数。 |
| 配对区间 | 显式三类名称，混淆矩阵方向正确；每次以相同 multinomial 组计数作用于两模型，先汇总行计数再算固定三类指标。缺失、重复、错组、错真值及错模型集合拒绝。 | 不是每组等权指标、精确有限样本证书、训练过程区间或漂移保证。 |
| 私有边界 | 数据准备/训练路径限制在 private；模型、词表及逐行预测不进入 aggregate。打包排除任意大小写的 private 路径组件与文件符号链接。 | 本次检查不是对所有旧公共文稿作逐字隐私取证；最终归档只按实际成员及清单复核。 |

## 问题、修补与保留意见

### I01 — important，已关闭：训练输出与评估入口模型名不一致

初版训练器联合预测使用 `word_tfidf_lr / char_tfidf_lr / entity_only_tfidf_lr`，而 bootstrap 入口要求 `word / char / entity_only`。两个模块的各自测试都可能通过，但真实评估将被 schema 检查拒绝。审查发现后立即通知主代理。

修复采用显式 `PREDICTION_KEYS` 映射：私有输入保持训练器长名称，公开展示用短名称；验证要求完整、唯一的长名称集合。新增测试直接引入训练器 `SYSTEMS`，并拒绝旧短名称输入。独立重跑 3 项 bootstrap 测试通过。此修复没有改动模型、C、分组、特征或已冻结的主比较，不构成测试分数驱动选择。

### I02 — important，科学边界仍开放：词法簇不证明独立事件或历史可得性

有 1,570 个测试词法簇和零跨区定义近重复边，只能证明当前算法的词法隔离。不同词法描述仍可能对应同一新闻事件；本轮全部语料参与构图及冲突清理，来源语料亦非首次接触的外部样本。因此名义 95% 区间只能按所述条件作近似解释。修补方式是保留这一限制；未来若提出事件独立、历史无前视或部署风险主张，必须另行建立事件/时间证据和对应设计。当前代码测试不能关闭这项科学门。

### I03 — important，科学边界仍开放：标签与简单模型比较不足以证明语言模型必要性

测试 entity-only macro-F1 为 0.533588，说明在该划分上实体身份和标签先验具备预测性。它是替代解释的诊断，不能将它与主模型 F1 的比值称为“解释了多少百分比的性能”：macro-F1 不是可加贡献分解，两者也是不同拟合模型。主模型的目标字面匹配不是语义解析审计。

本轮没有人工重标、完整事件审查、FinBERT 或零样本 LLM 对照；不能称完成原导师三基线要求、证明某类模型普遍优劣或证明必须从零预训练语言模型。当前关闭的是“有一个可检查的新来源任务基线”，并非旧 G0/G1、金融投资标签金标准或研究新颖性。

### M01 — minor，说明缺口已补：聚合流水账的分母必须保留

准备汇总的 13 是异常源行，7 是冲突标题—实体键，73 是合并的额外实体出现次数。它们不能直接相加，也不能把 7 写成冲突源行数。PREPARE_README 已明确此点。当前主 manifest 未给完整展开实体出现数与冲突实体出现数，故仅由该表不能完整核销所有清理步骤；如补充，应保留原始运行身份与哈希，不静默改写训练已绑定的 manifest。

作者随后增补 [PREPARATION_ACCOUNTING](../real_baseline/PREPARATION_ACCOUNTING.md)，保留原 manifest 与训练输入不变，分别给出 `10,753=13+10,740` 源行和 `14,371=14+73+14,284` 成功解析实体出现核销。已独立阅读并检查这些等式及分区计数一致性；补计数来自作者对固定源 CSV 的只读核算，本审查员没有重新读取源行。说明缺口关闭，不升级为对原始标签语义的独立复核。

### M02 — minor，两个实体匹配计数口径不同

prepare 的原始 substring 未匹配数为 19；训练使用有词边界、大小写不敏感的 literal marker，未匹配为 train 81、dev 10、test 21，共 112。这不是算术矛盾。报告应保留各自定义，不能说全部语义实体绑定已成功，也不能用 19 代替模型实际 marker 未匹配数。

## 线程修复与预算证据

本机 threadpoolctl 的 Windows snapshot 枚举路径异常在构造测试阶段暴露。实现先尝试正常控制器，仅在 FileNotFoundError 且为 Windows 时，使用 context 内的 patch 让库走它自身的 Unicode 模块枚举 fallback。独立读取库源码确认返回 None 会进入该 fallback；退出 context 恢复 patch，没有改写 site-packages。失败不会被当成成功忽略。

训练前后各有三个数值库报告配置线程数为 2，真实运行记录了此发现方式。其含义是库自报线程配置，不是实测 OS 峰值线程数或进程只存在两条线程。环境变量是进程内启动请求。实际训练及输出总耗时 13.809371 秒，9 个 LR 候选均没有收敛警告；峰值内存未测，不能据此宣称已验证 RAM≤2GB。

## 独立检查与结果算术

独立执行了 prepare 12、train 8、初版 bootstrap 2 项构造测试，共 22 项通过（0.825 秒）；另外 evaluation 8 与 package 1，共 9 项通过（0.348 秒）。接口修复后只重跑受影响的 bootstrap 3 项，全部通过。没有重复旧数学全套，也没有重新训练真实模型。

另构造了三个不等大簇，穷举全部 27 种有放回组抽样并重复四次，以独立 Fraction 混淆矩阵公式手算 macro-F1、两模型配对差及分位数。与 evaluator 的点估计和区间一致；该 oracle 检查的是组加权与配对实现，不是实际语料上的覆盖率证明。

由公开训练汇总的全部 21 份混淆矩阵独立重算 accuracy、macro-F1 及支持数，均与精确分数记录一致。三个 selected C 分别为 word 10、char 1、entity-only 0.1，均是列出的 dev 三候选精确最优。公开训练源码哈希、manifest 文件哈希和配置哈希均重新计算一致；数据摘要在准备及训练汇总间一致，实际私有字节没有由本审查员重读。

| 系统 | 固定 C | Test macro-F1 | Test accuracy |
|---|---:|---:|---:|
| majority | — | 0.181295 | 0.373517 |
| word TF-IDF LR | 10 | 0.792016 | 0.794020 |
| char TF-IDF LR | 1 | 0.754783 | 0.753678 |
| entity-only TF-IDF LR | 0.1 | 0.533588 | 0.537257 |

准备记录的保留实体行数为 14,284；train/dev/test 为 10,041/2,136/2,107，测试有 1,570 个词法簇。四系统在同一冻结测试行上报告；没有按测试结果改变主比较方向。字面任务上的强词语基线是后续研究必须解释和超过的参照，不自动产生理论创新。

## 最终增量复核

已读取 [bootstrap_summary](../experiments/real_baseline/bootstrap_summary.json)：2,107 行、1,570 个词法簇、10,000 次抽样、seed 130。主配对差为 **−0.0372334174**，名义 95% percentile 区间为 **[−0.0530594770, −0.0215595431]**，方向保留 char−word。四系统点估计均与训练汇总一致；没有用两个单模型 CI 的端点相减来代替配对 CI。

另阅读了 [实验报告](../experiments/real_baseline/report.md)、[第四轮进展](2026-11-16-round4.md)和[审查回应](../real_baseline/REVIEW_RESPONSE.md)。它们保留了主比较设计分歧、不同匹配口径、身份捷径诊断限制和旧 G0 未通过状态；未发现将本轮成绩直接冒充旧模型分数或历史投资证书的主张。

独立检查了评估源码文件哈希，以及公开汇总间三条身份绑定：prepared rows 摘要、准备 manifest 摘要、联合测试预测摘要；全部一致。联合预测摘要为 `d18a8a43c8ee10c5ce248ae7d0e96207ce759cbdf238dc36436f911e7f10adab`。这里没有重新打开或重算真实逐行预测。真实 bootstrap 用时 2.306168 秒；其三次系统汇总复用固定预测，不是新增模型训练或重新选参。

最终解释可以写为：“在本次来源原任务的固定非时间词法组划分和预定分析下，word 的测试 macro-F1 高于 char；所给配对近似区间方向一致。”实体先验、来源测量误差、跨簇事件关联以及先前研究者接触仍是未排除的解释。I01 的工程问题已关闭；I02/I03 的科学门仍开放。

归档边界：先检查实际工作树的 `package_handoff.files()`，当时 115 个候选公共文件的 private 路径成员及模型权重成员均为 0；构造私有目录排除测试已通过。随后独立检查本轮首次重建的第四轮 zip（不是沿用第三轮清单）：共 123 个成员，其中 122 个 payload 与 HANDOFF_MANIFEST 逐项一一对应，所有字节数与 SHA256 匹配，CRC 检查通过。没有 private 路径组件、模型权重后缀、CSV 或 JSONL 成员；本轮协议、回应、计数核销、审查及两个 aggregate 结果均在包中。先检查成员边界，再读取公共清单及公共成员做哈希；未打开私有产物。

该检查快照 zip SHA256 为 `bc8fd9825043b11367430affed0dff52bb4ab835afe9dc313533d25b322a9c2b`。本段补记会由主代理再打入最终包，因此最终 zip 自身摘要必然不同，应以最终交付记录为准；不能在包内嵌入它自身的最终 SHA256。打包代码只更新第四轮索引、阅读次序和状态描述，其 private 排除逻辑保持不变。

### 审查快照 SHA256

路径相对 `research/`。这些是本次审查的公开内容身份；打包入口摘要已更新至第四轮归档版本。

| 文件 | SHA256 |
|---|---|
| `real_baseline/PROTOCOL.md` | `9bc87c797f415c63c2f70cc59d0ae85ca53f58a0280ec57e24d4a15eb36dfda3` |
| `real_baseline/DESIGN_REVIEW.md` | `377f6cd944a2c7777c481041df2fa029df79b778054d7aca8d04b29bd4758954` |
| `real_baseline/prepare.py` | `c7f56b29875b6e76b7d2201cb4de6bea329c97b3582523218424096af53af06c` |
| `real_baseline/test_prepare.py` | `ff856de047249c9062379add77153e11d7138dd80061e414f54b7e6371d922f9` |
| `real_baseline/train_baselines.py` | `4859f8cfd01eb4650285116476c8a61f6b19bbe5790a34b58fe186c40b5e1136` |
| `real_baseline/test_train_baselines.py` | `1f791e588987a496b6d46f71256e59c52c4152b902f047f15fd46f6794e6f84f` |
| `real_baseline/bootstrap_results.py` | `c677b85f551294239a0088d1e12d0c272d3e7a8d1f8675d6d332e2c99e5cc8d6` |
| `real_baseline/test_bootstrap_results.py` | `27b000dc48ff8742a55e0416d0e5c6b0be67c605929448bf7850830ab9eba626` |
| `evaluation/evaluate.py` | `2b1ffc7c03ed92918e3de35e2c4c5269454587017998e0d3416983def7b73d00` |
| `evaluation/test_evaluate.py` | `b396d753af9829dd4f7c0e6e5b49449f13825a0186c71b10b1901b8fe49af5b4` |
| `package_handoff.py` | `1b6b455b8b65943d26f4715ad477979fad678e2f255f9448eaf9b72d75ad8539` |
| `test_package_handoff.py` | `e906a13f5a1e03e457c48015f61452f390cf86f1e836485cf3c948575ceaf81f` |
| `real_baseline/aggregate_manifest.json` | `6a8e8175bbbe391e866528e8b9d1e35fb3292c9d693da61948a4a91a44eac212` |
| `experiments/real_baseline/baseline_summary.json` | `6a4c98bd5dd92c45c747d6d8a123ab0fd5cd4bd8a78ebe63c495fdbd50e2a69a` |
| `experiments/real_baseline/bootstrap_summary.json` | `e9cf9561de7d9469463bc6f2c7ccd5859deabcc736325acedd0657a009267c1b` |
