# The Limits of Audio-Only Popularity Prediction: An AutoResearch Investigation of Spotify Track Popularity

**Emily Yoo**
AutoResearch Program, Weeks 2–6

---

## Abstract

This paper presents a six-week autonomous research study on Spotify popularity prediction using numeric audio features. Starting from a LinearRegression baseline (RMSE 22.06, R² = 0.026), the project demonstrates that tree-based ensemble models — specifically RandomForestRegressor — dramatically outperform linear models (RMSE 15.02, R² = 0.548), a 31.9% relative improvement. However, the central finding is not the performance gain itself but the speed at which further progress halts: subsequent feature engineering, hyperparameter tuning, and alternative model experiments produced only marginal improvements beyond the initial Random Forest gain.. A popularity bucket analysis explains why. The model performs adequately on medium-popularity tracks (RMSE 11.53) but fails severely on high-popularity tracks (RMSE 28.48, systematic bias −23.26), because the factors that elevate a song to breakout popularity — artist reputation, playlist placement, and release context — are entirely absent from the numeric audio feature set. A feature-bucket error analysis confirms that the failure is localized to popularity-outcome space, not audio-feature space: slicing by danceability, energy, or tempo produces at most a 3.1-unit RMSE spread with near-zero bias, while slicing by popularity bucket produces a 15.2-unit spread and a 33.9-unit bias swing. The project's primary contribution is characterizing this information ceiling precisely and demonstrating that it is not addressable through model selection, hyperparameter tuning, or preprocessing alone.

---

## 1. Introduction

Music popularity is a natural target for machine learning: it is a numeric outcome associated with structured, measurable audio properties, and Spotify exposes those properties through its audio analysis API. The intuition that a song's sound — its energy, danceability, tempo, and acousticness — should predict how popular it becomes is plausible and has motivated several prior studies. The harder question is not whether audio features predict popularity, but how well, for whom, and what the ceiling is.

This project investigates that question through a constrained, reproducible experiment. The dataset is a fixed 114,000-track Spotify corpus with 13 numeric audio features and a popularity score from 0 to 100. The evaluation metric is validation RMSE, computed on a held-out split with a frozen random seed. The experimental protocol is a structured keep/discard/crash loop: each modification to the model or preprocessing pipeline is retained only if it improves validation RMSE; otherwise it is reverted. No external data, categorical features, or neural architectures are introduced.

Over six weeks and 16 experiments, this project arrives at a clear and interpretable result: RandomForest with minimal log-transform preprocessing is the best achievable model from this feature set, and its accuracy plateaus sharply. The theoretical reason for the plateau is identifiable and quantifiable: the numeric audio features do not contain the information needed to predict breakout popularity. The project's contribution is making this ceiling explicit — locating it in popularity-outcome space, ruling out audio-feature-space explanations, and quantifying how severely it affects high-popularity track prediction.

---

## 2. Research Question

**Can Spotify track popularity be predicted from numeric audio features, and what are the practical limits of audio-only prediction?**

The numeric audio features available are: danceability, energy, loudness, tempo, speechiness, acousticness, instrumentalness, liveness, valence, key, mode, time signature, and duration. The target variable is `popularity`, an integer from 0 to 100.

The sub-questions that structure the analysis are:

1. Do tree-based nonlinear models substantially outperform linear models on this task?
2. Do improvements plateau after the initial model-family switch, and if so, how quickly?
3. Does prediction quality vary by popularity range, and can the failure mode be explained?
4. Is the failure mode localized to the popularity dimension or to specific audio-feature profiles?

---

## 3. Dataset and Methodology

### 3.1 Dataset

The dataset consists of 114,000 Spotify tracks. The target variable `popularity` ranges from 0 to 100 with a right-skewed distribution: the majority of tracks cluster at low-to-medium popularity, and breakout popular tracks (popularity > 67) constitute approximately 6.7% of the dataset (n = 7,600 in the full dataset; n ≈ 1,556 in the validation split).

