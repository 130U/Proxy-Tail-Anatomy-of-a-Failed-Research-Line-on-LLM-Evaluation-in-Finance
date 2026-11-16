# WP0.6：公开声明与证据审计

日期：2026-11-15。审计版本：`8e4dd0b33c95ac2ac1a6015eba6f2dfafe5c1254`。没有修改 README、docs 或既有代码，没有对外发布。

## Charter

目标：区分公开代码实现、历史运行记录、仅方法设计和不可核实的效果；为重做研究定位提供可追溯基线。范围是此仓库的 README 与全部 docs，包含 PDF 的文字和图中文字。审计对象是可检验的事实/实现/效果主张；操作命令、任务定义和建议不自动当成完成声明。重复主张按下表合并，但每个来源文件在覆盖表中登记。研究类型：直接检查加描述性审计；不是对私有训练的外部复现，也不是新颖性判决。

本轮已读全部 Markdown 正文，并用本地 pypdf 提取 9 页项目 PDF 全文；没有对 PDF 做版面质量审查。联网核查和数据下载未用于本审计；用户最新要求不联系外部。原文中的外链及历史许可判断仅登记为历史记录，不重新背书。文件字节 SHA256 见 [claims_sources.json](claims_sources.json)。

## Canonical sources

1. 精确 commit 下的代码与配置，用于判定公开实现。
2. 仓库公开 `reports/*.json` 与 `docs/experiment-results.md`，用于判定存在什么历史记录；保留其“用户日志转录”“未下载 checkpoint”“本地替代测试”等原始限定。
3. README、docs 和 PDF，是被审计主张，不是证明自身真实的独立证据。
4. 导师快照用于提出问题；它未读代码，不能替代本轮检查。

分类 **A 有公开证据**、**B 只有设计/代码，无所称运行或效果证据**、**C 无法核实**。A 只在列明的范围成立，例如“存在一份报告”不等于“独立核实了模型权重”；B 不代表设计有错；C 不代表事实为假。

## Findings ledger

### 2.4B 相关声明（单列）

| ID | 公开主张/位置 | 分类与证据 | 建议措辞 |
|---|---|---|---|
| C01 | README:11、MODEL_CARD:3、INTRO:3、PDF p1：项目已有 private 2.4B model | C：未见该尺度 checkpoint、运行日志、任务预测或独立可核查的产物；公开代码和报告属于 24M | “项目公开了 24M Trial，并提出 2.4B 架构与训练方案；私有 2.4B 的执行状态尚无公开证据可核验。” |
| C02 | MODEL_CARD 的 28层、hidden2560、Q20/KV4、词表65536、参数2,397,459,968 | A（架构算式）/B（实例运行）：按公开参数分解算式成立，不能证明曾完成模型训练 | “所列 2.4B 配置的理论参数量为……；运行状态另列。” |
| C03 | PROJECT_OVERVIEW:21：2.4B 权重、词表、校准已重建 | C：缺实际词表 hash、weights hash、校准拟合记录 | “扩展到该尺度需要重新构建词表、权重与校准；完成与否待运行材料核验。” |
| C04 | PROJECT_OVERVIEW:34：2.4B 能处理更复杂关系且资源可管理 | B：设计动机，缺匹配预算对照、任务效果和实际吞吐/显存证据 | “选择该尺度的目标是……；收益与资源需求尚待实测。” |
| C05 | 32k gold，12k/4k/4k/4k/8k 划分 | B：原文已写 recipe allocation，未见实际 32k 库；不能算成已标注数量 | 保留“计划分配”，不要改写为“拥有/训练过 32k gold”。 |
| C06 | 50B + 5B 输入 token，4B/.75B/.20B/.05B mixture | B：原文已写 recipe，未见消费日志；与实际24M的26,115,096监督位置不同 | “配方预算”；另列实际已消费位置与独立文档。 |
| C07 | PDF p8：8k natural test + 3k family probes | B：图中附加 probe 规划；无对应测试预测 | “拟定测试与派生探针预算；探针不算新增独立样本。” |
| C08 | ENGINEERING:27、PDF p6：38.36GB FP32主要训练状态 | A（算术）：2,397,459,968 × 16 bytes = 38,359,359,488 bytes；不是实际峰值 | “参数、梯度、双Adam状态的静态估算38.36 GB，尚不含激活等，也不是T4运行记录。” |
| C09 | PROJECT_OVERVIEW:92、PDF p5：1GiB→0.5MiB输出张量 | A（算术）/B（该实现）：2×2048×65536×4 与2×65536×4字节正确；公开24M没有投影前gather | “理论张量尺寸对比；公开Trial仍投影全部位置，尚未测得此节省。” |
| C10 | 2.4B serves private workflow / personalized standards learned | C：私有使用或效果不可由24M记录证明 | “目标用途为个人研究；个性化学习效果尚无公开独立评测。” |

