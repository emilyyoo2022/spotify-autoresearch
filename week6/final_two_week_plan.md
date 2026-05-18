# Final Two-Week Plan — Weeks 6 and 7

**Date:** 2026-05-18
**Project state:** Scientific analysis complete. Story locked. All Week 6 deliverables generated.

---

## Week 6 — Scope Lock and Final Analysis (COMPLETE)

### Deliverables

- [x] Locked project direction and main claim (program.md updated)
- [x] Ran popularity bucket analysis using best retained model
- [x] `popularity_bucket_analysis.csv` — per-bucket RMSE, MAE, bias, error distribution stats
- [x] `error_by_bucket_plot.png` — three-panel visualization (RMSE/MAE bars, error violins, track counts)
- [x] `week6_scope_lock_memo.md` — best/worst performance zones and feature ceiling implications
- [x] `final_story.md` — complete project narrative with Revised Project Statement
- [x] `dropped_directions.md` — all dropped directions with explicit rationale
- [x] `ablation_table.md` — full experimental summary across all weeks
- [x] `data_quality_summary.md` — dataset analysis (rows, duplicates, missing values, distribution)
- [x] `feature_importance_summary.md` — RF feature importances with interpretation
- [x] `week6_deliverable_checklist.md` — full artifact audit
- [x] `final_two_week_plan.md` (this document)

### Key finding from bucket analysis

| Bucket | N | RMSE | MAE | Mean Bias |
|--------|---|------|-----|-----------|
| Low (0–33) | 11,127 | 14.16 | 9.48 | +8.99 (overpredicts) |
| Medium (34–66) | 10,117 | **11.53** | **8.36** | −6.84 |
| High (67–100) | 1,556 | **31.72** | **27.86** | −27.85 (severely underpredicts) |

The model regresses to the mean for both extremes. The high-popularity failure (RMSE 31.72, bias −27.85) is the clearest evidence that numeric audio features cannot identify breakout hits.

---

## Week 7 — Polish, Presentation, and Final Report (LOCKED SCOPE)

Week 7 is a communication and presentation week. The scientific work is done. No new experiments, no model changes, no new analysis directions.

### Permitted tasks

**Visual polish**
- Review `error_by_bucket_plot.png` for presentation quality (font sizes, axis labels, title)
- Optionally add a predicted-vs-actual scatter colored by bucket to make the regression-to-the-mean pattern visually direct
- All plots must be 150+ DPI with a clean, consistent color palette

**Final report**
- Synthesize `final_story.md` into a structured report:
  - Abstract (2–3 sentences)
  - Background and motivation
  - Methods (data, model, evaluation)
  - Results: baseline vs. best model
  - Results: bucket analysis
  - Discussion: feature ceiling
  - Conclusion and future directions
- All quantitative claims must be traceable to `experiment_log.md` or `popularity_bucket_analysis.csv`

**Presentation**
- Five key numbers to anchor the presentation:
  1. Baseline RMSE: 22.06
  2. Best model RMSE: 15.02 (−31.9%)
  3. Medium-bucket RMSE: 11.53 (best zone)
  4. High-bucket RMSE: 31.72 (worst zone, 2.7× medium)
  5. High-bucket bias: −27.85 (the model misses hits by ~28 popularity units on average)
- One slide or figure per key finding, not per experiment

**Confirmation checks only**
- Re-run `python3 run.py` once to confirm the best model still produces RMSE 15.0196
- Re-run `python3 week6/analyze_buckets.py` once to confirm bucket numbers are stable
- No new experiments from these runs

### Week 7 artifacts

- [ ] `week7/final_report.md`
- [ ] `week7/presentation_figures/` — polished versions of key plots
- [ ] `week7/abstract.md` — standalone 150-word summary

---

## What Week 7 Must NOT Do

- Run new experiments or modify model.py
- Add new evaluation metrics or redefine popularity buckets
- Reopen any dropped direction
- Introduce new datasets, external APIs, or categorical features
- Add qualifications or hedges that contradict the locked story

The project's scientific work is complete as of Week 6.
