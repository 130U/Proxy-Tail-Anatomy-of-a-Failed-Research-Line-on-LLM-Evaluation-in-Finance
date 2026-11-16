# 在本仓库复算

当前结果可由保存的评分复算，不调用agent、不需要API凭据，也不训练模型。命令从仓库根目录运行。

实际数值环境为Python 3.12.14，依赖版本见`requirements-analysis.txt`。依赖已存在时运行：

```sh
python research/tail_screening/review_measurements.py
python research/tail_screening/analyze_agent_methods.py --method all
python research/tail_screening/analyze_agent_methods_validation.py
```

第一条用独立实现核对原始输出与保存结果，不改结果。后两条重写对应JSON、PNG、PDF图和逐项报告；运行时间可变，统计数值和判定应相同。原始评分不变。详细定义及旧开发/词法复算见[当前复算说明](research/tail_screening/REPRODUCE_CURRENT.md)。

抽样准备脚本已移除旧仓库目录名依赖，保留种子及拒绝覆盖既有实验的行为；已存数据无需重新准备。验证成对分批：

```sh
python research/tail_screening/prepare_agent_methods.py --verify-batches
```

历史原始数据准备脚本可使用`--source source_materials/130U-FinLLM/data/raw/candidates/sentfin/SEntFiN.csv`。它拒绝覆盖已有样本和聚合文件；复读结果无需重做。历史混淆矩阵重建的来源路径已增加本仓库快照回退，不改变数学或随机设置。

历史FOMC日期复核输入已附上：

```sh
python research/data/fomc_source_audit.py --self-test
python research/data/fomc_source_audit.py --source-root source_materials/source_audit
```

第二条重写历史审计派生JSON（时间字段会变化）。当前上传保留原报告与原JSON，版本见[source说明](source_materials/README.md)。其他历史复算见[research/REPRODUCE.md](research/REPRODUCE.md)，旧绝对路径是当时运行记录。

阅读版PDF构建源码需要`reportlab`、`pypdf`及合法可用的中文TrueType字体。Windows默认微软雅黑；其他环境传入字体。只检查素材、不生成PDF：

```sh
python research/tail_screening/render_reports.py --check --font-regular /path/to/regular.ttf --font-bold /path/to/bold.ttf
```

去掉`--check`会重建两份阅读版PDF。字体与排版可能受环境影响，保存PDF为已经逐页检查的交付版。

迁移只作路径适配、补齐来源和更新导航，没有重新评分、调整门槛或改写研究结果。保存的agent输出能重算；重新调用模型不保证输出相同。
