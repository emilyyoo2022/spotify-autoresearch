# Spotify Popularity Prediction — AutoResearch Project

## Project Overview

This project investigates whether Spotify track popularity can be predicted from numeric audio features alone, using an automated research workflow. The work was conducted as part of an AutoResearch project spanning multiple weeks of model development, experimentation, and analysis.

## Research Question

Can Spotify track popularity be predicted from numeric audio features, and what are the practical limits of audio-only prediction?

## Final Results

| Split | Model | RMSE | R² |
|---|---|---|---|
| Validation | Random Forest (final, artifact-free) | 15.7187 | — |
| **Held-out test set** | **Random Forest (final, artifact-free)** | **15.7636** | **0.4965** |
| Baseline | Linear Regression | 22.0630 | 0.026 |

The final model achieved a **28.5% reduction in prediction error** over the linear baseline on the held-out test set.

**Test set protocol:** The held-out test set was opened exactly once, after the model was fully locked following Week 6 analysis. No tuning or experimentation was performed after observing the test result. The near-identical validation RMSE (15.7187) and test RMSE (15.7636) — a gap of 0.0449 (0.3%) — confirm that the result is stable and that no overfitting to the validation set occurred during development.

Error was highest in the high-popularity bucket (RMSE: 28.48), where audio features are least predictive.

**Main conclusion:** Audio features provide meaningful signal for popularity prediction, but a feature ceiling exists. Contextual factors — playlist placement, artist reputation, release timing — are not captured in audio data and account for the residual error.

## Repository Structure

```
week3/          Early exploration and data analysis
week4/          Feature engineering and initial model experiments
week5/          Hyperparameter tuning and cross-validation
week6/          Bucket analysis and error characterization
final_deliverables/   Final report, slides, results, and reflection
```

## Running the Code

```bash
pip install -r requirements.txt
python run.py
```

## Final Deliverables

All final outputs are in `final_deliverables/`:

- `final_report.pdf` — Full written report
- `final_presentation_slides.pptx` — Presentation deck
- `final_results_table.md` — Summary of all model results
- `reflection_memo.md` — Reflection on the research process
- `full_experiment_record.md` — Complete log of experiments and findings
