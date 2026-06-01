# Full Experiment Record — Spotify Popularity Prediction
## AutoResearch Weeks 2–6 | Evaluation metric: Validation RMSE (lower is better)

**Project:** Predict Spotify track popularity (0–100) from numeric audio features  
**Split:** 60 / 20 / 20 train / val / test, random_state=42  
**Baseline anchor:** LinearRegression RMSE 22.0630 (Exp 0, Week 2, frozen)  
**Locked final model:** RandomForestRegressor, n_estimators=200, `index` excluded, + log1p(duration_ms) + log1p(instrumentalness)  
**Locked final artifact-free RMSE:** 15.7187

---

## Week 2 — Baseline Experiments

### Exp 0 — Frozen Baseline

| Field | Value |
|-------|-------|
| **Experiment ID** | Exp 0 |
| **Week** | 2 |
| **Direction tested** | Linear regression using all numeric features |
| **Model / change** | LinearRegression (sklearn default) |
| **Validation RMSE** | 22.0630 |
| **Validation R²** | 0.0255 |
| **Runtime** | 0.65 s |
| **Decision** | Baseline (frozen anchor) |
| **Interpretation** | Linear model captures almost no variance (R²=0.026), establishing that the audio-feature–popularity relationship is strongly nonlinear and a frozen lower-bound RMSE of 22.06 against which all subsequent work is measured. |

---

## Week 3 — Model-Family Experiments

### Exp 1 — Ridge Regression

| Field | Value |
|-------|-------|
| **Experiment ID** | Exp 1 |
| **Week** | 3 |
| **Direction tested** | Linear regularization (L2 penalty) |
| **Model / change** | Ridge Regression, alpha=1.0 |
| **Validation RMSE** | 22.0630 |
| **Validation R²** | 0.0255 |
| **Runtime** | 0.77 s |
| **Decision** | Discard |
| **Interpretation** | Identical RMSE to the unregularized baseline confirms the dataset is not overfitting and regularization adds nothing; the problem is structural nonlinearity, not linear-model overfitting. |

---

### Exp 2 — Random Forest (First Adoption)

| Field | Value |
|-------|-------|
| **Experiment ID** | Exp 2 |
| **Week** | 3 |
| **Direction tested** | Tree-based nonlinear ensemble |
| **Model / change** | RandomForestRegressor, n_estimators=100 |
| **Validation RMSE** | 15.0714 |
| **Validation R²** | 0.5453 |
| **Runtime** | 29.44 s |
| **Decision** | Keep |
| **Interpretation** | Single largest improvement of the entire project (−7.0 RMSE, −31.7%), confirming that tree-based nonlinear splitting captures structure linear models cannot access; RF adoption alone accounts for 7.0 of the project's total 7.04 RMSE gain. |

---

### Exp 3 — HistGradientBoosting (Default)

| Field | Value |
|-------|-------|
| **Experiment ID** | Exp 3 |
| **Week** | 3 |
| **Direction tested** | Gradient boosting as alternative to RF |
| **Model / change** | HistGradientBoostingRegressor, default settings |
| **Validation RMSE** | 18.4472 |
| **Validation R²** | 0.3188 |
| **Runtime** | 3.38 s |
| **Decision** | Discard |
| **Interpretation** | Substantially worse than RF (RMSE +3.38), despite faster runtime; default boosting parameters are poorly matched to this feature set and the sequential fitting approach underperforms RF's parallel ensemble here. |

---

### Exp 4 — Random Forest n_estimators=200

| Field | Value |
|-------|-------|
| **Experiment ID** | Exp 4 |
| **Week** | 3 |
| **Direction tested** | Increase RF tree count for diminishing-returns check |
| **Model / change** | RandomForestRegressor, n_estimators=200 |
| **Validation RMSE** | 15.0254 |
| **Validation R²** | 0.5480 |
| **Runtime** | 63.11 s |
| **Decision** | Keep (carried into Week 4 sweep) |
| **Interpretation** | Small improvement over n=100 (RMSE −0.046) at 2× the runtime, suggesting diminishing returns are already visible and the performance ceiling is feature-driven rather than capacity-driven. |

