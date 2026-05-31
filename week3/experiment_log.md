Experiment 0: Baseline
Model/change: LinearRegression using numeric features only
Validation RMSE: 22.0630
Validation R2: 0.0255
Runtime: 0.65 seconds
Decision: baseline
Notes: This is the frozen Week 2 baseline. Future dry runs will compare against this result.

Experiment 1
Model/change: Ridge Regression (alpha=1.0)
Validation RMSE: 22.0630
Validation R2: 0.0255
Runtime: 0.77 seconds
Decision: discard
Notes:
Ridge regression produced identical performance to the baseline linear regression model.
This suggests that regularization did not meaningfully change the model behavior on this dataset.
Likely reason is that the baseline is already very simple and not overfitting.

Experiment 2
Model/change: Random Forest (n_estimators=100)
Validation RMSE: 15.0714
Validation R2: 0.5453
Runtime: 29.44 seconds
Decision: keep
Notes:
Random Forest significantly improved performance over the baseline linear model.
This suggests that the relationship between audio features and popularity is nonlinear.
Tree-based models are better able to capture these patterns.
The tradeoff is increased runtime compared to the baseline.

Experiment 3
Model/change: HistGradientBoostingRegressor (default settings)
Validation RMSE: 18.4472
Validation R2: 0.3188
Runtime: 3.38 seconds
Decision: discard
Notes:
HistGradientBoosting performed worse than the current best model (Random Forest).
Although it was significantly faster, the higher RMSE indicates lower predictive performance.
This suggests that default boosting parameters are not yet optimized for this dataset.

Experiment 4
Model/change: Random Forest (n_estimators=200)
Validation RMSE: 15.0254
Validation R2: 0.5480
Runtime: 63.11 seconds
Decision: keep
Notes:
Increasing the number of trees from 100 to 200 produced a very small improvement in RMSE (15.0714 → 15.0254).
However, runtime more than doubled, indicating diminishing returns.
This suggests that further increasing model complexity may not be an efficient direction without other changes.