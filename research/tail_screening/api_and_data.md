# 尾部筛选：API 连续评分与公开标题数据可行性

**最新任务切换：用户已明确要求在当前会话内用多个 agent 执行。当前工作按 `agent_pilot.md` 推进，API 插件或密钥不再是这一试跑的前置条件。** 下文关于 API 连接与套餐赠送额度的内容保留为原方案/备选方案说明，不代表当前要求用户先完成接入。

**当前接入状态与费用约束（2026-11-16 更新）：只使用套餐赠送的 API credits，不充值、不开自动充值。**[官方说明](https://developers.openai.com/api/docs/guides/chatgpt-api-credits)确认，符合条件且已付费至少 7 天的 ChatGPT Pro / Business 订阅可将福利关联到本人拥有的 API 组织，无需添加 API 支付方式；这是独立的 API 赠送额度，不是 ChatGPT / Codex 交互额度。免费额度先消耗，但耗尽后若组织仍有已购买额度，请求会继续消耗后者，因此不能仅凭“未开启自动充值”保证本实验不使用付费余额。开始实验前须核实账户关联、赠送余额及其有效期，并将实验消耗限制在赠送额度内；文中的美元估算仅用于额度预算，不代表充值授权。目前没有 API 密钥，官方 OpenAI Developers 插件已建议但尚未安装或连接；**插件安装连接是当前待用户完成的接入步骤**，完成后继续原尾部评分任务。尚未确认用户的实际套餐、资格或余额，插件连接本身也不等于额度已到账。

核验日期：2026-11-16。范围为本地依赖检查、官方接口文档、原作者发布页与约 2.10 MB 数据试读；未安装 OpenAI SDK、下载整库、训练模型或发起付费 API 请求。词法基线绘图另用了临时目录中的 Matplotlib 依赖。

**结论：两档模型的单 token 连续评分具有接口基础，但“每条标题都能取得两个候选分数”尚须实测。FNSPID 的规模和字段满足候选池要求，新闻文字的授权范围仍待澄清；目前没有核验到同时满足规模、来源和文字授权均明确的现成数据集。**

## 1. 本地状态与两档模型

本地 `pyproject.toml` 没有 `openai` 依赖；旧仓库虚拟环境和 bundled Python 中均未发现 OpenAI SDK。当前进程 `OPENAI_API_KEY`：**无**。只检查了存在性，没有读取、打印或寻找其他个人位置的密钥。账户的模型访问权限、额度和实际请求兼容性均未验证。接入时可按[官方 quickstart](https://developers.openai.com/api/docs/quickstart)配置 SDK 或直接调用 HTTPS；本任务未实施接入。

| 用途 | 建议模型 | 连续评分所需配置 | 标准 input / output，美元每百万 token |
| --- | --- | --- | --- |
| 低成本筛选器 | `gpt-6-luna` | 推理设为 `none` | 0.10 / 0.50 |
| 较高成本参照评分器 | `gpt-6-sol` | 推理设为 `none` | 2.00 / 10.00 |

两者官方页面均列出 Chat Completions、Responses 和 `none` 推理档。这里的高成本参照模型是 GPT-6 Sol，不能擅自替换为 GPT-6.1 Sol：最新指南明确后者及 GPT-6 Astra 不支持 `none`，而启用推理时需要移除 logprobs 相关参数。高成本也不等于本任务上已证实更准确。[Luna 模型页](https://developers.openai.com/api/docs/models/gpt-6-luna)、[Sol 模型页](https://developers.openai.com/api/docs/models/gpt-6-sol)、[参数兼容指南](https://developers.openai.com/api/docs/guides/latest-model)、[当前价格](https://developers.openai.com/api/docs/pricing)。

优先用短提示：按每标题 **80–180 input token（含固定提示）与 1–2 output token**，各模型评分 20,000 条、关闭推理、无缓存折扣：Luna 约 **$0.162–$0.362**；Sol 约 **$3.24–$7.24**；40,000 次请求合计约 **$3.402–$7.602**。最小稳定性试跑 **100 条 × 3 次 × 两模型**，同样假设下约 **$0.051–$0.114**。这是 token 长度假设，须用试跑 usage 验证；设 `max_completion_tokens=1` 或 `2`，不让自由解释增加输出费用。用户可据此确定主跑费用上限。

若提示需要更多解释，按 200–600 input 与 1–4 output token 的宽预算，各 20,000 条为 Luna **$0.41–$1.24**、Sol **$8.20–$24.80**。公式为 `请求数 × (输入token数 × 输入单价 + 输出token数 × 输出单价) / 10^6`。两种预算均为短上下文标准服务估计，未包含重试、额外重复评分、缓存写入或地区附加费；实际费用以 usage 为准。Batch 当前价格通常为标准价的一半，但应先验证相同参数可用，不能预先把折扣当成已发生节省。[定价依据](https://developers.openai.com/api/docs/pricing)。

## 2. 连续分数怎样取得，何时不能取得

先用文字定义尾部事件，再固定二元标签，例如 `A=目标事件`、`B=非目标事件`。标签须分别是该模型下的单个 token，并检查是否存在前导空格变体；当前没有实测 token ID，不能照抄其他模型的编号。提示只要求返回标签，不能让 JSON 的左花括号成为被评分的第一个 token。官方已有使用 logprobs 做分类的示例，但示例不证明金融任务的校准或排序质量。[官方示例](https://developers.openai.com/cookbook/examples/using_logprobs)。

Chat Completions 可使用 `reasoning_effort="none"`、`logprobs=true`、`top_logprobs=20` 和 `max_completion_tokens=1`，并固定提示、温度及其他采样设置。Responses 对应 `reasoning={"effort":"none"}`、`include=["message.output_text.logprobs"]`、`top_logprobs=20`；该接口的输出上限参数是 `max_output_tokens`。两种接口的候选数上限都是 20，实际返回可少于请求数。短标题不应依赖自动截断上下文。[Chat 参数](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)、[Responses 参数](https://developers.openai.com/api/reference/resources/responses/methods/create)。

若**同一个请求、同一个输出位置**同时返回两个有效候选 logprob，定义

\[
D(x)=\log P(A\mid x)-\log P(B\mid x),\qquad
p_{AB}(x)=\frac{1}{1+\exp[-D(x)]}.
\]

建议直接按 `D` 排序，避免 sigmoid 接近 1 时产生额外浮点饱和。`p_AB` 只是模型输出在这两个标签中的归一化份额，不是经过校准的真实事件概率；还要观察非标签输出。若业务需要多个 token 代表同一标签，应在已知候选集合内求和，并重新说明截断问题，不能只取最有利的拼写。

主要障碍是 **top-20 不保证包含 A 和 B**。缺失候选不能补成零概率；文档中的 `-9999` 是极低概率的哨兵，也不能拿来当精确 logprob 形成虚假的极端连续分数。应标为不可评分或仅有界的信息。分别强制输出 A、B 的两次不同请求再相减，通常不共享同一个归一化分布，不能当作上述 `D`。[返回值定义](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)。

Chat 的 `logit_bias` 可对核验后的 A/B token ID 加相同正偏置，例如各 `+20`，以提高两者进入 top-20 的概率；在确实为同一 logits 分布加相同常数的数学模型下，共同偏置和归一化常数在两者 log-odds 中抵消。官方 Chat 端点明确列出该参数，但本次没有找到 Luna/Sol 各自的逐项 `logit_bias` 支持表，也没有账户实调；应在 100 条 pilot 中检验是否接收参数、A/B 覆盖率，以及未偏置时两者均可见的样本上分数差异。这是可执行的连续评分候选方案，不能因 top-20 限制就直接判其不可行，也不能承诺 100% 覆盖。[logit_bias 定义](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)。

先做约 100 条、每条 3 次的小试评分，报告 A/B 同时可用率、非标签/拒答率、重复分数变化以及筛选边界附近的名次变化。温度为零和固定 seed 都不构成确定性证明，官方仅承诺 seed 的尽力复现。**主统计保留边界全部同分并报告实际放行率；确定性排序仅用于展示，不伪造连续性，也不添加隐藏扰动。**只生成一个有效标签时，`finish_reason=length` 可以是预期的单 token 截断，不能一律判无效；空输出、仅空白、拒答或缺少有效候选则不能得分。主比较应固定一次评分结果，重复试验另行检验稳定性。[seed 与结束原因](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)。

## 3. 至少十万条公开金融标题：原始来源核验

| 候选 | 原作者所报规模与当前可见内容 | 使用判断 |
| --- | --- | --- |
| FNSPID | 作者称 15.7 million 金融新闻记录、1999–2023；原作者 Hugging Face 提供 `Article_title`、日期、URL、publisher 等字段 | **规模与字段满足候选要求；文字授权待确认。** 新闻记录数不是去重后的独立标题数，未下载统计。 |
| Bloomberg / Reuters Financial News Dataset | 原仓库称 Bloomberg 450,341、Reuters 109,110 条 | **不选。** 原作者明确因版权原因不再在线提供；没有寻找绕过撤下的镜像，也未联系作者。 |
| NIFTY | 作者数据卡提供 2,111 个按日聚合样本；每行可含多个标题，卡片标 MIT | **不能据此认定满足十万独立标题。** 未统计展开后的独立标题；论文称来源包含 WSJ、Reuters 等，卡片标签不足以证明第三方标题文字授权。 |

FNSPID 的来源为[原作者仓库](https://github.com/Zdong104/FNSPID_Financial_News_Dataset)及[原作者数据卡](https://huggingface.co/datasets/Zihan1004/FNSPID)。仓库 README 顶部 2025-07-24 公告称开放商业及研究使用；但旧段落仍限制代码的商业使用，[LICENSE](https://github.com/Zdong104/FNSPID_Financial_News_Dataset/blob/main/LICENSE)仍为 CC BY-NC 4.0。较宽新公告和较窄旧许可不一致，**并不等于禁止非商业研究**；可以将其保留为按 CC BY-NC 非商业范围、署名条件使用的首选技术候选。不过，旧限制明指代码，仓库 LICENSE 与新闻文字的具体适用范围没有被单独说明，聚合者也不能自动证明各新闻源授予其全部文字权利。当前 HF viewer 还显示数据生成错误，不能未经试读就保证默认 `load_dataset` 路径可用。上述均为发布页观察，未作法律许可结论。

第二项依据为[原作者仓库 README](https://github.com/philipperemy/financial-news-dataset)。第三项依据为[NIFTY 作者数据卡](https://huggingface.co/datasets/raeidsaqur/NIFTY)和[作者论文的数据来源章节](https://arxiv.org/html/2405.09747v1)。本次通过 GitHub 连接器读取原仓库，不将 Kaggle 或转存者的许可标签当作权属保证，也没有把论文的许可当作新闻文字许可。

当前可推进的是：明确尾部事件和评分提示，配置 API 后完成极小规模接口试评分；正式大样本数据以 FNSPID 为优先候选，在报告中保留非商业研究范围及第三方新闻文字权属的未确认项。研究使用、向外部 API 提交标题、公开再分发文字是不同问题；仅发布 ID、分数与汇总可减少文字再分发，却不能证明全部来源方权利。这是证据边界，不额外设立泛化许可审批，也不把“可下载”直接写成“文字权属已完全确认”。

## 4. FNSPID 小规模访问实测：可以试读，文件头不是随机样本

2026-11-16 对[原作者 Stock_news 目录](https://huggingface.co/datasets/Zihan1004/FNSPID/tree/main/Stock_news)及其[文件元数据 API](https://huggingface.co/api/datasets/Zihan1004/FNSPID/tree/main/Stock_news?recursive=false&expand=false)作了只读检查。目录只有以下两个 CSV，没有单独的标题投影文件。对两文件均发送 `Range: bytes=0-1048575`，实际响应均为 **HTTP 206**，`Content-Range` 与所请求区间一致。

| 文件 | 元数据精确大小 | 首 1 MiB 内保守计入的完整行 | 精确唯一标题 | 股票代码数 |
| --- | ---: | ---: | ---: | ---: |
| `All_external.csv` | 5,731,397,037 bytes | 4,605 | 4,356 | 5 |
| `nasdaq_exteral_data.csv` | 23,232,979,597 bytes | 152 | 139 | 1 |

实测 CSV 表头为 `Date, Article_title, Stock_symbol, Url, Publisher, Author, Article, Lsa_summary, Luhn_summary, Textrank_summary, Lexrank_summary`；第二个文件另有开头的 `Unnamed: 0` 列。以 UTF-8 严格解码、CSV 解析，并保守丢弃区间末端最后一条解析结果，避免把截断行当完整记录；第二个文件的尾端确实截在未完成的引用字段内。表中所有计入行都有非空标题。只输出字段、日期和计数，**没有输出标题或保存新闻正文**。

`All_external.csv` 前缀不是全局日期单调序列，而且单一股票占其中 2,739 行；该数字是出现总数，不是经核验的连续块长度。`nasdaq_exteral_data.csv` 前缀全部属于同一股票，日期从 2023-12-16 向 2023-05-09 递减。上述只描述本次前缀，不能外推全文件排序；但已经足以否定“读取前 20,000 行就是随机金融标题样本”的做法。精确去重后仍可能有大小写/格式变体，也不能把不同标题直接当作独立新闻事件。

本次 Python 访问累计读取响应正文 **2,097,790 bytes**：目录元数据 638 bytes，加两个各 1,048,576 bytes 的区间；低于 10 MB 上限。另查看了目录网页，未下载整库、未调用付费接口，也未向模型提交新闻。

**十万标题池的结论：**原作者所报规模足够，HTTP Range 的低成本访问已验证；但这次只实测了上述几千个唯一标题，尚未证明能在 10 MB 内取得十万去重标题，更没有证明事件独立性。仅凭文件字节大小或前缀密度不能保证全库唯一数量。

若采用 `All_external.csv` 作为明确限定的候选总体，较简单的下一步是顺序流式扫描，用固定的标题规范化规则去重，对首次出现的新标题做均匀 reservoir 抽样，再从这个去重池随机抽取评分样本。这样无需保存文章正文，也不会把文件头冒充随机样本；但仍要传输该文件约 **5.73 GB**，读取部分列不会自动降低 CSV 网络传输量。若总体定义为两文件合并，则须处理约 **28.96 GB** 及跨文件重复。随机抽取字节窗口只能作为访问诊断或明确标注的块样本，窗口边界、记录长度和股票聚集会使其不同于均匀标题抽样。本次没有执行这些扫描或抽样。