The train/validation/test split is 60/20/20 with random_state=42, frozen for the duration of the project. The test set is not touched during any experiment. All reported metrics are validation RMSE unless explicitly noted otherwise.

One dataset artifact was identified and validated in Week 6: the `index` column (the CSV's row number, 0–113,999) was included in the raw feature set and achieved the highest RF feature importance at 35.8%. The artifact arose because the CSV is sorted by genre, making row position a noisy genre proxy. Removing `index` raises overall validation RMSE by 0.70 units (from 15.02 to 15.72) but reduces high-popularity bucket RMSE by 3.24 units and redistributes importance evenly across the 8 core audio features. All three project conclusions survive removal. The artifact-free model (RMSE 15.72) is the honest representation of what numeric audio features alone achieve.

### 3.2 Experimental Protocol

Each experiment modifies a single aspect of model.py — model family, a hyperparameter, or a preprocessing step — runs `python3 run.py`, and records the validation RMSE. The decision rule is:

- **Keep**: validation RMSE improves vs. current best → retain the change
- **Discard**: RMSE worsens or is unchanged → revert model.py to previous state
- **Crash**: code fails to run or does not return RMSE → revert and log the failure

The evaluation logic in run.py is frozen. The random_state is fixed at 42 throughout. The dataset is not modified. This protocol ensures that RMSE comparisons across all 16 experiments reflect genuine model changes, not evaluation variation.

---

## 4. AutoResearch Workflow

The project ran across five active weeks of experiments (Weeks 2–6) structured as follows:

**Week 2 (Baseline and First Models):** Established the LinearRegression baseline (RMSE 22.06), confirmed that Ridge regularization (α = 1.0) produced identical RMSE (no overfitting to correct), and introduced RandomForest as the first alternative. The RF immediately reduced RMSE to 15.07.

**Week 3 (RF Confirmation and HistGBR):** Confirmed RF as the retained model family. Tested HistGradientBoosting with default parameters (RMSE 18.45) — discarded. Logged results and began artifact review.

**Week 4 (Controlled n_estimators Experiment):** Systematically varied n_estimators across {50, 100, 200, 300} with all other hyperparameters fixed. Found monotonically improving RMSE (15.18 → 14.99) but sharply diminishing returns: a 6× runtime increase for a 0.5% total RMSE gain. Retained n_estimators = 200 as the cost-performance optimum. This week's controlled comparison produced a clean diagnosis: the feature ceiling, not model capacity, is the limiting factor.

**Week 5 (Autonomous Feature Engineering Block):** Ran 12 experiments across log transforms, interaction features, additional model families, and regularization variants. Kept two changes: log1p(duration_ms) (−0.002 RMSE) and log1p(instrumentalness) (−0.004 RMSE). Discarded 10 changes. The total post-RF gain from the entire week: 0.058 RMSE units.

**Week 6 (Analysis and Validation):** Locked the model. Ran popularity bucket analysis, feature-bucket error analysis, and index artifact validation. No model changes were made. The scope-lock decision formalized the shift from optimization to explanation.

The keep/discard/crash loop ran reliably across all 16 experiments with zero crashes. Every rollback correctly restored the prior baseline.

---

## 5. Experimental Results

### 5.1 Linear Regression Baseline

The LinearRegression model achieves validation RMSE 22.06 and R² = 0.026. The near-zero R² confirms that popularity and audio features are not linearly related in any meaningful sense. Ridge regularization (α = 1.0) produces identical RMSE, indicating the dataset is not overfitting at the linear level — the problem is structural, not statistical.

### 5.2 The Model-Family Switch: Linear to Random Forest

The single most consequential change in the project is the replacement of LinearRegression with RandomForestRegressor (n_estimators = 100, random_state = 42). This reduces validation RMSE from 22.06 to 15.07 — a 7.00-unit absolute improvement and a 31.7% relative reduction. R² jumps from 0.026 to 0.545.

Tree-based splitting captures nonlinear structure that linear models cannot. The popularity–audio relationship exhibits feature interactions and threshold effects that emerge naturally in RF splits but require explicit specification in linear models. This gain is not engineering — it is an architectural choice, and it accounts for 7.00 of the project's total 7.04-unit RMSE improvement.

### 5.3 Hyperparameter Scaling and Diminishing Returns

The controlled n_estimators experiment (Week 4) quantifies the return on model complexity within the RF family:

| n_estimators | Validation RMSE | Δ vs. n=100 | Runtime |
|---|---|---|---|
| 50 | 15.18 | +0.11 | 9.7 s |
| 100 | 15.07 | — | 16.2 s |
| 200 | 15.03 | −0.04 | 32.8 s |
| 300 | 14.99 | −0.077 | 58.5 s |

Increasing from n=100 to n=300 costs 3.6× more compute for a 0.5% RMSE gain. Doubling from n=200 to n=400 would follow the same diminishing curve. The conclusion at the end of Week 4 is unambiguous: the bottleneck is the feature set, not model capacity. n=200 is retained as the operating point.

### 5.4 Feature Engineering Results

Week 5's 12 experiments test log transforms, manual interaction terms, feature dropping, and alternative model families. Three directions are retained; nine are discarded.

**Retained:**
- log1p(duration_ms): −0.002 RMSE. Duration is right-skewed with a sparse high tail; log compression improves linearity of the split criterion.
- log1p(instrumentalness): −0.004 RMSE. Instrumentalness has a mass at zero with a sparse right tail; log compression separates near-zero values more cleanly.

**Discarded:**
- log1p(loudness), log1p(speechiness), log1p(acousticness): +0.003–0.007 RMSE. These features are bounded, not zero-inflated; log compression adds noise rather than resolving distributional skew.
- Interaction terms (danceability×energy, energy×loudness, tempo×danceability): +0.004–0.019 RMSE. RF discovers interactions natively through tree splits; manually engineered products introduce collinear noise.
- HistGradientBoosting (tuned, lr=0.05, max_depth=6, 500 iterations): RMSE 17.75. Sequential boosting underperforms RF on this dataset even after configuration.
- ExtraTreesRegressor: RMSE 15.45. Random split thresholds are inferior to RF's best-split search on this signal pattern.
- RF max_features=0.5 and min_samples_leaf=3: RMSE 15.38 and 15.28. Regularization is not the bottleneck.

The combined gain from all 12 Week 5 experiments: **0.058 RMSE units**. The locked final model is RF (n_estimators=200) with log1p(duration_ms) and log1p(instrumentalness), achieving RMSE 15.02 (with index) or RMSE 15.72 (artifact-free).

**Full ablation summary:**

| Experiment | RMSE | Δ vs. Prior | Decision |
|---|---|---|---|
| LinearRegression (baseline) | 22.06 | — | Frozen baseline |
| Ridge (α=1.0) | 22.06 | 0.000 | Dropped |
| RandomForest (n=100) | 15.07 | −7.00 | **Kept** |
| HistGBR (default) | 18.45 | +3.38 | Dropped |
| RF (n=200, controlled) | 15.03 | −0.04 | **Kept** |
| log1p(duration_ms) | 15.02 | −0.002 | **Kept** |
| log1p(loudness) | 15.03 | +0.003 | Dropped |
| Feature dropping (key, mode, time_sig) | 15.73 | +0.711 | Dropped |
| Interaction terms (×3 experiments) | 15.04–15.06 | +0.004–+0.019 | Dropped |
| log1p(instrumentalness) | **15.02** | −0.004 | **Kept — final best** |
| log1p(speechiness, acousticness) | 15.03 | +0.007 | Dropped |
| HistGBR (tuned, 500 iter) | 17.75 | +2.73 | Dropped |
| RF max_features=0.5 | 15.38 | +0.357 | Dropped |
| ExtraTreesRegressor | 15.45 | +0.432 | Dropped |
| RF min_samples_leaf=3 | 15.28 | +0.260 | Dropped |

### 5.5 Popularity Bucket Analysis

The strongest result of the project emerges from stratifying the validation set by popularity range. Using the artifact-free model (RMSE 15.72):

| Popularity Bucket | N (validation) | RMSE | MAE | Mean Bias |
|---|---|---|---|---|
| Low (0–33) | 11,127 | 15.22 | 11.22 | +10.67 (overpredicts) |
| Medium (34–66) | 10,117 | 13.31 | 9.86 | −8.79 (slight underprediction) |
| High (67–100) | 1,556 | 28.48 | 23.27 | −23.26 (severe underprediction) |

The model performs best on medium-popularity tracks and worst on high-popularity tracks by a factor of 2.1× in RMSE. The high-popularity bucket exhibits systematic underprediction of approximately 23 popularity units — a clear regression-to-the-mean failure. The model can recognize that a high-popularity song sounds good, but it cannot identify which good-sounding songs become hits, because those tracks are differentiated by unobserved factors: artist reputation, label support, editorial playlist placement, and release timing.

The low-popularity bucket shows moderate overprediction (+10.67). This is the symmetric failure: some obscure tracks sound like mainstream pop but remain unknown. The audio features signal quality but not visibility.

### 5.6 Index Artifact Validation

When `index` is included as a feature, the RF assigns it 35.8% importance — higher than any genuine audio feature. Removing it costs 0.70 overall RMSE but produces three important effects:

1. High-popularity bucket RMSE improves from 31.72 to 28.48 (−3.24). The `index` column was providing genre-correlated borrowed signal that partially masked the severity of high-end failure.
2. Feature importances redistribute evenly across the 8 core audio features, each contributing 8–11%. No single audio feature dominates.
3. All three project conclusions survive unchanged. The no-index model (RMSE 15.72) still outperforms the linear baseline by 28.8%, still plateaus immediately, and still shows severe high-popularity bias.

The artifact-free model is the honest measure of what audio features alone achieve. It is reported as the primary result throughout the analysis sections.

---

## 6. Failure Analysis

### 6.1 Feature-Bucket Error Analysis

To determine whether the model's failures arise from misreading audio profiles or from popularity-space regression, the validation errors are stratified by three audio features: danceability, energy, and tempo.

**Danceability:**

| Bucket | RMSE | Bias |
|---|---|---|
| Low (<0.4) | 14.53 | +0.62 |
| Medium (0.4–0.7) | 15.24 | −0.45 |
| High (>0.7) | 17.58 | −0.51 |

Error rises monotonically with danceability. High-danceability tracks are the *hardest* to predict, not the easiest — contrary to the prior expectation that mainstream-sounding tracks would be genre-coded and therefore more predictable. The finding illustrates that audio-feature confidence does not convert to prediction accuracy: the model identifies a track as highly danceable but cannot determine whether it is a chart-topping pop release or an obscure underground electronic track, because both sound identical in the feature space.

**Energy:**

| Bucket | RMSE | Bias |
|---|---|---|
| Low (<0.33) | 15.60 | −0.24 |
| Medium (0.33–0.66) | 15.94 | −0.59 |
| High (>0.66) | 15.61 | −0.10 |

Energy shows essentially no variation across buckets (0.34-unit RMSE span). Despite being an informative RF feature (8.8% importance in the artifact-free model), energy level does not differentiate prediction difficulty. High-energy tracks span every genre and popularity level equally.

**Tempo:**

| Bucket | RMSE | Bias |
|---|---|---|
| Low (<90 BPM) | 15.36 | −0.50 |
| Medium (90–140 BPM) | 16.18 | −0.33 |
| High (>140 BPM) | 14.82 | −0.07 |

Extreme tempos are slightly more predictable than mid-range. The 90–140 BPM range is the most crowded in the spectrum — it spans mainstream pop, hip-hop, rock, and country simultaneously, making the audio signal uninformative about genre and therefore about popularity distribution.

### 6.2 Comparison of Error Structures

| Slicing Dimension | RMSE Span | Bias Span |
|---|---|---|
| Popularity buckets | 13.31 → 28.48 (**15.2 units**) | +10.67 to −23.26 (**33.9 units**) |
| Danceability buckets | 14.53 → 17.58 (3.1 units) | +0.62 to −0.51 (1.1 units) |
| Energy buckets | 15.60 → 15.94 (0.3 units) | −0.24 to −0.59 (0.4 units) |
| Tempo buckets | 14.82 → 16.18 (1.4 units) | −0.07 to −0.50 (0.4 units) |

The contrast is unambiguous. Slicing by popularity produces a 15-unit RMSE swing and a 34-unit bias swing. Slicing by any audio feature produces at most a 3-unit RMSE swing and near-zero bias. The model's systematic failure does not arise from misreading audio profiles; it arises from the absence of information about which songs within any audio profile become popular.

### 6.3 The Index Artifact: A Methodological Failure

The `index` column went undetected as an artifact for five weeks across Weeks 3, 4, and 5. It was the highest-importance feature at 35.8% the entire time. The agent never inspected feature importances during the experiment loop; the artifact was discovered only when Week 6 interpretability analysis began.

This failure has a clear structural cause: the keep/discard/crash rule optimizes RMSE monotonically and has no self-auditing component. A feature that improves RMSE — even through a meaningless proxy correlation — is retained without scrutiny. The fix is procedural: feature importance inspection should be mandatory after initial model training, with any feature exceeding ~20% importance flagged for human review before experiments proceed.

The artifact does not invalidate the project's conclusions — all three survive removal — but it means the project carried a bad feature for five weeks and reported slightly inflated performance numbers as the "best" result.

---

## 7. Reflection on Agent-Guided Research

### 7.1 What the Loop Did Well

The keep/discard/crash loop ran reliably across all 16 experiments with zero crashes and correct rollbacks throughout. The mechanical discipline was sound: every revert restored the correct baseline state, and the logging was consistent.

Diminishing returns were identified and named accurately. After the Week 4 n_estimators sweep showed a 6× runtime increase for a 0.5% RMSE gain, the agent correctly concluded that model capacity was not the bottleneck and moved to feature engineering. This is a meaningful judgment, not an obvious one.

The log-transform criterion was applied correctly. log1p was beneficial exactly for features with heavy zero-inflation and sparse right tails (instrumentalness, duration_ms) and harmful for bounded features with no zero-mass spike (loudness, speechiness, acousticness). The agent articulated this distinction and did not apply the transform indiscriminately.

### 7.2 What the Loop Did Poorly

**The index artifact went undetected for five weeks.** This is the most consequential failure and a structural limitation of pure RMSE optimization without self-auditing.

**Three consecutive failed interaction experiments should have been one.** After danceability×energy (E4) failed, it was already clear that RF discovers interactions natively and does not benefit from manually engineered products. Running energy×loudness (E5) and tempo×danceability (E6) added overhead without adding information. The agent was executing its checklist rather than updating its beliefs.

**The analysis phase started too late.** The bucket analysis — the project's strongest interpretive contribution — was conducted in Week 6. Had it been run after Week 3, the team would have known by Week 4 that the high-popularity failure mode was structural, and could have spent fewer resources on preprocessing experiments that could not address it.

### 7.3 What Required Human Judgment

Three decisions in this project required human intervention that the optimization loop could not make autonomously:

1. **The scope lock.** The Week 6 decision to stop expanding the model search and shift entirely to analysis required judgment about project framing. The agent had reached the correct technical conclusion (feature ceiling) by Week 4 but could not decide when to stop trying and start explaining.

2. **Whether the index artifact invalidated the project.** The discovery raised a genuine scientific question: are the prior results dishonest? The answer — that all conclusions survive removal, and the artifact-free model is the more interpretable result — required judgment about what "honest" means for a constrained experiment.

3. **The program constraints themselves.** The frozen evaluation logic, fixed random seed, and prohibition on external data were human decisions encoded in program.md. These constraints are what make the RMSE comparisons meaningful across 16 experiments. An autonomous loop cannot design its own validity constraints.

### 7.4 Proposed Redesign

Four changes would make the loop substantially more reliable:

1. **Mandatory feature audit before any model training.** Inspect all feature importances after the first RF fit; flag any feature exceeding ~20% importance for human review before proceeding.
2. **Diminishing-returns checkpoints.** After three consecutive experiments on the same axis produce improvements below 0.01 RMSE, declare that axis exhausted and move on.
3. **Interleaved interpretability checks.** Run a popularity bucket analysis after Week 3, not Week 6. Diagnostic runs should be first-class experiments, not optional documentation steps.
4. **Differentiated decision logic.** A single failed HistGBR run with one hyperparameter configuration is weak evidence against the model family. A third failed interaction term is strong evidence against the approach. The flat keep/discard/crash rule should weight evidence by the replaceability of the hypothesis.

---

## 8. Conclusion

This project set out to ask how well Spotify track popularity can be predicted from numeric audio features. The answer is: substantially better than a linear model, but with a hard ceiling that cannot be overcome through model refinement or preprocessing.

The progression from LinearRegression (RMSE 22.06) to RandomForest (RMSE 15.02) accounts for 31.9% of all RMSE improvement. The switch to tree-based nonlinear splitting was the single decisive move; every subsequent experiment across four additional weeks of iteration moved RMSE by a combined 0.06 units. The feature ceiling is real and measurable.

The popularity bucket analysis locates the ceiling precisely. For medium-popularity tracks — the majority of the dataset — the model achieves RMSE 13.31 and near-unbiased predictions. For high-popularity tracks, RMSE is 28.48 with a systematic underprediction bias of 23 popularity units. The factors that turn a well-made song into a breakout hit — artist reputation, playlist placement, label promotion, release timing — are entirely absent from the 13-column numeric feature set. The model cannot find what is not there.

The feature-bucket error analysis rules out the alternative explanation that the model fails because it misreads certain audio profiles. Error is nearly flat and unbiased across danceability, energy, and tempo slices. The 15-unit RMSE gap between the best and worst popularity buckets has no counterpart in audio-feature space, where the largest comparable gap is 3.1 units. The failure is in the popularity dimension, not the audio dimension.

The primary contribution of this project is not the best validation RMSE. It is identifying, characterizing, and explaining the hard limit of audio-only popularity prediction: **numeric audio features describe what a song sounds like; they cannot determine which songs the world hears.**

Closing this gap would require artist-level features (follower counts, prior release history), release-context features (label, editorial playlist status, release date relative to cultural moments), and social engagement signals. These are structurally different from audio features — they describe a song's position in the industry rather than its sonic character. That distinction is what the bucket analysis makes precise, and it is the natural starting point for any future work on this problem.

---

## Summary Statistics

| Metric | Value |
|---|---|
| Linear baseline RMSE | 22.0630 |
| RF first adoption RMSE | 15.0714 |
| Final model RMSE (artifact-free) | 15.7187 |
| Final model RMSE (project best, with index) | 15.0196 |
| Total RMSE improvement vs. baseline | −7.04 units (−31.9%) |
| Improvement from RF adoption alone | −7.00 units (−31.7%) |
| Improvement from all post-RF experiments | −0.04 units (−0.3%) |
| Medium-popularity bucket RMSE (artifact-free) | 13.31 |
| High-popularity bucket RMSE (artifact-free) | 28.48 |
| High-popularity systematic bias | −23.26 popularity units |
| Total experiments run | 16 (Exp 0–4 + E1–E12) |
| Directions retained | 3 (RF adoption, log_duration_ms, log_instrumentalness) |