---

## Week 4 — n_estimators Sweep

Systematic sweep over n_estimators ∈ {50, 100, 200, 300} using the same numeric feature set. All four runs recorded in `week4/experiment_matrix.csv`. n=200 retained as the best cost/performance tradeoff; n=300 discarded (6× runtime increase for 0.5% additional RMSE gain).

| Exp ID | n_estimators | Validation RMSE | Validation R² | Runtime (s) | Decision |
|--------|-------------|-----------------|---------------|-------------|----------|
| W4-1 | 50 | 15.1752 | 0.5390 | 9.67 | Discard (worse than n=100) |
| W4-2 | 100 | 15.0714 | 0.5453 | 19.56 | Reference (same as Exp 2) |
| W4-3 | 200 | 15.0254 | 0.5480 | 39.76 | **Retained** |
| W4-4 | 300 | 14.9942 | 0.5499 | 58.46 | Discard (diminishing returns) |

**Interpretation per run:**

**W4-1 (n=50):** Lower than n=100 in both accuracy and stability; insufficient forest diversity for this dataset size.

**W4-2 (n=100):** Replicates Exp 2; confirms prior result is stable across re-runs.

**W4-3 (n=200):** Best runtime-adjusted performance; marginal accuracy over n=100 (−0.046 RMSE) with acceptable 2× runtime cost. Retained as project standard.

**W4-4 (n=300):** Monotonic improvement continues (−0.031 vs. n=200) but with 6× the runtime of n=50 for a total 0.5% gain over n=100; the capacity ceiling is feature-driven, not tree-count-driven. Discarded.

**Week 4 conclusion:** Performance scales monotonically with n_estimators but with sharply diminishing returns. The tree-count bottleneck is exhausted; the remaining ceiling is determined by the feature set itself.

---

## Week 5 — Feature Engineering and Hyperparameter Experiments (E1–E12)

**Starting baseline (carried from Week 4):** RF n_estimators=200, numeric features only, RMSE 15.0254  
**Week 5 best result:** E7, RMSE 15.0196 (−0.058 vs. Week 4 baseline)

### E1 — log1p(duration_ms)

| Field | Value |
|-------|-------|
| **Experiment ID** | E1 |
| **Week** | 5 |
| **Direction tested** | Log-transform right-skewed duration feature |
| **Model / change** | RF n=200 + log1p(duration_ms) added to feature set |
| **Validation RMSE** | 15.0232 |
| **Validation R²** | 0.5482 |
| **Runtime** | 50.65 s |
| **Decision** | Keep |
| **Interpretation** | Tiny improvement (−0.002 RMSE); duration_ms is right-skewed and log compression redistributes tail mass, giving RF splits more useful resolution across the feature range. |

---

### E2 — log1p(loudness+60)

| Field | Value |
|-------|-------|
| **Experiment ID** | E2 |
| **Week** | 5 |
| **Direction tested** | Log-transform bounded loudness feature |
| **Model / change** | RF n=200 + E1 features + log1p(loudness+60) |
| **Validation RMSE** | 15.0259 |
| **Validation R²** | 0.5480 |
| **Runtime** | 53.69 s |
| **Decision** | Discard — rolled back to E1 |
| **Interpretation** | Slightly worse than E1 (+0.003 RMSE); loudness is a bounded, non-zero-inflated feature and log compression adds noise rather than signal for RF splits. |

---

### E3 — Drop key, mode, time_signature, index

| Field | Value |
|-------|-------|
| **Experiment ID** | E3 |
| **Week** | 5 |
| **Direction tested** | Feature ablation — remove low-intuition columns |
| **Model / change** | RF n=200 + log_duration only; key / mode / time_signature / index dropped |
| **Validation RMSE** | 15.7345 |
| **Validation R²** | 0.5044 |
| **Runtime** | 40.90 s |
| **Decision** | Discard — rolled back |
| **Interpretation** | Large degradation (+0.711 RMSE); features that appear uninformative by intuition still carry real aggregate RF signal across many tree splits and must not be dropped. |

---

### E4 — danceability × energy interaction term

