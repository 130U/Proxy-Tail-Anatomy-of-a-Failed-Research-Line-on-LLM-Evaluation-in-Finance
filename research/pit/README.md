# T1.1 历史快照管线参考实现

这是一组纯标准库、无模型训练的构造性组件，按 [执行前协议](PROTOCOL.md) 实现。它检验“只依赖给定知识截止日前信息”的代码依赖链，不认证来源时间真实，不是新金融模型，也不是论文新颖性证据。以下接口不读取真实私有语料、不联网。

## 事件日志与合法输入域

每次 upsert 是完整状态，不是从“当前最新对象”读取字段的补丁。事件包含 `event_id,document_id,knowledge_time,record_time,operation,payload`。upsert 的 payload 包含 `text,content_sha256,source,core,label,metadata`；墓碑 payload 为 null。标签即使不用来拟合词表，也与来源、核心标记和元数据一起版本化，不得未来回写旧状态。

`knowledge_time` 是**声称该完整状态已经可知的时刻**，决定投影与版本选择；`record_time` 是保留的原始记录声称时间，不能替代知识时间。修订可有新的 knowledge_time 而保留旧 record_time。可见记录要求整数且 `record_time≤knowledge_time`，这只是声明内部一致性检查。知识时间至少晚于内容、标签、source/core、规则元数据等全部字段真实知悉时间，是**外部前提**；当前实现没有逐字段知悉时间证据，不能声称验证了它。

合法外层域是有限 list/tuple，每个元素为字典，头部 event/document ID 为非空字符串，knowledge_time 为非 bool 整数。读取外层头是确定投影所必需；任意损坏头不在“未来追加不变”的承诺域。对合法头且 knowledge_time>cutoff 的事件，程序不读取、校验、序列化或 hash 载荷，即使 future payload 是错误类型、坏 hash 或缺少 body 字段，也不改变过去结果。

先投影，后检查**全部可见事件**的完整 schema、声明 hash、标签/元数据类型、record_time 约束及可见 event_id 唯一性，再按 `(knowledge_time,event_id)` 升序取同 document_id 最新状态。该确定性并列规则不使用输入行号；event_id 本身须历史冻结。未来 event_id 与旧 event_id 重复，不会令旧快照失败；到它可见时才作为可见日志冲突拒绝。未来墓碑不删除旧快照，生效时删除最新活动对象。回溯修改旧事件或追加一个知识时间也回溯的事件，不是合法的“纯未来追加”。

日志 append-only、完整性、真实时间语义与不可篡改性均是数据来源契约；本模块是投影和处理函数，不是实现了防篡改存储或认证时间服务。

## 稳定产物与历史等价

`HistoricalSnapshot` 保留规范化的**全部可见事件历史**及据此还原的活动文档；历史等价是相同 cutoff 下这份投影相同，不只是最终活动文档相同。即使两个日志最后活动文档相同，若过去修订历史不同，history hash 可以不同。全日志 hash、全库长度、未来排除数和运行耗时不进入任何稳定产物。

主入口为：

```python
from research.pit.pipeline import FrozenConfig, build_at_cutoff, world_adapter
from research.local.world import generate

events = world_adapter(generate(companies=4, quarters=6, contamination=0))
artifacts = build_at_cutoff(events, cutoff=0, config=FrozenConfig(), seed=130)
# artifacts: dict[str, bytes]，供调用者保存或逐项比较。
```

较低层入口 `canonical_history(events,cutoff=...)` 返回 snapshot，`run_pipeline(snapshot,cutoff=...,config=...,seed=...)` 重新检查其规范化历史与文档一致，并绑定 cutoff。直接伪造不同文档或掺入未来历史的 snapshot 会被拒绝；这不是历史完整性的密码学证明。任意手工制造的 State 不是独立认证对象，六阶段的保证针对主入口从验证快照产生的状态及其复合。每个阶段仍会拒绝 cutoff 不一致或记录知识时间晚于 cutoff 的输入。

稳定文件有：`configuration.json`、`history.json`、`snapshot.json`、`filter.json`、`deduplicate.json`、`sample.json`、`split.json`、`tokenizer_candidates.json`、`selected_tokenizer.json`、`artifact_hashes.json`。它们是规范排序、UTF-8 JSON 字节，无运行时钟。对同一历史投影、代码版本、外生配置及 seed，在同一Python/Unicode规范化运行环境下，所有阶段均应逐字节相同；不声称跨Unicode版本确定性。运行环境版本/hash、计时及全日志操作信息由外部 runner 放在独立记录，不能混进“不变”的对象。

