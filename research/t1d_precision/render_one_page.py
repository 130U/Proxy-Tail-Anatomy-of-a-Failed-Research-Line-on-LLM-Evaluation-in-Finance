"""Render the requested compact result page only from a complete results.json."""
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parent


def estimate(summary, percent=False, decimals=2):
    value = summary.get('estimate') if summary else None
    if value is None:
        return '—'
    scale = 100 if percent else 1
    suffix = '%' if percent else ''
    digits = 1 if percent else decimals
    point_digits = 2 if percent and min(abs(100*value-80), abs(100*value-90)) < .05 else digits
    text = f'{scale*value:.{point_digits}f}{suffix}'
    interval = summary.get('ci95')
    if interval is not None:
        text += f' [{scale*interval[0]:.{digits}f}{suffix}, {scale*interval[1]:.{digits}f}{suffix}]'
    return text


def kappa(summary):
    return estimate({'estimate': summary.get('kappa'), 'ci95': summary.get('kappa_ci95')})


def percentage_point_change(summary):
    value = summary.get('estimate') if summary else None
    if value is None:
        return '—'
    text = f'{100*value:+.1f} 个百分点'
    interval = summary.get('ci95')
    if interval is not None:
        text += f' [{100*interval[0]:+.1f}, {100*interval[1]:+.1f}]'
    return text


def require_complete(result):
    if not (result.get('complete') and result.get('inference_complete') and result.get('semantic_review_complete')):
        raise ValueError('Main inference or mandatory semantic review is incomplete; ONE_PAGE must not be rendered.')
    reviews = result.get('semantic_reviews', {})
    if not reviews.get('complete') or not all(reviews.get(name, {}).get('complete') for name in ('review_b', 'review_c')):
        raise ValueError('The embedded semantic review summary is incomplete.')
    for condition in ('A', 'B', 'C'):
        expected = result['sample']['expected_by_condition'][condition]
        if result['summary_table'][condition]['available_n'] != expected:
            raise ValueError('Primary response counts do not match the frozen design.')
    b = reviews['review_b']
    if b.get('first_valid_n') != 139 or not isinstance(b.get('strict_valid_n'), int) or not isinstance(b.get('majority_valid_n'), int):
        raise ValueError('The requested 139-to-strict-retention comparison is unavailable.')
    if not 0 <= b['strict_valid_n'] <= 139 or not b['strict_valid_n'] <= b['majority_valid_n'] <= 196:
        raise ValueError('Inconsistent strict/majority retention counts.')
    if result['precision_decision']['status'] not in ('classified', 'exclusions_above_10pct'):
        raise ValueError('The frozen decision rule has not been evaluated.')


