# 真实 Phase 0：来源原任务的私有数据准备

本工具只准备 SEntFiN 原始**实体相关情绪**，标签顺序固定为 `negative, neutral, positive`，不改名为投资立场。它不加载旧模型、不训练、不联网。真实执行使用本轮 [预注册协议与预算](PROTOCOL.md)，已执行状态见末尾记录。

## 固定契约

输入是本地原始 CSV，表头顺序严格为 `S No.,Title,Decisions,Words`。先按有效标题构造全部词法连通簇，之后才读取标签决定保留或隔离；因此标签不参与相似度、组身份或切分。即使某条标签随后被隔离，其有效标题仍可连接近重复标题，避免因标签状态变化拆开相似度图。

规范化为 Unicode NFKC、casefold、空白折叠，保留数字。标题相同的全部实体必须同簇；词法近重复采用 Unicode `\w+` token set、精确 Jaccard≥4/5，传递合并。全局 token 频率排序的安全 prefix 长度为 `|X|−ceil(.8|X|)+1`，候选对再用整数 `5*intersection≥4*union` 验证。若相似度达到门槛，最早公共 token 必须同时落在两集合 prefix 中，否则交集小于 `ceil(.8|X|)` 或 `ceil(.8|Y|)`，与 Jaccard 门槛矛盾。因此不是近似 MinHash；测试与完整 all-pairs 比较。空 token 标题不计算 0/0，不互相连边，只合并规范化完全相同者。

`Decisions` 先 `ast.parse(mode='eval')`，核查原始 Dict 键，拒绝原始／规范化重复实体键，然后 `ast.literal_eval`；禁止 `eval`。非字典、异常语法、空键、未知标签、重复键等整行隔离，不猜测修复。跨行同规范化标题、同规范化实体的不同标签全部隔离；同标题不同实体标签不同是合法多目标监督。相同标题＋实体＋标签仅保留一条样本，保留全部来源 ID，避免重复计权。近重复而非相同标题的不同标签保留，但必须同簇。重复来源 ID 的全部记录隔离。

族 ID 为排序后完整规范化成员标题的 SHA256；split 使用固定 seed=130 的族 ID hash，整数边界为 70% train / 15% development / 15% test。比例是确定性 hash 分配的设计比例，实际样本比例不强制相等，不按标签或性能重新切分。任一分区为空，真实 CLI 拒绝输出，不换 seed。分区后检查 id 唯一、family 不跨 split、规范化标题跨 split 为 0、近重复边跨 split 为 0，并报告最大连通分量。

非字面出现的实体不删除，分别统计原始精确 substring 与规范化 substring 两种存在性；不因此声称实体身份或证券映射已经核验。这个 split **不是时间切分，也未完成语义事件去重**。词法簇只给定当前算法的隔离，不证明未来或事件独立性；下游训练向量器只能在 train 上拟合。

## 私有 schema 与产物

所有行级产物只写 `research/private/<run-directory>/`，默认 `research/private/real_baseline/`。已有产物拒绝覆盖。原始旧仓库只读。

`rows.jsonl` 及 `train.jsonl`、`development.jsonl`、`test.jsonl` 每行包含：

- `id`：规范化标题与实体的稳定样本 hash；`headline`、`target`：保留的来源文本与实体。
- `label`、`label_id`：原任务标签及固定 0/1/2；`family_id`、`split`：词法簇与冻结分区。
- `source_ids`：合并重复样本的全部原始来源编号。
- `input_text`：`[ENTITY] target` 换行后 `[TITLE] headline`，保留目标字段。
- `entity_literal_substring`、`entity_normalized_substring`：目标存在性诊断，不作为删除条件。

`quarantine.jsonl` 为私有异常明细，含固定 reason、行号及需要审核的源字段；不出现在公共报告。`aggregate_manifest.json` 可分享，只有总量、每类／每分区计数、冲突类型计数、最大簇、去重比较数量、隔离核验、输入及产物哈希，不包含逐条文本、标签、组成员或预测。

```powershell
& '..\130U-FinLLM\.venv\Scripts\python.exe' -X utf8 -m unittest research.real_baseline.test_prepare -v
& '..\130U-FinLLM\.venv\Scripts\python.exe' -X utf8 -m research.real_baseline.prepare --source '../130U-FinLLM/data/raw/candidates/sentfin/SEntFiN.csv'
```

单元测试只使用人工 synthetic 例子，无真实新闻文本。公开准备代码不读取 SEntFiN 行后打印文本；CLI 仅打印聚合计数。本文不替代父任务的训练预注册，也不把原有许可记录解释为第三方出版方权利已经完全核实。

## 已执行：2026-11-16

在父任务确认预注册与私有目录排除检查已完成后运行。12 项 synthetic 测试通过，最新一次用时约 0.020 秒；其中 prefix 筛选与全对 oracle 分别在 7-token 全部子集和固定随机集合／长度边界上逐边相等。这是实现检查，候选无漏边的全域理由仍是上面的前缀论证。

真实准备运行 Python 3.12.14，0.766725 秒；未测峰值内存，GPU/网络请求/训练 token 均为 0。原始 CSV 的 SHA256 与预注册值一致，严格读取 10,753 行；原文件未修改。公开数值来自 [aggregate_manifest.json](aggregate_manifest.json)，所有逐行结果留在私有目录。

| 项目 | 本轮观测 |
|---|---:|
| 语法异常整行隔离 | 13 |
| 同规范标题＋实体的异标签冲突键隔离 | 7 |
| 相同标题＋实体＋标签合并的额外出现次数 | 73 |
| 保留实体样本／词法簇 | 14,284／10,591 |
| 保留但实体非原始字面 substring 的样本 | 19 |
| 全输入规范化标题／词法连通分量 | 10,686／10,611 |
| 精确 Jaccard 比较次数／满足阈值边数 | 40,488／77 |
| 最大连通分量的规范化标题数／保留样本数 | 3／7 |
| family／规范化标题／近重复边跨 split | 0／0／0 |

13 是整行解析异常数，7 是冲突的实体—标题键数，不能相加后称为“20 个源文件行”。标签异常没有猜测修复；保留的不同实体可以合法拥有不同标签。

| split | 样本 | 词法簇 | negative | neutral | positive |
|---|---:|---:|---:|---:|---:|
| train | 10,041 | 7,438 | 2,658 | 3,831 | 3,552 |
| development | 2,136 | 1,583 | 572 | 838 | 726 |
| test | 2,107 | 1,570 | 558 | 787 | 762 |

三个分区均有三类支持，未出现巨连通簇；没有因这些结果重新选 seed 或改变分组。私有 `rows.jsonl` 的 SHA256 为 `8ab314ebd74680466f3a24055433f3a44d442107773607204cd3983122d87567`。准备源码 SHA256 为 `c7f56b29875b6e76b7d2201cb4de6bea329c97b3582523218424096af53af06c`；完整分区与隔离文件指纹在 aggregate manifest。后续训练器应先核验这些指纹，再使用独立冻结的实体标记转换；原始 `input_text` 不是已经做过 `TARGET_ENTITY` 替换的特征文本。

这些是真实来源原任务的数据准备结果，没有模型性能结论，不证明完整事件独立、历史无前视或本项目投资立场金标准已经成立。
