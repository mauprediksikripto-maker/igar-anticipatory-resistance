import pandas as pd,numpy as np
r=pd.read_csv('labels/10_random_wave_AI.csv')
POL={'paksaan','beban','ketidakpercayaan'}
labs=['paksaan','beban','ketidakpercayaan','gagal_teknis','eksklusi','privasi','exit_siasat','patuh_menerima','lainnya']
def ind(df,k):
    if k=='POL': return df.label_ai.isin(POL).values.astype(float)
    if k=='GAP': return df.label_ai.isin(POL).values-(df.label_ai=='gagal_teknis').values.astype(float)
    return (df.label_ai==k).values.astype(float)
cells={(a,p):r[(r.app==a)&(r.periode==p)] for a in ['pertamina','JMO'] for p in ['pre','post']}
rng=np.random.default_rng(7)
for k in ['POL']+labs+['GAP']:
    v={c:ind(df,k) for c,df in cells.items()}
    m={c:x.mean()*100 for c,x in v.items()}
    did=(m['pertamina','post']-m['pertamina','pre'])-(m['JMO','post']-m['JMO','pre'])
    B=[]
    for b in range(4000):
        mm={c:rng.choice(x,len(x)).mean()*100 for c,x in v.items()}
        B.append((mm['pertamina','post']-mm['pertamina','pre'])-(mm['JMO','post']-mm['JMO','pre']))
    lo,hi=np.percentile(B,[2.5,97.5])
    print(f"{k:16s} P {m['pertamina','pre']:.1f}->{m['pertamina','post']:.1f}  J {m['JMO','pre']:.1f}->{m['JMO','post']:.1f}  DiD {did:+.1f} [{lo:.1f},{hi:.1f}]")
po=cells['pertamina','post']; a=po[po.date<'2022-07-01']; b=po[po.date>='2022-07-01']
for x in (a,b): print(len(x), x.label_ai.isin(POL).mean()*100, (x.label_ai=='gagal_teknis').mean()*100)