### 方法与实现

| ID | 主张 | 分类、公开证据与限制 | 建议措辞或保留条件 |
|---|---|---|---|
| C11 | 金融语义许可：INV/LBL/relabel，配对一致性与log-odds margin | B：TRAINING_SYSTEM:23起有定义；`src/finllm/training.py` 的实际阶段为pretrain/domain/sft/dpo；全src及scripts未见对应permission损失或编辑对管线 | “提出了监督规范；公开24M尚未实现/验证该损失。” 不把 DPO 当作该损失。 |
| C12 | 权限损失改善模型语义响应 | C：无同编辑样本CE对照或打乱许可对照 | “效果待匹配数据和预算消融”；本轮合成实验另报，不追溯替代历史结果。 |
| C13 | stance、metric direction、personal judgment 分开建模 | B：任务定义明确；MODEL_CARD:23明确公开接口只支持stance | “三个任务在方案中区分；公开Trial只实现stance。” |
| C14 | family先划分，再派生视图，避免事件泄漏 | A（部分构件）/B（完整方案）：`data.py:114–185` 联合id/group_id/event_id和词法去重后划分；没有通用QA/edit派生视图或family损失加权；TASK_REVIEW:23说旧数据event_id全空 | “实现了已知关系和词法重复分组；完整语义事件独立性尚未审计。” |
| C15 | 多卡全局有效分母公式 | B：公式在梯度平均前提下合理；公开trainer无DDP/all_reduce/world_size路径；单设备 accumulation 有实际分母修正 | “多卡方法规格”；不可称公开Trial已多卡验证。 |
| C16 | supervised hidden states在词表投影之前被选择 | B：公开`model.py:196`对全部位置lm_head；`training.py`之后才answer_logits筛选监督logits | “Trial在损失计算时选择答案位置，尚未实现投影前稀疏计算。” |
| C17 | packing使用segmented causal attention | B：`model.py:170–196`只接受二维padding mask并加普通causal mask；`TokenBlockDataset`只有input_ids/labels，没有segment IDs | “分段packing是2.4B方案；公开Trial没有该接口。” EOS不等于attention隔离。 |
| C18 | 24M random init、dense GQA/RoPE/RMSNorm/SwiGLU/QK norm、tied embedding | A：`model.py`、`configs/model_24m.json`，参数数有公开CPU检查报告；本次未重训 | 保留版本边界，不称架构机制本身原创。 |
| C19 | 全词表CE，三标签条件概率另算 | A：`training.py:24–47`中的answer_logits/sft_loss；`inference.py`筛选标签logits；不是三类CE替代词表CE | 可保留。 |
| C20 | 精确resume恢复optimizer/RNG/data cursor；新stage只移权重 | A（实现及历史局部测试）：`checkpoint.py`、`training.py`；`reports/expanded_continuation_checks_20261011.json`含同环境tiny CPU dropout逐位比较 | “在已验证硬件/软件/配置与输入契约内的恢复检查”；不推成任意硬件逐位确定性或所有分片训练证明。 |
| C21 | tokenizer是自训8192 BPE | A：`tokenizer.py:40–88`和`reports/seed_data_preparation.json`记录hash/vocab；训练输入是seed train的455篇抽样，Wikipedia快照20231101 + FOMC 2021–2024会议文本 | 保留自训声明；其候选来源包含2025-01发布的minutes，实际455篇的最晚可得时间仍需逐条核查，因此不能直接用于此前历史cutoff证书。 |
| C22 | tokenizer和LM训练排除评测文本 | A（机制）/C（全部事件无泄漏）：`preparation.py`冻结候选池、词法去重；SHA证明身份，不证明完全语义隔离 | “对冻结文本和指定近重复规则排除”；不称完整无泄漏证明。 |
| C23 | inference：三类概率、direction score、review标记、拒绝非法输入 | A：`inference.py`、`tokenizer.py`、`evaluation.py`；所称score的算式可直接检查 | 保留；score不是收益率/价格预测，也不代表校准后的真实逐点错误概率。 |
| C24 | temperature/threshold分开拟合且绑定权重、词表、target_mode | A（代码）：`evaluation.py`的assert_disjoint_calibration、validate_calibration、run_calibration；阈值选择显式说明是经验规则 | 保留；不得声称有限样本未来准确率保证。 |
| C25 | DPO已实现 | A（代码/合成smoke）/B（真实训练）：`training.py`与`reports/cpu_smoke_check.json`；docs明确无真实金融DPO结果 | “有DPO路径和合成工程检查，未运行真实偏好实验。” |
| C26 | Review workspace本地保存、人工确认与资产验证分开 | A（设计与实现）：`scripts/build_review_workspace.py`、`review_import.py`及相应tests；没有本轮浏览器运行 | “有本地工具及历史测试”；标签确认不建立事件/许可/证券身份。 |
| C27 | 来源/权利字段、hash、固定revision保证可用数据 | A（字段检查）/C（法律或时间真实性）：`validate_training_row`检查元数据；库中历史来源审查记录存在，但本轮未重查外部条款 | “记录与校验来源声明”；不能把flag/机器时间戳当零错误事实。 |
| C28 | MiniMind来源与修改、Apache-2.0代码 | A（仓库归属记录）：model.py头注、THIRD_PARTY_NOTICES固定revision、LICENSE；未外网重新diff上游 | 保留归属。数据/权重权利另行记录，不能由代码许可推出。 |

