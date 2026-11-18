import numpy as np,pandas as pd,os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import f1_score
B='work/chunks'
c=pd.read_csv('labels/08_coding_AI_claude.csv')
ef=sorted(f for f in os.listdir(B) if f.startswith('emb_'))
rid=np.concatenate([pd.read_parquet(f'{B}/'+f.replace('emb_','scores_').replace('.npy','.parquet'),columns=['rid']).rid.values for f in ef])
pos=pd.Series(np.arange(len(rid)),index=rid); c=c[c.rid.isin(pos.index)]
X=np.concatenate([np.load(f'{B}/{f}') for f in ef])[pos[c.rid].values].astype(np.float32)
y=np.asarray(c.label_ai.astype(str).tolist(),dtype=object)
yh=cross_val_predict(LogisticRegression(max_iter=3000,class_weight='balanced',C=2.0),X,y,cv=StratifiedKFold(5,shuffle=True,random_state=42))
G=lambda a:np.where(np.isin(a,['paksaan','beban','ketidakpercayaan']),'pol',np.where(a=='gagal_teknis','tek','lain'))
print(len(c),'9',round(f1_score(y,yh,average='macro'),3),'3grp',round(f1_score(G(y),G(yh),average='macro'),3))
