"""T1b residual check, rounded-position null, and documented 50-row reading."""
from part1_changes import *
from scipy.stats import qmc
import numpy as np, random

def uniform_sum_cdf(z,n):
    if z<=0:return F(0)
    if z>=n:return F(1)
    return sum((-1)**k*math.comb(n,k)*(z-k)**n for k in range(min(n,math.floor(z))+1))/math.factorial(n)

def weighted_cdf(z,widths):
    n=len(widths)
    if not n:return F(z>=0)
    if z<=0:return F(0)
    if z>=sum(widths):return F(1)
    total=F(0)
    for mask in product([0,1],repeat=n):
        t=z-sum(w*m for w,m in zip(widths,mask))
        if t>0:total+=(-1)**sum(mask)*t**n
    return total/(math.factorial(n)*math.prod(widths))

def heterogeneous_pmf(terms,centers,hs,d):
    negative=[k for k,v in terms.items() if v<0];positive=[k for k,v in terms.items() if v>0]
    target=negative[0] if len(negative)==1 else positive[0] if len(positive)==1 else negative[-1]
    coeff=terms[target];others=[k for k in terms if k!=target]
    center=-sum(terms[k]*centers[k] for k in others)/coeff
    widths=[2*abs(terms[k]/coeff)*hs[k] for k in others if hs[k]]
    half=sum(widths)/2;quantum=2*hs[target]
    if not quantum:return {}
    result={}
    for j in range(math.floor((center-half)/quantum)-1,math.ceil((center+half)/quantum)+2):
        lo=(F(j)-F(1,2))*quantum-center+half;hi=lo+quantum
        prob=weighted_cdf(hi,widths)-weighted_cdf(lo,widths)
        if prob:
            residual=-coeff*(j*quantum-center)/d
            result[str(residual)]=str(prob)
    assert sum(map(F,result.values()))==1
    return result

def sums():
    path=WORK/'proxy-tail-t1b/research/t1b_tighten/results/constraint_inventory.jsonl'
    docs={d['doc_id']:d for d in documents('finqa')}
    oldrows={r['id']:r for r in map(json.loads,(OLD/'results/per_question.jsonl').read_text(encoding='utf-8').splitlines())}
    rows=[];seen=set();expected=defaultdict(float)
    for q in map(json.loads,path.read_text(encoding='utf-8').splitlines()):
        for i,c in enumerate(q['constraints']):
            if c['type']!='reviewed_sum':continue
            terms={k:F(v) for k,v in c['terms'].items()}
            centers={k:(F(q['bounds'][k][0])+F(q['bounds'][k][1]))/2 for k in terms}
            hs={k:(F(q['bounds'][k][1])-F(q['bounds'][k][0]))/2 for k in terms}
            for k in terms:
                m=re.fullmatch(r'table_(\d+):(\d+)',k)
                if m:
                    t=docs[q['id'].rsplit('-',1)[0]]['table'];nn=number(t[int(m[1])][int(m[2])])
                    if nn:
                        centers[k]=nn['value']
                        if hs[k]:hs[k]=nn['half']
                elif k in oldrows[q['id']].get('input_provenance',{}):
                    v=oldrows[q['id']]['input_provenance'][k];centers[k]=F(v['value']);hs[k]=F(v['half'])
            # Preserve original 511 relations; mark repeated source relations.
            key=(q['id'].rsplit('-',1)[0],tuple(sorted(terms.items())))
            repeat=key in seen;seen.add(key)
            d=max(abs(terms[k])*hs[k] for k in terms)*2 or F(1)
            residual=-sum(terms[k]*centers[k] for k in terms)/d
            positive_h=[abs(terms[k])*h for k,h in hs.items() if h]
            equal=len(set(positive_h))<=1
            n=max(0,len(positive_h)-1)
            probs={}
            if equal and n==0:
                probs={'0':'1'};expected[0]+=1
            elif equal:
                for k in range(-math.ceil(n/2),math.ceil(n/2)+1):
                    prob=uniform_sum_cdf(F(k)+F(1,2)+F(n,2),n)-uniform_sum_cdf(F(k)-F(1,2)+F(n,2),n)
                    probs[str(k)]=str(prob);expected[k]+=float(prob)
            else:probs=heterogeneous_pmf(terms,centers,hs,d)
            rows.append(dict(id=q['id'],relation=i,terms=c['terms'],reason=c['reason'],ulp=str(d),residual=str(residual),equal_precision=equal,primitive_count=n,repeated_source_relation=repeat,predicted_distribution=probs))
    csvout(HERE/'part1_sum_residuals.csv',rows);dump(HERE/'part1_sum_residuals.json',rows)
    supported=[r for r in rows if r['equal_precision']]
    s=dict(n=len(rows),unique_relations=sum(not r['repeated_source_relation'] for r in rows),residual_counts=dict(Counter(r['residual'] for r in rows)),equal_precision=len(supported),expected_counts=dict(expected),predicted_nonzero=sum(v for k,v in expected.items() if k!=0)/len(supported),observed_nonzero=sum(F(r['residual'])!=0 for r in rows)/len(rows),observed_nonzero_supported=sum(F(r['residual'])!=0 for r in supported)/len(supported),all_predicted_nonzero=sum(1-float(F(r['predicted_distribution'].get('0','0'))) for r in rows)/len(rows))
    dump(HERE/'part1_sum_summary.json',s);print('SUMS',json.dumps(s))