def render_one_page(result):
    require_complete(result)
    table = result['summary_table']
    lines = ['| | 条件 A 不问 | 条件 B 问 | 条件 C 问并教 |', '|---|---:|---:|---:|']
    rows = [
        ('可打分的回答数', None, False),
        ('声称位数的中位数', 'claimed_digits', False),
        ('真实可信位数的中位数', 'true_digits', False),
        ('多报一位以上的比例', 'overreported', True),
        ('区间“准确”的比例', 'width_accurate', True),
        ('区间“过窄”的比例', 'width_narrow', True),
        ('1% 判断准确率', 'onepct_accuracy', True),
    ]
    for label, metric, percent in rows:
        values = []
        for condition in ('A', 'B', 'C'):
            summary = table[condition]
            if metric is None:
                values.append(f'{summary["scorable_n"]}/{summary["available_n"]}；{estimate(summary["scorable_fraction"], percent=True)}')
            else:
                values.append(estimate(summary['metrics'].get(metric), percent=percent))
        lines.append('| ' + ' | '.join([label, *values]) + ' |')
    lines.extend(['', '表内方括号为固定 237 个页面簇、10,000 次 bootstrap 的 95% 区间；第一行同时给出可评分比例。A 的“声称位数”仅指字面打印位数。前轮16/12位对应144道同源同式增长题的分组中位数。', ''])

    decision = result['precision_decision']
    if decision['status'] == 'classified':
        lines.append(f'按执行前固定门槛（区间准确比例 ≥80%，且 1% 判断准确率 ≥90%），本轮归类为 **{decision["classification"]}**。')
    else:
        exclusions = []
        for condition in ('A', 'B', 'C'):
            s = table[condition]
            if s['available_n'] and s['excluded_n'] / s['available_n'] > .1:
                exclusions.append(f'{condition} 排除 {s["excluded_n"]}/{s["available_n"]}')
        causes = {condition: table[condition]['exclusion_reasons'] for condition in ('A', 'B', 'C') if table[condition]['excluded_n']}
        reasons = '；'.join(f'{condition}：' + '、'.join(f'{reason}={count}' for reason, count in sorted(values.items())) for condition, values in causes.items())
        lines.append('触发任务预设例外：' + '；'.join(exclusions) + '，超过 10%；先报告排除原因，暂不强行套用三分类。' + reasons + '。')
    paired = result['paired_C_minus_B']['all_scorable']['all']
    metrics = paired['metrics']
    if paired['paired_scorable_n']:
        lines.append(f'同题配对 C−B：区间准确比例 {percentage_point_change(metrics["width_accurate"])}；1% 判断准确率 {percentage_point_change(metrics["onepct_accuracy"])}。'
                     f'其中 {paired["truth_transition"]["truth_changed"]["count"]}/{paired["paired_scorable_n"]} 题的真实 1% 状态随算式或来源改变；差异不能解释为精度意识的纯因果效应。')
    else:
        lines.append('没有同题双方均可评分的回答，未估计 C−B 配对差。')
    if result['sample']['C_design'] == 'half':
        extra = result['sample'].get('extra_C_n', 0)
        lines.append(f'C 使用执行前固定抽取的 98 对、196 题；额外 {extra} 条 C 回答保留但不进入主分析。')

    reviews = result['semantic_reviews']
    rb, rc = reviews['review_b'], reviews['review_c']
    stable = rb['second_invalid_or_uncertain']['control']
    witness = rb['second_invalid_or_uncertain']['witness']
    strict = rb['strict_valid_n']
    lines.extend(['', f'语义复核主数字：**139 → {strict}**（两轮均 valid）；多数判 valid 为 {rb["majority_valid_n"]}。'
                  f'196 道见证的两轮一致率 {estimate(rb["agreement"], percent=True)}，κ={kappa(rb["agreement"])}。'
                  f'二轮 invalid/uncertain：稳定题 {stable["count"]}/{stable["n"]}（{estimate(stable, percent=True)}），'
                  f'见证题 {witness["count"]}/{witness["n"]}（{estimate(witness, percent=True)}）。'])
    ref = rc['reference_error_strict_fraction_of_all_reviewed']
    alt = rc['reasonable_alternative_strict_fraction_of_all_reviewed']
    ref_agreed = rc['reference_error_fraction_of_agreed_causes']
    alt_agreed = rc['reasonable_alternative_fraction_of_agreed_causes']
    lines.append(f'T1C 的 68 个拒绝案例：两轮归因一致率 {estimate(rc["agreement"], percent=True)}，κ={kappa(rc["agreement"])}；'
                 f'在 {ref_agreed["n"]} 个两轮归因一致案例中，“参考答案有问题” {ref_agreed["count"]}/{ref_agreed["n"]}（{estimate(ref_agreed, percent=True)}），'
                 f'“合理口径差异” {alt_agreed["count"]}/{alt_agreed["n"]}（{estimate(alt_agreed, percent=True)}）；'
                 f'两类严格计数占全部复核案例分别为 {ref["count"]}/{ref["n"]}、{alt["count"]}/{alt["n"]}。')
    blind_limits = sorted(set(rb.get('adjudication_origin_blinding_limitation_ids', []) + rc.get('adjudication_origin_blinding_limitation_ids', [])))
    if blind_limits:
        lines.append(f'第三轮 {len(blind_limits)} 条理由因流程字样与实质论据无法安全拆开而保留，来源盲化有限；不影响“两轮均 valid”的主计数。')

    secondary = result.get('secondary_B')
    if secondary and secondary.get('inference_complete'):
        ss = secondary['summary']
        model = '、'.join(secondary.get('model_counts', {})) or '另一档模型'
        effort = '、'.join(secondary.get('reasoning_effort_counts', {}))
        source = model + (' / ' + effort if effort else '')
        lines.extend(['', f'独立复跑 B（{source}）：{ss["scorable_n"]}/{ss["available_n"]} 可评分，'
                      f'区间准确 {estimate(ss["metrics"]["width_accurate"], percent=True)}，'
                      f'多报一位以上 {estimate(ss["metrics"]["overreported"], percent=True)}，'
                      f'1% 判断准确率 {estimate(ss["metrics"]["onepct_accuracy"], percent=True)}；不混入主结论。'])
    elif secondary and secondary.get('status') != 'not_run':
        lines.extend(['', f'另一档 B 未完成，仅保存 {secondary.get("available_n", 0)}/{secondary.get("expected_n", 392)} 条可分析回答，不作为完整复跑或纳入主结论。'])

    lines.extend(['', '解释边界：A 的打印位数不等于主动声明可信精度；B 已提醒数字经过舍入，测的是提醒后能否计算。真值均按各回答自身算式。FinQA 公开，训练暴露可能存在；没有区间标签不等于已排除污染。A 的精确服务版本未暴露，且 B/C 分时运行，跨条件比较保留服务条件限制。'])
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results', type=Path, default=ROOT / 'results.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'ONE_PAGE.md')
    args = parser.parse_args()
    result = json.loads(args.results.read_text(encoding='utf8'))
    try:
        text = render_one_page(result)
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f'Refusing final one-page output: {exc}') from exc
    args.output.write_text(text, encoding='utf8', newline='\n')
    print(json.dumps({'written': str(args.output), 'complete': True, 'characters': len(text)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
