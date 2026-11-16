# 离线复现

第9轮默认集成包含125项单元测试和13条子命令，最终已全部通过；来源解析10项自测另计。新增 `python -m research.planning.run_randomization` 按[协议](planning/RANDOMIZATION_PROTOCOL.md)重算32个同质阈值构造，输入第八轮当前JSON，输出精确风险/少一篇风险/最小样本量及hash；没有训练、私有原文或网络。单独运行时先确保已有完整第八轮结果，统一脚本已按依赖顺序执行。首次表0.643217秒，最终集成表0.651663秒，峰值内存未测。

独立核对命令为 `python research/reports/randomization_review_checks.py --verify-results`，不导入作者内核，检查总体≤10的709个预算格及主表32行；只用标准库。报告见[独立审查](reports/randomization_review.md)。每次重跑会刷新耗时/输入hash，历史审查hash只绑定其明确版本；不应为凑旧hash修改实际结果。第九轮定理的自适应与期望预算扩展是纸笔证明，当前采样器只实现固定样本量构造。

在本工作区根目录执行；Python 3.12.14、NumPy 2.5.3、PyTorch 2.14.1+cpu 是本次实际环境。理论检查器主要用标准库，评测用NumPy，合成训练用PyTorch；第四轮真实基线及其构造测试还使用SciPy 1.18.1、scikit-learn 1.9.1、joblib 1.6.0、threadpoolctl 3.7.0。无需GPU、API key或下载。

归档中的 `research/` 可独立解压；从其父目录用 `python research/reproduce.py` 运行新代码。下面旧指标重建命令额外读取原仓库 `docs/experiment-results.md` 的哈希，须在本包注明的基线仓库中执行；现成的重建JSON已随包提供。没有在归档内复制整个旧仓库或任何私有材料。

```powershell
& '..\130U-FinLLM\.venv\Scripts\python.exe' research/reproduce.py
```

重跑四配置三seed合成训练：

```powershell
& '..\130U-FinLLM\.venv\Scripts\python.exe' research/reproduce.py --train
```

其他机器可在已具备上述依赖的环境中把解释器换成 `python`。脚本不自动安装依赖、不联网、不下载权重。原环境路径只是本机便利用法，不包含在可移植代码逻辑内。

旧公开指标的汇总重建：

```powershell
python -m research.evaluation.reconstruct
```

`research/reproduction_log.json` 记录本机检查命令、退出码与输出。理论JSON只是数学组件示例；真实模型、真实解析和可信核心前提未被这些命令验证。合成实验报告的叙事被固定到本轮配置，修改配置后需人工复核结论。

第2轮加入 `certificates/` 的共同分片accuracy/macro-F1检查器和 `planning/` 的精确审计量前沿。集成命令会运行两套新测试、手工票型示例、规划前沿及条件审计链示例。`certificates/` 输入为每个头的类别预测；`planning/` 输入为每类票数，具体schema请读各自README，不能互换。

第3轮集成命令还包含影响图审计8项、阈值设计5项（单元测试合计49项），日期绑定解析器10项自测，以及20格固定阈值族扫描。来源审计的10份真实文件重读需原仓库本地数据，另按 `data/source_audit.md` 的 `--source-root` 命令执行；主集成命令只运行其可移植自测，不会寻找或下载原始数据。

第4轮加入原生三类标签评测、真实基线准备/训练/联合预测接口的构造测试和私有归档排除测试，当轮共74项集成单元测试；来源解析10项自测另计。默认命令只在人工构造行上验证新训练器，不读取私有真实来源，也不重复真实9次拟合。真实运行另按以下显式命令进行；运行前读 `real_baseline/PROTOCOL.md`，结果和局限见 `experiments/real_baseline/report.md`。

```powershell
python -m research.real_baseline.prepare --source '../130U-FinLLM/data/raw/candidates/sentfin/SEntFiN.csv'
python -m research.real_baseline.train_baselines --input research/private/real_baseline/rows.jsonl --private-output research/private/real_baseline/trained --summary research/experiments/real_baseline/baseline_summary.json --manifest research/real_baseline/aggregate_manifest.json
python -m research.real_baseline.bootstrap_results --predictions research/private/real_baseline/trained/predictions_test.jsonl
```