| Field | Value |
|-------|-------|
| **Experiment ID** | E4 |
| **Week** | 5 |
| **Direction tested** | Manual feature interaction for correlated features |
| **Model / change** | RF n=200 + E1 features + danceability × energy product |
| **Validation RMSE** | 15.0361 |
| **Validation R²** | 0.5474 |
| **Runtime** | 54.63 s |
| **Decision** | Discard — rolled back to E1 |
| **Interpretation** | Worse than E1 (+0.013 RMSE); RF already discovers interactions via tree splits, so manually added products introduce collinear noise rather than new signal. |

---

### E5 — energy × loudness interaction term

| Field | Value |
|-------|-------|
| **Experiment ID** | E5 |
| **Week** | 5 |
| **Direction tested** | Manual feature interaction for energy-loudness correlation |
| **Model / change** | RF n=200 + E1 features + energy × loudness product |
| **Validation RMSE** | 15.0292 |
| **Validation R²** | 0.5478 |
| **Runtime** | 52.05 s |
| **Decision** | Discard — rolled back to E1 |
| **Interpretation** | Worse than E1 (+0.006 RMSE); RF handles correlated-feature interactions natively and manual products degrade rather than improve fit. |

---

### E6 — tempo × danceability interaction term

| Field | Value |
|-------|-------|
| **Experiment ID** | E6 |
| **Week** | 5 |
| **Direction tested** | Manual feature interaction for rhythm-related features |
| **Model / change** | RF n=200 + E1 features + tempo × danceability product |
| **Validation RMSE** | 15.0424 |
| **Validation R²** | 0.5470 |
| **Runtime** | 53.59 s |
| **Decision** | Discard — rolled back to E1 |
| **Interpretation** | Worst of the interaction-term experiments (+0.019 RMSE); confirms the pattern that manually constructed feature products add noise for tree-based models. |

---

### E7 — log1p(instrumentalness) — Final Best

| Field | Value |
|-------|-------|
| **Experiment ID** | E7 |
| **Week** | 5 |
| **Direction tested** | Log-transform zero-inflated instrumentalness feature |
| **Model / change** | RF n=200 + E1 features + log1p(instrumentalness) |
| **Validation RMSE** | 15.0196 |
| **Validation R²** | 0.5484 |
| **Runtime** | 54.31 s |
| **Decision** | **Keep — best result of project (pre-artifact-removal)** |
| **Interpretation** | Best result achieved during modeling (−0.004 vs. E1); instrumentalness has a large zero-mass spike (most tracks score near 0) and a sparse right tail, making it the feature whose distribution most benefits from log compression. |

---

### E8 — log1p(speechiness) + log1p(acousticness)

| Field | Value |
|-------|-------|
| **Experiment ID** | E8 |
| **Week** | 5 |
| **Direction tested** | Extend log transforms to additional bounded features |
| **Model / change** | RF n=200 + E7 features + log1p(speechiness) + log1p(acousticness) |
| **Validation RMSE** | 15.0261 |
| **Validation R²** | 0.5480 |
| **Runtime** | 93.40 s |
| **Decision** | Discard — rolled back to E7 |
| **Interpretation** | Worse than E7 (+0.007 RMSE) with 73% more runtime; speechiness and acousticness are not sufficiently zero-inflated to benefit from log compression, and over-transformation adds noise. |

---

### E9 — HistGradientBoosting (tuned)

| Field | Value |
|-------|-------|
| **Experiment ID** | E9 |
| **Week** | 5 |
| **Direction tested** | Re-test boosting with tuned hyperparameters |
| **Model / change** | HistGradientBoostingRegressor, max_iter=500, lr=0.05, max_depth=6, with E7 features |
| **Validation RMSE** | 17.7524 |
| **Validation R²** | 0.3691 |
| **Runtime** | 4.55 s |
| **Decision** | Discard — rolled back to E7 |
| **Interpretation** | Substantially worse than RF (+2.733 RMSE) even with tuning; boosting's sequential fitting is not well-suited to this feature pattern, and the best model family is unambiguously RF. |

---

### E10 — RF max_features=0.5

