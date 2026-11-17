# 本地真实语料盘点：可以从原始文本重新起步

盘点日期：2026-11-15（America/New_York）。方式：完全离线；仅核对用户指定旧仓库的 `data/`、`reports/`、`runs/` 文件清单、大小、来源/许可/划分元数据及其文件哈希。没有打印原始标题、逐条标签或文本，没有加载任何 checkpoint，没有修改旧仓库，没有把原始语料复制进交接包。

原仓库绝对路径：`<workspace>/130U-FinLLM`。下文相对文件标识均相对于该路径，**不相对于新的 research 工作区**。

## 1. 结论

**本地确有可读的、非合成原始语料，不能因为缺旧 checkpoint 或逐样本预测就说没有真实数据。** 最直接的重新起步材料是 120 份 Federal Reserve FOMC 会议纪要文本及其本地 HTML 快照；另有 28,486 篇 Wikipedia 快照文本和 SEntFiN 原始候选数据。它们足以启动小规模、从随机初始化的新训练与真实文本方法验证。

FOMC 的本地元数据最清楚：全部记录标为 `synthetic=false`、`training_allowed=true`、`license=public-domain-US-government`，具备来源 URL、发布日期、抓取日期、文本哈希、HTML 哈希；120 个 HTML 快照全部存在并与 manifest 哈希一致。这里确认的是**本地来源及许可记录的完整性**，没有重新联网核实许可网页，也没有把记录自身视为不可推翻的法律证明。

这些数据还**不能直接支持历史无泄漏的最终证书**。FOMC 是 2026 年抓取的内容版本加历史发布日期，尚未证明这些内容在历史时点没有修订；Wikipedia 没有逐篇 `published_at`；既有预处理、任务集划分均非时间切分。真实 P2 数字解析研究可以从 FOMC 文本开始，但当前元数据没有数字、单位、比较基准的金标，也未发现本地 XBRL/iXBRL 对齐数据，不能把“有真实文本”说成“解析真值已齐”。

## 2. 盘点范围与防误计数

- `data/` 实际有 431 个文件、671,700,099 字节（文件系统观测，包含原始数据、派生文件、token 文件和缓存重复，**不是 671.7 MB 独立语料**）。
- `reports/` 有 25 个文件、224,012 字节；读取了选定准备报告的元数据和限制说明。
- `runs/` 的初始文件名清单显示大量 `test_*`、`pytest_*`、临时 `original-runtime`/`drive` 夹具。它们不作为真实训练集或真实 checkpoint 证据。进一步只核对 `task_pilot`、`review_packages` 等有实际任务用途目录的清单与 manifest；没有宣称逐个审查全部测试夹具内容。
- seed 与 expansion 的源候选互相重叠。expansion 的 120 份 FOMC 包含 seed 的 32 份；Wikipedia expansion 来源前缀包含 seed 的 825 篇。不能相加成 152 份和 29,311 篇独立文档。现有 preparation manifest 已记录这部分排除。
- `domain_mix` 是既有 token 的混合重排，不能重复记为独立新增语料。

## 3. 可用原始文件及来源

以下行数由仅提取许可、来源与时间字段的 JSONL 遍历核对；文本和标题字段没有输出。

| 本地文件 | 实际字节数 | 记录数 | 本地来源/许可记录 | 判断 |
|---|---:|---:|---|---|
| `data/raw/seed_v1/corpora/finance_candidate.jsonl` | 1,791,245 | 32 | Federal Reserve FOMC；`public-domain-US-government` | 真实文本候选，不是示例占位文件 |
| `data/raw/expansion_v1/corpora/finance_candidate.jsonl` | 6,977,681 | 120 | 同上；全部 `training_allowed=true` | 优先用于从头训练的本地金融文本源 |
| `data/raw/seed_v1/corpora/general_candidate.jsonl` | 19,985,370 | 825 | `wikimedia/wikipedia`；`CC-BY-SA-3.0`、`GFDL` | 真实通用文本候选；保留归属等条件 |
| `data/raw/expansion_v1/corpora/general_candidate.jsonl` | 199,996,572 | 28,486 | 同上，配置 `20231101.en` | 可启动更大本地重训练；不是随机代表性样本 |
| `data/raw/candidates/sentfin/SEntFiN.csv` | 1,118,162 | manifest 记 10,753 行、10,686 个精确唯一标题 | 固定的作者仓库版本；本地 MIT LICENSE | 原始候选存在；新闻发布者权利与任务语义另有已记录限制 |
| `data/examples/annotation_template.jsonl` | 785 | 未用于研究计数 | 模板文件 | 此文件才是小样例，不能代表全部本地数据 |

