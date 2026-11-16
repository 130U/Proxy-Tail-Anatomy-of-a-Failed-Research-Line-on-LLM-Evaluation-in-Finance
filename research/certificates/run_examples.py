"""Run frozen, constructed vote examples; no model training or downloads."""
import hashlib
import json
from pathlib import Path
import platform
import time

from research.certificates.collective import certify


def main():
    started=time.perf_counter()
    cases=[dict(name='shared_budget_strict_improvement',votes=[[0,1],[1,0],[0,1],[1,0]],labels=[0,0,1,1],classes=2,budget=1),
           dict(name='component_optima_incompatible',votes=[[1,1,1,2,2],[1,1,1,1,1],[2,2,2,2,2]],labels=[0,1,2],classes=3,budget=1),
           dict(name='no_contamination_perfect',votes=[[0,0,1],[1,1,2],[2,2,0]],labels=[0,1,2],classes=3,budget=0),
           dict(name='all_heads_change',votes=[[0,0,1],[1,1,2],[2,2,0]],labels=[0,1,2],classes=3,budget=3)]
    records=[]
    for case in cases:
        for method in ('component','exact'):
            tick=time.perf_counter()
            result=certify(case['votes'],case['labels'],case['classes'],case['budget'],method)
            records.append(dict(name=case['name'],method=method,result=result,elapsed_seconds=time.perf_counter()-tick))
    root=Path('research/experiments/collective_metrics'); root.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(cases,sort_keys=True,indent=2).encode('utf-8')
    (root/'constructed_inputs.json').write_bytes(raw)
    data=dict(source_level='our_experiment_mathematical_constructed_examples',
              data_sha256=hashlib.sha256(raw).hexdigest(),base_commit='8e4dd0b33c95ac2ac1a6015eba6f2dfafe5c1254',
              checker_sha256=hashlib.sha256(Path('research/certificates/collective.py').read_bytes()).hexdigest(),
              python=platform.python_version(),platform=platform.platform(),processor=platform.processor(),
              elapsed_seconds=time.perf_counter()-started,records=records,
              status='conditional_component_verified; real_model_and_timestamp_premises_unverified')
    (root/'results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 集体统计量包络：实际计算结果','',
           '所有数值来源：我们的实验（构造票矩阵，非真实模型）。实际计算耗时 %.4f 秒。'%data['elapsed_seconds'],'',
           '| 输入 | 方法 | 逐点accuracy | 集体accuracy | 逐点macro-F1 | 集体macro-F1 |','|---|---|---|---|---|---|']
    def show(x):return '['+x['lower_exact']+', '+x['upper_exact']+']'
    for row in records:
        r=row['result']; independent=r['independent']; collective=r['collective']
        lines.append('| '+ ' | '.join([row['name'],row['method'],show(independent['accuracy']),show(collective['accuracy']),
                                       show(independent['macro_f1']),show(collective['macro_f1'])])+' |')
    lines+=['','第一例证明共同受影响头约束可能严格收紧界；第二例证明逐类F1分别取极值只是外包络，不能宣称联合可达。',
            'exact指在固定集合、选定头可自由改变所有输出这一放松模型内精确；不指真实训练过程能实现每个端点。',
            '统计量包含固定的全部K类，零支持且零预测类贡献0，不能在每次扰动后动态删去类别。',
            '实际部署须先另行证明可信核心和共享组件不受污染改变，再由有效审计确定影响头预算。这些输入前提没有在本实验中核实。',
            '本轮不据此通过G0或G1，不声称集体投毒证书或macro-F1优化是新理论。',
            '状态预算或子集预算耗尽时程序拒绝输出；当前实现的指数/组合复杂度限制了大规模使用。']
    (root/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=data['status'],cases=len(cases),methods=2,
                          elapsed_seconds=data['elapsed_seconds'],report=str(root/'report.md'))))


if __name__=='__main__':main()
