# Feature Bucket Error Analysis — Week 6

**Date:** 2026-05-18
**Model:** RandomForestRegressor (n_estimators=200, random_state=42, `index` excluded, log transforms applied)
**Overall validation RMSE:** 15.7187
**Purpose:** Descriptive/interpretive only. No model changes. Analyzes how prediction error varies across feature value ranges for danceability, energy, and tempo.

---

## Bucket Definitions and Results

### Danceability (0–1 scale)

| Bucket | N | RMSE | MAE | Mean Bias |
|--------|---|------|-----|-----------|
| Low (<0.4) | 3,850 | **14.53** | 10.86 | +0.62 |
| Medium (0.4–0.7) | 13,508 | 15.24 | 11.08 | −0.45 |
| High (>0.7) | 5,442 | **17.58** | 12.73 | −0.51 |

### Energy (0–1 scale)

| Bucket | N | RMSE | MAE | Mean Bias |
|--------|---|------|-----|-----------|
| Low (<0.33) | 3,182 | 15.60 | 11.94 | −0.24 |
| Medium (0.33–0.66) | 7,469 | 15.94 | 11.49 | −0.59 |
| High (>0.66) | 12,149 | **15.61** | 11.28 | −0.10 |

### Tempo (BPM)

| Bucket | N | RMSE | MAE | Mean Bias |
|--------|---|------|-----|-----------|
| Low (<90 BPM) | 3,209 | 15.36 | 11.19 | −0.50 |
| Medium (90–140 BPM) | 13,677 | 16.18 | 11.76 | −0.33 |
| High (>140 BPM) | 5,914 | **14.82** | 10.82 | −0.07 |

---

## Findings by Feature

### Danceability — High danceability is harder to predict, not easier

The most counterintuitive result. Error rises monotonically with danceability: RMSE goes from 14.53 (low) to 17.58 (high). The pre-analysis expectation was the reverse — that highly danceable tracks would be more genre-coded and therefore easier to predict.

What this actually shows: high danceability is a necessary but not sufficient condition for mainstream popularity. Extremely danceable tracks exist across a vast popularity range — from underground electronic music with near-zero popularity to chart-topping pop. Knowing a track scores 0.85 on danceability tells you what it sounds like, not who made it or where it landed. The audio feature is distinctive enough to make the RF confident in a prediction, but that confidence is often misplaced, because the real determinant (artist, label, release) is invisible.

Low-danceability tracks (RMSE 14.53) are slightly easier — they span a narrower popularity range in this dataset, with a higher concentration of niche or obscure material that the model can place near the low end of the popularity scale with reasonable accuracy.

### Energy — Essentially no relationship with prediction error

Energy shows almost no variation in RMSE across buckets: 15.60 (low), 15.94 (medium), 15.61 (high). The spread is 0.34 RMSE units — effectively flat. Energy does not differentiate how well the model predicts.

This makes sense in retrospect: energy is a continuous measure of intensity that cuts across nearly every genre and popularity level. High-energy tracks include both critically acclaimed rock records and forgotten radio filler. Low-energy tracks include both beloved acoustic singer-songwriters and anonymous ambient obscurities. The feature does not help narrow down who the track is or how successful it became.

### Tempo — Extreme tempos are more predictable; mid-tempo is the hardest

High-tempo tracks (>140 BPM) have the lowest RMSE (14.82) and near-zero bias (−0.07). Low-tempo tracks are intermediate (15.36). Mid-tempo tracks (90–140 BPM) are hardest (16.18).

This makes structural sense: extreme tempos are stronger genre markers. Tracks above 140 BPM are concentrated in electronic dance music, metal, and certain fast-pop sub-genres with more predictable popularity distributions. Tracks below 90 BPM include ballads and certain folk/classical content that also have somewhat predictable (often lower) popularity. The 90–140 BPM range is the most crowded part of the spectrum — it contains mainstream pop, hip-hop, rock, country, and everything in between. At this tempo, the audio signal cannot distinguish a hit from a miss because every genre and popularity level overlaps.

