import nbformat, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
os.environ.setdefault('IJIM_BASE','work')
nb=nbformat.read('notebook/IJIM_IGAR_resistensi_colab.ipynb',4)
g={}
for k in (1,2,3,4,5):
    exec(nb.cells[k].source, g)
P=g['P']; meta=g['meta']; its_rows=g['its_rows']; SEED=g['SEED']
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import classification_report, f1_score
c=pd.read_csv('labels/08_coding_AI_claude.csv')
emb_files=sorted(f for f in os.listdir(P('chunks')) if f.startswith('emb_'))
rid_all=np.concatenate([pd.read_parquet(P('chunks',f.replace('emb_','scores_').replace('.npy','.parquet')),columns=['rid']).rid.values for f in emb_files])
pos=pd.Series(np.arange(len(rid_all)),index=rid_all)
c=c[c.rid.isin(pos.index)]
X=np.concatenate([np.load(P('chunks',f)) for f in emb_files])[pos[c.rid].values].astype(np.float32)
y=np.asarray(c.label_ai.astype(str).tolist(),dtype=object)
clf=LogisticRegression(max_iter=3000,class_weight='balanced',C=2.0)
yhat=cross_val_predict(clf,X,y,cv=StratifiedKFold(5,shuffle=True,random_state=SEED))
rep=classification_report(y,yhat,zero_division=0); print(rep)
print('macro-F1',round(f1_score(y,yhat,average='macro'),3),'n',len(y))
open('results/out_ai_classifier_report.txt','w').write(rep)
clf.fit(X,y); del X
preds=[]
for f in emb_files:
    e=np.load(P('chunks',f)).astype(np.float32)
    r=pd.read_parquet(P('chunks',f.replace('emb_','scores_').replace('.npy','.parquet')),columns=['rid'])
    pr=clf.predict_proba(e); r['k']=clf.classes_[pr.argmax(1)]; preds.append(r)
fin=pd.concat(preds).merge(meta[['rid','app','score','date']],on='rid')
fin.to_parquet('results/ai_label_final.parquet',index=False)
share=(pd.get_dummies(fin.set_index(['app','date']).k).groupby(level=[0,1],observed=True).mean()
       .join(fin.groupby(['app','date'],observed=True).size().rename('n'))).reset_index()
share.to_csv('results/ai_share_daily.csv',index=False)
cols=[k for k in share.columns if k not in ('app','date','n')]
t=its_rows(share,cols,rng=np.random.default_rng(SEED))
t.to_csv('results/ai_its_konstruk.csv',index=False)
print(t[(t.app=='pertamina')][['desain','outcome','level','se','p','p_placebo','n_placebo']].round(4).to_string())
print(t[(t.app=='satusehat')&(t.desain=='DiD')][['event','outcome','level','p','p_placebo']].round(3).to_string())
