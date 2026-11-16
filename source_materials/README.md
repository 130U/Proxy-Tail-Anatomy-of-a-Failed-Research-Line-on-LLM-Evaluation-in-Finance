# 研究所用的来源材料

此目录补齐报告与复算引用的旧项目材料，未复制虚拟环境、账户配置或无关个人文件。

`130U-FinLLM/`以声明审计的旧工作树提交`8e4dd0b33c95ac2ac1a6015eba6f2dfafe5c1254`为主要源码/文档来源，附本地保存的来源数据和补充文件。它是研究来源快照，不是完整Git历史。`research/claims_sources.json`列出的全部原文已逐字节核对一致。原始上游仓库为[130U/130U-FinLLM](https://github.com/130U/130U-FinLLM)。

`source_audit/`单独保存历史FOMC/权利复核实际读取的本地版本，因为四份文档与声明审计旧版本不同。它包括完整120条纪要JSONL、120份纪要HTML、12份索引快照、manifest及八份权利/语义证据；八份证据与`research/data/source_audit.json`记录完全一致。这样两个历史审计都可核验，不以新版本覆盖旧证据。

SEntFiN原始CSV、实体列表、README、candidate manifest及原作者MIT许可位于`130U-FinLLM/data/raw/candidates/sentfin/`。保留[原作者LICENSE](130U-FinLLM/data/raw/candidates/sentfin/LICENSE)。派生实体行、词法族、固定划分及逐条预测位于`research/private/real_baseline/`。作者数据许可和此前保存的新闻来源权利限制分别保留，不把本次上传解释为额外版权授权。

FOMC记录注明Federal Reserve Board纪要出处、抓取时间和权利说明。保存2026年的页面不证明同一字节在早年即已可得；原研究限制未改变。旧manifest还登记未在当前实验使用的其他语料，本目录不把那些登记项冒充已附数据。当前尾部实验只使用保存的SEntFiN实体标题。

源码与来源数据各自保留已有许可，本次没有为第三方内容声明统一的新许可。复算命令见[根目录说明](../REPRODUCE.md)。
