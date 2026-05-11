import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.ensemble import RandomForestRegressor


def _engineer_features(X):
    X = pd.DataFrame(X).copy()
    X['log_duration_ms'] = np.log1p(X['duration_ms'])
    X['log_instrumentalness'] = np.log1p(X['instrumentalness'])
    return X


def build_model():
    return Pipeline([
        ('features', FunctionTransformer(_engineer_features, validate=False)),
        ('model', RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))
    ])
