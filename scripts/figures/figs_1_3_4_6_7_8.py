import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, json
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
INK='#1f1f1f'; MUTED='#5c5c5c'; BLUE='#2a78d6'; ORANGE='#eb6834'; FILL='#eef3fa'; FILL2='#f4f4f1'; GREEN='#e5f4e4'; YEL='#f9eeda'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8})
def save(fig,name):
    fig.savefig('figures/'+name+'.png',dpi=300,bbox_inches='tight'); fig.savefig('figures/'+name+'.pdf',bbox_inches='tight')
    fig.savefig('figures/'+name+'.tiff',dpi=600,bbox_inches='tight',pil_kwargs={'compression':'tiff_lzw'}); plt.close(fig)
def box(ax,x,y,w,h,title=None,body=None,fc=FILL2,ec=MUTED,tsz=8,bsz=7,lw=1,bold=True,tgap=3.2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.3,rounding_size=0.8',fc=fc,ec=ec,lw=lw))
    if title and body:
        ax.text(x+w/2,y+h-1.4,title,ha='center',va='top',fontsize=tsz,fontweight='bold' if bold else 'normal',color=INK)
        ax.text(x+w/2,y+h-1.4-tgap*(title.count('\n')+1),body,ha='center',va='top',fontsize=bsz,color=INK,linespacing=1.3)
    elif title: ax.text(x+w/2,y+h/2,title,ha='center',va='center',fontsize=tsz,fontweight='bold' if bold else 'normal',color=INK,linespacing=1.3)
def arr(ax,a,b,c=MUTED,lw=1):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=9,lw=lw,color=c))
def canvas(w,h,xm,ym):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_xlim(0,xm); ax.set_ylim(0,ym); ax.axis('off'); return fig,ax

# ---------- Fig 1: theories and unexplained gaps ----------
fig,ax=canvas(7.4,4.6,100,62)
cols=[('Resistance to IS','Markus (1983); Joshi (1991);\nLapointe & Rivard (2005);\nKim & Kankanhalli (2009)','Explains resistance as a response\nto threats and switching costs\nduring implementation and use'),
      ('Mandatory use','Hartwick & Barki (1994);\nBrown et al. (2002); Beaudry &\nPinsonneault (2005); Bhattacherjee\net al. (2018)','Explains how employees cope with\nsystems they cannot avoid, after\nuse has begun'),
      ('Citizens and the state','Hirschman (1970); Chan et al. (2010);\nMoynihan et al. (2015);\nMadsen et al. (2022)','Explains exit and voice and the\nburdens that digital procedures\nshift onto citizens')]
for i,(t,refs,expl) in enumerate(cols):
    x=2+i*33
    box(ax,x,36,30,24,t,refs+'\n\n'+expl,fc=FILL,ec=BLUE,bsz=6.6)
    arr(ax,(x+15,35.6),(x+15,29.6))
box(ax,2,13,96,16,'Unexplained gaps','Gap 1  Can citizens resist a mandate before they must comply?   (RQ1)\nGap 2  Why do some mandates provoke voice while others do not?   (RQ2)\nGap 3  What do citizens object to: the system or the mandate?   (RQ3)',fc=YEL,ec=MUTED,bsz=7.4,tgap=3.6)
ax.text(50,4,'This study: citizen reviews around two app-based mandates, with control apps and placebo tests',ha='center',va='center',fontsize=7.6,color=INK,style='italic')
arr(ax,(50,9.6),(50,6.2))
save(fig,'Figure_1')

# ---------- Fig 3: research design overview ----------
fig,ax=canvas(7.4,5.0,100,72)
ax.text(1,69,'Research\nquestions',fontsize=8,fontweight='bold',va='top'); ax.text(1,50,'Research\nprocess',fontsize=8,fontweight='bold',va='top'); ax.text(1,16,'Findings',fontsize=8,fontweight='bold',va='top')
rq=[('RQ1','Does the announcement trigger\nvoice before enforcement?'),('RQ2','Do mandates differ in the\nvoice they provoke?'),('RQ3','Which forms of resistance\ndominate citizens\' voice?')]
for i,(t,b) in enumerate(rq): box(ax,14+i*29,58,27,12,t,b,fc=FILL,ec=BLUE,bsz=6.8)
ph=[('Phase 1\nQuasi-experiment','Data: 609,090 reviews, four apps\nITS and DiD (Newey–West SE)\nPlacebo tests on 245–300 dates\nCoordination check'),
    ('Phase 2\nText measurement','Codebook of nine labels\nLLM coding, blind to app and date\nRandom sample n = 450\nClassifier on 900 stratified labels'),
    ('Phase 3\nValidation','Two blind coders, n = 200\nPolarity κ 0.89 → 0.98 (coder 1)\nModel–human κ 0.81, 0.89\nHuman–human κ 0.78\nClassifier transfer check')]
