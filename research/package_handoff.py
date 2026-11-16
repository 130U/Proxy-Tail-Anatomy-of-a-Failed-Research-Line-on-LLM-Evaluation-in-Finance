"""Build a local review bundle and portable archive; never upload or send."""
import hashlib
import json
import posixpath
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


ROOT=Path(__file__).resolve().parent
EXCLUDED={'FABLE_REVIEW_BUNDLE.md','HANDOFF_MANIFEST.json'}
HANDOFF_DATE='2026-11-16'
ARCHIVE_NAME=f'FABLE_HANDOFF_COMPLETE_{HANDOFF_DATE}.zip'


def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                  and 'private' not in [part.casefold() for part in p.relative_to(ROOT).parts]
                  and not p.is_symlink()
                  and p.suffix != '.pyc' and p.name not in EXCLUDED
                  and not (p.name.startswith('FABLE_HANDOFF_') and p.suffix == '.zip'))


def main():
    description={
        'START_HERE.md':'完整交付首读指引、阅读顺序与文件导航',
        'FABLE_FULL_REPORT.md':'截至第九轮的完整研究总报告、证据与未关闭问题',
        'FABLE_HANDOFF.md':'阶段交接说明与需要导师复核的问题；先读新首读页和总报告',
        'reports/2026-11-15-round1.md':'自足进展报告、修正和G0/G1状态',
        'claims_audit.md':'46项公开主张审计与文件覆盖',
        'claims_sources.json':'审计来源文件哈希',
        'theory/notes.md':'T0–T3完整假设、证明与反例',
        'theory/notes.tex':'LaTeX理论稿，未编译PDF',
        'theory/independent_review.md':'独立数学复核与限定',
        'literature/literature_review.md':'17条一手证据台账与差异判断',
        'literature/question_status.md':'Q01–Q32完成状态与缺口',
        'literature/local_review.md':'独立代码复核、修复与有限域检查',
        'checks/results.json':'10万点数学检查与有限耦合枚举实际输出',
        'REPRODUCE.md':'本地复现指令和环境',
        'reproduction_log.json':'125项集成单元测试、10项来源自测及13条复现命令',
        'reports/2026-11-16-round9.md':'任意随机审计的精确解、强简单对照及研究判断',
        'theory/randomized_audit.md':'RA1–RA4、匹配下界、自适应/期望预算及公平渐近',
        'planning/RANDOMIZATION_PROTOCOL.md':'随机配额探索范围、非退化输出约定及预算',
        'planning/randomized_audit.py':'精确风险、最小样本量与固定规模策略采样器',
        'planning/test_randomized_audit.py':'文档子集枚举、边界和采样构造测试',
        'planning/run_randomization.py':'完整32格离线比较运行器与来源hash',
        'planning/randomization_results.json':'32个同质人工构造的精确风险与最小审计量',
        'planning/randomization_table.md':'全部32格，保留合取族零新增收益',
        'reports/randomization_review.md':'独立AI数学及实现审查，709格与32行核对',
        'reports/randomization_review_checks.py':'不导入作者内核的文档级穷举和整表复核',
        'reports/2026-11-16-round8.md':'位置价值边界、强简单组合与随机配额替代',
        'theory/localization_value.md':'LV1–LV5、常数sharp界、原尺度等价及简单基线',
        'planning/localization_results.json':'44个精确比较及4个仅解析界构造，人工输入',
        'planning/localization_table.md':'完整48行表，不挑选有利比较器',
        'planning/localization_io_failure.json':'Windows原子替换失败的真实快照与错误链',
        'planning/pooled_scope_check.json':'类外pooled随机配额的单个精确反方核对',
        'reports/localization_review.md':'新理论与全部结果的独立审查，保留程序类边界',
        'reports/2026-11-16-round7.md':'集中技术稿、最强简单对照与论文级反方审查',
        'reports/paper_review.md':'独立AI论文审查；原创性与现实性仍开放',
        'reports/paper_review_checks.py':'26个均衡设计及9261配额的独立精确核对',
        'paper/manuscript.md':'英文内部技术稿；条件证明与最强简单替代',
        'paper/manuscript.tex':'与Markdown对应的LaTeX稿，未编译',
        'paper/output/pdf/audit_budgets_working_report.pdf':'本地MathML排版的技术报告PDF，非投稿完成稿',
        'paper/FABLE_DECISION_NOTE.md':'给Fable的三个优先裁定问题，尚未发送',
        'paper/BUILD_RECORD.md':'本地PDF构建、公式与逐页版面检查记录',
        'reports/2026-11-16-round6.md':'P2语义集合、必要宽度、符号对照与选择风险',
        'reports/numeric_envelope_review.md':'语义包络定理和有理检查器独立复核',
        'theory/semantic_envelopes.md':'SE1–SE6完整条件、证明与候选相对边界',
        'numeric/record.md':'25格完整结果及七类构造反例，非自然覆盖率',
        'reports/2026-11-16-round5.md':'历史非干扰、可测性与来源准入的义务分离',
        'reports/pit_review.md':'PNI1–PNI6与PIT代码独立审查、反例和修复',
        'theory/pit_noninterference.md':'六项条件命题、条件随机性及两世界识别下界',
        'pit/record.md':'210次构造比较、3错标仍准入与实际时间记录',
        'reports/2026-11-16-round4.md':'真实来源实体情绪基线与独立审查闭环',
        'reports/real_baseline_review.md':'独立实现/统计复核及修复记录',
        'experiments/real_baseline/report.md':'word/char真实简单基线与配对区间；非历史证书',
        'reports/2026-11-16-round3.md':'影响结构审计与真实日期来源核对进展',
        'reports/impact_review.md':'新证明/优化器/日期绑定的独立复核与修复',
        'theory/impact_audit.md':'IA1–IA8证明及矩形程序成本分离',
        'planning/impact_report.md':'预定20格全表；全族中位收益0，未过提案门',
        'data/source_audit.md':'10份保存FOMC来源日期核对，历史字节仍未知',
        'paths/COMPARATIVE_ANALYSIS.md':'五份路径比较、Top3条件建议与保留分歧',
        'paths/PEER_REVIEW.md':'独立AI反方审查、数学核对与修订复核',
        'paths/REVIEW_RESPONSE.md':'七项important回应与尚未关闭的科学门',
        'paths/DECISION_CRITERIA.md':'下一轮可否决阈值及联合样本预算提案',
        'paths/SENIOR_REVIEW_REQUEST.md':'给用户指定资深助手的待发问题包',
        'reports/2026-11-15-round2.md':'集体统计量证书与本地原料盘点增量',
        'reports/completion_audit.md':'全部工作包、32题和G0/G1终态逐项验收',
        'reports/local_data_inventory.md':'真实本地来源元数据与哈希核查，未复制原文',
        'theory/collective_metrics.md':'共同分片下accuracy与macro-F1包络证明',
    }
    rows=['# 研究产出索引', '', f'完整交付登记日期为{HANDOFF_DATE}；原始研究日期见各文件。先读[START_HERE.md](START_HERE.md)和[FABLE_FULL_REPORT.md](FABLE_FULL_REPORT.md)。下列索引逐文件登记已有研究；代码不是已验证的真实金融模型，项目G0/G1仍未通过。', '',
          'advisor_reference中的原导师材料是注明来源和日期的历史背景快照，不是本次新增执行授权。当前交付仅在本地整理，未向外部发送。', '',
          '| 日期 | 编号 | 文件 | 结论或用途 |','|---|---|---|---|']
    for p in files():
        rel=p.relative_to(ROOT).as_posix()
        if rel=='INDEX.md': continue
        if rel.startswith('advisor_reference/'):
            code='导师历史参考'; meaning='原导师材料的来源/日期快照；背景参考，不构成新增执行授权'
        elif rel in {'START_HERE.md','FABLE_FULL_REPORT.md'}:
            code='完整交付入口'; meaning='截至第九轮的阅读导航与完整研究总报告'
        elif rel.startswith('answers/'):
            code=p.stem; meaning='重点文献题部分完成；子问题缺口见正文'
        elif rel.startswith('paths/'):
            code='路径比较'; meaning='离线候选分析与审查；非已确认原创/真实有效'
        elif rel.startswith('certificates/') or rel.startswith('experiments/collective_metrics/'):
            code='CM1–CM5'; meaning='共同分片统计量条件证书；构造输入非真实模型'
        elif rel.startswith('planning/'):
            code='T1.4/规划'; meaning='固定零发现条件的最小审计量；非序贯有效'
        elif rel.startswith('data/'):
            code='来源核对'; meaning='本地日期声明与元数据；不是历史版本证明'
        elif rel.startswith('pit/'):
            code='T1.1/WP1.2'; meaning='给定日志的历史非干扰构造；不认证真时间'
        elif rel.startswith('numeric/'):
            code='P2/SE1–SE6'; meaning='有限语义候选的严格数值包络；非真实解析证书'
        elif rel.startswith('paper/'):
            code='集中技术稿'; meaning='条件数学与比较边界；非原创性/真实整链验收'
        elif rel.startswith('real_baseline/') or rel.startswith('experiments/real_baseline/'):
            code='新WP0.1'; meaning='来源原任务新基线；私有逐行产物不入包'
        elif rel.startswith('experiments/wp0_1/') or rel.startswith('evaluation/'):
            code='WP0.1'; meaning='汇总重建/簇评测；真实三基线仍缺失'
        elif rel.startswith('theory/') or rel.startswith('checks/'):
            code='WP0.3'; meaning='条件数学命题与健全性检查'
        elif rel.startswith('xbrl/'):
            code='WP0.4'; meaning='受限离线样例；无真实时间戳证书'
        elif rel.startswith('local/') or rel.startswith('experiments/local_foundations/'):
            code='WP0.2/0.5/T1.4'; meaning='合成世界、消融与精确审计计算'
        else: code='交接'; meaning='本地研究材料'
        rows.append(f'| {HANDOFF_DATE} | {code} | [{rel}]({rel}) | {description.get(rel,meaning)} |')
    rows += [f'| {HANDOFF_DATE} | 打包 | [FABLE_REVIEW_BUNDLE.md](FABLE_REVIEW_BUNDLE.md) | 全部可交付Markdown的完整合并阅读版，含编号目录与来源标题 |',
             f'| {HANDOFF_DATE} | 打包 | [HANDOFF_MANIFEST.json](HANDOFF_MANIFEST.json) | 文件SHA256及合并Markdown数量/完整列表，不含清单自身 |',
             f'| {HANDOFF_DATE} | 打包 | [{ARCHIVE_NAME}]({ARCHIVE_NAME}) | 已有研究截至第九轮的完整本地归档；不含私有数据、权重或旧ZIP |']
    (ROOT/'INDEX.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    order=['START_HERE.md','FABLE_FULL_REPORT.md','paths/COMPARATIVE_ANALYSIS.md','FABLE_HANDOFF.md',
           'reports/2026-11-16-round9.md','theory/randomized_audit.md',
           'planning/randomization_table.md','reports/randomization_review.md','planning/RANDOMIZATION_PROTOCOL.md',
           'reports/2026-11-16-round8.md','theory/localization_value.md',
           'planning/localization_table.md','reports/localization_review.md','planning/LOCALIZATION_PROTOCOL.md',
           'paper/FABLE_DECISION_NOTE.md','reports/2026-11-16-round7.md',
           'paper/manuscript.md','reports/paper_review.md','paper/BUILD_PROTOCOL.md','paper/BUILD_RECORD.md',
           'reports/2026-11-16-round6.md','theory/semantic_envelopes.md',
           'numeric/record.md','reports/numeric_envelope_review.md','numeric/PROTOCOL.md','numeric/README.md',
           'reports/2026-11-16-round5.md','theory/pit_noninterference.md',
           'pit/record.md','reports/pit_review.md','pit/PROTOCOL.md','pit/README.md',
           'reports/2026-11-16-round4.md','experiments/real_baseline/report.md',
           'real_baseline/PROTOCOL.md','real_baseline/DESIGN_REVIEW.md',
           'reports/real_baseline_review.md','real_baseline/REVIEW_RESPONSE.md',
           'real_baseline/PREPARATION_ACCOUNTING.md',
           'reports/2026-11-16-round3.md','planning/impact_report.md',
           'theory/impact_audit.md','data/source_audit.md','reports/impact_review.md',
           'paths/COMPARATIVE_ANALYSIS.md',
           'paths/PATH_01_audited_information_set.md','paths/PATH_02_numeric_sensitivity.md',
           'paths/PATH_03_audit_design_frontier.md','paths/PATH_04_dependence_robust_risk.md',
           'paths/PATH_05_proof_carrying_numeric_reasoning.md',
           'paths/PEER_REVIEW.md','paths/REVIEW_RESPONSE.md','paths/DECISION_CRITERIA.md',
           'paths/INDEPENDENT_CHALLENGES.md','paths/SENIOR_REVIEW_REQUEST.md','paths/STUDY_CHARTER.md',
           'reports/2026-11-15-round2.md','reports/completion_audit.md','reports/local_data_inventory.md',
           'theory/collective_metrics.md','experiments/collective_metrics/report.md',
           'planning/record.md','literature/collective_review.md',
           'reports/2026-11-15-round1.md','INDEX.md','theory/notes.md',
           'theory/independent_review.md','claims_audit.md','literature/literature_review.md',
           'literature/question_status.md',*[f'answers/Q{q}.md' for q in ['03','10','13','29','30','31','32']],
           'experiments/wp0_1/record.md','experiments/local_foundations/report.md','checks/record.md',
           'xbrl/record.md','literature/local_review.md','REPRODUCE.md']
    # Keep the requested reading order, deduplicate it, then include every
    # remaining eligible Markdown file. files() continues to exclude private
    # paths, symlinks, caches, prior ZIPs, the generated bundle and manifest.
    markdown_files={p.relative_to(ROOT).as_posix():p for p in files() if p.suffix.casefold()=='.md'}
    ordered=[]
    seen=set()
    for rel in order:
        if rel not in markdown_files:
            raise FileNotFoundError(f'Required Markdown input missing or excluded: {rel}')
        if rel not in seen:
            ordered.append(rel)
            seen.add(rel)
    for rel in markdown_files:
        if rel not in seen:
            ordered.append(rel)
            seen.add(rel)
    order=ordered
    assert len(order)==len(markdown_files) and set(order)==set(markdown_files)
    parts=[f'# Fable 完整研究交付阅读版\n\n交付登记日期：{HANDOFF_DATE}。本文件完整合并截至第九轮已有研究中全部可交付Markdown，共{len(order)}份，而非精选摘要。先读首读指引、完整总报告和路径比较，再按目录查阅证明、审查、实验记录与历史参考。\n\n'
           f'配套源码、JSON结果、可编辑TeX和现有PDF保存在[{ARCHIVE_NAME}]({ARCHIVE_NAME})中；本阅读版不以粘贴代码或数值文件替代原始产物。文件清单、SHA256及Markdown合并覆盖列表见[HANDOFF_MANIFEST.json](HANDOFF_MANIFEST.json)。私有文本、逐行标签、预测、权重、缓存与旧ZIP不进入此归档。\n\n'
           '各历史材料保留原始研究日期和当时状态；原导师材料位于advisor_reference，属于带来源的历史背景，不是新执行授权。后续记录对早期主张的修订应结合完整总报告理解，不能把早期阶段性结论当作最新验收结果。\n\n'
           '这是已有研究的完整交付，不是已完成的认证金融模型、原创性确认或论文投稿。项目G0/G1仍未通过；内部AI审查不代表Fable意见。本次仅本地打包，尚未对外发送。\n\n## 阅读目录\n\n']
    parts.extend(f'{number}. [{rel}](#source-{number:03d})\n' for number,rel in enumerate(order,1))
    for number,rel in enumerate(order,1):
        p=markdown_files[rel]
        content=p.read_text(encoding='utf-8')
        def links(match):
            target=match.group(2)
            if '://' in target or target.startswith(('#','/')): return match.group(0)
            rewritten=posixpath.normpath(posixpath.join(posixpath.dirname(rel),target))
            return f'[{match.group(1)}]({rewritten})'
        content=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',links,content)
        parts.append(f'\n\n---\n\n<a id="source-{number:03d}"></a>\n\n## {number:03d} · 来源：{rel}\n\n'
                     f'独立源文件：[{rel}]({rel})\n\n<!-- source: {rel} -->\n\n'+content)
    bundle=ROOT/'FABLE_REVIEW_BUNDLE.md'
    bundle.write_text(''.join(parts),encoding='utf-8')
    payload=files()+[bundle]
    manifest=dict(date=HANDOFF_DATE,base_commit='8e4dd0b33c95ac2ac1a6015eba6f2dfafe5c1254',
                  branch='research/certifiable',
                  status='complete delivery of existing research through round9; project G0/G1 not passed',
                  archive_name=ARCHIVE_NAME,
                  merged_markdown_count=len(order),merged_markdown_files=order,
                  markdown_coverage=dict(eligible_count=len(markdown_files),complete=True,
                                         generated_bundle_excluded='FABLE_REVIEW_BUNDLE.md'),
                  advisor_reference_status='historical background with original source/date, not new execution authorization',
                  network_policy='offline since explicit user steering; no publication or external messages',
                  files=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,
                              sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in payload])
    mf=ROOT/'HANDOFF_MANIFEST.json'; mf.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    archive=ROOT/ARCHIVE_NAME
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in payload+[mf]: z.write(p,'research/'+p.relative_to(ROOT).as_posix())
    with ZipFile(archive) as z:
        assert z.testzip() is None
        for f in manifest['files']:
            assert hashlib.sha256(z.read('research/'+f['path'])).hexdigest()==f['sha256']
    print(json.dumps(dict(files=len(payload)+1,merged_markdown_count=len(order),archive_bytes=archive.stat().st_size,
                          bundle_bytes=bundle.stat().st_size,archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest()),indent=2))


if __name__=='__main__': main()
