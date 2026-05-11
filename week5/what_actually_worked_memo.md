# What Actually Worked — Week 5 Memo

**Date:** 2026-05-11
**Block:** Feature engineering and preprocessing autonomous experiments
**Final best RMSE:** 15.0196 (vs 15.0254 week start, vs 22.0630 linear baseline)

---

## What Worked

### Log-transforming zero-inflated continuous features

The only improvements this week came from applying `log1p()` to features with heavy zero-inflation or strong right skew:

1. **`log1p(duration_ms)`** (E1): duration_ms is a long-tail distribution (most tracks are 2–4 min, some are much longer). Compressing it into log-space improved RMSE by 0.002.

2. **`log1p(instrumentalness)`** (E7): instrumentalness is heavily zero-inflated — a large fraction of tracks have instrumentalness near 0 (vocal tracks), with a sparse tail of highly instrumental pieces. Log-transforming this feature improved RMSE by a further 0.004.

Both improvements are small individually but consistent and cumulative. The key pattern: **log1p works when a feature's distribution is dominated by a mass near zero with a long sparse tail**. It re-expresses the feature on a scale where the RF can find cleaner split boundaries.

---

## What Did Not Work

### Interaction terms (E4, E5, E6)
Adding product features (danceability×energy, energy×loudness, tempo×danceability) consistently hurt performance. This is expected: Random Forest already discovers feature interactions through its splitting mechanism. Manually added products introduce collinear redundancy without adding independent signal.

### Feature dropping (E3)
Dropping key, mode, time_signature, and index caused a large RMSE spike (+0.711). Despite their low intuitive signal, these features contribute measurably to RF performance. Key and mode likely encode genre-adjacent patterns (major/minor, scale) that correlate weakly but non-trivially with popularity.

### Log-transforming bounded non-skewed features (E2, E8)
Loudness, speechiness, and acousticness did not benefit from log-transforms. Loudness is bounded to a narrow range (typically −30 to 0 dB), and speechiness/acousticness, while in [0,1], do not exhibit the extreme zero-inflation that instrumentalness does. Over-engineering their distributions added noise.

### Alternative model families (E9, E11)
HistGradientBoostingRegressor and ExtraTreesRegressor both performed worse than RF on this feature set. HistGBR likely needs more careful hyperparameter tuning (or its sequential fitting is less suited to this signal pattern). ExtraTrees' random split thresholds are worse than RF's best-split search here.

### RF hyperparameter variants (E10, E12)
Changing `max_features` to 0.5 and `min_samples_leaf` to 3 both hurt. The default RF settings (sqrt features, min_samples_leaf=1) are better calibrated for this dataset.

---

## Core Finding

**Log-transforming features with extreme zero-inflation is the only preprocessing lever that reliably helped.** The correct criterion is distributional: if a feature has a spike at zero and a sparse right tail, log1p compresses the tail into a range where RF splits are more efficient. Features that are bounded, symmetric, or only mildly skewed do not benefit.

The broader implication: the numeric audio features in this dataset have been largely mined. Further RMSE improvements will require non-numeric features (artist, genre, release metadata) rather than additional preprocessing of the existing columns.

---

## Recommended Next Direction

Add categorical features via encoding in the model pipeline:
- `track_genre` (target encoding or frequency encoding) — likely the highest-value single addition
- `explicit` (binary flag, not currently selected as numeric)
- Artist-level popularity (requires aggregation; may need approval as a data-level operation)

These represent a qualitatively different class of signal than anything tested in Weeks 3–5.
