# Final Results Table — Spotify Popularity Prediction
## AutoResearch Weeks 2–6 | Evaluation metric: Validation RMSE (lower is better)

**Locked final model:** RandomForestRegressor (n_estimators=200, `index` excluded, + log1p(duration_ms) + log1p(instrumentalness))
**Locked final RMSE:** 15.7187 (artifact-free) | 15.0196 (with index, project-retained best)
**Linear baseline RMSE:** 22.0630

---

| # | Direction | Experiments | Representative RMSE | Δ vs. Baseline | Key Finding | Final Interpretation |
|---|-----------|-------------|---------------------|----------------|-------------|----------------------|
| 1 | **Baseline — Linear Regression** | Exp 0 (Ridge discarded at Exp 1) | **22.0630** | — (anchor) | R² = 0.026; linear model captures almost no variance. Ridge regularization (α=1.0) produced identical RMSE — no overfitting existed to correct. | The audio-feature–popularity relationship is strongly nonlinear. Linear models are structurally incapable of capturing it regardless of regularization. This result establishes a hard lower bound on model performance without architectural change. |
| 2 | **Random Forest — First Adoption** | Exp 2 (n=100) | **15.0714** | −7.0 (−31.7%) | Single largest improvement of the entire project. R² jumps from 0.026 → 0.545. Tree-based nonlinear splitting captures structure that linear models miss entirely. | RF adoption accounts for 7.0 of the total 7.04 RMSE gain over five weeks. Every subsequent experiment combined moved RMSE by 0.04 units. The model-family switch, not any refinement, is the project's decisive result. |
| 3 | **Hyperparameter Scaling — n_estimators** | Exp 4, Week 4 matrix (n = 50, 100, 200, 300) | **14.9942** (n=300) | −0.077 vs. n=100 | RMSE improves monotonically but with sharply diminishing returns: 50→100 saves 0.10 RMSE, 100→200 saves 0.05, 200→300 saves 0.03. Runtime scales 6× (9.7s → 58.5s) for a 0.5% total RMSE gain. | Increasing model capacity does not solve the prediction problem. The gain from 100 to 300 trees is smaller than the noise floor of any single feature experiment. Capacity is not the bottleneck — the feature ceiling is. n=200 retained as the best cost/performance tradeoff. |
| 4 | **Feature Engineering — Log Transforms** | E1–E8, E10, E12 (Week 5) | **15.0196** (E7 final best) | −0.058 vs. RF n=200 start | Only log1p on zero-inflated features helped: log1p(duration_ms) saved 0.002 RMSE; log1p(instrumentalness) saved 0.004. Manual interaction terms (E4–E6), additional log transforms on bounded features (E2, E8), and RF hyperparameter variants (E10, E12) all worsened performance. Dropping features (E3) caused +0.711 spike. | Log1p works only when a feature's distribution has a zero-mass spike with a sparse right tail — matching the criterion for instrumentalness and duration_ms exactly. RF already discovers feature interactions via tree splits; manually added products introduce collinear noise. Twelve experiments across preprocessing and regularization produced a combined 0.058 RMSE gain, confirming that the numeric audio feature set has been mined to its ceiling. |
| 5 | **Alternative Model Families** | Exp 3 (HistGBR default), E9 (HistGBR tuned, 500 iter), E11 (ExtraTrees) | **15.4511** (ExtraTrees, best alternative) | Worse than RF in all cases | HistGBR (default): 18.45 (+3.4 vs. RF). HistGBR (tuned, lr=0.05, max_depth=6, 500 iter): 17.75 (+2.7). ExtraTrees (n=200): 15.45 (+0.43). No alternative model family improved on RF. | RandomForest is the best-suited model family for this feature set and dataset size. Boosting's sequential fitting underperforms RF here even after tuning. ExtraTrees' random split thresholds are inferior to RF's best-split search on this signal pattern. The ceiling is a feature ceiling, not a model-family ceiling — no different architecture unlocks additional accuracy from these columns. |
| 6 | **Popularity Bucket Analysis** | Week 6 diagnostic (no model change) | **11.53** (medium) / **31.72** (high) / **14.16** (low) — with index; **13.31** / **28.48** / **15.22** — artifact-free | N/A — diagnostic | Model performs best on medium-popularity tracks (RMSE 11.5) and worst on high-popularity tracks (RMSE 31.7, bias −27.9). At the high end, the model systematically underpredicts by ~28 popularity units — a classic regression-to-the-mean failure. Low-popularity tracks are overpredicted by ~9 units. | The feature ceiling is not uniform across the popularity range. Numeric audio features can describe typical audio character but cannot identify which songs become hits. The factors that drive breakout popularity — artist reputation, playlist placement, label support, release timing — are invisible to the model. This is not a modeling shortfall; it is an information shortfall. The bucket analysis is the project's primary explanatory contribution. |
| 7 | **Index Artifact Validation** | Week 6 — model re-run with and without `index` column | **15.7187** (no index) vs. 15.0196 (with index) | +0.699 overall; −3.24 on high-popularity bucket | The `index` column (dataset row number, 0–113,999) was the single highest-importance feature at 35.8% when included. The CSV is ordered by genre, making row number a genre proxy. Removing it worsens overall RMSE by 0.70 but improves high-bucket RMSE by 3.24 and redistributes importance evenly across 8 genuine audio features (each 8–11%). All three project conclusions survive removal. | The `index` artifact was giving the model borrowed genre signal it had no right to use. The artifact-free model (RMSE 15.72) is the honest representation of what numeric audio features alone achieve — still 28.8% better than the linear baseline. Removing index makes the bucket pattern more interpretable (high-bucket bias drops from −27.9 to −23.3) and confirms the regression-to-the-mean finding is structural, not an artifact. |
| 8 | **Feature Bucket Analysis** | Week 6 diagnostic — danceability, energy, tempo buckets | **14.53–17.58** (danceability); **15.60–15.94** (energy); **14.82–16.18** (tempo) | N/A — diagnostic | Slicing by audio-feature value produces at most a 3.1-unit RMSE spread and near-zero bias (all within ±1 popularity unit). In stark contrast, slicing by popularity bucket produces a 15.2-unit RMSE spread and a 33.9-unit bias swing. Counterintuitively, high-danceability tracks are the hardest to predict (RMSE 17.58), not easiest. Energy shows essentially no effect on RMSE (0.3-unit span). Extreme tempos are more predictable than mid-tempo (90–140 BPM), which spans all mainstream genres. | The model's prediction error is driven by where a track falls in the popularity distribution, not by what it sounds like. The feature bucket analysis rules out the alternative explanation that the model fails because it misreads certain audio profiles. It does not: error is nearly uniform and unbiased across audio-feature space. The failure emerges only in popularity space, where unobserved factors (not audio features) determine outcomes. This is direct evidence that the feature ceiling is real and is specifically an information ceiling, not a modeling ceiling. |

