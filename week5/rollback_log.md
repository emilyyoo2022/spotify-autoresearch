# Rollback Log — Week 5 Autonomous Experiment Block

**Date:** 2026-05-11
**Block:** Feature engineering and preprocessing for Spotify popularity prediction
**Active baseline throughout:** RF n_estimators=200, RMSE 15.0254

---

## Rollback Events

### E2 — Rolled back
- **Change attempted:** Add log1p(loudness + 60) on top of E1 (log_duration_ms)
- **RMSE after change:** 15.0259 (worse than current best E1: 15.0232)
- **Why reverted:** RMSE degraded. The loudness variable ranges from about −60 to 0 dB and does not exhibit the same zero-inflation that makes log transforms useful. Shifting and logging added noise rather than compressing a meaningful skew.
- **State restored:** E1 model (log_duration_ms only, RF n_estimators=200)

---

### E3 — Rolled back
- **Change attempted:** Drop key, mode, time_signature, index columns + keep log_duration_ms
- **RMSE after change:** 15.7345 (much worse than current best E1: 15.0232; +0.711)
- **Why reverted:** Significant RMSE degradation. Dropping these features assumed they were low-signal noise, but they carry measurable predictive information. Key, mode, and time_signature likely encode genre-adjacent patterns correlated with popularity.
- **State restored:** E1 model (log_duration_ms only, RF n_estimators=200)

---

### E4 — Rolled back
- **Change attempted:** Add danceability × energy product feature on top of E1
- **RMSE after change:** 15.0361 (worse than current best E1: 15.0232)
- **Why reverted:** RMSE degraded. Random Forest already discovers feature interactions via its splitting mechanism. Manually adding product terms does not add independent signal and may introduce collinearity.
- **State restored:** E1 model (log_duration_ms only, RF n_estimators=200)

---

### E5 — Rolled back
- **Change attempted:** Add energy × loudness product feature on top of E1
- **RMSE after change:** 15.0292 (worse than current best E1: 15.0232)
- **Why reverted:** RMSE degraded. Same failure mode as E4 — RF does not benefit from manually engineered interaction terms.
- **State restored:** E1 model (log_duration_ms only, RF n_estimators=200)

---

### E6 — Rolled back
- **Change attempted:** Add tempo × danceability product feature on top of E1
- **RMSE after change:** 15.0424 (worse than current best E1: 15.0232)
- **Why reverted:** RMSE degraded. Third consecutive interaction term to hurt performance. Interaction engineering is not the right lever for RF on this dataset.
- **State restored:** E1 model (log_duration_ms only, RF n_estimators=200)

---

### E8 — Rolled back
- **Change attempted:** Add log1p(speechiness) and log1p(acousticness) on top of E7 (log_duration_ms + log_instrumentalness)
- **RMSE after change:** 15.0261 (worse than current best E7: 15.0196)
- **Why reverted:** RMSE degraded. Speechiness and acousticness are bounded [0, 1] but less zero-inflated than instrumentalness. Adding their log-transforms over-engineered the feature space without compression benefit.
- **State restored:** E7 model (log_duration_ms + log_instrumentalness, RF n_estimators=200)

---

### E9 — Rolled back
- **Change attempted:** HistGradientBoostingRegressor (max_iter=500, lr=0.05, max_depth=6) with E7 features
- **RMSE after change:** 17.7524 (much worse than current best E7: 15.0196; +2.733)
- **Why reverted:** Severe RMSE degradation. HistGBR with these hyperparameters substantially underperforms the RF baseline. The tuned settings (low learning rate, limited depth) did not compensate for the model family mismatch on this feature set.
- **State restored:** E7 model (log_duration_ms + log_instrumentalness, RF n_estimators=200)

---

### E10 — Rolled back
- **Change attempted:** RF max_features=0.5 with E7 features
- **RMSE after change:** 15.3764 (worse than current best E7: 15.0196; +0.358)
- **Why reverted:** RMSE degraded. Increasing the feature fraction from sqrt (~27%) to 50% reduced tree diversity and hurt generalization. The default sqrt setting is better calibrated for this feature count.
- **State restored:** E7 model (log_duration_ms + log_instrumentalness, RF n_estimators=200)

---

### E11 — Rolled back
- **Change attempted:** ExtraTreesRegressor n_estimators=200 with E7 features
- **RMSE after change:** 15.4511 (worse than current best E7: 15.0196; +0.432)
- **Why reverted:** RMSE degraded. Extra randomization in split selection (ExtraTrees) hurts on this dataset. RF's best-split search at each node outperforms random threshold selection here.
- **State restored:** E7 model (log_duration_ms + log_instrumentalness, RF n_estimators=200)

---

### E12 — Rolled back
- **Change attempted:** RF min_samples_leaf=3 with E7 features
- **RMSE after change:** 15.2800 (worse than current best E7: 15.0196; +0.260)
- **Why reverted:** RMSE degraded. Increasing minimum leaf size restricts tree depth and loses granularity. The default min_samples_leaf=1 allows finer splits that are beneficial here.
- **State restored:** E7 model (log_duration_ms + log_instrumentalness, RF n_estimators=200)

---

## Final Model State

After all rollbacks, model.py retains the E7 configuration:
- Pipeline: log1p(duration_ms) + log1p(instrumentalness) → RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
- Validation RMSE: **15.0196**
- Validation R2: **0.5484**

No crashes occurred during this block.
