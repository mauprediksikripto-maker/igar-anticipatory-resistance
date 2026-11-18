# Voiced resistance before enforcement - replication package

Code, coding instruments, labels, and estimation outputs for the article
**"Voiced resistance before enforcement: Quasi-experimental evidence from app-based government mandates in Indonesia"**
(submitted to the *International Journal of Information Management*).

The study analyses Google Play reviews of Indonesian government apps around two app-based mandates: the MyPertamina fuel-subsidy registration (announced 27 June 2022; control app JMO) and the PeduliLindungi access mandates of August 2021 (control app Mobile JKN). It combines single-app interrupted time series (ITS), comparative ITS/difference-in-differences (DiD) with Newey–West standard errors, in-time and in-space placebo tests, and blind coding of review content validated against two independent human coders.

## Data source

The raw reviews are **not** redistributed here. They come from the IGAR dataset:

> Isnan, M., & Pardamean, B. (2025). *IGAR: Indonesian Government App Reviews* (Version 3) [Data set]. Mendeley Data. https://doi.org/10.17632/7zryc6k76z.3 — licence CC BY 4.0.

The notebook downloads `Rating_labeled.csv` from Mendeley Data and checks its SHA-256 (`a27a0cf3dae752789fa25e97a5fb39b906f5bc2ea3d93891ff652d0168a3a4a7`). The label files in `labels/` repeat the text of the sampled reviews from that dataset, under the same CC BY 4.0 licence. IGAR contains no reviewer names or user identifiers; reviews are referred to by their row index in the dataset (`rid`).

## Repository structure

```
notebook/   IJIM_IGAR_resistensi_colab.ipynb   full pipeline (download → daily series → ITS/DiD + placebo → embeddings → construct shares)
scripts/    stand-alone analyses used for the tables, appendix, and figures
  placebo_dist.py           placebo distributions for Figure 6 → results/placebo_dist.json
  robustness_tableA1.py     Table A.1 (windows, lags, announcement day, control app alone, pre-trend)
  random_wave_did.py        Table 5 / Figure 7: construct shares and DiD in the random samples (bootstrap CIs)
  validation_kappa.py       Cohen's kappa: model vs coder 1, model vs coder 2, coder 1 vs coder 2
  run_ai_classifier.py      classifier trained on the 900 coded reviews, applied to all reviews (needs embeddings)
  run_composite.py          ITS/DiD for the policy-grievance composite (needs embeddings)
  classifier_cv_f1.py       cross-validated macro-F1 of the classifier (needs embeddings)
  llm_labels/               label lists as recorded during LLM coding (provenance; the CSVs in labels/ are authoritative)
  figures/                  scripts for Figures 1–8, Figure A.1, and the graphical abstract
labels/     coded samples and human validation labels (see data dictionary below)
results/    estimation outputs; results/notebook_out/ holds the notebook outputs
docs/       codebook.md (Appendix B), second_coder_protocol.md
figures/    rendered figures (PNG, PDF; 1000-dpi TIFFs are with the journal submission)
```

## How to reproduce

```bash
pip install -r requirements.txt
export IJIM_BASE=work                       # working folder for raw data, embeddings, and notebook outputs
jupyter nbconvert --to notebook --execute notebook/IJIM_IGAR_resistensi_colab.ipynb
```

Run every script **from the repository root**, for example `python scripts/validation_kappa.py`.

- `validation_kappa.py`, `random_wave_did.py`, `robustness_tableA1.py`, and the figure scripts run directly from the files in this repository.
- `placebo_dist.py` needs the raw data in `work/raw/` (created by notebook steps 1–2).
- `run_ai_classifier.py`, `run_composite.py`, and `classifier_cv_f1.py` need the sentence embeddings in `work/chunks/` (notebook step 6; about 0.5 GB, not stored here). Embeddings use `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`; a GPU is recommended. The notebook also runs on free Google Colab, where it saves to Google Drive and can resume after a disconnect.

Random seeds: 42 (notebook, placebo p-values, cross-validation) and 7 (bootstrap in `random_wave_did.py`). Placebo dates for Figure 6 are spaced evenly, not drawn at random. With the files provided, the scripts reproduce the reported values exactly (for example, DiD level shift in mean rating −1.343 against 245 placebo dates; kappa 0.81, 0.89, and 0.78).

## Data dictionary

Construct labels are stored in Indonesian. Translation:

| Label in files | Construct in the article |
|---|---|
| `paksaan` | Coercion |
| `beban` | Burden |
| `ketidakpercayaan` | Distrust |
| `gagal_teknis` | Technical failure |
| `eksklusi` | Exclusion |
| `privasi` | Privacy concern |
| `exit_siasat` | Exit or workaround |
| `patuh_menerima` | Acceptance |
| `lainnya` | Other |

Three-group coding (`kelompok` / `ai`): `kebijakan` = policy grievance (coercion + burden + distrust), `teknis` = technical failure, `lain` = other. Polarity (`label_manusia`): `positif` / `negatif`.

| File | Contents |
|---|---|
| `labels/08_coding_AI_claude.csv` | Stratified sample of 900 reviews (225 per app; up to 25 per app for each preliminary embedding-screen label), coded by the LLM coder from the review text only; training data for the classifier |
| `labels/10_random_wave_AI.csv` | Simple random sample of 450 reviews coded by the LLM coder from the review text only: MyPertamina 150 before and 150 after, JMO 75 before and 75 after (60 days before vs six days after 27 June 2022); `periode` = `pre`/`post` |
| `labels/rand_wave_sample.parquet` | The drawn random sample before coding |
| `labels/09_validasi_gabung.csv` | 200 reviews: polarity label by human coder 1 (`label_manusia`) and model label (`label_ai`); `sampel` = `random`/`stratified` |
| `labels/09b_validasi_kelompok_hasil.csv` | Same 200 reviews: three-group label by human coder 1 (`kelompok`), model label and its group (`ai`) |
| `labels/09c_validasi_kelompok_pengode2.csv` | Same 200 reviews: three-group label by human coder 2, coded blind from text only |
| `results/notebook_out/02_harian.csv` | Daily series per app: number of reviews `n`, mean rating, one-star share `bintang1`, `log_n` |
| `results/notebook_out/04_its_rating_volume.csv` | ITS and DiD level shifts with HAC standard errors and placebo p-values |
| `results/notebook_out/09_ringkasan.md` | Notebook summary (in Indonesian) |
| `results/placebo_dist.json` | Observed and placebo DiD estimates (Figure 6) |
| `results/tableA1_robustness.md` | Table A.1 |
| `results/10_random_wave_table5.csv` | Table 5 |
| `results/ai_label_final.parquet`, `ai_share_daily.csv`, `ai_its_konstruk.csv`, `ai_its_komposit.csv`, `out_ai_classifier_report.txt` | Classifier labels for all reviews, daily construct shares, and construct-level ITS/DiD |

Comments inside the notebook and some intermediate column names are in Indonesian; the analysis steps are numbered to match the article's Section 4.

## Use of a large language model

A large language model (Claude Opus 5.5, Anthropic) served as a coding instrument, seeing only the review text, and assisted in writing code. Its labels were validated against two independent human coders (Section 4.6 of the article). All labels it produced are released here so that they can be inspected and recoded.

## Licence

Code: MIT (see `LICENSE`). Labels, outputs, and figures: CC BY 4.0. Review texts: CC BY 4.0, from the IGAR dataset (cite Isnan & Pardamean, 2025).

## Citation

If you use this package, please cite the article (full reference to be added on publication) and the IGAR dataset.