### 历史运行与结果

| ID | 主张 | 分类与证据 | 限制/建议 |
|---|---|---|---|
| C29 | seed 300 updates、4,914,941有效token、loss5.5419 | A（公开转录）：`reports/colab_t4_continuation_20261011.json`；source_revision/torch/cuda为空，未独立下载cloud checkpoint | 必须写用户日志记录；不足以独立完整复现实验。 |
| C30 | expansion1220、19,988,195、loss3.6929 | A（公开报告）：`reports/colab_t4_expanded_continuation_20261030.json`记历史notebook SHA和来源commit | 1220含610，不能相加；本轮未读取云权重。 |
| C31 | domain74、1,211,960、loss3.2375，general retention变差 | A（公开转录）：domain报告记录来源、模型hash、runtime、输入hash；明确raw log未归档、未独立下载 | 保留“观测到”而非因果/显著性推断；不同验证集loss不可直接比较。 |
| C32 | 合计26,115,096有效监督位置 | A：上述三个阶段相加一致 | 不是unique token/独立文档数量；不与2.4B 55B预算混用。 |
| C33 | 初始SFT dev全部neutral，acc75.25%、F1.2863；test acc58.42%、F1.2458 | A（公开汇总）：`docs/experiment-results.md`；没有公开行级输出 | 保留“历史摘要”；不能称新holdout复验。 |
| C34 | balanced SFT dev 79/101正确，F1.6549 | A（公开汇总，非权重独立核验）：相同报告的P/R/support可算回；本轮精确重建见WP0.1 | 明确开发集用于选型，无置信区间的点结果不能支持优于基线。 |
| C35 | TF-IDF dev acc75.25%、F1.6087 | A（公开汇总/实现）：`baselines.py`以及balanced script的对照；无公开逐行配对 | 与.6549的差异显著性不可识别，不宣称正效应或零效应。 |
| C36 | balanced增加17个方向正确、减少14个neutral正确 | A（算术）：对角5+12与62对照初始0+0与76 | 调整采样、epochs、updates、LR schedule一起变，不能归因采样本身。 |
| C37 | 2000审核、1993确认、1879三类、1008pool、705训练 | A（公开审核汇总）：human_headline_review报告及TASK_REVIEW定义；人审本身为用户声明，未二次标注 | 池≠训练；上下文AI≠人工gold；资产/事件未验证。 |
| C38 | 1473exposures/epoch、3epochs、4419label tokens、139updates | A（算术与日志摘要）：491×3×3=4419；script和experiment-results | 重采样曝光不是新增独立样本。 |
| C39 | calibration T≈1.50634、threshold≈.57380且导出完成 | A（存在公开陈述）/C（独立核实实际产物）：export脚本可检查，未见该最终weights/calibration原件 | “用户提供运行输出报告已完成”；不是本轮下载核验。 |
| C40 | FinBERT、重复seed、event bootstrap、独立新holdout | B/未完成：DATA_GUIDE结尾明确这些尚未执行，experiment-results同样说明 | 报告未完成，不用合成或历史dev替代。 |
| C41 | 本地工程测试128/205/232/274等通过 | A（历史记录）：对应dated reports记录测试命令、hash、环境及local替代cloud；不是本轮重跑 | “当时报告通过”；局部固定案例不证明所有输入或所有运行环境。 |
| C42 | 下载/预处理真实数量、tokenizer hash和shard数量 | A（历史aggregate）：seed/expansion preparation报告和源审查内hash；未再次读取语料原文 | 时间/日期按各历史阶段解释，不把早期“未训练”误当今日状态。 |
| C43 | Kaggle full/lite迁移、原始四pool已验证 | A（代码、用户输出记录），lite明确不含旧pool、不能独立复核 | 说明full和lite验证能力差异；本轮不执行云迁移。 |
| C44 | Wikipedia、FOMC、SEntFiN来源/许可/大小 | A（存在历史来源核查记录），当前外部事实C | 本轮不重新确认许可或最新状态；SEntFiN label不是stance，CSV无可靠逐条日期。 |
| C45 | Eva-4B、FinanceParam、FinLCR/ARTS等引文与外部性能比较 | C（本审计范围内未联网复核）；这些引文不构成本项目创新或优越性的证据 | 仅作方法背景；具体结论交给独立文献核查并按实际访问层级标注。 |
| C46 | 完成整个训练流程意味着production-ready、投资回报或金融能力 | C：仓库明确没有这种实证；反而多处主动限缩 | 继续保留这些限制，不在新定位中重新引入过强表述。 |

