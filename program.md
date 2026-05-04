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