import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
INK='#1f1f1f'; MUTED='#5c5c5c'; BLUE='#2a78d6'; ORANGE='#eb6834'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8})
d=pd.read_csv('results/notebook_out/02_harian.csv',parse_dates=['date']); E=pd.Timestamp('2022-06-27')
out=[]
fig,axs=plt.subplots(1,3,figsize=(7.2,2.6))
for ax,(y,lab) in zip(axs,[('rating','(a) Mean rating'),('bintang1','(b) One-star share'),('log_n','(c) Log daily reviews')]):
    t=d[d.app=='pertamina'][['date',y]].merge(d[d.app=='JMO'][['date',y]],on='date',suffixes=('_t','_c'))
    t['diff']=t[y+'_t']-t[y+'_c']; t['t']=(t.date-E).dt.days
    t=t[(t.t>=-60)&(t.t<6)]; t['wk']=np.floor(t.t/7).astype(int)
    g=t.groupby('wk')['diff'].agg(['mean','std','count']); g['ci']=1.96*g['std']/np.sqrt(g['count'])
    pre=t[(t.t<0)&(t.t>=-60)]; r=smf.ols('diff ~ t',pre).fit()
    xs=np.linspace(-60,5,50); ax.plot(xs/7,r.params.Intercept+r.params.t*xs,color=MUTED,lw=1,ls='--',label='Pre-announcement linear trend')
    pg=g[g.index<0]; ax.errorbar(pg.index+0.5,pg['mean'],yerr=pg['ci'],fmt='o',color=BLUE,ms=3.5,lw=1,capsize=2,label='Weekly mean difference, before')
    ax.errorbar([0.43],[g.loc[0,'mean']],yerr=[g.loc[0,'ci']],fmt='s',color=ORANGE,ms=4,lw=1,capsize=2,label='27 Jun–2 Jul 2022')
    ax.axvline(0,color=INK,lw=0.8); ax.set_title(lab,fontsize=8.5,color=INK,loc='left')
    ax.set_xlabel('Weeks relative to announcement',color=INK); ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y',color='#e6e6e6',lw=0.6); ax.set_xticks(range(-9,2,2))
    out.append((y,g.round(3).to_dict()))
axs[0].set_ylabel('MyPertamina minus JMO',color=INK)
h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc='lower center',ncol=3,frameon=False,fontsize=7.5,bbox_to_anchor=(0.5,-0.02))
fig.tight_layout(rect=(0,0.09,1,1))
for ext,kw in [('png',{'dpi':300}),('pdf',{})]: fig.savefig(f'figures/Figure_A1.{ext}',**kw)
for y,o in out: print(y,{k:round(v,3) for k,v in o['mean'].items()})