Wikipedia 数据源版本为 `b04c8d1ceb2f5cd4588862100d08de323dccfbaa`，配置 `20231101.en`。SEntFiN 作者仓库版本为 `eba43610fe3cb57a3e5773cd6c037da1f8992ad5`。这些版本号来自本地已保存 manifest，本轮没有向外部服务请求确认。

两套候选语料均保留 `candidate_only=true`；其意义是源候选仍需要研究所要求的去重、切分和审计。它不等于数据不存在或合成数据，也不证明直接沿用旧划分就满足新研究。

## 4. 哈希与时间字段核验

四个原始 JSONL 的实际 SHA256 均匹配对应 source manifest：

| 文件简名 | SHA256 |
|---|---|
| seed/general_candidate | `cee8dfb34401588ca8ecde6ec8d13d1ffa275efb5e0ca1391499da16e6a1b22f` |
| seed/finance_candidate | `f864068487758cdcec3142a526c9abcc5da7e92f14f289f201078f34e424f1c6` |
| expansion/general_candidate | `5b2b8def467868f177afd438c27ba4254fe41d746a5bbabb4bbbf3046769d547` |
| expansion/finance_candidate | `5a9b357c4b979b5e85dc7622e28c5793068baeb67a48abbd218e81e7d8219a0a` |

另核对 `SEntFiN.csv` 实际 SHA256 为 `570af7ba58f724f3fcc414dd5ba80da5b1a3b342134d76c6ebdf53a32c54a92f`；本地 `LICENSE` 为 1,110 字节，文件开头明确为 MIT License。

| 属性 | seed FOMC | expansion FOMC | Wikipedia |
|---|---|---|---|
| `published_at` 范围 | 2021-02-17 至 2025-01-08 | 2011-02-16 至 2025-12-30 | 全部缺失 |
| source manifest 抓取时间 | 2026-10-09T13:43:00.227319+00:00 | 2026-10-11T10:39:20.795698+00:00 | 对应 seed/expansion 抓取时间 |
| `meeting_date` | 每条存在 | 每条存在 | 不适用 |
| `source_url`、`text_sha256` | 每条存在 | 每条存在 | 每条存在 |
| HTML 快照 | 32 个全部存在并匹配 SHA256 | 120 个全部存在并匹配 SHA256 | 未保存逐篇 HTML 哈希字段 |

FOMC 的 `meeting_date` 与 `published_at` 是两个不同字段；例如 2024 年底会议对应 2025 年初公布，不能用会议日期代替真实可得时间。此次只核对时间元数据存在及范围，**没有审阅 HTML 正文以独立重建其发布时间、时区或修订历史**。哈希匹配证明当前文件与已保存 manifest 一致，不证明 2011 年那天就有同一内容。

## 5. 本地许可记录分层

### 来源明确、可优先复用的候选

FOMC 每条 `rights_note` 记录：文本来自 Federal Reserve Board 原始会议纪要；保留机构归属；依据保存的 disclaimer 来源标为 public domain；排除明确版权标记、第三方图片和外链内容。所有记录 `training_allowed=true`、`synthetic=false`。这足以避免把本地材料误说成来源未知，但全文筛选是否完全执行仍是管线声明，应在新的数据卡中保留为假设或检查项目。

Wikipedia 每条注明文章 URL 归属、快照卡的 CC-BY-SA-3.0/GFDL 与后续 Wikimedia 条款版本差异；`training_allowed=true`。其本地来源元数据可追踪，不应把它称为无来源数据，也不应无条件称为 public domain。原文需要的归属和其他适用条件应保留；本轮未重新审查许可网页。

### 明确私有派生/用途受限的候选

SEntFiN 原始作者仓库 LICENSE 为 MIT，但 `runs/task_pilot/entity_v1/task_manifest.json` 明写：

- `private_research_only=true`；
- 作者仓库许可不独立保证原新闻发布者权利；
- `scope` 是字面实体，不是已验证证券；
- `semantic_event_audit_complete=false`；
- 现有数据是非时间、字面/source-group 隔离的 pilot，不是最终独立测试。

因此可以确认实体任务原始/派生数据实际存在，不能以“无权利记录”一概否定；但不能把私有研究衍生集打包公开，或直接改称权利与历史时间均已审核的证书数据。

`data/raw/sentfin_review_v1/ai_review_manifest.json` 明确标记 AI proposals、非人工批准、`not_for_formal_training=true`。较晚的人工复核报告也限定确认范围不包含来源权利、历史时间和完整事件划分。不同阶段的标签批准状态不能混用；此盘点没有读取逐条标签来裁定哪些行可用于训练。

