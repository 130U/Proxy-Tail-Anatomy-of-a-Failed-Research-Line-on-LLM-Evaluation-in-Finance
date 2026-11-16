# 仓库现状快照（截至 2026-11-15）

**来源：** GitHub 上的 `README.md`、`docs/PROJECT_OVERVIEW.md`、`docs/MODEL_CARD.md`、`docs/TRAINING_SYSTEM.md`、`docs/ENGINEERING.md`、`docs/experiment-results.md`，以及仓库文件树。

**局限：** 导师只读了文档，没有读代码，也没有运行代码。第 8 节列出需要你在代码里核实的事项。

---

## 1. 公开的 24M Trial

| 项目 | 值 |
|---|---|
| 参数量 | 24,255,744 |
| 层数 / hidden / FFN | 6 / 512 / 1,664 |
| 注意力 | GQA，8 个 query head，4 个 KV head，head dim 64 |
| 其他组件 | RoPE（theta 1e6）、RMSNorm、SwiGLU、QK norm、输入输出权重共享 |
| 词表 / 上下文 | 8,192 / 512 |
| 骨干来源 | MiniMind 的一个固定版本，修改记录在 `docs/THIRD_PARTY_NOTICES.md` |
| 训练流程 | 随机初始化 → next-token 预训练 → 金融域适配 → target-conditioned stance SFT → 校准与接受阈值 |
| 任务 | 输入英文金融标题 + 字面目标实体，输出 bearish / neutral / bullish、三类概率、方向分数 `100 × (P(bull) − P(bear))`、复核标记 |

---

## 2. 数据与结果

**SFT 数据：**

- 训练集 705 行：491 neutral / 140 bullish / 74 bearish。
- 开发集 101 条：76 neutral / 15 bullish / 10 bearish。
- 测试集 101 条。

**结果：**

| 系统 | 划分 | 样本数 | Accuracy | Macro-F1 |
|---|---|---:|---:|---:|
| 初始 SFT | 开发集 | 101 | 75.25% | 0.2863 |
| 初始 SFT | 测试集 | 101 | 58.42% | 0.2458 |
| 类加权 TF-IDF + 逻辑回归 | 开发集 | 101 | 75.25% | 0.6087 |
| 类平衡 SFT | 开发集 | 101 | 78.22% | 0.6549 |

**类平衡 SFT 在开发集上的分类别结果：**

| 类别 | 样本数 | Precision | Recall | F1 | 正确数 | 被预测为该类的数量 |
|---|---:|---:|---:|---:|---:|---:|
| Bearish | 10 | 0.4545 | 0.5000 | 0.4762 | 5 | 11 |
| Neutral | 76 | 0.9394 | 0.8158 | 0.8732 | 62 | 66 |
| Bullish | 15 | 0.5000 | 0.8000 | 0.6154 | 12 | 24 |

最后两列由导师从 precision、recall 和样本数推算。三类的预测数加起来是 101，与总数一致。

**文档自己写明的限制：**

- 初始 SFT 在开发集和测试集上把所有样本判成 neutral。
- 类平衡 SFT 是在同一个开发集上做的探索性选型，不是独立测试。测试集已经在初始运行时看过，没有再用来评估类平衡模型。
- 划分不是按时间的，事件级独立性没有完全审计。
- 类平衡运行的指标来自 Theodore 提供的 Kaggle 日志，它的 checkpoint 没有被独立下载核实。
- 类平衡运行的参数：3 个 epoch，139 次 optimizer 更新，4,419 个有监督的标签 token，每个 epoch 每类重复采样到 491 次曝光。代码版本 `75a90c3fca66ae08abf77742ccbd4368e50c7e25`。
- 仓库里有 DPO 的代码和配置，但没有任何 DPO 运行结果。

---

## 3. 文档描述的两项"核心设计"

### 3.1 Financial semantic permissions

对每个"原文–编辑"样本对、每个任务轴，人工标注四种关系之一：

- 标签保持（label-preserving）
- 分布保持（distribution-preserving）
- 改标签（relabel）
- 不加约束（no constraint）

损失由三部分组成：

1. 原文和编辑后文本各自的交叉熵；
2. 分布等价对上的一致性约束；
3. 改标签对上的相对响应 margin。当标签从 a 改为 b 时：

```
D = [log q(b|edited) − log q(a|edited)] − [log q(b|orig) − log q(a|orig)]
L_change = max(0, margin − D)
```

