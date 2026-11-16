# WP0.4：离线 inline-XBRL 受限解析原型

日期：2026-11-15。状态：**离线原型完成，真实语料可行性未评估**。这里所有样例均为人工编写的 synthetic XML，不是 SEC filing，不是从外部抓取的数据，也不是完整 iXBRL 合规样例。程序只有本地文件接口，无联网代码。

```powershell
python -m research.xbrl.parse_local research/xbrl/synthetic_fixture.xml research/xbrl/example_result.json
python -m unittest research.xbrl.test_parse_local -v
```

支持域：2013 iXBRL namespace 中的 `nonFraction`；不带 transformation 的非负十进制字面值；负号仅由 `sign="-"` 表达；整数 `scale`、整数或 `INF` 的 `decimals`；引用一个简单 measure 的unit；显式entity identifier、instant或startDate/endDate的context。`scale` 与有限 `decimals` 限于 [-18,18]，数字字面值最多100字符。使用 Decimal 精确转换声明数值。QName 展开到 URI，**不验证 taxonomy 的实际存在或经济语义**。

以下情况返回拒绝/abstain，而不猜测：unknown format/transformation、括号负数/逗号数字、continuation、嵌套事实文本、nil、缺unit/context、复杂单位、维度/scenario、未知/倒置/非ISO期间、precision属性。重复XML id、namespace重绑定或非法XML会拒绝整份文件。`fraction/nonNumeric`只计入unsupported，不解析；其他 namespace 的未知结构不应被解释成已验证。

`declared_rounding_enclosure` 只是在“文档的decimals准确度声明可信、采用相应舍入解释”的条件下，围绕声明值给出的保守闭区间。它不证明公司真实数值，不保证财务恒等式，也不证明文档标注正确。`INF`按声明值精确处理；这里不是官方XBRL验证器。

时间证书始终输出 `null`。`accepted`、报表period、网页发布日期、下载时间是不同语义字段；受理时间与当前下载的内容版本之间还需要来源与修订对应证据。**accepted字段存在不等于已证明该内容在受理瞬间已公开可得**，不得把它直接当零失败概率的核心证据。季度聚合文件也不能自动当作过去某时刻可见的快照：须处理后续修正、重述、重复事实和版本选择。这个原型没有读取或确认SEC字段格式、精度、公开延迟、calculation关系或季度真实数据统计。

后续真实验证的可接入物：本地、允许使用的文件及其内容hash；受理/公开可得/下载/修订时间元数据；人工校验的 fact-text 对齐与解析结果。不能把这4个手工事实的通过/拒绝比例外推为真实coverage或错误率。新增数据若不在支持域，先扩充明确规范和反例，再测准确率；不要静默fallback到猜数字。