## README 与 docs 覆盖表

以下文件全部读取；PDF覆盖9页可提取文字，未核查视觉版式。每行的主张通过上表对应。操作流程只审查其“已存在实现/历史完成”的表达，不逐个重演云服务动作。

| 文件 | 对应主张 / 结论 |
|---|---|
| README.md | C01–C28、C33–C35；首屏2.4B完成状态需限缩 |
| docs/130U-FinLLM.pdf | C01–C17、C33–C45；p8额外3k probes是计划 |
| docs/DATA_EXPANSION.md | C20–C22、C27、C30、C41–C42；local/cloud证据分开 |
| docs/DATA_GUIDE.md | C14、C21–C27、C40；规范不等于执行 |
| docs/DATA_IMPORT.md | C20、C22、C29–C39；stage lineage与SHA限界 |
| docs/DOMAIN_TRAINING.md | C20、C31–C32、C37、C41 |
| docs/ENGINEERING.md | C08–C17、C20、C24、C33–C36 |
| docs/ENTITY_SFT_PILOT.md | C22–C23、C33–C39、C41–C43 |
| docs/EXPANDED_CONTINUATION.md | C20、C30、C41；累计计数/同环境恢复 |
| docs/experiment-results.md | C33–C40；点估计与限制写明 |
| docs/INTRO.zh-CN.md | C01、C03、C10–C17 |
| docs/KAGGLE_LITE.md | C20、C22、C33–C39、C43 |
| docs/KAGGLE_TRANSFER.md | C20、C22、C41、C43；单T4非双卡合并显存 |
| docs/MAINTENANCE.md | C20–C25、C29–C43；缺原件则不可完整复现 |
| docs/MODEL_CARD.md | C01–C10、C13、C18–C24、C28 |
| docs/NOTEBOOK_RUNTIME.md | C20、C41、C43；本地替代测试不认证云服务 |
| docs/PROJECT_OVERVIEW.md | C01–C19、C29–C45 |
| docs/REVIEW_WORKSPACE.md | C26–C27、C37 |
| docs/SEED_DATA.md | C21–C22、C29、C37、C41–C44 |
| docs/STATUS.md | C01、C18–C25、C29–C43 |
| docs/T4_PILOT.md | C20、C29、C41；峰值为PyTorch allocation，非总GPU占用 |
| docs/TASK_REVIEW.md | C14、C26–C27、C37；明确event_id全空 |
| docs/THIRD_PARTY_NOTICES.md | C28；固定上游归属记录存在，未重联网diff |
| docs/TRAINING_LEDGER.md | C05–C06、C20、C29–C39 |
| docs/TRAINING_SYSTEM.md | C05–C09、C11–C17、C19–C24 |
| docs/TRIAL_GUIDE.md | C18–C25、C28、C33–C43 |
| docs/TRIAL_SPEC.md | C18–C25、C28–C40 |
| docs/research/20261031-posttraining-plan.md | C12、C24–C25、C34–C40、C44–C45 |
| docs/research/corpus_sources_20261009.md | C21–C22、C27、C41–C44 |
| docs/research/DATA_DECISIONS.md | C21–C22、C27、C37、C42–C44；按历史时点读 |
| docs/research/expanded_corpus_sources_20261011.md | C20–C22、C27、C41–C44 |
| docs/research/stance_sources_20261009.md | C27、C37、C41、C44；source sentiment不得自动改成stance |

