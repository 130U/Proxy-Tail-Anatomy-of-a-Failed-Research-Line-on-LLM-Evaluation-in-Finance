# 集中技术报告的构建与阅读版验收

日期：2026-11-16。最终交付为10页A4英文[阅读版PDF](output/pdf/audit_budgets_working_report.pdf)，约4,636词正文，19个显示公式、157个行内公式、3张表。可编辑[Markdown](manuscript.md)与[LaTeX](manuscript.tex)另附。本PDF由本地Chromium原生MathML排版，**不是TeX编译结果**；原全套理论notes.tex的规定编译验收没有因此完成。

## 内容与身份核对

[独立论文审查](../reports/paper_review.md)逐项回应PR01–PR06，比较两个源稿的全部176段数学表达，最终仅忽略空白后顺序完全一致。全部20格的Direct、Box、Balanced成本与精确节省也和既有结果JSON一致。发现并修复了D定义被错误转义的问题；盒预算整数约定已写明。审查支持内部技术报告定位，保留原创性、实际用途和G0/G1的科学缺口。

| 文件 | 最终SHA256 |
|---|---|
| manuscript.md | a9cd81ab194e54bb583dab69cbc7f3440745468b2f701ee6146e66c02d844ce0 |
| manuscript.tex | f4b423e730e235c38d816d4f50ea61fa2a6cb6b16d0aac94b906e29f144c02f2 |
| build_pdf.py | 52de49e5d830fbb0be69d24c28229d4bb3cdb1c751dfd3688fbdf25b895db8cb |
| 最终PDF | dabaf18262c037aabd8d3c2a67047bfc16f0047ad1b0f6e34789efd782b3f1f8 |

机器可读构建信息见[BUILD_RESULT.json](BUILD_RESULT.json)。PDF可能包含生成时间等元数据，重建不承诺逐字节相同；内容源哈希用于核对本次被审版本。

## 本地构建与视觉检查

按[执行前约定](BUILD_PROTOCOL.md)运行。PDF技能要求的marker已在首次生成前成功执行一次；随后只修排版并重建，未重复marker。使用已有Python、Playwright、Chrome 157.0.8103.78与Poppler，没有安装依赖。浏览器隔离临时profile、上下文离线、请求拦截及禁止外部资源的CSP均启用；本页构建记录的请求计数为0。

首轮内部构建耗时1.7981秒，生成10页。逐页查看Poppler图像后发现普通括号不应随整式拉高、数学text首尾空格丢失及孤立标点问题。只修改构建器：普通分隔符禁止自动拉伸、显式成对分隔符局部伸缩、保留text空白、绑定紧邻标点并避免引导句和公式分离；稿件正文与数学源哈希未变。

最终内部构建耗时1.4061秒；外层命令墙钟约3.39秒，Poppler渲染约1.85秒。没有GPU训练，峰值内存未测。运行程序检测176个数学节点、原生分式可用、公式和表格横向越界列表为空。pypdf确认10页并提取33,006个字符；文字提取不替代版面检查。

主代理查看了最终全部10页的100dpi渲染：未观察到裁切、重叠、缺失方块字形、断裂表行或缺页。重点核对accuracy式、超几何比值、D定义、矩形max风险、阶数分离、阈值优化、语义式和完整20格表。跨页表头重复且全部20行保留，页码连续1/10至10/10。当前PDF使用原生MathML字体样式，不声称与TeX字形排印逐像素一致。

## 复现

在仓库根目录、已有Python环境中：

```powershell
python research/paper/build_pdf.py --check
python research/paper/build_pdf.py --render
```

`--check`只在内存解析；`--render`需要本机已有的Chrome或Edge、Node、Playwright及pypdf。默认指向本次捆绑runtime，换机器可以传`--node`、`--playwright`、`--browser`；不自动下载。未知数学命令、原生MathML不可用或公式越界会明确失败。临时HTML、profile及渲染页图不进入研究归档。

本轮只新增排版、内容审查及独立精确数学检查，没有重跑既有模型实验。打包私有数据边界的1项既有测试再次通过；第六轮106项集成单元测试仍属于此前运行记录，未冒充本轮新跑106项。
