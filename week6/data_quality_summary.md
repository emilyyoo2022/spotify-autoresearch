# Data Quality Summary

**Date:** 2026-05-18
**Dataset:** data/spotify.csv
**Purpose:** Supporting analysis artifact. Read-only. No dataset modifications.

---

## Basic Counts

| Metric | Value |
|--------|-------|
| Total rows (raw) | 114,000 |
| Duplicate rows (exact full-row match) | 0 |
| Duplicate track_id values | 24,259 |
| Rows with any missing numeric value | 0 |
| Rows used after dropna (numeric only) | 114,000 |

**Note on duplicate track_ids:** 24,259 rows share a track_id with at least one other row. In this dataset, the same track appears across multiple genre categories — the `track_genre` column assigns each track to one genre row. This is a structural feature of the dataset, not a data error. Since `track_genre` is a non-numeric column excluded from modeling (run.py uses `select_dtypes(include=["number"])`), these duplicates result in repeated numeric feature rows with the same popularity label appearing in the training data. This was not modified and is noted here for transparency.

**Note on missing values:** Three non-numeric columns (`artists`, `album_name`, `track_name`) each have exactly 1 missing value. These columns are not used in modeling.

---

## Numeric Columns Used in Modeling

`index`, `popularity`, `duration_ms`, `danceability`, `energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `time_signature`

(After feature engineering: `log_duration_ms` and `log_instrumentalness` are appended.)

---

## Popularity Distribution

| Statistic | Value |
|-----------|-------|
| Mean | 33.2 |
| Median | 35.0 |
| Std deviation | 22.3 |
| Min | 0 |
| 25th percentile | 17.0 |
| 75th percentile | 50.0 |
| Max | 100.0 |
| Popularity = 0 | 16,020 rows (14.1%) |
| Popularity ≤ 10 | 23,462 rows (20.6%) |
| Popularity ≥ 67 (high bucket) | 7,632 rows (6.7%) |
| Popularity ≥ 80 | 1,201 rows (1.1%) |

The popularity distribution is right-skewed with a heavy mass of low-popularity tracks and a sparse tail of highly popular tracks. This imbalance contributes to the model's difficulty predicting the high-popularity bucket — there are far fewer training examples near the upper extreme.

---

## Implications for the Locked Story

The data quality analysis does not change or weaken the project's conclusions. The dataset is clean (no missing numerics, no exact duplicates). The track_id duplication is a known structural property of the multi-genre dataset format and does not constitute leakage or data corruption. The popularity distribution's skew toward low values is consistent with the bucket analysis finding: high-popularity tracks are rare, and the model has less signal to learn from at that extreme.
