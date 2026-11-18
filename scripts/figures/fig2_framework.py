import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
INK='#1f1f1f'; MUTED='#5c5c5c'; FILL='#eef3fa'; EDGE='#2a78d6'; FILL2='#f4f4f1'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5})
fig,ax=plt.subplots(figsize=(7.6,4.2)); ax.set_xlim(0,104); ax.set_ylim(0,58); ax.axis('off')
def box(x,y,w,h,title,body,fc=FILL,ec=EDGE,tl=1):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.4,rounding_size=1.2',fc=fc,ec=ec,lw=1))
    ax.text(x+w/2,y+h-2.2,title,ha='center',va='top',fontsize=8.6,fontweight='bold',color=INK)
    ax.text(x+w/2,y+h-3.2-3.4*tl-1.2,body,ha='center',va='top',fontsize=7.0,color=INK,linespacing=1.35)
def arrow(x0,y0,x1,y1,lab=None,lx=0,ly=0):
    ax.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle='-|>',mutation_scale=10,lw=1,color=MUTED))
    if lab: ax.text((x0+x1)/2+lx,(y0+y1)/2+ly,lab,ha='center',va='center',fontsize=7.6,color=INK,fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.25',fc='white',ec='none'))
box(0.5,18,25,20,'Announced mandate','App-based condition\non access to a\nservice or good\n(exit removed)')
box(37,38,30,18,'What the mandate gates','Adds a condition to an\nexisting entitlement vs.\nbundles compliance with\nrestored access',fc=FILL2,ec=MUTED)
box(37,2,30,22,'Anticipated costs','Learning and compliance\nburden; coercion;\ndistrust of motives\n(administrative burden,\nstatus quo bias)',fc=FILL2,ec=MUTED)
box(78,14,25.5,26,'Voiced resistance\nbefore enforcement','Surge of negative\nreviews; shift from\ntechnical complaints\nto coercion, burden,\ndistrust',tl=2)
arrow(26.5,28,77.5,28,'P1',0,0)
arrow(52,37.4,52,29.2,'P2',3.4,0.4)
arrow(67.6,13,79,13.6,'P3',0,-2.2)
arrow(13,17.4,37.4,12.5)
fig.savefig('figures/Figure_2.png',dpi=300,bbox_inches='tight'); fig.savefig('figures/Figure_2.tiff',dpi=600,bbox_inches='tight',pil_kwargs={'compression':'tiff_lzw'}); fig.savefig('figures/Figure_2.pdf',bbox_inches='tight')