来源/许可审核文档的路径已记录在 manifest 中，但位于 `docs/`；本任务限定只查 `data/`、`reports/`、`runs/`，所以没有读取那些文档，也没有夸称完成独立权利核验。

## 6. 已有划分与预处理可以参考，不能继承为新证书

| 证据文件 | 记录的规模/划分 | 新研究含义 |
|---|---|---|
| `data/raw/seed_v1/prepared/preparation_manifest.json` | general 794 train /31 validation；finance 31/1；seed=130，hash split | 数据存在；非时间划分；finance validation 仅一篇，不能支撑稳定金融总体评估 |
| `data/raw/expansion_v1/prepared/preparation_manifest.json` | 去除 seed 后 general 26,267/1,394；finance 84/4 | 这是增量部分；不能与源候选重复计数；仍为非时间 hash split |
| `data/processed/seed_v1/seed_summary.json` | general train 4,976,894 token；finance train 341,309 token | 旧 tokenizer 下已测规模，不保证新 tokenizer 相同；本次不读 token 二进制 |
| `data/processed/expansion_v1/expansion_summary.json` | general train 41,499,364；finance train 972,438 token | 旧 tokenizer 下增量 token；`domain_mix` 不能重复加作新数据 |
| `runs/task_pilot/entity_v1/split_manifest.json` | train 705、development 101、calibration 101、test 101；1,008 groups | 真正任务数据存在；`grouped_non_temporal`，非历史测试 |

任务文件实际大小：`train.jsonl` 482,398 字节，`development.jsonl` 69,978 字节，`test.jsonl` 68,771 字节，`calibration.jsonl` 69,882 字节，另有 temperature/threshold calibration 分文件。存在这些文件不代表已经取得每个旧模型的 predictions；这是不同的证据问题。

本次目标是从零构建研究，应以原始文本重新确定新的训练/验证/审计边界及 tokenizer，而不是把旧权重或旧开发集成绩当作新结果。旧非时间 split 可用于检查数据结构和复现旧工程状态，不自动继承到 P1 信息集证书。

## 7. 对下一步工作的具体判定

| 计划动作 | 本地材料是否够启动 | 仍需关闭的缺口 |
|---|---|---|
| 从随机初始化训练一个真实金融文本小模型 | **够启动**：120 份 FOMC 原文及快照可读；可按预算取子集 | 新训练预算、内容检查、训练/验证设计、tokenizer 新建；规模小不代表语言能力足够 |
| 用真实通用文本补充预训练 | **够启动**：28,486 篇固定 Wikipedia 快照候选 | 许可归属保留、时间信息缺口、非代表性前缀、与金融任务的独立划分 |
| 在本地真实金融文本验证 P2 数字/单位解析 | **够启动文本抽取与人工核验准备** | 没有已验证数字/单位/期间/比较基准金标；FOMC 非 XBRL 语料，不能承诺自动获得完整监督 |
| P1 可信历史核心直接拿来认证 | **不够直接认证，但不是缺原文** | 2026 抓取版本的历史修订问题、发布时区/精度、历史选择与共享组件契约 |
| 重新训练标题三分类基线 | 原始候选和私有 pilot 文件存在 | 逐行批准状态、权利边界、任务语义、独立评测集仍需明确；不能复用旧开发集作最终证据 |
| 真实 XBRL 对齐证书 | **未在 `data/` 找到相应材料** | 按文件名及扩展名查无 `.xbrl`、`.xhtml`、`companyfacts`、XBRL/financialstatement 命名数据；没有宣称检查了所有 HTML 的内部标签 |

**推荐的最小可行动路径：** 先用本地 FOMC 原始文本建立一份新的、可哈希重现的小语料快照，冻结用途和划分，再从零训练受预算约束的小模型。P2 的解析金标和 P1 的历史版本证据各自独立列为待完成项目。这样继续做真实研究所需的下一步，而不是把旧训练资产缺失扩大成“没有可用原始语料”。

## 8. 证据等级与未做事项

本报告的文件大小、JSONL 数量、SHA256 一致性和快照存在性来自本轮文件系统核验；来源许可、旧 split 和旧 token 计数来自明确列出的本地元数据，未作外部复核。没有浏览网页、访问 SEC、下载数据、阅读/执行旧脚本、加载权重或评估原始标签。

没有输出原始标题、新闻正文、逐条标签或私有审核表，没有把上述数据复制进新的仓库或 Fable 包。这个报告只交付可供决策的清单和证据边界。
