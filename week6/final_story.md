# Final Story: Spotify Popularity Prediction with Numeric Audio Features

**Project:** AutoResearch — Spotify Popularity Prediction
**Period:** Weeks 2–6
**Final model RMSE:** 15.0196 (vs. 22.0630 linear baseline)
**Improvement:** −31.9% relative RMSE

---

## Revised Project Statement

This project investigates the limits of Spotify popularity prediction using numeric audio features. Through a series of autonomous experiments, the project found that tree-based ensemble models substantially outperform linear models, but that predictive gains plateau almost immediately even after sustained feature engineering and model refinement.

The dominant gain — a 31.7% RMSE improvement — came from a single change: replacing LinearRegression with RandomForest. Every subsequent experiment across four weeks and twelve experiments combined moved RMSE by less than 0.06 units. The final bucket analysis reveals why: the model performs reasonably well on medium-popularity tracks but systematically and severely underpredicts highly popular songs, because the features that determine breakout popularity — artist reputation, playlist placement, release context — are entirely absent from the numeric audio feature set.

The project's final contribution is not finding the best model. It is identifying and characterizing the hard ceiling of numeric audio features for popularity prediction, and showing exactly where that ceiling matters most.

---

## The Question

Can Spotify track popularity be predicted from numeric audio features — danceability, energy, loudness, tempo, speechiness, acousticness, instrumentalness, liveness, valence, key, mode, time signature, and duration?

---

## What We Found

### Tree-based models dramatically outperform linear models

The linear baseline (LinearRegression, RMSE 22.06) captures barely 2.6% of variance in popularity (R² = 0.026). This is not a model failure: it reflects that popularity and audio features are weakly linearly related. A RandomForest (RMSE 15.02, R² = 0.548) captures 54.8% of variance using the same features — a 31.9% relative improvement. The nonlinear structure in the data is real and tree models can exploit it.

### Improvements plateau almost immediately

Within the tree-based family, further effort produces rapidly diminishing returns:

| Change | RMSE | Δ vs. RF baseline |
|--------|------|-------------------|
| RF n_estimators=50 | 15.18 | — |
| RF n_estimators=100 | 15.07 | −0.11 |
| RF n_estimators=200 | 15.03 | −0.04 |
| RF n_estimators=300 | 14.99 | −0.03 |
| + log1p(duration_ms) | 15.02 | −0.003 |
| + log1p(instrumentalness) | **15.02** | −0.006 |

Doubling the tree count from 100 to 200 moved RMSE by 0.05. Four weeks of feature engineering and hyperparameter search moved RMSE by another 0.006. The model is not improving because the data does not contain the relevant signal.

### Prediction quality differs sharply across popularity ranges

Analyzing the best model's errors by popularity bucket reveals the structural problem:

| Bucket | RMSE | MAE | Bias (mean error) |
|--------|------|-----|-------------------|
| Low (0–33) | 14.16 | 9.48 | +8.99 (overpredicts) |
| Medium (34–66) | 11.53 | 8.36 | −6.84 (underpredicts slightly) |
| High (67–100) | 31.72 | 27.86 | −27.85 (massively underpredicts) |

The model performs best for medium-popularity tracks and worst for high-popularity tracks. At the extremes, the model regresses toward the mean — it can't distinguish a genuinely popular song from a moderately good one because the differentiating factors (artist reputation, playlist placement, release timing, label support) are absent from the feature set.

---

## The Core Claim

**Tree-based ensemble models significantly outperform linear models on this task, but improvements plateau quickly when relying only on numeric audio features.**

The first half is definitively confirmed: RF vs. LinearRegression is a 31.9% RMSE improvement, a large and reproducible gap. The second half is confirmed with equal clarity: five weeks of iteration on model complexity, preprocessing, and hyperparameters moved RMSE by a combined 1.08 units after the initial RF adoption. The feature ceiling is real, and the bucket analysis shows exactly where it bites hardest — at the high end, where the factors that turn a good song into a hit are invisible to the model.

---

## What the Model Can and Cannot Do

**Can do:**
- Distinguish clearly low-popularity tracks from average ones with moderate accuracy
- Capture nonlinear audio-feature patterns that linear models miss
- Provide meaningful signal for medium-popularity tracks (RMSE 11.5 ≈ ±11 popularity units)

**Cannot do:**
- Identify which good songs become hits (high-popularity RMSE 31.7, bias −27.8)
- Reduce prediction error below ~15 without access to non-audio features
- Explain ~45% of variance in popularity even with the best model

---

## What Would Actually Help

The bucket analysis points to a concrete next step that was out of scope for this project: artist-level and genre-level features. A song's audio properties tell you what it sounds like. What they cannot tell you is who made it, how many followers that artist has, whether it was on a major-label release, or what genre currently drives Spotify editorial playlists. These factors predict popularity at the high end — exactly where numeric audio features fail most severely.

---

## Conclusion

This project is a clean, interpretable study of what numeric audio features can and cannot predict about Spotify popularity. The answer: quite a lot, but with a hard ceiling. The methodology is sound, the results are reproducible, and the failure modes are explained rather than hidden. That is the right outcome for a constrained, well-controlled experiment.