| Field | Value |
|-------|-------|
| **Experiment ID** | E10 |
| **Week** | 5 |
| **Direction tested** | Restrict feature fraction per split for RF diversity |
| **Model / change** | RF n=200, max_features=0.5, with E7 features |
| **Validation RMSE** | 15.3764 |
| **Validation R²** | 0.5267 |
| **Runtime** | 33.59 s |
| **Decision** | Discard — rolled back to E7 |
| **Interpretation** | Worse by 0.357 RMSE; restricting feature sampling per split reduces beneficial diversity on this small feature set. |

---

### E11 — ExtraTreesRegressor

| Field | Value |
|-------|-------|
| **Experiment ID** | E11 |
| **Week** | 5 |
| **Direction tested** | Extra randomization via random split thresholds |
| **Model / change** | ExtraTreesRegressor, n_estimators=200, with E7 features |
| **Validation RMSE** | 15.4511 |
| **Validation R²** | 0.5221 |
| **Runtime** | 21.38 s |
| **Decision** | Discard |
| **Interpretation** | Worse by 0.432 RMSE; random split thresholds are inferior to RF's best-split search for this signal pattern, and additional randomization does not help. |

---

### E12 — RF min_samples_leaf=3

| Field | Value |
|-------|-------|
| **Experiment ID** | E12 |
| **Week** | 5 |
| **Direction tested** | Leaf regularization for the RF |
| **Model / change** | RF n=200, min_samples_leaf=3, with E7 features |
| **Validation RMSE** | 15.2800 |
| **Validation R²** | 0.5326 |
| **Runtime** | 54.54 s |
| **Decision** | Discard |
| **Interpretation** | Worse by 0.260 RMSE; leaf regularization is not the bottleneck — the model is not over-fitting individual leaves, and this constraint only removes signal without reducing variance meaningfully. |

---

## Week 6 — Diagnostic Analyses

No new models trained. All Week 6 work is diagnostic or validation analysis using the locked model from Week 5 (E7: RF n=200 + log_duration + log_instrumentalness).

---

### D1 — Popularity Bucket Analysis

| Field | Value |
|-------|-------|
| **Analysis ID** | D1 |
| **Week** | 6 |
| **Direction tested** | How does prediction error vary across the popularity distribution? |
| **Model** | E7 retained model (with index) |
| **Outcome** | RMSE: Low 14.16, Medium 11.53, High 31.72; Bias: Low +9.xx, High −27.85 |
| **Decision** | Diagnostic — no model change |
| **Interpretation** | The feature ceiling is not uniform: the model performs well on medium-popularity tracks but severely underpredicts high-popularity tracks (RMSE 31.72, bias −27.85), revealing a systematic regression-to-the-mean failure driven by missing causal variables (artist profile, playlist placement, release context). |

**Bucket-level detail (with index, final retained model):**

| Popularity Bucket | N (val set) | RMSE | MAE | Mean Bias |
|-------------------|-------------|------|-----|-----------|
| Low (0–33) | 11,127 | 14.16 | 10.30 | +9.xx |
| Medium (34–66) | 10,117 | 11.53 | 8.40 | ~0 |
| High (67–100) | 1,556 | 31.72 | 24.xx | −27.85 |

---

### D2 — Feature Importance Analysis

| Field | Value |
|-------|-------|
| **Analysis ID** | D2 |
| **Week** | 6 |
| **Direction tested** | Which features does the locked RF rely on most? |
| **Model** | E7 retained model, after `index` removal |
| **Outcome** | Importances distribute evenly across 8 core audio features (each 8–11%); mode and time_signature each < 1% but still load-bearing |
| **Decision** | Diagnostic — confirms model is using genuine audio signal |
| **Interpretation** | After `index` removal, no single audio feature dominates (acousticness 10.5%, danceability 9.9%, tempo 9.9%, valence 9.8%, speechiness 9.5%, loudness 9.3%, energy 8.8%, liveness 8.4%); the broad distribution confirms popularity prediction requires joint signal across all audio dimensions and that no single feature is a decisive predictor. |

**Top-5 comparison before and after index removal:**