## 六个显式 cutoff 的组件

1. `filter_documents`：只能读 snapshot，按外生 allowed_sources、require_core 过滤；以固定 Unicode NFKC/casefold/空白规则和 `\w+` 分词，再按外生 stopwords 去词。source/core 的真值不由布尔检查证明。
2. `deduplicate`：仅在历史过滤结果上，规范化全文精确重复或非空 token-set Jaccard 达到固定有理阈值时连边，做确定性传递合并。选知识时间最早、再按文档/事件 ID 的代表。空 token 集合不因 0/0 互相连接。本参考实现用全对检查，预算规模最多 1,000 事件；不会按未来近重复桥建立簇。
3. `sample_documents`：用独立外生 seed 与**历史文档 ID**的固定 hash 排序取 sample_limit。不使用全库长度、全日志 hash、未来候选数或先给未来对象消耗随机流。固定配置下的 ID hash 是排序工具，不是来源证明。
4. `split_documents`：使用另一个固定 hash 命名空间与 seed，在历史样本内划 train/development。不会为了填满开发集去查看未来。只承诺此合成引用管线的划分，不宣称该划分具有真实事件独立性。
5. `fit_tokenizer`：仅统计历史 train token，候选为预先给定的 `(capacity,min_frequency)`。按 train 频数降序、词典序并列生成词表，保留未知词/填充编号。词表拟合属于预处理，不是神经训练。
6. `select_tokenizer`：只读相同历史来源的、不重叠 train/development；以开发集未知 token 率加 `固定容量惩罚×capacity` 选择，全部使用 Fraction 精确分数。并列按外生候选顺序。无开发 token 时固定选首候选；空历史给空词表。空 train 时保留空词表，以可见 dev 计算结果，不借未来语料补训练。

配置候选、stopwords、source/core 规则、所有阈值、seed 和算法版本都须历史可用或来自独立外生机制。若要声称随机seed不额外携带未来信息，应独立于整个世界，或满足给定历史后与未来条件独立；仅与未来边际独立不够。可测函数复合本身不需要此独立性，详见 [数学稿](../theory/pit_noninterference.md)。今天根据未来表现挑出一个“固定配置”，不会因写进 FrozenConfig 就变成历史可测。

## 合成 adapter、反例与测试

`world_adapter` 只读取 WP0.5 行的 `id,recorded_time,text`；测试用限制字段访问的对象检查它不会读取 `available_time,contaminated,stance,price` 等字段。它把 recorded_time 赋给 knowledge_time 是人工样例的声明约定，**不会检测污染记录时间，也不证明 true available_time**。来源固定标为 synthetic-world，core=false，label=null；不能将模拟样本说成真实可信核心。

三个 `naive_*` 函数是专门保留的错误反例，不被主管线调用：全库先拟合词表会纳入未来词；全库先选最新重复代表会使旧文档被未来副本挤掉；即使只选旧文档，按全库长度选择旧文档也能泄漏未来信息。正确实现逐阶段稳定与错误实现出现反例，是机制检查，不能单独支持创新主张。

```powershell
& '..\130U-FinLLM\.venv\Scripts\python.exe' -X utf8 -m unittest research.pit.test_pipeline -v
```

测试覆盖未来同 ID 修订/墓碑/source/core/label/metadata、未知未来载荷、未来重复事件 ID、声明时间与知识时间不同、同时间并列、排列不变、未来重复桥、空历史/空开发集、train-only 词表、各阶段 cutoff 绑定、伪造 snapshot 拒绝、多个 cutoff 的有限未来扩展及三类实际反例。有限测试不穷尽所有程序 bug、隐藏输入或真实来源风险。外部 runner 的实际记录及独立理论证明另行交付，不在此预填通过结果。

## 独立审查修复记录

审查者在首轮代码中构造了 bool/int 一致性绕过：Python 的 dataclass 相等比较会把 `False` 与 `0`、`True` 与 `1` 判为相等，因而 `label=0→False`、`core=True→1` 或 `cutoff=1→True` 可通过旧检查，却改变规范 JSON 字节。现已修为严格字段类型检查，加上重建历史后规范文档字节比较；State 的 cutoff 和文档类型也同样检查。回归包含这三类输入及文档知识时间的 bool 变体。该修复关闭实际入口问题，不是把它推给外部时间真实性假设；初版结果不作为通过证据。