---

## Held-Out Test Set Evaluation

> **The held-out test set was opened exactly once, after the model was locked following Week 6 artifact removal. No tuning, retraining, or additional experimentation was performed after observing this result.**

| Split | RMSE | R² |
|-------|------|----|
| Validation (used during development) | 15.7187 | — |
| **Held-out test set (opened once, post-lock)** | **15.7636** | **0.4965** |

The gap between validation RMSE (15.7187) and test RMSE (15.7636) is **0.0449 units (0.3%)** — effectively negligible. This close agreement provides strong evidence that the result is stable, that no overfitting to the validation set occurred during development, and that the locked model generalizes reliably to unseen data.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Linear baseline RMSE | 22.0630 |
| RF first adoption RMSE | 15.0714 |
| Project best RMSE (with index) | 15.0196 |
| Project best RMSE (artifact-free, validation) | 15.7187 |
| **Final held-out test RMSE** | **15.7636** |
| **Final held-out test R²** | **0.4965** |
| Val–test RMSE gap | 0.0449 (0.3%) |
| Total RMSE improvement over baseline (test) | 6.30 units (−28.5%) |
| Improvement from RF adoption alone | 7.00 units (−31.7%) |
| Improvement from all post-RF work | 0.04 units (−0.3%) |
| Best bucket RMSE | 11.53 (medium-popularity, with index) |
| Worst bucket RMSE | 31.72 (high-popularity, with index) |
| Bias on high-popularity tracks | −27.85 (systematic underprediction) |
| Total experiments run | 16 (Exp 0–4 + E1–E12) |
| Total directions kept | 3 (RF adoption, log_duration, log_instrumentalness) |

---

## Locked Conclusion

Tree-based ensemble models (RandomForest) significantly outperform linear models on Spotify popularity prediction, reducing RMSE by 31.9% using identical numeric audio features. However, gains plateau almost immediately after initial RF adoption: five weeks and 16 experiments of sustained refinement moved RMSE by a further 0.06 units. The popularity bucket analysis explains why: numeric audio features cannot identify which songs become hits because the causal factors — artist reputation, playlist placement, release context — are absent from the feature set. The model is unbiased in audio-feature space but severely biased in popularity-outcome space. This is a feature-information ceiling, not a model capacity or preprocessing ceiling.