for i,(t,b) in enumerate(ph): box(ax,14+i*29,26,27,24,t,b,fc=FILL2,bsz=6.6,tgap=3.0)
for i in range(2): arr(ax,(41.2+i*29,38),(42.8+i*29,38))
fd=[('MyPertamina: surge before\nregistration opened','DiD one-star +41.9 pp\n(placebo p = .004)'),('PeduliLindungi:\nno comparable shift','All placebo p ≥ .28'),('Burden and coercion,\nnot technical failure','Policy grievance +40.0 pp\n[28.7, 51.3]')]
for i,(t,b) in enumerate(fd): box(ax,14+i*29,2,27,15,t,b,fc=GREEN,ec=MUTED,bsz=6.8,tsz=7.4)
for i in range(3):
    arr(ax,(27.5+i*29,57.6),(27.5+i*29,50.6)); arr(ax,(27.5+i*29,25.6),(27.5+i*29,17.6))
save(fig,'Figure_3')

# ---------- Fig 4: data and coding flow ----------
fig,ax=canvas(7.4,5.6,100,76)
box(ax,26,65,44,9,'IGAR dataset\n617,722 Google Play reviews, six apps',fc=FILL,ec=BLUE,tsz=7.4)
box(ax,74,65,24,9,'Excluded: BMKG (1,321)\nand KAI (7,311);\nreviews end 2015/2017',fc='white',tsz=6.4,bold=False)
arr(ax,(70.4,69.5),(73.6,69.5)); arr(ax,(48,64.6),(48,61.6))
box(ax,22,52,56,9,'Analytic corpus: 609,090 reviews\nMyPertamina, PeduliLindungi, JMO, Mobile JKN',fc=FILL,ec=BLUE,tsz=7.2)
for x in (17,50,83): arr(ax,(50 if x==50 else (40 if x<50 else 60),52.6),(x,46.6))
box(ax,2,30,30,16,'Daily series','ITS and DiD on rating,\none-star share, volume;\nplacebo dates 245–300;\nduplication check',bsz=6.6)
box(ax,35,30,30,16,'Stratified sample, n = 900','Up to 25 per app × construct;\nLLM labels; trains the\nclassifier (macro-F1 0.53)',bsz=6.6)
box(ax,68,30,30,16,'Random sample, n = 450','MyPertamina 150 + 150,\nJMO 75 + 75 (60 days before /\n6 days after); shuffled, blind',bsz=6.6)
arr(ax,(50,29.6),(58,23.6)); arr(ax,(83,29.6),(70,23.6))
box(ax,40,12,40,11,'Blind validation, two coders','n = 200; polarity κ 0.89 → 0.98 (coder 1)\nmodel–coder κ 0.81, 0.89; coder–coder 0.78',fc=YEL,bsz=6.6)
arr(ax,(83,29.6),(88,10.6)); box(ax,78,1,20,9.4,'Table 5 (RQ3)',fc=GREEN,tsz=7.2)
arr(ax,(17,29.6),(17,10.6)); box(ax,4,1,26,9.4,'Table 4, Fig. 5–6\n(RQ1, RQ2)',fc=GREEN,tsz=7.2)
save(fig,'Figure_4')

# ---------- Fig 6: placebo distributions ----------
pdist=json.load(open('results/placebo_dist.json'))
fig,axs=plt.subplots(2,3,figsize=(7.4,4.4),gridspec_kw={'hspace':0.62,'wspace':0.28})
lab={'rating':'Mean rating (stars)','bintang1':'One-star share','log_n':'Log daily reviews'}
pv={'pertamina':{'rating':'.024','bintang1':'.004','log_n':'.004'},'satusehat':{'rating':'.53','bintang1':'.49','log_n':'.32'}}
for r,(app,name) in enumerate([('pertamina','(a) MyPertamina vs JMO, announcement 27 Jun 2022'),('satusehat','(b) PeduliLindungi vs Mobile JKN, travel announcement 25 Aug 2021')]):
    for c,y in enumerate(['rating','bintang1','log_n']):
        a=axs[r,c]; v=pdist[f'{app}|{y}']; plc=np.array(v['plc']); obs=v['obs']
        lo,hi=min(plc.min(),obs),max(plc.max(),obs); pad=(hi-lo)*0.08
        a.hist(plc,bins=30,range=(lo-pad,hi+pad),color='#c9d6e8',edgecolor='white',lw=0.4)
        a.axvline(obs,color=ORANGE if app=='pertamina' else BLUE,lw=1.6)
        a.set_title(lab[y],fontsize=7.6,color=INK,loc='left')
        a.text(0.98,0.92,f'observed {obs:+.2f}\nplacebo p = {pv[app][y]}',transform=a.transAxes,ha='right',va='top',fontsize=6.6,color=INK,bbox=dict(fc='white',ec='none',alpha=0.85,pad=1.2))
        for s in ['top','right']: a.spines[s].set_visible(False)
        a.tick_params(labelsize=6.6); a.spines['left'].set_color(MUTED); a.spines['bottom'].set_color(MUTED)
        if c==0: a.set_ylabel('Placebo dates',fontsize=7)
    axs[r,0].annotate(name,(0,1.28),xycoords='axes fraction',fontsize=8,fontweight='bold',color=INK)
