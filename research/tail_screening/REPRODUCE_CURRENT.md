# 复算当前尾部筛选研究

复算读取保存的模型判断，不重新调用agent。没有API密钥、费用、训练或联网要求。所有路径相对于解压后的项目根目录，保留research目录结构；原metadata里的绝对路径只记录当时来源，统计分析使用当前目录下的相对位置。

本次实际复算环境为Python 3.12.14、numpy 2.5.3、scipy 1.18.1、matplotlib 3.11.2；它们不是模型版本保证。已有环境中的matplotlib放在`../tmp/tail_plot_deps`，本机运行因此加`--plot-deps ../tmp/tail_plot_deps`；普通已安装依赖的环境可省去该参数。其他版本未逐一验证兼容性。

```powershell
python research/tail_screening/analyze_agent_methods.py --method all
python research/tail_screening/analyze_agent_methods_validation.py
python research/tail_screening/review_measurements.py
```

前两条重建阶段1及阶段2JSON、PNG/PDF图、逐项报告，覆盖同名派生文件，不改原始评分。第三条是独立内部复核，另行实现关键整数聚合、边界人数和通过条件，不调用生产分析函数。执行耗时可变，数字与gate应一致。原始JSON拒绝重复key、缺失/重复ID和非法值；保留全部真实并列，不添加随机扰动。

数据位置：`research/private/agent_tail_methods/stage1_n32/`含32条输入、32份pair结果及16份rank结果；`stage2_n128_sol/`含128条输入及8份rank结果。两处保存exact prompt、随机顺序和family映射。成对原始496对整批输入保留，但分析仅使用正式4×124分批结果；两次无输出尝试记录在methods_protocol.md，不伪造JSON。

抽样准备脚本仅供研究溯源，已有数据目录会拒绝覆盖，不需要为了复算重新抽样。可只验证stage1分批：

```powershell
python research/tail_screening/prepare_agent_methods.py --verify-batches
```

当前分析每份报告写明主分母q90/p=放行人数/(N×p)，并另列实际B/A。名义人数floor(Np)，边界全部同分纳入；90%目标人数ceil(0.9×A实际人数)。阶段1主p=.25，阶段2主p=.1/.2。8个重复排序不是8组新文本，两个方向及组合范围不是CI。

旧开发和词法曲线也可复算：

```powershell
python research/tail_screening/analyze_agent_pilot.py --variant v1
python research/tail_screening/analyze_agent_pilot.py --variant v2
python research/tail_screening/analyze_baselines.py
```

词法复算使用保存的word/char逐条预测，并执行固定200次配对词法簇bootstrap；不重训模型。结果条件于固定模型、划分与词法簇假设，有限窗口斜率不是结构α。private/real_baseline中的来源文本及历史预测随当前本地交付保存，许可和来源说明见research/data及历史研究说明，不将本地保存视为新的无限再分发授权。

历史九轮的复算入口为research/REPRODUCE.md。旧FABLE_REVIEW_BUNDLE、HANDOFF_MANIFEST和package_handoff.py属于旧包历史记录，不是当前交付的合并正文或验证清单；本轮未新增哈希清单或打包脚本。当前先读FABLE_CURRENT_REPORT，再用单独源文件核验。

可复算的是已保存判断的统计结果。fresh agent的服务器版本、内部采样与上下文过程无法完全固定，因此重新评分不保证得到同一排序。数学和文献报告中的开放问题也不会因代码运行成功自动解决。
