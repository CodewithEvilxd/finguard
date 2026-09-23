"""
Production Hybrid Inference Engine for FinGuard AI.
Integrates trained XGBoost classifier, Isolation Forest anomaly detector,
deterministic rule engine, unified risk scoring, and native TreeSHAP explainability.
"""

import os
import json
import math
import joblib
from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
import xgboost as xgb

from app.features.pipeline import feature_pipeline
from app.risk.rule_engine import rule_engine
from app.risk.scorer import risk_scorer
from app.explainability.shap_explainer import explainer
from app.core.config import ml_settings


class InferenceEngine:
    def __init__(self):
        self.model_version = "finguard-xgboost-v1.0.0"
        self.anomaly_model_version = "finguard-isolation-forest-v1.0.0"
        self.xgb_model: Optional[xgb.Booster] = None
        self.iforest_model: Optional[Any] = None
        self.load_models()

    def load_models(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        xgb_path = os.path.join(base_dir, "models/xgboost/v1/model.json")
        iforest_path = os.path.join(base_dir, "models/isolation-forest/v1/model.joblib")

        # Load XGBoost Booster
        if os.path.exists(xgb_path):
            try:
                booster = xgb.Booster()
                booster.load_model(xgb_path)
                self.xgb_model = booster
            except Exception as e:
                print(f"Warning: Failed to load XGBoost model from {xgb_path}: {e}")

        # Load Isolation Forest
        if os.path.exists(iforest_path):
            try:
                self.iforest_model = joblib.load(iforest_path)
            except Exception as e:
                print(f"Warning: Failed to load Isolation Forest from {iforest_path}: {e}")

    def predict(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Feature Engineering (17 dimensions)
        features = feature_pipeline.transform(transaction)
        feature_names = feature_pipeline.feature_names

        # 2. Supervised Fraud Probability via Trained XGBoost
        if self.xgb_model is not None:
            dmatrix = xgb.DMatrix(features.reshape(1, -1), feature_names=feature_names)
            raw_prob = float(self.xgb_model.predict(dmatrix)[0])
            fraud_prob = round(max(0.001, min(0.999, raw_prob)), 4)
        else:
            # Fallback heuristic calculation
            amount = float(transaction.get("amount", 0.0))
            fraud_prob = round(min(0.95, amount / 100000.0), 3)

        # 3. Anomaly Score via Trained Isolation Forest
        if self.iforest_model is not None:
            feat_df = pd.DataFrame([features], columns=feature_names)
            raw_decision = float(self.iforest_model.decision_function(feat_df)[0])
            # Normalize decision score: lower decision function means higher anomaly
            # Typical decision function is between -0.25 (highly anomalous) and +0.15 (highly normal)
            norm_anomaly = 1.0 - (np.clip(raw_decision, -0.25, 0.15) - (-0.25)) / (0.40)
            anomaly_score = round(float(np.clip(norm_anomaly, 0.01, 0.99)), 4)
        else:
            anomaly_score = round(0.15 if fraud_prob < 0.2 else 0.85, 3)

        # 4. Deterministic Rule Engine Evaluation
        rule_score, rule_findings = rule_engine.evaluate(transaction)

        # 5. Unified Multi-Modal Risk Scoring
        final_risk_score, risk_level = risk_scorer.compute_score(
            fraud_probability=fraud_prob,
            anomaly_score=anomaly_score,
            rule_score=rule_score,
        )

        # 6. Native TreeSHAP Explanations
        if self.xgb_model is not None:
            feature_attributions = explainer.explain_with_booster(
                booster=self.xgb_model,
                feature_vector=features,
                feature_names=feature_names,
            )
        else:
            feature_attributions = explainer.fallback_explain(
                features=features,
                feature_names=feature_names,
            )

        explanation_payload = {
            "top_risk_factors": feature_attributions,
            "rule_findings": rule_findings,
            "scoring_breakdown": {
                "supervised_component": round(fraud_prob * 100.0 * risk_scorer.w_sup, 2),
                "unsupervised_component": round(anomaly_score * 100.0 * risk_scorer.w_unsup, 2),
                "rule_component": round(min(100.0, rule_score) * risk_scorer.w_rules, 2),
                "weights": {
                    "supervised": risk_scorer.w_sup,
                    "unsupervised": risk_scorer.w_unsup,
                    "rules": risk_scorer.w_rules,
                },
            },
            "models_used": {
                "classifier": self.model_version,
                "anomaly_detector": self.anomaly_model_version,
            },
        }

        return {
            "transaction_id": transaction.get("transaction_id"),
            "fraud_probability": fraud_prob,
            "anomaly_score": anomaly_score,
            "rule_score": rule_score,
            "final_risk_score": final_risk_score,
            "risk_level": risk_level,
            "model_version": self.model_version,
            "feature_version": feature_pipeline.version,
            "scoring_version": risk_scorer.version,
            "explanation_payload": json.dumps(explanation_payload),
        }


inference_engine = InferenceEngine()
