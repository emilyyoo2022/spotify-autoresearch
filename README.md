Spotify AutoResearch Baseline

Project goal:
Predict Spotify song popularity using Spotify audio features.

Current baseline:
Linear regression using numeric features only.

Validation metric:
RMSE on a fixed validation set.

Data split:
60% train / 20% validation / 20% test
Random state fixed at 42.
The 20% test set is fully held out and will not be accessed during model development or agent iteration.

How to run:
1. Install dependencies:
   pip3 install -r requirements.txt

2. Run baseline:
   python3 run.py

Expected output:
The script prints the number of rows, train/validation/test sizes, validation RMSE, validation R2, and runtime.

Current baseline result:
- Rows: 114000
- Train size: 68400
- Validation size: 22800
- Locked test size: 22800
- Validation RMSE: 22.0630
- Validation R2: 0.0255
- Runtime (seconds): 0.65