文档自己写道：需要在同一批编辑样本上和普通交叉熵对比。这个对比**没有做过**。

### 3.2 Objective-preserving scaling

包括以下几项：

- sample family 记账：同一事件派生的所有视图属于一个 family，先划分 family 再派生视图；
- 跨设备和梯度累积时使用全局有效分母：`local_loss_r = W × Σ_j λ_j S_rj / C_j`；
- 只在有监督的位置做全词表投影，以节省输出层计算；
- 打包时使用分段因果注意力，防止一个样本看到相邻样本的答案；
- 断点恢复时同时恢复 optimizer 状态、随机状态和数据消费位置。

---

## 4. 仓库结构

| 目录 | 数量 | 说明 |
|---|---:|---|
| `src/finllm/` | 27 个模块 | 其中 `kaggle_*`、`*_runtime`、`expansion*`、`continuation` 等大部分是运行环境和流程相关 |
| `scripts/` | 26 个 | 大部分是 notebook 生成器、Colab/Kaggle 导出、数据抓取 |
| `notebooks/` | 19 个 | 00–06 各阶段及其变体 |
| `tests/` | 40 个 | 测试覆盖较好，这是优点 |
| `reports/` | 20 个 | JSON 运行记录和检查结果 |
| `docs/` | 约 25 个 | 包括 `docs/research/` 下的 5 份数据和后训练计划 |
| `configs/` | 6 个 | model_24m、pretrain、pretrain_pilot、domain、sft、dpo |

---

## 5. 2.4B 私有版本

文档给出的架构：28 层，hidden 2,560，FFN 8,320，Q20 / KV4，head dim 128，词表 65,536，上下文 4,096，总参数 2,397,459,968。

文档把"50B + 5B 输入 token"和"32k 人工 gold 标注"写成 **recipe allocation**（配方分配），并说明实际消耗另行记录。

**公开材料无法判断 2.4B 是否已经训练完成。** 这是给 Theodore 的开放问题，见 `08_DECISION_LOG.md` 的 O1。如果它只是设计，README 首屏的表述和"让结论可验证"的定位是冲突的。WP0.6 的声明审计会把这一点写清楚。

---

## 6. 诊断小结

| 问题 | 严重程度 | 说明 |
|---|---|---|
| 没有"为什么要从零训练"的答案 | 根本性 | 新方向的出发点 |
| 证据不足以支持"模型有效" | 高 | 0.655 对 0.609，样本很少，没有置信区间，没有独立测试 |
| 任务饱和 | 高 | 标题三分类情感 |
| 核心设计未检验 | 中 | permission 损失没有消融 |
| 声明超出公开证据 | 中 | 2.4B 的表述 |
| 工程多、研究少 | 中 | 大量代码是运行环境搬运 |

---

## 7. 要保留的资产，以及它们在新方向里的作用

| 现有资产 | 在新方向中的作用 |
|---|---|
| `as_of` 字段、来源记录（provenance） | P1：信息集证书的数据前提 |
| tokenizer 与评测集排除边界 | P1：F_t-可测管线的一部分 |
| 确定性训练、恢复语义 | P1：分片聚合证书要求每个分片的训练是确定性函数 |
| sample family、先划分再派生 | P3 和评测地基：family 就是天然的簇 |
| semantic permissions | P2：敏感度规范的雏形，也是软约束 vs 硬约束对比中的"软"一侧 |
| 校准 / 阈值 / 最终测试分区 | P3：部署风险证书使用校准后的概率 |
| 40 个测试 | 证书检查器的测试框架 |
| 24M 架构代码 | 合成世界实验的小骨干 |

---

## 8. 需要你在代码里核实的事项

1. permission 损失（3.1 节的公式）是否已经在代码里实现？在哪个文件？有没有生成编辑样本对的代码？
2. 分段因果注意力和"只在有监督位置投影"是否实现在 24M 的代码里？
3. 同 seed 在 CPU 上重跑，是否得到逐位相同的权重？分片聚合证书需要这一点。
4. tokenizer 是用什么数据训练的？那些数据的时间范围是什么？
5. SFT 数据是否来自 SEntFiN？仓库里的 `scripts/prepare_sentfin_review.py` 暗示是。如果是，我们可以从公开的 SEntFiN 重建一个公开版本，用于 WP0.1 和 WP0.2。
6. `reports/` 里的 JSON 记录了哪些可复现信息？是否足以重建实验？
