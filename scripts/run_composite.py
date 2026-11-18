import nbformat, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore'); os.environ.setdefault('IJIM_BASE','work')
nb=nbformat.read('notebook/IJIM_IGAR_resistensi_colab.ipynb',4); g={}
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    for k in (1,2,3,4,5): exec(nb.cells[k].source,g)
its_rows=g['its_rows']; SEED=g['SEED']
s=pd.read_csv('results/ai_share_daily.csv',parse_dates=['date'])
s['kebijakan']=s.paksaan+s.beban+s.ketidakpercayaan
s['gap_kebijakan_teknis']=s.kebijakan-s.gagal_teknis
t=its_rows(s,['kebijakan','gagal_teknis','gap_kebijakan_teknis'],rng=np.random.default_rng(SEED))
t.to_csv('results/ai_its_komposit.csv',index=False)
print(t[['app','desain','event','outcome','level','se','p','p_placebo','n_placebo']].round(4).to_string())
# reliability of composite (CV preds re-collapsed)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import f1_score, cohen_kappa_score, classification_report
P=g['P']; c=pd.read_csv('labels/08_coding_AI_claude.csv')
ef=sorted(f for f in os.listdir(P('chunks')) if f.startswith('emb_'))
rid=np.concatenate([pd.read_parquet(P('chunks',f.replace('emb_','scores_').replace('.npy','.parquet')),columns=['rid']).rid.values for f in ef])
pos=pd.Series(np.arange(len(rid)),index=rid)
X=np.concatenate([np.load(P('chunks',f)) for f in ef])[pos[c.rid].values].astype(np.float32)
y=np.asarray(c.label_ai.astype(str).tolist(),dtype=object)
yh=cross_val_predict(LogisticRegression(max_iter=3000,class_weight='balanced',C=2.0),X,y,cv=StratifiedKFold(5,shuffle=True,random_state=SEED))
m={'paksaan':'kebijakan','beban':'kebijakan','ketidakpercayaan':'kebijakan','gagal_teknis':'teknis'}
Y=np.array([m.get(a,'lain') for a in y]); YH=np.array([m.get(a,'lain') for a in yh])
print(classification_report(Y,YH,digits=3)); print('kappa AI-vs-classifier 9 kelas',round(cohen_kappa_score(y,yh),3),'3 kelas',round(cohen_kappa_score(Y,YH),3))
