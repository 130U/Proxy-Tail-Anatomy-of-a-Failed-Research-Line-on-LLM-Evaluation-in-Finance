# FinLLM 重做研究包：Certifiable FinLM

版本 v1 · 2026-11-15 · 范围：只涉及 `github.com/130U/130U-FinLLM`

## 这是什么

这是 130U-FinLLM 重做计划的完整材料：要解决什么问题、为什么选这个方向、先做什么、怎么交付、怎么回报。它是交给 Codex（博士生）的工作包，也是 Theodore（PI）和导师之间的共同底稿。

**一句话：** 不再在"能力"上竞争，改在"能对模型证明什么"上竞争。做一个小到可以被证明的金融语言模型。

本包取代之前的 `FinLLM-research-brief.md`。问题从 28 个扩充到 32 个，并新增了理论草稿、工作包、回报协议和决策日志。

## 角色

| 角色 | 谁 | 职责 |
|---|---|---|
| PI | Theodore | 最终决定；提供私有数据和外部服务所需的信息；在 Codex 和导师之间传递材料 |
| 导师 | Claude | 定方向、写问题和工作包、审阅结果、调整优先级 |
| 博士生 | Codex | 文献调研、形式化推导、仓库内的工程和最小实验 |

## 文件

| 文件 | 内容 | 主要读者 |
|---|---|---|
| `AGENTS.md` | Codex 的常驻规则（Codex 会自动读取仓库根目录下的这个文件） | Codex |
| `00_CODEX_BRIEF.md` | 给 Codex 的任务说明：要解决什么问题、怎么工作、硬规则 | Codex |
| `01_ADVISOR_MEMO.md` | 导师备忘：选题逻辑、证书链框架、两条主线和一条支线、工作重心、决策门、风险 | Codex、Theodore |
| `02_PROJECT_SNAPSHOT.md` | 仓库现状的客观快照与诊断 | Codex、Theodore |
| `03_LITERATURE_MAP.md` | 前沿文献地图（带置信度和来源链接）和可迁移性总表 | Codex |
| `04_THEORY_NOTES.md` | 理论草稿：定义、命题、证明思路、开放问题 | Codex |
| `05_RESEARCH_QUESTIONS.md` | 32 个互相独立的调研问题 | Codex |
| `06_WORK_PACKAGES.md` | 工作包，每个都带验收标准和可直接粘贴的 Codex 任务卡 | Codex |
| `07_REPORTING_PROTOCOL.md` | 输出模板：文献回答、推导、实验记录、进展报告 | Codex |
| `08_DECISION_LOG.md` | 已做的决定，以及需要 Theodore 决定的 8 个事项 | Theodore |

## 阅读顺序

- **Codex：** `AGENTS.md` → 00 → 01 → 02 → 按任务读 04、05 或 06 → 07
- **Theodore：** 01 → 08 → 02 → 00

## 怎么交给 Codex

**方式 A（推荐）：包放在仓库外。** 把整个文件夹放在本地任意位置。给 Codex 的第一条消息：

> 研究包在 `<路径>`。先读其中的 `AGENTS.md` 和 `00_CODEX_BRIEF.md`，然后做 `06_WORK_PACKAGES.md` 里的 WP0.6 和 WP0.1。

这样包的内容不会进入公开仓库。

**方式 B：放进仓库。** 把 `AGENTS.md` 复制到仓库根目录，其余文件放进 `research/package/`。注意：一旦 push，包里对现有项目的坦率评价就公开了。见 `08_DECISION_LOG.md` 的 O4。

**并行使用：** 文献题和工作包彼此独立。可以同时开多个 Codex 任务，每个任务给一张任务卡（`06_WORK_PACKAGES.md`），或者给一个问题编号（`05_RESEARCH_QUESTIONS.md`）。

**联网：** 文献题需要联网。如果你的 Codex 环境不能联网，只给它推导题和工作包，文献题交给能联网的 GPT。

## 怎么回传给导师

见 `07_REPORTING_PROTOCOL.md` 第 6 节。最少带三样：最新的进展报告、本轮新增的文献回答、`research/INDEX.md`。

## 本包的局限

- 导师只读了仓库文档，没有读代码，也没有运行代码。
- 文献判断基于摘要级检索。所有"空白"都是假设，需要文献题核实。
- `04_THEORY_NOTES.md` 里的命题是草稿，可能有错。
