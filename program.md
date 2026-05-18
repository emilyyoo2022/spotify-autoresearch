# AutoResearch Program: Spotify Popularity Prediction

## Goal
Improve prediction of Spotify song popularity by reducing validation RMSE.

## Task
The project predicts Spotify track popularity using the Spotify dataset. The target variable is `popularity`.

## Optimization Target
The agent must optimize validation RMSE. Lower RMSE is better.

## Editable File
The agent may only modify:

model.py

The agent may change:
- model type
- model hyperparameters
- feature preprocessing inside the model pipeline

## Frozen Files
The agent must not modify:
- run.py
- data/spotify.csv
- README.md
- requirements.txt
- experiment_log.md

## Protected Evaluation Logic
The train/validation/test split in run.py must remain fixed.
The random_state must remain 42.
The validation metric must remain RMSE.
The final test set must not be used during iteration.

## Baseline
The baseline is LinearRegression using numeric features only.

## Run Command
Each experiment must be run with:

python3 run.py

## Keep / Discard / Crash Rule
Keep a change if validation RMSE improves compared to the current best.
Discard and revert the change if validation RMSE gets worse or stays meaningfully the same.
Mark a run as crash if the code fails to run or does not return validation RMSE.

## Logging
After each experiment, record:
- experiment number
- model/change attempted
- validation RMSE
- validation R2
- runtime
- decision: keep, discard, or crash
- short note explaining what happened

## Search Ideas
Try simple model changes first:
1. Ridge regression
2. Random forest
3. Gradient boosting
4. HistGradientBoosting
5. Simple preprocessing changes

Do not try deep learning yet.
Do not add external data.
Do not change the target variable.

## Week 4 Controlled Experiment Plan

### Experiment Axis
The experiment axis for this week is the number of trees (n_estimators) in the RandomForestRegressor model.

### Conditions Tested
- n_estimators = 50
- n_estimators = 100
- n_estimators = 200
- n_estimators = 300

### What Is Held Fixed
The following components are held constant across all experiments:
- dataset (data/spotify.csv)
- feature set (numeric features only)
- train/validation/test split
- random_state = 42
- evaluation metric (validation RMSE)
- model family (RandomForestRegressor)

### Logging and Artifacts
The agent may create and update files in the week4/ directory, including:
- experiment_matrix.csv
- metric_over_time.png
- error_taxonomy.md
- failure_analysis_memo.md

The agent may NOT modify:
- run.py
- data/spotify.csv
- evaluation logic

### Goal
The goal of this experiment is to determine how increasing model complexity (via number of trees) affects validation RMSE and runtime, and to identify whether diminishing returns occur.

## Week 5 Autonomous Block Plan

### Goal
Run a real autonomous experiment block focused on feature engineering and preprocessing to improve validation RMSE for Spotify popularity prediction.

### Starting Point
The current best model is RandomForestRegressor with n_estimators=200 or the best retained Random Forest model from Week 4.

### Optimization Target
Minimize validation RMSE.

### Agent May Modify
- model.py
- files inside week5/

### Agent May Not Modify
- run.py
- data/spotify.csv
- train/validation/test split
- target variable
- RMSE evaluation logic
- requirements.txt unless a package is already installed and approved

### Experiment Focus
The agent should test feature engineering and preprocessing changes, such as:
- adding interaction features between numeric audio variables
- using polynomial features cautiously
- scaling or transforming numeric features
- trying feature selection
- testing whether duplicate removal should be proposed as a future data-level experiment, but not modifying the dataset directly

### Rules
Each run must make one interpretable change.
Each run must be logged.
Each run must be labeled keep, discard, or crash.
Changes should be kept only if validation RMSE improves.
If a run worsens performance or crashes, revert to the previous best model.py.

### Required Week 5 Artifacts
The agent should create:
- week5/experiment_log_bundle.csv
- week5/metric_trajectory.png
- week5/keep_discard_crash_summary.md
- week5/best_vs_baseline.md
- week5/what_actually_worked_memo.md

## Week 6 Scope Lock

### Locked Final Direction
The project focuses on understanding where Spotify popularity prediction succeeds and fails using numeric audio features. No new directions, datasets, or model families will be introduced. All remaining work is analysis, polishing, and explanation of existing evidence.

### Main Claim
Tree-based ensemble models significantly outperform linear models, but improvements plateau quickly when relying only on numeric audio features.

### Bucket Analysis Result (Week 6 Final Analysis)
Popularity prediction quality differs sharply by range. The model performs best on medium-popularity tracks (RMSE 11.53) and worst on high-popularity tracks (RMSE 31.72, bias −27.85). This is a regression-to-the-mean effect caused by unobserved features — artist fame, playlist placement, release context — that determine which good-sounding songs become hits.

### Officially Dropped Directions
- continued RF n_estimators scaling beyond 300
- aggressive hyperparameter tuning (grid/random search)
- major model-family exploration (XGBoost, LightGBM, CatBoost, SVR, stacking)
- neural networks
- external data / API integration
- large dataset expansion
- broad feature explosion (polynomial, all pairwise interactions, PCA)
- categorical feature encoding (track_genre, explicit, artist)
- changing evaluation logic or switching from RMSE

### Final Two-Week Plan

Week 6 (complete):
- lock project story and main claim
- run and document popularity bucket analysis
- finalize ablation evidence table
- write dropped directions, final story, and scope-lock memo
- generate supporting artifacts (data quality, feature importances)
- perform deliverable audit

Week 7 (polish and presentation only):
- polish final plots for presentation quality
- assemble final report
- prepare presentation
- run confirmation checks only
- do not reopen model search or introduce new analysis directions

### Future Work Scope
Future work is limited to polishing, validating, and explaining the existing evidence. The scientific analysis is complete. No new experiments, model changes, or dataset modifications are in scope.