---

## Comparison: Feature-Bucket vs. Popularity-Bucket Patterns

| Dimension | RMSE range across buckets | Bias range | Pattern |
|-----------|--------------------------|------------|---------|
| Popularity buckets (low/med/high) | 13.31 → 28.48 (span: **15.2 units**) | +10.67 to −23.26 (span: **33.9 units**) | Severe, asymmetric, worsens drastically at high end |
| Danceability buckets | 14.53 → 17.58 (span: **3.1 units**) | +0.62 to −0.51 (span: **1.1 units**) | Mild, nearly unbiased |
| Energy buckets | 15.60 → 15.94 (span: **0.3 units**) | −0.24 to −0.59 (span: **0.4 units**) | Flat, negligible bias |
| Tempo buckets | 14.82 → 16.18 (span: **1.4 units**) | −0.07 to −0.50 (span: **0.4 units**) | Mild, nearly unbiased |

The contrast is stark. Slicing by popularity bucket produces a 15-unit RMSE swing and a 34-unit bias swing. Slicing by any audio feature produces at most a 3-unit RMSE swing and almost no bias.

This asymmetry is the key finding.

---

## How This Connects to the Locked Final Story

### The error structure is driven by popularity, not by audio features

If the model's failures were fundamentally about getting audio-feature signal wrong — misreading danceability or misinterpreting energy — then slicing by those features would reveal large, structured error differences. It does not. Feature buckets show small, nearly unbiased variation. This means the model handles the audio domain reasonably consistently: it does not catastrophically fail on any particular sound profile.

What it fails on is predicting *which* tracks within any audio profile become popular. A high-danceability cluster, a mid-energy cluster, a 120-BPM cluster — in each case the model can describe the typical audio character but cannot identify the breakout songs. That failure emerges only when you slice by popularity, not by feature value.

### Danceability finding strengthens the ceiling argument

High-danceability tracks should, by genre intuition, be the "easiest" category — they're the sound of mainstream pop and dance music. Instead they're the hardest feature bucket to predict (RMSE 17.58). This is direct evidence that audio-feature confidence does not translate to prediction accuracy. The model knows what a highly danceable track sounds like. It does not know which highly danceable track becomes a hit — because that is determined by factors entirely outside the audio domain.

### Bias pattern confirms the popularity-bucket finding is structural

Across all feature buckets, mean bias is tiny (all within ±1 popularity unit). Across popularity buckets, bias is enormous: the model overpredicts low-popularity tracks by +10.67 and underpredicts high-popularity tracks by −23.26. This means the model's systematic error is not about misjudging audio features — it is about regressing to the mean when the true popularity signal is absent. The model is unbiased in audio-feature space but severely biased in popularity-outcome space. That is exactly what a feature ceiling looks like.

### Energy flatness is interpretively useful

The finding that energy barely affects prediction error (0.3-unit RMSE span) is useful for the presentation: it illustrates that even a feature with significant RF importance (8.8% in the no-index model) does not produce structured prediction error. The model uses energy as one signal among many, but no energy level is particularly predictable or unpredictable. The difficulty lies elsewhere.

---

## Effect on the Locked Story

**The feature-bucket analysis strengthens, not weakens, every element of the project's final story:**

1. **Tree models outperform linear models** — unaffected. This analysis is descriptive and adds no new modeling evidence.

2. **Improvements plateau quickly** — supported. The feature analysis shows the model is already extracting audio signal consistently. There is no obvious audio-feature dimension where it is failing badly and could improve with more engineering.

3. **Regression-to-the-mean on high-popularity tracks** — strengthened. Feature buckets show near-zero bias; popularity buckets show massive bias. The systematic failure is in the popularity dimension, not the audio-feature dimension. This rules out the explanation that the model simply fails at certain types of sound.

4. **The feature ceiling is real** — strengthened. High danceability — the most "mainstream-sounding" feature profile — produces the highest feature-bucket RMSE. The model cannot convert audio-feature confidence into popularity-prediction accuracy, because audio features do not determine which songs become hits.