准备/训练命令写入同名本地产物；保留旧运行时应先复制整个工作目录再执行。原CSV、逐行派生数据、词表和模型不在归档中；未持有匹配哈希的本地原始CSV时，只能执行公开构造测试并检查已有汇总，不能声称独立重跑了真实成绩。训练器会核验输入指纹；本机Windows中文DLL路径后备修复只在进程内生效，不更改已安装库。线程证据是库自报配置，峰值内存未实测。

路径比较轮的独立审查另有标准库检查（已加入第3轮集成命令，但不计入49项单元测试，也没有重新训练）：

```powershell
python research/paths/review_checks.py
```

标准输出应与 `paths/review_checks.json` 对应：1,008个R1有理可达性例、1,024个D1分层漏检概率例，以及理想条件样本预算。脚本只输出JSON，不修改记录；没有执行R2线性规划，不使用真实模型结果。数学有限检查不替代定理证明。

`theory/notes.tex` 尚未编译；可读证明在 `theory/notes.md`，本包没有冒充编译后的PDF。

第5轮加入18项PIT构造测试，当前共92项集成单元测试、10项来源解析自测；统一脚本包含10条子命令，均已通过。最后的 `python -m research.pit.run_checks` 对30个历史基例做210次整链/2100次字节比较，还包含3类故意错误程序、3条错标时间边界、16个布尔seed映射和旧公开来源元数据再汇总。该运行器只有标准库依赖，不读取私有语料、不训练模型。结果写 `pit/results.json`，运行环境/时间与历史稳定产物分开；详见 `pit/record.md`。旧公开source_audit.json已随包提供，不需原始FOMC文件即可重算本轮元数据表。

第6轮加入14项语义包络单测，当轮共106项集成单元测试、10项来源解析自测；统一脚本11条子命令均已通过。`python -m research.numeric.run_checks` 重算严格有理数包络、25格人工宽度门和各反例，结果写 `numeric/results.json`。它不调用自然文本解析器、不训练模型，不将模型概率当真实概率；详见 `numeric/record.md`。源码、配置及外部依赖未变时，复跑产生的耗时字段仍可变化，历史审查报告的快照hash只绑定当时版本。

第8轮加入10项最强总数门测试和第12条子命令 `python -m research.planning.run_localization`。该命令按[冻结执行范围](planning/LOCALIZATION_PROTOCOL.md)重算20个原阈值比较、8个合取、16个star及4个仅含解析界的sharp构造，最长墙钟60秒；没有主线训练、真实审计或联网。完整记录写`planning/localization_results.json`，包含源码/输入哈希、每格状态和`min(Box,TotalK)`强简单对照；不得将4个bounds-only行当成全局最优数值解。统一复跑会先刷新原阈值JSON的时间字段，新记录绑定其当前哈希；历史报告仍只描述当时运行。

独立反方核对另可执行 `python research/reports/localization_review_checks.py`；加`--verify-results`复核完整表及最终推导hash，不调用作者风险或优化内核。这些是有限数学检查，不是新颖性或真实模型效果验收。第7轮10页PDF的本地重建说明见[构建记录](paper/BUILD_RECORD.md)，它不属于数学批量复现命令。

本轮未运行原仓库完整训练/全部原有测试，因为未修改原应用代码。只运行与新增研究代码相关的检查。

第8轮曾在第12条命令的原子结果替换遇到Windows共享错误，失败快照保存在`planning/localization_io_failure.json`。修复后新增3项I/O回归测试，最终统一复跑为119项单元测试、12条命令全部通过；10项来源自测另计。`python research/reports/localization_review_checks.py --verify-pooled`还可独立核对类外pooled抽样的单点计算；该点不属于48行固定配额主表。私有原始文本和模型训练未在这些检查中读取或重跑。