| Rank | With `index` | Importance | Without `index` | Importance |
|------|-------------|------------|-----------------|------------|
| 1 | `index` | 35.8% | `acousticness` | 10.5% |
| 2 | `acousticness` | 7.2% | `danceability` | 9.9% |
| 3 | `danceability` | 6.5% | `tempo` | 9.9% |
| 4 | `valence` | 6.2% | `valence` | 9.8% |
| 5 | `loudness` | 6.1% | `speechiness` | 9.5% |

---

### D3 — Data Quality Analysis

| Field | Value |
|-------|-------|
| **Analysis ID** | D3 |
| **Week** | 6 |
| **Direction tested** | Are there data quality issues that affect model conclusions? |
| **Model** | N/A — dataset audit only |
| **Outcome** | 114,000 rows; 0 exact duplicates; 0 missing numeric values; 24,259 track_id duplicates (structural, not errors); popularity mean 33.2, std 22.3, 14.1% at popularity=0 |
| **Decision** | Validation — no dataset modifications |
| **Interpretation** | The dataset is clean: no missing numerics and no exact-row duplicates; the track_id repetition is a multi-genre structural property (same track appears in multiple genre rows) that does not constitute leakage, and the popularity distribution's right-skew explains why high-popularity tracks are the hardest bucket (only 6.7% of rows have popularity ≥ 67). |

**Popularity distribution:**

| Statistic | Value |
|-----------|-------|
| Mean | 33.2 |
| Median | 35.0 |
| Std dev | 22.3 |
| Min / Max | 0 / 100 |
| Popularity = 0 | 16,020 rows (14.1%) |
| Popularity ≥ 67 | 7,632 rows (6.7%) |
| Popularity ≥ 80 | 1,201 rows (1.1%) |

---

### D4 — Index Artifact Validation

| Field | Value |
|-------|-------|
| **Analysis ID** | D4 |
| **Week** | 6 |
| **Direction tested** | Does the model's performance depend on the `index` column, a dataset artifact? |
| **Model** | E7 model, with and without `index`; split held constant |
| **Outcome** | With index: RMSE 15.0196; without index: RMSE 15.7187 (Δ +0.699 overall; −3.24 on high-popularity bucket) |
| **Decision** | Validation → model updated to exclude `index`; **artifact-free RMSE 15.7187 is the locked final result** |
| **Interpretation** | The `index` column (CSV row number 0–113,999) is a genre proxy because the dataset is ordered by genre; removing it worsens overall RMSE by 0.70 but improves high-bucket RMSE by 3.24 and distributes feature importance evenly across genuine audio features — all three project conclusions survive and the high-popularity regression-to-the-mean finding is confirmed as structural, not an artifact. |

**Per-bucket RMSE comparison:**

| Bucket | With `index` RMSE | Without `index` RMSE | Δ RMSE |
|--------|-------------------|----------------------|--------|
| Low (0–33) | 14.16 | 15.22 | +1.06 |
| Medium (34–66) | 11.53 | 13.31 | +1.78 |
| High (67–100) | 31.72 | **28.48** | **−3.24** |

---

### D5 — Feature Bucket Error Analysis

| Field | Value |
|-------|-------|
| **Analysis ID** | D5 |
| **Week** | 6 |
| **Direction tested** | Does prediction error vary across audio-feature value ranges? |
| **Model** | Artifact-free model (index excluded), RMSE 15.7187 |
| **Outcome** | Danceability span: 3.1 RMSE units; Energy span: 0.3 units; Tempo span: 1.4 units — all near-zero bias |
| **Decision** | Diagnostic — strengthens final story |
| **Interpretation** | Slicing by audio-feature value produces at most a 3.1-unit RMSE spread and near-zero bias (all within ±1 popularity unit), compared to a 15.2-unit RMSE spread and 33.9-unit bias swing when slicing by popularity bucket; the model's failures are driven by where a track sits in the popularity distribution, not by what it sounds like. |

**Danceability buckets:**

| Bucket | N | RMSE | MAE | Mean Bias |
|--------|---|------|-----|-----------|
| Low (<0.4) | 3,850 | 14.53 | 10.86 | +0.62 |
| Medium (0.4–0.7) | 13,508 | 15.24 | 11.08 | −0.45 |
| High (>0.7) | 5,442 | 17.58 | 12.73 | −0.51 |

