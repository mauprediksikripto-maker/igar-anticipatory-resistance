import nbformat, os, numpy as np, pandas as pd, warnings, io, contextlib, json
warnings.filterwarnings('ignore'); os.environ.setdefault('IJIM_BASE','work')
nb=nbformat.read('notebook/IJIM_IGAR_resistensi_colab.ipynb',4); g={}
with contextlib.redirect_stdout(io.StringIO()):
    for k in (1,2,3,4): exec(nb.cells[k].source,g)
    src=nb.cells[5].source.split('rng = np.random.default_rng(SEED)')[0]; exec(src,g)
its,did_its,daily,EVENTS,CONTROLS,MAX=g['its'],g['did_its'],g['daily'],g['EVENTS'],g['CONTROLS'],g['MAX_PLACEBO']
out={}
for app,dt in [('pertamina','2022-06-27'),('satusehat','2021-08-25')]:
    ctrl=CONTROLS[app]; d=daily[daily.app==app]; first=pd.Timestamp(EVENTS[app][0][0])
    both=pd.Series(sorted(set(d.date)&set(daily[daily.app==ctrl].date)))
    el=both[(both<first-pd.Timedelta(days=30))&(both>both.min()+pd.Timedelta(days=20))].values
    if len(el)>MAX: el=el[np.linspace(0,len(el)-1,MAX).astype(int)]
    for y in ['rating','bintang1','log_n']:
        obs=did_its(daily,app,ctrl,dt,y)['level']
        plc=[r['level'] for p in el if (r:=did_its(daily,app,ctrl,p,y,post=min(30,(first-pd.Timestamp(p)).days)))]
        out[f'{app}|{y}']=dict(obs=obs,plc=plc); print(app,y,round(obs,3),len(plc))
json.dump(out,open('results/placebo_dist.json','w'))