## Scope filter

不把工程可运行性推成任务有效性；不把定理风格设计或术语命名推成理论新颖性。把所有数据许可证/权利描述限制为历史记录，未进行新的法律判断。删除“24M已经实现完整semantic permission训练”的默认推断（C11–C17）；保留其可复用的训练、元数据和恢复构件。

## Object filter

2.4B方案与24M公开实现必须分开。日期较早报告中的“尚未SFT”仅描述当时状态，不能覆盖后续日志摘要；后续摘要也不能替代当时缺失的原始checkpoint。样本来源是headline literal entity，不能自动迁移到证券代码、Twitter或投资决策。测试通过只覆盖所测试条件，不作为F_t可测或绝对确定性证明。

## Conclusions

1. 公开资产有真实工程内容，但研究贡献尚缺对照与定理支持；“工程卫生”可成为未来证书的前提，不能直接升级成已成立的证书（C11–C28）。
2. 2.4B的架构算式与recipe可审查；训练完成、私有应用效果仍无法从公开材料核实（C01–C10）。这不是对未公开工作的否定。
3. 原 balanced SFT分数是小开发集的选型结果，统计优势未判定；用户确认不依赖旧产物，后续应冻结新的测试协议并从零生成证据（C33–C40、WP0.1）。
4. 原tokenizer/来源记录不能直接承接历史无前视保证；缺cutoff覆盖、事件身份与逐内容版本可得时间核验（C14、C21–C22、C37、C44）。

## Next steps / Risks

本轮仅形成改写建议，README与docs原文保持不变。需要对外重定位时，先由PI审阅一份具体差异稿。研究应优先执行合成地基、完整假设推导与失败案例，再收集本地允许使用的真实数据。WP0.6的文档阅读和主要重复主张归并审计完成；它不等于所有历史运行、全部外部引用或私有资产获得独立认证。
