# Best vs Baseline — Week 5

**Date:** 2026-05-11

---

## Comparison Table

| Model | RMSE | R2 | Notes |
|-------|------|----|-------|
| LinearRegression (Week 2 baseline) | 22.0630 | 0.0255 | Frozen baseline; numeric features only |
| RF n_estimators=200 (Week 5 start) | 15.0254 | 0.5480 | Week 4 retained model |
| **RF + log_duration + log_instrumentalness (E7)** | **15.0196** | **0.5484** | **Week 5 best** |

---

## Improvement Over LinearRegression Baseline

- RMSE reduction: 22.0630 → 15.0196
- Absolute improvement: **7.0434 RMSE units**
- Relative improvement: **31.9%**

## Improvement Over Week 5 Starting Point

- RMSE reduction: 15.0254 → 15.0196
- Absolute improvement: **0.0058 RMSE units**
- Relative improvement: **0.04%**

---

## Week 5 Best Model Configuration

```python
Pipeline([
    FunctionTransformer(
        lambda X: X.assign(
            log_duration_ms=np.log1p(X['duration_ms']),
            log_instrumentalness=np.log1p(X['instrumentalness'])
        )
    ),
    RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
])
```

**Features added:** `log_duration_ms`, `log_instrumentalness` (appended to all original numeric columns)

---

## Interpretation

The feature engineering experiments this week produced only marginal improvement over the already-strong RF baseline. The dominant story is that the cumulative gain from Weeks 2–5 is substantial (31.9% over LinearRegression), but the incremental gain within Week 5 is small (0.04%). This confirms the Week 4 hypothesis: the limiting factor is feature ceiling, not model capacity or preprocessing. The numeric audio features have largely been mined for their predictive signal by the RF.
