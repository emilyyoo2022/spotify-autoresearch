# Dropped Directions — Week 6 Scope Lock

**Date:** 2026-05-18

This document records directions that were considered during the project and explicitly dropped, along with the reason each was set aside. These are deliberate scope decisions that keep the project clean and the story intact. All drops are final.

---

## 1. Continued RF n_estimators Scaling (Beyond 300)

**What it would involve:** Testing n_estimators = 400, 500, or higher; possibly combined with cross-validation.

**Why dropped:** Week 4 ran a full controlled experiment across n_estimators = 50, 100, 200, 300. The marginal gain per additional 100 trees shrank monotonically: −0.10 (50→100), −0.05 (100→200), −0.03 (200→300). Total improvement from 50 to 300 trees was 0.18 RMSE at 6× runtime cost. There is no evidence the curve reverses. Further scaling is not a productive direction.

---

## 2. Aggressive Hyperparameter Tuning

**What it would involve:** Grid search or random search over RF parameters — max_depth, max_features, min_samples_split, min_samples_leaf — possibly with cross-validation.

**Why dropped:** Week 5 tested two RF hyperparameter variants directly: max_features=0.5 (RMSE +0.357) and min_samples_leaf=3 (RMSE +0.260). Both made performance worse. The default RF settings are better calibrated to this dataset than the alternatives tested. The remaining error is structural (missing features), not recoverable by tuning within the model family.

---

## 3. Major Model-Family Exploration

**What it would involve:** XGBoost, LightGBM, CatBoost, Support Vector Regression, or stacking ensembles.

**Why dropped:** HistGradientBoostingRegressor (Week 3, RMSE 18.45) and ExtraTreesRegressor (Week 5, RMSE 15.45) both underperformed the retained RandomForest on this feature set. The week 5 what-actually-worked memo concluded that the limiting factor is feature quality, not model family. Switching to another gradient boosting variant with better defaults might close a fraction of the gap, but this would not change the core story. The project's contribution is identifying the feature ceiling, not finding the single best model.

---

## 4. Neural Networks

**What it would involve:** MLP regressor or a lightweight feedforward network trained on the numeric feature set.

**Why dropped:** Neural networks require either substantially more data or richer input representations than 13 numeric columns to justify their complexity. There is no theoretical reason a feedforward network would outperform an RF on a tabular regression task with this feature count. The program explicitly deferred deep learning, and this decision stands.

---

## 5. External Data and API Integration

**What it would involve:** Augmenting the dataset with additional Spotify tracks via the Spotify API, Billboard chart data, streaming count data, or external popularity proxies.

**Why dropped:** External data integration is a data-level operation that falls outside program constraints (run.py and data/spotify.csv are frozen). It would also change the research question from "what can numeric audio features predict" to "what can a larger or richer dataset predict," which is a different project with different scope.

---

## 6. Large Dataset Expansion

**What it would involve:** Scraping or downloading additional track records to increase training set size.

**Why dropped:** Same reason as external data integration — the dataset is frozen. Additionally, the current dataset has 114,000 rows, which is sufficient to train a well-fitted RandomForest. The remaining error is not attributable to dataset size.

---

## 7. Broad Feature Explosion

**What it would involve:** Polynomial features (degree 2 or 3), all pairwise interaction terms, PCA components, or embedding-based feature representations.

**Why dropped:** Week 5 tested hand-crafted interaction terms (danceability×energy, energy×loudness, tempo×danceability) and found consistent performance degradation — all three hurt RMSE by 0.004–0.019. Random Forest already discovers feature interactions through its splitting mechanism; manually adding products introduces collinear redundancy without independent signal. Polynomial expansion would compound this problem at scale.

---

## 8. Categorical Feature Encoding

**What it would involve:** Including `track_genre`, `explicit`, or artist identity in the model via target encoding, frequency encoding, or binary flags.

**Why dropped:** Adding categorical features would likely produce the largest single improvement available — genre almost certainly explains a substantial share of the remaining variance. However, run.py is frozen to numeric columns only (`select_dtypes(include=["number"])`). Introducing categorical features requires modifying run.py, which cannot be changed. This remains the correct next step for a future unconstrained project.

---

## 9. Changing Evaluation Logic or Switching from RMSE

**What it would involve:** Replacing RMSE with MAE, MAPE, rank correlation (Spearman), or classification-style accuracy metrics as the primary optimization target.

**Why dropped:** Changing the metric would invalidate all cross-week comparisons and break the controlled experiment structure established in Week 2. RMSE is the locked evaluation metric per program spec. MAE is used descriptively in the bucket analysis only, and was not used for any model selection decision.

---

## What Was Not Dropped

The following remain active and final:

- The locked best model: RF n_estimators=200 with log1p(duration_ms) and log1p(instrumentalness), RMSE 15.0196
- The evaluation structure: train/val/test split with random_state=42
- The core claim: tree models significantly outperform linear models, but performance plateaus quickly with numeric-only features
- The bucket analysis: the final targeted analysis showing where the feature ceiling matters most
