import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from src.config import LGBM_PARAMS

try:
    from lightgbm import LGBMClassifier
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False
    from sklearn.ensemble import HistGradientBoostingClassifier

class StackingEnsemble:
    """
    LightGBM (or HistGradientBoosting fallback) + LogisticRegression meta-learner stacking.
    """
    def __init__(self):
        if HAS_LIGHTGBM:
            self.lgbm = LGBMClassifier(**LGBM_PARAMS)
        else:
            self.lgbm = HistGradientBoostingClassifier(
                max_iter=LGBM_PARAMS.get('n_estimators', 100),
                learning_rate=LGBM_PARAMS.get('learning_rate', 0.05),
                max_leaf_nodes=LGBM_PARAMS.get('num_leaves', 31),
                random_state=42
            )
        self.meta_model = LogisticRegression(random_state=42)
        
    def fit(self, features: np.ndarray, labels: np.ndarray, mlp_preds: np.ndarray):
        """
        Train gradient booster on features, then stack with MLP preds.
        features: (N, D)
        labels: (N,)
        mlp_preds: (N,) probabilities or logits
        """
        self.lgbm.fit(features, labels)
        lgbm_preds = self.lgbm.predict_proba(features)[:, 1]
        
        stacked_features = np.column_stack((mlp_preds, lgbm_preds))
        self.meta_model.fit(stacked_features, labels)
        
    def predict(self, features: np.ndarray, mlp_pred: float or np.ndarray) -> np.ndarray:
        """
        Return blended probability.
        """
        if features.ndim == 1:
            features = features.reshape(1, -1)
        lgbm_preds = self.lgbm.predict_proba(features)[:, 1]
        mlp_pred_arr = np.atleast_1d(mlp_pred)
        if len(mlp_pred_arr) != len(lgbm_preds):
            mlp_pred_arr = np.repeat(mlp_pred_arr, len(lgbm_preds))
            
        stacked_features = np.column_stack((mlp_pred_arr, lgbm_preds))
        res = self.meta_model.predict_proba(stacked_features)[:, 1]
        return res[0] if len(res) == 1 else res
        
    def save(self, path: str):
        joblib.dump({
            'lgbm': self.lgbm,
            'meta_model': self.meta_model
        }, path)
        
    def load(self, path: str):
        # Compatibility shim for cross-platform / cross-version unpickling of HistGradientBoostingClassifier
        try:
            import sys
            import sklearn._loss._loss
            sys.modules['_loss'] = sklearn._loss._loss
        except (ImportError, AttributeError):
            pass
        models = joblib.load(path)
        self.lgbm = models['lgbm']
        self.meta_model = models['meta_model']