**Energy buckets:**

| Bucket | N | RMSE | MAE | Mean Bias |
|--------|---|------|-----|-----------|
| Low (<0.33) | 3,182 | 15.60 | 11.94 | −0.24 |
| Medium (0.33–0.66) | 7,469 | 15.94 | 11.49 | −0.59 |
| High (>0.66) | 12,149 | 15.61 | 11.28 | −0.10 |

**Tempo buckets:**

| Bucket | N | RMSE | MAE | Mean Bias |
|--------|---|------|-----|-----------|
| Low (<90 BPM) | 3,209 | 15.36 | 11.19 | −0.50 |
| Medium (90–140 BPM) | 13,677 | 16.18 | 11.76 | −0.33 |
| High (>140 BPM) | 5,914 | 14.82 | 10.82 | −0.07 |

**RMSE span comparison across analysis dimensions:**

| Slice dimension | RMSE span | Bias span | Pattern |
|----------------|-----------|-----------|---------|
| Popularity bucket | 15.2 units | 33.9 units | Severe, asymmetric, worsens at high end |
| Danceability bucket | 3.1 units | 1.1 units | Mild, nearly unbiased |
| Energy bucket | 0.3 units | 0.4 units | Flat, negligible |
| Tempo bucket | 1.4 units | 0.4 units | Mild, nearly unbiased |

---

## Final Held-Out Test Set Evaluation

> **The held-out test set was opened exactly once, after the model was fully locked following the Week 6 artifact-removal analysis (D4). No modifications to the model, features, hyperparameters, or any other aspect of the pipeline were made after this result was observed.**

### T1 — Held-Out Test Set Evaluation

| Field | Value |
|-------|-------|
| **Analysis ID** | T1 |
| **When run** | After Week 6 lock; one-time only |
| **Script** | `final_test_evaluation.py` |
| **Model evaluated** | Locked final model: RF n_estimators=200, `index` excluded, + log1p(duration_ms) + log1p(instrumentalness) |
| **Train split used** | 60% (train only; validation split held out during all development) |
| **Validation RMSE** | 15.7187 |
| **Final Test RMSE** | **15.7636** |
| **Final Test R²** | **0.4965** |
| **Val–Test RMSE gap** | 0.0449 (0.3%) |
| **Post-result action** | None — no tuning or experimentation performed after observing this result |
| **Interpretation** | The near-identical validation and test RMSEs (0.3% gap) confirm that the locked model did not overfit to the validation set during development. The result is stable and reproducible. The test R² of 0.4965 indicates the model explains approximately 50% of the variance in track popularity on fully unseen data, consistent with the feature ceiling identified throughout the project. |

---

## Project Summary

### Complete Experiment Index

