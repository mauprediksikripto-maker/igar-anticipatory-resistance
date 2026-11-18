import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
INK='#1f1f1f'; MUTED='#5c5c5c'; BLUE='#2a78d6'; ORANGE='#eb6834'; FILL='#eef3fa'; GREY='#9a9a9a'
plt.rcParams.update({'font.family':'DejaVu Sans'})
cm=1/2.54; fig=plt.figure(figsize=(13*cm,5*cm),dpi=300)
fig.text(0.5,0.94,'Anticipatory resistance to an app-based government mandate',ha='center',va='center',fontsize=8.2,fontweight='bold',color=INK)
def panel(x,w,title):
    ax=fig.add_axes([x,0.08,w,0.74]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    ax.add_patch(FancyBboxPatch((0.01,0.01),0.98,0.98,boxstyle='round,pad=0,rounding_size=0.04',fc='white',ec='#c9c9c9',lw=0.6))
    ax.text(0.5,0.9,title,ha='center',va='center',fontsize=6.6,fontweight='bold',color=INK,linespacing=1.15); return ax
a=panel(0.01,0.32,'MyPertamina fuel mandate\nannounced 27 Jun 2022')
a.text(0.5,0.62,'×58',ha='center',va='center',fontsize=15,fontweight='bold',color=ORANGE)
a.text(0.5,0.47,'daily reviews vs control',ha='center',fontsize=6,color=INK)
a.text(0.5,0.31,'+42 pp one-star share',ha='center',fontsize=6.6,fontweight='bold',color=ORANGE)
a.text(0.5,0.13,'47% of reviews came before\nregistration opened',ha='center',fontsize=5.8,color=MUTED,linespacing=1.15)
b=panel(0.345,0.32,'What citizens voiced\n(blind-coded random sample)')
ax=fig.add_axes([0.345+0.32*0.36,0.17,0.32*0.52,0.44])
labels=['Burden,\ncoercion,\ndistrust','Technical\nfailure']; pre=[10.0,41.3]; post=[51.3,20.0]
y=[1,0]; ax.barh([v+0.17 for v in y],pre,height=0.32,color=GREY,label='Before')
ax.barh([v-0.17 for v in y],post,height=0.32,color=ORANGE,label='After')
for v,p,q in zip(y,pre,post):
    ax.text(p+1.5,v+0.17,f'{p:.0f}%',va='center',fontsize=5.6,color=INK); ax.text(q+1.5,v-0.17,f'{q:.0f}%',va='center',fontsize=5.6,color=INK)
ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=5.6,color=INK); ax.set_xlim(0,80); ax.set_xticks([])
for s in ['top','right','bottom']: ax.spines[s].set_visible(False)
ax.legend(fontsize=5.4,frameon=False,loc='upper right',bbox_to_anchor=(1.18,1.04),handlelength=1,borderaxespad=0)
c=panel(0.68,0.31,'PeduliLindungi mandates\nthat came with reopening')
c.text(0.5,0.6,'No comparable\nshift',ha='center',va='center',fontsize=9,fontweight='bold',color=BLUE,linespacing=1.1)
c.text(0.5,0.36,'placebo p ≥ .28',ha='center',fontsize=6.4,color=INK)
c.text(0.5,0.15,'What a mandate gates\nshapes whether citizens resist',ha='center',fontsize=5.8,color=MUTED,linespacing=1.15)
for ext,kw in [('png',{'dpi':300}),('pdf',{})]: fig.savefig(f'figures/Graphical_abstract.{ext}',**kw)
fig.savefig('figures/Graphical_abstract.tiff',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
