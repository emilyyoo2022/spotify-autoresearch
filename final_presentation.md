# Final Presentation — The Limits of Audio-Only Popularity Prediction

**Emily Yoo | AutoResearch Program | Weeks 2–6**
**Target runtime: 5–6 minutes | 8 slides**

---

## Slide 1 — Title

**Title:** The Limits of Audio-Only Popularity Prediction

**Slide text:**
> Can Spotify popularity be predicted from audio features alone?

- Dataset: ~114,000 Spotify tracks
- 16 experiments over 5 weeks
- Baseline RMSE: 22.06 → Final RMSE: 15.72

**Visuals:** None (title slide)

**Speaker notes:**
My project asked whether numeric audio features — things like energy, danceability, and tempo — can predict how popular a song becomes on Spotify. The short answer is: better than a linear model, but with a hard ceiling that no amount of modeling can break through. That ceiling is the real finding.

---

## Slide 2 — Topic → AutoResearch Contract

**Title:** The Contract

**Slide text:**
**Research question:** Can audio features predict popularity, and where does prediction break down?

**Agent instructions:**
- Improve RMSE on each iteration
- Keep changes that help; revert changes that don't
- Record every experiment
- Maintain reproducible results

**Visuals:** None

**Speaker notes:**
The AutoResearch loop had a simple rule: run an experiment, measure validation RMSE, keep it if it improves, discard it if it doesn't. The loop is fully reproducible — frozen train/validation split, fixed random seed, no external data. That discipline is what makes the 16 RMSE numbers comparable to each other.

---

## Slide 3 — Directions Explored

**Title:** What the Loop Explored

**Slide text:**

| Direction | Result |
|---|---|
| Random Forest adoption | Major gain |
| Hyperparameter tuning | Diminishing returns |
| Feature engineering | Minimal gain |
| Alternative model families | Discarded |
| Popularity bucket analysis | Key insight |
| Index artifact validation | Key insight |

**Visuals:** `week5/metric_trajectory.png`

**Speaker notes:**
The trajectory chart shows this cleanly. There is one large step down — the switch to Random Forest — and then the curve flattens. Everything after that first drop produced combined improvement of 0.06 RMSE units across 12 experiments. The loop explored the right directions; it just ran out of signal to exploit.

---

## Slide 4 — Stable Value

**Title:** What Produced Real, Reproducible Value

**Slide text:**

| Model | RMSE |
|---|---|
| Linear Regression (baseline) | 22.06 |
| Random Forest | 15.72 |

**31.9% reduction. One architectural decision.**

- Tree splits capture nonlinear feature interactions
- Reproducible across all runs
- Accounted for 7.00 of the project's total 7.04-unit gain

**Visuals:** `week4/metric_over_time.png`

**Speaker notes:**
The single most important decision in the entire project was switching from Linear Regression to Random Forest. That one change accounts for 99% of the total improvement. Everything else — transforms, hyperparameter tuning, alternative ensembles — moved the needle by a combined 0.06 units. If the loop had stopped after Week 2, the result would have been essentially the same.

---

## Slide 5 — Noise and Failure

**Title:** What Was Tried and Discarded

**Slide text:**

**Discarded (10 of 16 experiments):**
- Interaction terms (×3 experiments) — RF finds interactions natively
- HistGradientBoosting — RMSE 18.45, worse than RF
- ExtraTreesRegressor — RMSE 15.45, inferior to RF
- Additional hyperparameter tuning — 6× runtime for 0.5% gain
- Log transforms on bounded features — added noise

**Combined effect of all discarded work: 0.00 RMSE improvement**

**Visuals:** None

**Speaker notes:**
Documenting failure is as important as documenting success. Three consecutive interaction-term experiments all failed for the same reason — RF already discovers interactions through splits — but the loop ran all three before moving on. That's a structural weakness: the loop executes its checklist rather than updating its beliefs after the first failure. This is one of the clearest limits of the approach.

---

## Slide 6 — Most Important Discovery

**Title:** The Model Fails Where It Matters Most

**Slide text:**

| Popularity Range | RMSE | Bias |
|---|---|---|
| Low (0–33) | 15.22 | +10.67 |
| Medium (34–66) | 13.31 | −8.79 |
| High (67–100) | **28.48** | **−23.26** |

The model systematically underpredicts hits by ~23 popularity points.

**Audio features describe what a song sounds like. They cannot identify which songs the world hears.**

**Visuals:** `week6/error_by_bucket_plot.png`

**Speaker notes:**
This is the central result. The model performs reasonably on the average track but fails dramatically on breakout popular tracks. That's a 2.1× RMSE difference between the medium and high buckets. The high-popularity bucket is where all the interesting prediction happens — and that's exactly where the audio features run out of signal. The missing information is artist reputation, playlist placement, and release context. None of that is in the dataset.

---

## Slide 7 — Limits of the Loop

**Title:** Where the Ceiling Lives

**Slide text:**

**Feature-bucket analysis confirms the failure is not in audio space:**

| Sliced by | RMSE span | Bias span |
|---|---|---|
| Popularity buckets | **15.2 units** | **33.9 units** |
| Danceability | 3.1 units | 1.1 units |
| Energy | 0.3 units | 0.4 units |
| Tempo | 1.4 units | 0.4 units |

**The loop cannot fix what the data does not contain.**

**Visuals:** `week6/feature_bucket_error_plot.png`

**Speaker notes:**
This analysis rules out the alternative explanation — that the model fails because it misreads certain audio profiles. Slicing by any audio feature produces at most 3 units of RMSE variation and near-zero bias. Slicing by popularity produces 15 units of RMSE variation and 34 units of bias swing. The failure is in the popularity dimension, not the audio dimension. No model change, transform, or hyperparameter could have addressed this. The loop hit the ceiling of its own data.

---

## Slide 8 — Reflection and Takeaway

**Title:** What the Loop Can and Cannot Do

**Slide text:**

**Loop strengths:**
- Reliable mechanics: zero crashes, correct rollbacks
- Identified diminishing returns accurately
- Applied log transforms correctly

**Loop limits:**
- Missed an index artifact for 5 weeks (no self-auditing)
- Ran redundant experiments on exhausted directions
- Analysis started too late to redirect effort

**Final takeaway:**
> Improving prediction required understanding the limits of the data, not building more complex models.

**Future work:** Artist features · Playlist placement · Release context

**Visuals:** None

**Speaker notes:**
The loop is good at mechanical discipline and bad at knowing when to stop or what to look at. The index artifact — a CSV row number that acted as a genre proxy — was the highest-importance feature for five weeks because the loop had no self-auditing component. It was only caught when the interpretability analysis ran in Week 6. The fix is procedural: inspect feature importances after the first model fit, run a bucket analysis after Week 3, and build diminishing-returns checkpoints into the loop. The bigger lesson is that the most valuable output of this project was not the RMSE number — it was characterizing exactly why the number cannot get lower.
