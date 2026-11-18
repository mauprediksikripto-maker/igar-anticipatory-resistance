import pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
d=pd.read_csv('results/notebook_out/02_harian.csv',parse_dates=['date'])
T,C='#2a78d6','#eb6834'; INK='#2b2b2b'; MUTED='#6b6b6b'; GRID='#e6e6e3'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.edgecolor':MUTED,'axes.labelcolor':INK,
  'xtick.color':MUTED,'ytick.color':MUTED,'axes.spines.top':False,'axes.spines.right':False})
cases=[dict(t='pertamina',c='JMO',tn='MyPertamina',cn='JMO (control)',lo='2022-04-28',hi='2022-07-02',
            ev=[('2022-06-27','E1 ann.',0),('2022-07-01','E1 reg. opens',1)],shade=('2022-06-27','2022-07-01'),title='(a) MyPertamina, fuel mandate 2022',lx='2022-06-12'),
       dict(t='satusehat',c='mobileJKN',tn='PeduliLindungi',cn='Mobile JKN (control)',lo='2021-06-11',hi='2021-10-12',
            ev=[('2021-08-10','E2',0),('2021-08-25','E3 ann.',0),('2021-08-28','E3 enf.',1)],shade=('2021-08-25','2021-08-28'),title='(b) PeduliLindungi, mall and travel mandates 2021',lx='2021-09-25')]
fig,ax=plt.subplots(2,2,figsize=(7.2,5.0),sharey='row',gridspec_kw={'hspace':0.28,'wspace':0.08})
for j,cs in enumerate(cases):
    for i,(col,lab) in enumerate([('n','Reviews per day (log scale)'),('bintang1','One-star share')]):
        a=ax[i,j]
        for app,clr,name,lw in [(cs['c'],C,cs['cn'],1.1),(cs['t'],T,cs['tn'],1.6)]:
            s=d[(d.app==app)&(d.date>=cs['lo'])&(d.date<=cs['hi'])]
            a.plot(s.date,s[col],color=clr,lw=lw,label=name,solid_capstyle='round')
            if i==0:
                x0=pd.Timestamp(cs['lx']); y0=s.set_index('date')[col].rolling(5,center=True,min_periods=1).median().loc[x0]
                below=(app==cs['t'] and j==0)
                a.annotate(name.replace(' (control)',''),(x0,y0),xytext=(0,-9 if below else 6),textcoords='offset points',
                   color=INK,fontsize=7.5,ha='center',va='top' if below else 'bottom')
        a.axvspan(pd.Timestamp(cs['shade'][0]),pd.Timestamp(cs['shade'][1]),color='#d9d9d4',alpha=0.55,lw=0)
        for dt,_,_ in cs['ev']: a.axvline(pd.Timestamp(dt),color=MUTED,lw=0.8,ls=(0,(3,2)))
        if i==0:
            a.set_yscale('log'); a.set_ylim(0.6,1e5); a.set_title(cs['title'],loc='left',fontsize=9,color=INK,pad=24)
            for dt,txt,lev in cs['ev']:
                a.text(pd.Timestamp(dt),1.015+0.075*lev,txt,transform=a.get_xaxis_transform(),fontsize=6.6,color=MUTED,
                       va='bottom',ha='center',clip_on=False)
        else:
            a.set_ylim(0,1); a.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        if j==0: a.set_ylabel(lab)
        a.grid(axis='y',color=GRID,lw=0.6); a.set_axisbelow(True)
        a.xaxis.set_major_locator(mdates.MonthLocator()); a.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        a.set_xlim(pd.Timestamp(cs['lo']),pd.Timestamp(cs['hi'])+pd.Timedelta(days=(3 if j==0 else 4)))
        a.tick_params(labelsize=7.2)
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
fig.legend([Line2D([],[],color=T,lw=1.6),Line2D([],[],color=C,lw=1.1),Patch(color='#d9d9d4'),Line2D([],[],color=MUTED,lw=0.8,ls=(0,(3,2)))],
           ['Mandated app','Control app','Announcement to start','Mandate event'],loc='lower center',ncol=4,frameon=False,fontsize=7.5,bbox_to_anchor=(0.5,-0.01))
fig.subplots_adjust(bottom=0.13,top=0.88,left=0.09,right=0.95)
for ext,dpi in [('png',300),('tiff',600)]:
    fig.savefig(f'figures/Figure_5.{ext}',dpi=dpi,facecolor='white')
fig.savefig('figures/Figure_5.pdf',facecolor='white')
print('ok')
