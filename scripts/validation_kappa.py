"""Agreement between the LLM coder and two blind, independent human coders (Section 4.6).

Run from the repository root:  python scripts/validation_kappa.py
"""
import pandas as pd
from sklearn.metrics import cohen_kappa_score as K

POL = {'paksaan', 'beban', 'ketidakpercayaan'}          # coercion, burden, distrust -> "policy"

def group(label):
    return 'kebijakan' if label in POL else ('teknis' if label == 'gagal_teknis' else 'lain')

# 1) Polarity (coder 1): negative vs positive review, against the model's acceptance label
v = pd.read_csv('labels/09_validasi_gabung.csv')
h = (v.label_manusia == 'positif').astype(int)
a = (v.label_ai == 'patuh_menerima').astype(int)
print(f'Polarity, model vs coder 1: kappa={K(h, a):.3f}  agreement={(h == a).mean():.3f}  n={len(v)}')

# 2) Three-group coding (policy / technical / other): model vs coder 1 vs coder 2
c1 = pd.read_csv('labels/09b_validasi_kelompok_hasil.csv')
c2 = pd.read_csv('labels/09c_validasi_kelompok_pengode2.csv', encoding='utf-8-sig')
c2['kelompok'] = c2['kelompok'].astype(str).str.strip().str.lower()
assert (c1.label_ai.map(group) == c1.ai).all()
m = c1.merge(c2[['rid', 'kelompok']], on='rid', suffixes=('_c1', '_c2'))
print(f'n = {len(m)}')
print(f'Model vs coder 1  : kappa={K(m.ai, m.kelompok_c1):.3f}')
print(f'Model vs coder 2  : kappa={K(m.ai, m.kelompok_c2):.3f}')
print(f'Coder 1 vs coder 2: kappa={K(m.kelompok_c1, m.kelompok_c2):.3f}  '
      f'agreement={(m.kelompok_c1 == m.kelompok_c2).mean():.3f}')
for s in ['random', 'stratified']:
    x = m[m.sampel == s]
    print(f'  {s:10s} n={len(x):3d}  model-c1={K(x.ai, x.kelompok_c1):.3f}  '
          f'model-c2={K(x.ai, x.kelompok_c2):.3f}  c1-c2={K(x.kelompok_c1, x.kelompok_c2):.3f}')
print('Counts (policy/technical/other):')
for col, name in [('ai', 'model'), ('kelompok_c1', 'coder 1'), ('kelompok_c2', 'coder 2')]:
    print(f'  {name:8s}', m[col].value_counts().reindex(['kebijakan', 'teknis', 'lain']).tolist())
