Experiment 1
Date: 2026-04-20

Baseline model:
LinearRegression

Metric:
Validation RMSE

What I ran:
python3 run.py

Data split:
60% train / 20% validation / 20% test
Random state fixed at 42

Notes:
Created a reproducible baseline pipeline using numeric Spotify features only.
The final test set is locked and not used during baseline tuning.

Result:
Validation RMSE: 22.0630
Validation R2: 0.0255
Runtime: 0.65 seconds