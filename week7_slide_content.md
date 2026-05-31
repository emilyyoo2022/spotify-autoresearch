# Slide 1 — Title + Main Claim

## The Limits of Audio-Only Popularity Prediction: An AutoResearch Study

### Main Claim

Audio features can explain what a song sounds like, but they cannot reliably explain which songs become hits.

### Key Numbers

* Dataset: ~114,000 Spotify tracks
* Experiments Run: 16+
* Baseline RMSE: 22.06
* Final Artifact-Free RMSE: 15.72

### Speaker Notes

My original goal was to predict Spotify track popularity using audio features. While I achieved a substantial improvement over the baseline, the most important result became understanding why performance stopped improving and what information was missing from the dataset.

---

# Slide 2 — Topic → AutoResearch Contract

## Research Question

Can Spotify popularity be predicted from numeric audio features alone?

## AutoResearch Contract

The agent was instructed to:

* Improve prediction accuracy (RMSE)
* Record every experiment
* Keep reproducible results
* Compare alternatives systematically
* Retain successful directions and discard failed ones

### Speaker Notes

The project began as a predictive modeling problem. Over time it evolved into an AutoResearch process where the goal was not only to improve RMSE but also to understand which research directions produced stable value and which did not.

---

# Slide 3 — Directions Explored

## Major Directions Explored

| Direction                  | Outcome       |
| -------------------------- | ------------- |
| Random Forest adoption     | Success       |
| Hyperparameter tuning      | Small gains   |
| Feature engineering        | Minimal gains |
| Alternative model families | Failed        |
| Popularity bucket analysis | Major insight |
| Index artifact validation  | Major insight |
| Feature bucket analysis    | Major insight |

### Speaker Notes

The AutoResearch loop explored multiple modeling directions. The agent continuously evaluated whether each change produced meaningful improvement or simply added complexity without value.

---

# Slide 4 — Stable Value

## What Produced Stable, Reproducible Value?

| Model             | RMSE  |
| ----------------- | ----- |
| Linear Regression | 22.06 |
| Random Forest     | 15.72 |

### Stable Findings

* Tree-based models consistently outperformed linear models
* Random Forest produced the largest performance improvement
* Results were reproducible across repeated runs
* Nonlinear relationships mattered

### Speaker Notes

The single biggest improvement came from replacing Linear Regression with Random Forest. This accounted for nearly all meaningful improvement observed during the project.

---

# Slide 5 — Noise and Failure

## What Was Tried and Discarded?

### Discarded Directions

* Additional tree scaling
* Interaction terms
* Alternate ensemble models
* Extensive hyperparameter tuning
* Additional feature engineering

### Why They Were Discarded

* Minimal RMSE improvement
* Increased complexity
* Poor reproducibility
* No meaningful new insight

### Speaker Notes

One of the most important parts of the AutoResearch process was documenting failures. Most later experiments either produced negligible improvements or worsened performance, indicating that the bottleneck was no longer the model architecture.

---

# Slide 6 — Most Important Discovery

## Popularity Bucket Analysis

| Popularity Bucket | RMSE |
| ----------------- | ---- |
| Low               | ~14  |
| Medium            | ~12  |
| High              | ~28  |

### Key Finding

The model systematically underpredicted highly popular tracks.

### Interpretation

The model could identify musical characteristics, but could not identify which songs would become major hits.

### Speaker Notes

This became the central result of the project. The model performed reasonably well on average tracks but failed dramatically on highly popular songs. This suggested the missing signal was not audio-related.

---

# Slide 7 — Validation and Limits

## Index Artifact Validation

A potentially misleading feature (dataset index) appeared important.

After removing it:

* Overall conclusions remained unchanged
* High-popularity prediction actually improved
* The project narrative became stronger

## Feature Bucket Analysis

* Danceability, energy, and tempo produced small error differences
* Popularity produced large error differences

### Speaker Notes

These validation steps increased confidence that the conclusions were real and not artifacts of the dataset or modeling process.

---

# Slide 8 — Reflection and Final Takeaway

## What Did the Agent Do Well?

* Systematic experimentation
* Reproducible logging
* Rapid exploration of alternatives

## What Required Human Judgment?

* Determining when to stop searching
* Interpreting experimental results
* Identifying meaningful findings

## Final Takeaway

Improving prediction accuracy ultimately required understanding the limits of the available information rather than continuing to build more complex models.

### Future Work

* Artist popularity
* Playlist placement
* Release timing
* Social and cultural signals

### Speaker Notes

The project evolved from a prediction task into a study of predictive limits. Audio features explain musical style, but cultural success depends on information that was not present in the dataset.
