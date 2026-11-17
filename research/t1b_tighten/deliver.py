"""Build readable tables, the requested waterfall, and a one-page decision."""
import csv
import hashlib
import json
import platform
import os
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from prepare import HERE

def disposition(r):
    if r['stages']['duplicates']['status']=='certified_inside':return 'duplicate_determined'
    if r['stages']['sums']['status']=='certified_inside':return 'sum_determined'
    return r['final']

def write_csv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    out=HERE/'results';s=json.loads((out/'summary.json').read_text(encoding='utf8'))
    rows=[json.loads(l) for l in (out/'per_question.jsonl').read_text(encoding='utf8').splitlines()]
    reviews={r['id']:r for part in ('a','b') for r in json.loads((HERE/f'review_{part}.json').read_text(encoding='utf8'))}
    c=Counter(disposition(r) for r in rows);n=len(rows);keep=c['retained']
    assert sum(c.values())==196
    s['mutually_exclusive_waterfall_dispositions']=dict(c)
    s['reviewed_equations']=sum(len(r['equations']) for r in reviews.values())
    s['questions_with_equations']=sum(bool(r['equations']) for r in reviews.values())
    s['duplicate_disclosures']=sum(len(r['duplicates']) for r in reviews.values())
    s['questions_with_duplicates']=sum(bool(r['duplicates']) for r in reviews.values())
    s['questions_with_shrunk_input_box']=sum(r['stages']['original']['bounds']!=r['stages']['duplicates']['bounds'] for r in rows)
    s['questions_with_shrunk_output_after_sums']=sum(
        F(r['stages']['sums']['enclosure']['hi'])-F(r['stages']['sums']['enclosure']['lo']) <
        F(r['stages']['duplicates']['enclosure']['hi'])-F(r['stages']['duplicates']['enclosure']['lo']) for r in rows)
    (out/'delivery_summary.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    compact=[]
    for r in rows:
        compact.append({'id':r['id'],'category':r['category'],'sample40':r['sample40'],
            'review_verdict':r['review_verdict'],'final_semantics_first':r['final'],'waterfall_disposition':disposition(r),
            'original_lo':r['stages']['original']['enclosure']['lo'],'original_hi':r['stages']['original']['enclosure']['hi'],
            'after_duplicates_lo':r['stages']['duplicates']['enclosure']['lo'],'after_duplicates_hi':r['stages']['duplicates']['enclosure']['hi'],
            'after_sums_lo':r['stages']['sums']['enclosure']['lo'],'after_sums_hi':r['stages']['sums']['enclosure']['hi'],
            'inside_value':r['inside_witness']['value'] if r['inside_witness'] else '',
            'outside_value':r['stages']['sums'].get('witness_value',''),
            'range_exact':r['stages']['sums']['range_exact'],'review_reason':r['review_reason']})
    write_csv(out/'question_summary.csv',compact)
    write_csv(out/'sample40_review.csv',[{'id':r['id'],'binding_ok':reviews[r['id']]['binding_ok'],
        'quantity_ok':reviews[r['id']]['quantity_ok'],'program_ok':reviews[r['id']]['program_ok'],
        'verdict':r['review_verdict'],'reason':r['review_reason']} for r in rows if r['sample40']])
    inventory=[{'id':r['id'],'bounds':r['stages']['sums']['bounds'],'constraints':r['stages']['sums']['inventory']} for r in rows]
    (out/'constraint_inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in inventory),encoding='utf8')
    # Published waterfall follows numerical stages, then excludes semantic
    # problems; the MSI semantic uncertainty overlaps the duplicate removal.
    dup=c['duplicate_determined'];sums=c['sum_determined'];ref=c['reference_incompatible']
    invalid=c['semantic_invalid'];uncertain=c['semantic_uncertain'];other=n-keep-dup-sums-ref-invalid-uncertain
    assert other==0
    stages=[n,n-dup,n-dup-sums,n-dup-sums-ref,keep]
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    font_path=os.environ.get('T1B_FONT_PATH','C:/Windows/Fonts/msyh.ttc')
    font=FontProperties(fname=font_path) if Path(font_path).exists() else FontProperties(family='sans-serif')
    plt.rcParams.update({'axes.unicode_minus':False,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(11.7,6.3),layout='constrained')
    colors=['#254B65','#4A8E84','#4A8E84','#AD7551','#C48662','#254B65']
    heights=[n,dup,sums,ref,invalid+uncertain,keep]
    bottoms=[0,stages[1],stages[2],stages[3],keep,0]
    labels=['原始候选','重复披露\n收紧','增加加总\n约束','参考答案\n不相容','语义复核\n排除','最终保留']
    for i,(h,b,col) in enumerate(zip(heights,bottoms,colors)):
        if h:ax.bar(i,h,bottom=b,width=.64,color=col,zorder=3)
        else:ax.plot([i-.32,i+.32],[b,b],color=col,lw=3,zorder=3)
        if i in (0,5):text=str(h);y=h+4
        else:text=f'−{h}' if h else '0';y=b+h+4
        ax.text(i,y,text,ha='center',va='bottom',fontsize=14,fontweight='bold',color='#243B4A',fontproperties=font)
    levels=[n,stages[1],stages[2],stages[3],keep]
    for i,level in enumerate(levels):ax.plot([i+.32,i+.68],[level,level],color='#A5ADB3',lw=1)
    ax.axhline(58,color='#966E35',ls='--',lw=1.4,zorder=2)
    ax.text(.65,61,'保留门槛：58 道 / 1,147',fontproperties=font,color='#966E35',fontsize=10)
    ax.set_xticks(range(6),labels,fontproperties=font,fontsize=11)
    ax.set_ylabel('题数',fontproperties=font,fontsize=11)
    ax.set_ylim(0,220);ax.set_xlim(-.6,5.6)
    ax.set_yticks([0,50,100,150,200]);ax.grid(axis='y',alpha=.15,zorder=0)
    for side in ('top','right'):ax.spines[side].set_visible(False)
    ax.spines['left'].set_color('#CBD1D5');ax.spines['bottom'].set_color('#CBD1D5')
    ax.tick_params(axis='both',length=0)
    fig.suptitle(f'T1B：收紧并复核后，{keep} 道题仍有容差内外两种可行值',fontproperties=font,fontsize=17,color='#203C50')
    ax.set_title(f'占测试集 {keep}/1,147 = {keep/1147:.2%}；1% 为审计容差',fontproperties=font,fontsize=11,loc='left',pad=20,color='#53616B')
    fig.supxlabel('范围：FinQA 完整题目上下文。语义复核共发现 37 道明确问题、20 道存疑；其中 1 道已在重复披露阶段移除。',fontproperties=font,fontsize=9,color='#53616B')
    for suffix in ('png','pdf','svg'):fig.savefig(out/f'waterfall.{suffix}',dpi=200,facecolor='white')
    svg=out/'waterfall.svg'
    svg.write_bytes(('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf8').splitlines())+'\n').encode('utf8'))
    plt.close(fig)
    one=f'''# T1B 一页结论：结论保留，比例从 17.09% 降至 {keep/1147:.2%}

**最终保留 {keep}/1,147 = {keep/1147:.2%}，超过任务门槛 58 道。** 对每个保留题，都保存了两组严格位于舍入区间内部、精确满足全部已确认线性约束的有理数输入：一组结果在 gold 的 1% 容差内，另一组在外。这是存在性结论，不是模型通常答错的概率，也不是基准标注错误率。

范围经用户确认：FinQA 提供的完整表格与正文；不覆盖原始年报其他页面。只针对 T1 的 196 个 test 见证，不外推未审查题目的语义正确性。

|顺序归因（互斥）|题数|
|---|---:|
|仍有容差内外可行值|{keep}|
|重复披露使数值区间进入容差|{dup}|
|进一步加总使区间进入容差|{sums}|
|收紧后全区间与 gold 不相容|{ref}|
|其余题意、绑定或数量类型明确有问题|{invalid}|
|其余语义无法确认，保守剔除|{uncertain}|
|合计|196|

唯一由重复披露数值上收紧的 MSI/2008/page_69.pdf-2，本身也存在“损失下降/增长”的语义疑问；语义复核总计因此是 **37 明确问题 + 20 存疑**，不能再把它重复扣一次。CME/2010/page_69.pdf-2 只有额外假设列出的分项穷尽总授信额，才出现区间与 gold 不相容；原文“including”不足以支持这一假设，因此仅保存为敏感性分析，不进入主计数。

**抽样复核：** 固定种子 20261116 抽取 40 题，27 通过、8 明确问题、5 存疑。明确错误为20%；把存疑也算入风险则为32.5%，超过四分之一。按保守口径执行修正：核查单位、年份、经济角色、精确值/舍入值、程序覆盖与分母方向；将全部196题逐条复核，剔除全部57个非通过题，并对原始1147题重跑T1，确认原196队列可重现。未静默修正gold，也未声称另外951题已通过语义审查。

**计算与复核：** {s['duplicate_disclosures']} 条同事实追加披露，{s['reviewed_equations']} 条已确认线性关系；{s['questions_with_shrunk_input_box']} 题输入盒因重复披露变窄，{s['questions_with_shrunk_output_after_sums']} 题输出范围因加总进一步收窄。{s['exact_final_ranges']}/196 个最终范围达到精确极值，其余如有则使用已证明外包络。588 个阶段证书与 {keep} 对内外见证独立重放通过。

本次逐条语义复核由AI代理执行并交叉检查，**不是独立人类签字验收**。数学证明以列出的来源绑定、舍入模型及约束清单为条件；不声称穷尽文档所有可能的非线性语义约束。FinQA 可把显示数字本身定义为算术输入，故本结果仍不取代 T1C 的模型判分实验。

[瀑布图](results/waterfall.png) · [完整报告](REPORT.md) · [逐题摘要](results/question_summary.csv) · [40题复核](results/sample40_review.csv) · [逐题证书](results/per_question.jsonl)
'''
    (HERE/'FABLE_ONE_PAGE.md').write_text(one,encoding='utf8')
    import scipy,sympy
    manifest={'python':platform.python_version(),'scipy':scipy.__version__,'sympy':sympy.__version__,'matplotlib':matplotlib.__version__,
        'files_sha256':{str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.py'))},
        'review_sha256':s['review_sha256']}
    (out/'run_environment.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'waterfall':stages,'dispositions':dict(c),'equations':s['reviewed_equations'],'exact_ranges':s['exact_final_ranges']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