def positions():
    rows=json.loads((HERE/'part1_rows_all.json').read_text(encoding='utf-8'))
    u=qmc.Sobol(2,scramble=False).random_base2(12)-.5
    result=[]
    for ds in ['finqa','tatqa']:
        for kind in ['amount','percent']:
            selected=[r for r in rows if r['dataset']==ds and r['kind']==kind and r['status']=='compatible']
            raw=[];expected=[]
            for r in selected:
                lo,hi=float(F(r['lo'])),float(F(r['hi']));width=hi-lo
                if width==0:continue
                raw.append(r['position'])
                av=float(F(r['base']));bv=float(F(r['new']));da=2*float(F(r['base_half']));db=2*float(F(r['new_half']));dc=2*float(F(r['printed_half']))
                a=av+u[:,0]*da;b=bv+u[:,1]*db
                value=b-a if kind=='amount' else 100*(b/a-1)
                quant=np.copysign(np.floor(np.abs(value)/dc+.5),value)*dc
                expected.extend(((quant-lo)/width).tolist())
            interior=list(np.linspace(0,1,11));interior[-1]=np.nextafter(1.,np.inf)
            edges=[-np.inf]+interior+[np.inf]
            observed_counts=np.histogram(raw,bins=edges)[0];pred_counts=np.histogram(expected,bins=edges)[0]
            for j,(obs,pred) in enumerate(zip(observed_counts,pred_counts)):
                result.append(dict(dataset=ds,kind=kind,bin=j,lower=str(edges[j]),upper=str(edges[j+1]),observed_count=int(obs),observed_probability=int(obs)/len(raw) if raw else 0,predicted_probability=int(pred)/len(expected) if expected else 0,n=len(raw)))
    csvout(HERE/'part1_positions.csv',result)

def review():
    rows=json.loads((HERE/'part1_rows_all.json').read_text(encoding='utf-8'))
    non=[r for r in rows if r.get('box_status')=='nonintersection'];random.Random(1729).shuffle(non);sample=non[:50]
    # Read the actual headers and row strings before assigning these categories.
    exceptional={8:('reversed_change_direction','同表支出以减少为正，印差为旧减新，与统一新减旧定义相反。'),
        9:('unexplained_or_source_error','按表两水平重算约-17.49%，不落入-18%的半末位区间；材料无法区分印表错误、别的基数或预处理。'),
        10:('reversed_change_direction','Selling expenses下降被印作正百分比；为费用减少量。'),
        21:('unexplained_or_source_error','薪酬显示两水平对应约14.13%，不是13.75%；需原始薪酬基数解释，现有表不能支持舍入解释。'),
        22:('reversed_change_direction','融资成本下降被列为正Change；符号定义相反。'),
        30:('reversed_change_direction','同表融资成本下降被列为正Change。'),
        34:('reversed_change_direction','BCE支出增长被列为负Change；符号定义相反。'),
        35:('unexplained_or_source_error','8324/4706−1约76.88%，印67%；不可能由半末位舍入解释，未把疑似转录错误当已证实。'),
        41:('reversed_change_direction','费用下降被印作正百分比。')}
    for i,r in enumerate(sample):
        if r['status']=='different_basis_header':reason,note='adjusted_basis','表头明确Constant currency、Adjusted或Comp.；与未调整水平不是同一基数。'
        elif i in exceptional:reason,note=exceptional[i]
        elif F(r['base'])<0:reason,note='negative_base_convention','负基期下印百分比使用幅度分母/改善方向；统一有符号分母公式反号。'
        else:reason,note='unexplained_or_source_error','逐行阅读后不能由现有显示值与统一公式解释；不强行归因为舍入。'
        r.update(sample_index=i,reviewer='AI source reading; not human review',review_category=reason,review_note=note)
    dump(HERE/'part1_nonintersection_sample.json',sample);csvout(HERE/'part1_nonintersection_review50.csv',sample)
    summary=dict(n_numeric=sum(r.get('box_status') in ['compatible','nonintersection'] for r in rows),nonintersection=len(non),sample_n=len(sample),sample_categories=dict(Counter(r['review_category'] for r in sample)),remaining_comparable_nonintersection=sum(r['status']=='nonintersection' for r in rows))
    dump(HERE/'part1_nonintersection_summary.json',summary);print('REVIEW',json.dumps(summary))

if __name__=='__main__':sums();positions();review()