save(fig,'Figure_6')

# ---------- Fig 7: dumbbell of construct shares ----------
rows=[('Policy grievance',10.0,51.3,4.0,5.3),('  Coercion',0.7,10.0,0.0,0.0),('  Burden',8.0,38.0,4.0,4.0),('  Distrust',1.3,3.3,0.0,1.3),
      ('Technical failure',41.3,20.0,16.0,13.3),('Exclusion',0.7,2.0,0.0,0.0),('Exit or workaround',2.0,3.3,0.0,0.0),('Acceptance',38.0,6.0,77.3,73.3),('Other',8.0,17.3,2.7,8.0)]
fig,axs=plt.subplots(1,2,figsize=(7.4,3.6),sharey=True,gridspec_kw={'wspace':0.08})
ys=np.arange(len(rows))[::-1]
for k,(a,title) in enumerate(zip(axs,['(a) MyPertamina (n = 150 + 150)','(b) JMO, control (n = 75 + 75)'])):
    for y,r in zip(ys,rows):
        b,af=(r[1],r[2]) if k==0 else (r[3],r[4])
        a.plot([b,af],[y,y],color='#b8b8b2',lw=2,zorder=1)
        a.scatter([b],[y],s=26,color='white',edgecolor=MUTED,zorder=2,lw=1)
        a.scatter([af],[y],s=30,color=BLUE,zorder=3)
    a.set_xlim(-2,82); a.set_title(title,fontsize=8,loc='left',color=INK); a.set_xlabel('Share of reviews (%)',fontsize=7.4)
    a.grid(axis='x',color='#ececea',lw=0.6); a.set_axisbelow(True)
    for s in ['top','right','left']: a.spines[s].set_visible(False)
    a.tick_params(labelsize=7,length=0)
axs[0].set_yticks(ys); axs[0].set_yticklabels([r[0] for r in rows],fontsize=7.4)
from matplotlib.lines import Line2D
fig.legend([Line2D([],[],marker='o',ls='',mfc='white',mec=MUTED),Line2D([],[],marker='o',ls='',color=BLUE)],['60 days before announcement','Six days after announcement'],loc='lower center',ncol=2,frameon=False,fontsize=7.4,bbox_to_anchor=(0.55,-0.08))
save(fig,'Figure_7')

# ---------- Fig 8: results mapped on framework ----------
fig,ax=canvas(7.6,4.4,104,60)
box(ax,0.5,20,25,18,'Announced mandate','MyPertamina: registration\nfor subsidised fuel\nPeduliLindungi: malls\nand travel',fc=FILL,ec=BLUE,bsz=6.8)
box(ax,78,20,25.5,18,'Voiced resistance\nbefore enforcement','58-fold rise in daily\nreviews; one-star share\n+41.9 pp vs control',fc=FILL,ec=BLUE,bsz=6.8)
box(ax,37,44,30,13,'What the mandate gates','Condition on an existing good\n(MyPertamina) vs. access\nrestored (PeduliLindungi malls)',bsz=6.8)
box(ax,37,4,30,14,'Anticipated costs','Policy grievance 10% → 51%\nBurden 8% → 38%\nTechnical failure 41% → 20%',bsz=6.8)
arr(ax,(26,29),(77.5,29)); arr(ax,(52,43.6),(52,30.4)); arr(ax,(67.4,12),(84,19.6)); arr(ax,(13,19.6),(36.6,11))
def badge(x,y,t,fc): ax.text(x,y,t,ha='center',va='center',fontsize=6.8,color=INK,bbox=dict(boxstyle='round,pad=0.35',fc=fc,ec=MUTED,lw=0.6))
badge(52,26,'P1 supported for MyPertamina\n(placebo p ≤ .024)',GREEN)
badge(64.5,35.5,'P2 consistent, not tested\n(two mandates only)',YEL)
badge(81,10,'P3 supported\n(DiD +40.0 pp [28.7, 51.3])',GREEN)
save(fig,'Figure_8')
print('ok')