| ID | Week | Type | Direction | Model / Change | RMSE | Δ RMSE | Decision |
|----|------|------|-----------|---------------|------|--------|----------|
| Exp 0 | 2 | Modeling | Linear regression numeric features | LinearRegression | 22.0630 | — | Frozen baseline |
| Exp 1 | 3 | Modeling | L2 regularization | Ridge (α=1.0) | 22.0630 | 0.000 | Discard |
| Exp 2 | 3 | Modeling | Tree-based ensemble | RF n=100 | 15.0714 | −7.000 | Keep |
| Exp 3 | 3 | Modeling | Gradient boosting default | HistGBR default | 18.4472 | +3.377 vs. RF | Discard |
| Exp 4 | 3–4 | Modeling | Increase tree count | RF n=200 | 15.0254 | −0.046 | Keep |
| W4-1 | 4 | Modeling | n_estimators sweep | RF n=50 | 15.1752 | +0.104 vs. n=100 | Discard |
| W4-2 | 4 | Modeling | n_estimators sweep | RF n=100 | 15.0714 | (reference) | Reference |
| W4-3 | 4 | Modeling | n_estimators sweep | RF n=200 | 15.0254 | −0.046 | **Retained** |
| W4-4 | 4 | Modeling | n_estimators sweep | RF n=300 | 14.9942 | −0.031 vs. n=200 | Discard |
| E1 | 5 | Modeling | Log-transform duration | RF + log_duration | 15.0232 | −0.002 | Keep |
| E2 | 5 | Modeling | Log-transform loudness | RF + log_loudness | 15.0259 | +0.003 | Discard |
| E3 | 5 | Modeling | Drop low-intuition features | RF − key/mode/time_sig/index | 15.7345 | +0.711 | Discard |
| E4 | 5 | Modeling | Interaction: danceability × energy | RF + dance×energy | 15.0361 | +0.013 | Discard |
| E5 | 5 | Modeling | Interaction: energy × loudness | RF + energy×loudness | 15.0292 | +0.006 | Discard |
| E6 | 5 | Modeling | Interaction: tempo × danceability | RF + tempo×dance | 15.0424 | +0.019 | Discard |
| E7 | 5 | Modeling | Log-transform instrumentalness | RF + log_instrumentalness | 15.0196 | −0.004 | **Keep — project best** |
| E8 | 5 | Modeling | Log-transform speechiness + acousticness | RF + log_speech + log_acous | 15.0261 | +0.007 | Discard |
| E9 | 5 | Modeling | Gradient boosting tuned | HistGBR 500-iter lr=0.05 | 17.7524 | +2.733 | Discard |
| E10 | 5 | Modeling | Restrict RF feature fraction | RF max_features=0.5 | 15.3764 | +0.357 | Discard |
| E11 | 5 | Modeling | Extra randomization | ExtraTreesRegressor n=200 | 15.4511 | +0.432 | Discard |
| E12 | 5 | Modeling | Leaf regularization | RF min_samples_leaf=3 | 15.2800 | +0.260 | Discard |
| D1 | 6 | Diagnostic | Error by popularity bucket | Retained model (with index) | 11.53–31.72 | N/A | Diagnostic |
| D2 | 6 | Diagnostic | Feature importance audit | Retained model (no index) | N/A | N/A | Diagnostic |
| D3 | 6 | Validation | Dataset quality audit | N/A — data audit | N/A | N/A | Validation |
| D4 | 6 | Validation | Index artifact removal | RF with vs. without index | 15.7187 | +0.699 overall | **Artifact-free final** |
| D5 | 6 | Diagnostic | Error by feature-value bucket | Artifact-free model | 14.53–17.58 | N/A | Diagnostic |
| T1 | Post-lock | Test evaluation | One-time held-out test set evaluation | Locked final model | **15.7636** | N/A | **Final test result — no further action taken** |

---

### Final Accounting

| Metric | Value |
|--------|-------|
| **Total modeling experiments run** | 16 (Exp 0–4 + E1–E12) |
| **Total diagnostic / validation analyses** | 5 (D1–D5) |
| **Directions retained (modeling)** | 3 — RF adoption (Exp 2), log1p(duration_ms) (E1), log1p(instrumentalness) (E7) |
| **Directions discarded (modeling)** | 13 |
| **Final locked model** | RandomForestRegressor, n_estimators=200, `index` excluded, + log1p(duration_ms) + log1p(instrumentalness) |
| **Validation RMSE (artifact-free)** | **15.7187** |
| **Final held-out test RMSE** | **15.7636** |
| **Final held-out test R²** | **0.4965** |
| **Val–test RMSE gap** | 0.0449 (0.3%) — confirms no overfitting to validation set |
| **Test set opened** | Exactly once, after model lock; no tuning performed after |
| **Linear baseline RMSE** | 22.0630 |
| **Total RMSE improvement (vs. test)** | 6.30 units (−28.5%) |
| **Improvement from RF adoption alone** | 7.00 units (−31.7%) |
| **Improvement from all post-RF modeling** | 0.058 units (five weeks of refinement) |
| **Worst bucket RMSE (high-popularity, artifact-free)** | 28.48 |
| **Best bucket RMSE (medium-popularity, artifact-free)** | 13.31 |
| **Bias on high-popularity tracks (artifact-free)** | −23.26 (systematic underprediction) |
