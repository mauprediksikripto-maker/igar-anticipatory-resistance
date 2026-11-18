import pandas as pd, numpy as np, statsmodels.formula.api as smf, warnings
warnings.filterwarnings('ignore')
d=pd.read_csv('results/notebook_out/02_harian.csv',parse_dates=['date'])
def its(s0,t0,pre=60,post=60,y='rating',w=True,lags=7):
    t0=pd.Timestamp(t0); s=s0[(s0.date>=t0-pd.Timedelta(days=pre))&(s0.date<t0+pd.Timedelta(days=post))].copy()
    s['t']=(s.date-t0).dt.days; s['post']=(s.t>=0).astype(int); s['t_post']=s.t*s.post
    f=f'{y} ~ t + post'+(' + t_post' if s.post.sum()>=10 else '')
    m=smf.wls(f,s,weights=s.n) if (w and y!='log_n') else smf.ols(f,s)
    r=m.fit(cov_type='HAC',cov_kwds={'maxlags':lags}); return r.params['post'],r.bse['post'],r.pvalues['post'],r
def did(a,c,y):
    t=d[d.app==a][['date',y,'n']].rename(columns={y:'yt','n':'nt'}); k=d[d.app==c][['date',y,'n']].rename(columns={y:'yc','n':'nc'})
    m=t.merge(k,on='date'); m['diff']=m.yt-m.yc; m['n']=np.minimum(m.nt,m.nc); return m
E='2022-06-27'
print('== window/lag sensitivity, DiD MyPertamina vs JMO')
for y in ['rating','bintang1','log_n']:
    m=did('pertamina','JMO',y).rename(columns={'diff':'dy'})
    row=[]
    for pre in (30,45,60,90):
        b,se,p,_=its(m,E,pre=pre,y='dy',w=False); row.append(f'pre{pre}:{b:+.3f}({se:.3f})')
    for lags in (3,14):
        b,se,p,_=its(m,E,y='dy',w=False,lags=lags); row.append(f'lag{lags}:{b:+.3f}({se:.3f},p={p:.1e})')
    # excluding announcement day
    m2=m[m.date!=pd.Timestamp(E)]; b,se,p,_=its(m2,E,y='dy',w=False); row.append(f'noE0:{b:+.3f}({se:.3f})')
    print(y,' '.join(row))
print('== pre-trend: differential pre-period slope (60d) and weekly leads')
for y in ['rating','bintang1','log_n']:
    m=did('pertamina','JMO',y); s=m[(m.date>=pd.Timestamp(E)-pd.Timedelta(days=60))&(m.date<pd.Timestamp(E))].copy()
    s['t']=(s.date-pd.Timestamp(E)).dt.days
    r=smf.ols('diff ~ t',s).fit(cov_type='HAC',cov_kwds={'maxlags':7})
    s['wk']=(s.t//7).astype(int)  # -9..-1
    r2=smf.ols('diff ~ C(wk, Treatment(-1))',s).fit(cov_type='HAC',cov_kwds={'maxlags':7})
    names=[n for n in r2.params.index if 'wk' in n]
    jt=r2.wald_test(' , '.join(f'{n} = 0' for n in names),scalar=True)
    print(y,f'slope/day {r.params.t:+.4f} (se {r.bse.t:.4f}, p={r.pvalues.t:.2f}); leads range {r2.params[names].min():+.3f}..{r2.params[names].max():+.3f}; joint p={float(jt.pvalue):.2f}; pre mean diff {s["diff"].mean():.3f} sd {s["diff"].std():.3f}')
print('== placebo-in-space: ITS on control JMO at 27 Jun 2022')
j=d[d.app=='JMO']
for y in ['rating','bintang1','log_n']:
    b,se,p,_=its(j,E,y=y); print(y,f'{b:+.3f} ({se:.3f}) p={p:.2f}')

# ---- Table A.1 (Appendix A)
rows=[]
def did_row(label,**kw):
    out=[]
    for y in ['rating','bintang1','log_n']:
        m=did('pertamina','JMO',y).rename(columns={'diff':'dy'})
        if kw.get('drop0'): m=m[m.date!=pd.Timestamp(E)]
        b,se,p,_=its(m,E,pre=kw.get('pre',60),y='dy',w=False,lags=kw.get('lags',7)); out.append((b,se))
    rows.append((label,out))
did_row('Main specification: 60-day pre-window, 7 lags')
for pre in (30,45,90): did_row(f'{pre}-day pre-window',pre=pre)
for l in (3,14): did_row(f'Newey–West with {l} lags',lags=l)
did_row('Announcement day excluded',drop0=True)
out=[]
for y in ['rating','bintang1','log_n']:
    b,se,p,_=its(j,E,y=y); out.append((b,se))
rows.append(('Control app alone (ITS on JMO, same date)',out))
out=[]
for y in ['rating','bintang1','log_n']:
    m=did('pertamina','JMO',y); s=m[(m.date>=pd.Timestamp(E)-pd.Timedelta(days=60))&(m.date<pd.Timestamp(E))].copy(); s['t']=(s.date-pd.Timestamp(E)).dt.days
    r=smf.ols('diff ~ t',s).fit(cov_type='HAC',cov_kwds={'maxlags':7}); out.append((r.params.t,r.bse.t))
rows.append(('Pre-announcement difference in trend, per day',out))
f=lambda b,se,dp: f"{b:+.{dp}f} ({se:.{dp}f})".replace('-','−')
L=["**Table A.1.** Robustness of the MyPertamina estimates relative to JMO. Level shifts at 27 June 2022 (Newey–West standard errors in parentheses), except where noted.","","| Specification | Mean rating | One-star share | Log daily reviews |","|---|---|---|---|"]
for lab,o in rows:
    dp=4 if 'trend' in lab else 2
    dp3=3 if 'trend' in lab else 2
    L.append(f"| {lab} | {f(*o[0],3 if dp==4 else 2)} | {f(*o[1],4 if dp==4 else 2)} | {f(*o[2],3 if dp==4 else 2)} |")
L+=["","Note. Rows 1–7 are comparative ITS (DiD) estimates on the daily difference between MyPertamina and JMO; row 8 applies the single-app ITS model to JMO. Row 9 regresses the pre-announcement daily difference on a linear trend; the main models include this trend."]
open('results/tableA1_robustness.md','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
