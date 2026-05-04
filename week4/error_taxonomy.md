# Error Taxonomy — Week 4 Controlled Experiments

## Categories

### 1. Signal Failure
**Definition:** The model fails to learn meaningful patterns from the data — RMSE does not improve beyond a naive baseline, or improvements are negligibly small despite model changes.

**Observed in this experiment:** Partially. The RMSE reduction across the full n_estimators range (50 → 300) was only 0.181 units (15.1752 → 14.9942). Each doubling of trees yields diminishing marginal returns: the 50→100 jump saved 0.1038 RMSE, while the 200→300 jump saved only 0.0312. The model appears to be approaching a signal ceiling given the current feature set.

**Risk level:** Medium. The plateau suggests the numeric-only feature set may be insufficient to explain popularity variance, not that the model class is wrong.

---

### 2. Code Instability
**Definition:** The pipeline crashes, produces NaN outputs, or returns results that cannot be trusted due to bugs or environment issues.

**Observed in this experiment:** None. All 4 runs completed without errors. Outputs were deterministic and reproducible (random_state=42 fixed).

**Risk level:** Low.

---

### 3. Evaluation Leakage
**Definition:** Validation or test set information contaminates training — e.g., fitting a scaler on all data before splitting, or using the test set to select hyperparameters.

**Observed in this experiment:** None. The split is performed inside run.py which was not modified. No preprocessing was applied before the split. The test set was never inspected.

**Risk level:** Low. The frozen run.py guards against this category.

---

### 4. Agent Misbehavior
**Definition:** The agent modifies frozen files, changes the evaluation metric, alters the split, or changes more than the intended controlled variable.

**Observed in this experiment:** None. Only model.py was modified, and only the n_estimators parameter was changed between runs. All other parameters (random_state=42, n_jobs=-1, model family, feature set) were held fixed.

**Risk level:** Low. Controlled experiment constraints were respected.

---

## Summary Table

| Category           | Observed? | Severity |
|--------------------|-----------|----------|
| Signal failure     | Partial   | Medium   |
| Code instability   | No        | Low      |
| Evaluation leakage | No        | Low      |
| Agent misbehavior  | No        | Low      |
