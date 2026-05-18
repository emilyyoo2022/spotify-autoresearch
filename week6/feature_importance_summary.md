# Feature Importance Summary

**Date:** 2026-05-18
**Model:** RandomForestRegressor (n_estimators=200, random_state=42)
**Features:** All original numeric columns + log1p(duration_ms) + log1p(instrumentalness)
**Importance type:** Mean decrease in impurity (Gini importance), averaged across 200 trees

---

## Feature Importances (Ranked) — Final Model, `index` Excluded

*Updated 2026-05-18 after index artifact validation. The `index` column has been removed from the retained model (see `index_artifact_validation.md`). Importances below reflect the final artifact-free model.*

| Rank | Feature | Importance | Notes |
|------|---------|------------|-------|
| 1 | `acousticness` | 0.1050 | Proportion of acoustic vs. electronic sound |
| 2 | `danceability` | 0.0995 | Rhythmic suitability for dancing |
| 3 | `tempo` | 0.0986 | Beats per minute |
| 4 | `valence` | 0.0982 | Musical positiveness/mood |
| 5 | `speechiness` | 0.0953 | Presence of spoken words |
| 6 | `loudness` | 0.0927 | Overall loudness in dB |
| 7 | `energy` | 0.0882 | Perceptual intensity and activity |
| 8 | `liveness` | 0.0839 | Presence of live audience |
| 9 | `duration_ms` | 0.0539 | Raw track length (ms) |
| 10 | `log_duration_ms` | 0.0532 | Log-transformed track length |
| 11 | `key` | 0.0413 | Musical key (0–11) |
| 12 | `instrumentalness` | 0.0373 | Proportion of instrumental content (raw) |
| 13 | `log_instrumentalness` | 0.0372 | Log-transformed instrumentalness |
| 14 | `mode` | 0.0094 | Major (1) vs. minor (0) |
| 15 | `time_signature` | 0.0062 | Beats per bar |

---

## What Changed After Removing `index`

The original model (with `index`) showed the dataset row number as the single dominant feature at 35.8% importance — far above any audio feature. This was a dataset artifact: the CSV is ordered by genre, so row index correlates with genre, and genre correlates with popularity.

After removing `index`, importances redistribute evenly across the 8 core audio features (each 8–11%). This is the correct picture: no single audio feature dominates popularity prediction. The RF is drawing on the joint signal of all dimensions.

**Previous top-5 with index:** index (35.8%), acousticness (7.2%), danceability (6.5%), valence (6.2%), loudness (6.1%)
**Current top-5 without index:** acousticness (10.5%), danceability (9.9%), tempo (9.9%), valence (9.8%), speechiness (9.5%)

---

## Audio Feature Interpretation

- **Acousticness (10.5%):** Acoustic tracks cluster in genres (folk, singer-songwriter, classical) with distinct and predictable popularity distributions.
- **Danceability (9.9%):** High-danceability tracks are concentrated in dance, pop, and hip-hop — genres with systematically higher average popularity.
- **Tempo (9.9%):** BPM encodes genre conventions (e.g., very slow ballads, fast electronic music) that correlate with popularity.
- **Valence (9.8%):** Mood correlates with genre and listener preference patterns.
- **Speechiness (9.5%):** Distinguishes rap/spoken-word tracks from instrumental and melodic genres.

No single feature accounts for more than ~10% of importance. This broad distribution reflects that popularity is a multi-dimensional signal and the RF is using all available audio axes jointly.

**Duration pair:** `duration_ms` and `log_duration_ms` together account for ~10.7%. The RF splits responsibility between the raw and log-transformed versions. Both remain because the log transform (E1) helped by compressing the right tail — removing either would require re-validating.

**Instrumentalness pair:** Similarly, both raw and log versions total ~7.5%. The zero-inflated distribution of instrumentalness benefits from log compression (E7).

**Bottom features:** `mode` (0.94%) and `time_signature` (0.62%) contribute minimally. However, E3 showed that dropping them worsens RMSE by 0.711 — they carry aggregate signal across many trees even if each individual split is weak.

---

## Implications for the Locked Story

The cleaned importance distribution reinforces every element of the final story:

1. **Signal is distributed broadly** — no single audio feature is a strong predictor of popularity. This is consistent with popularity being determined by factors outside the audio domain.
2. **The RF captures multi-feature nonlinear patterns** — the broad importance spread is what tree models are designed for, and what linear regression cannot exploit.
3. **The model has no borrowed crutch** — without `index`, the RMSE is 15.72. This is the honest performance of numeric audio features alone, and it still outperforms the linear baseline by 28.8%.
4. **The feature ceiling is real and is the audio ceiling** — not partially an artifact of genre-ordered row numbers.
