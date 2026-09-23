"""
Native TreeSHAP Explainability Service.
Extracts mathematically exact feature contributions from the trained tree models.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import xgboost as xgb


FEATURE_EXPLANATION_TEMPLATES = {
    "amount_log": "Transaction monetary value deviates from typical baseline",
    "hour_of_day": "Transaction executed during unusual hour of day",
    "day_of_week": "Transaction executed on weekend or outside standard banking window",
    "is_night": "Transaction executed during off-hours night window (00:00 - 05:00)",
    "is_weekend": "Weekend execution pattern",
    "product_code_encoded": "High-risk transaction or wire product category",
    "card4_brand_encoded": "Card network brand characteristics",
    "card6_type_encoded": "Card type funding structure (credit vs debit)",
    "card1_freq": "Uncommon or low-frequency issuing institution profile",
    "addr1_freq": "Billing geographic zone occurrence frequency",
    "is_foreign_corridor": "Destination corridor differs from domestic registration",
    "email_domain_risk": "Email domain risk profile (temporary/anonymous provider)",
    "has_identity": "Digital footprint and device fingerprint telemetry presence",
    "is_mobile_device": "Mobile channel execution telemetry",
    "c1_velocity": "Rapid transaction count acceleration within observation window",
    "d1_recency": "Days elapsed since prior transactional event",
    "v100_masked_signal": "Masked behavioral indicator V100 contributed to the score",
}


class ExplainabilityService:
    def __init__(self, version: str = "shap-v1.0.0"):
        self.version = version

    def explain_with_booster(
        self,
        booster: xgb.Booster,
        feature_vector: np.ndarray,
        feature_names: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Uses native XGBoost TreeSHAP (pred_contribs=True) to extract exact log-odds attributions.
        """
        dmatrix = xgb.DMatrix(feature_vector.reshape(1, -1), feature_names=feature_names)
        contribs = booster.predict(dmatrix, pred_contribs=True)[0]

        # The last element in contribs is the model bias/intercept term
        feature_contribs = contribs[:-1]

        attributions = []
        for name, value, shap_val in zip(feature_names, feature_vector, feature_contribs):
            if abs(shap_val) > 0.001:
                direction = "increases_risk" if shap_val > 0 else "decreases_risk"
                template = FEATURE_EXPLANATION_TEMPLATES.get(
                    name,
                    f"Feature {name} contributed to the score"
                )
                attributions.append({
                    "feature": name,
                    "value": round(float(value), 3),
                    "attribution": round(float(shap_val), 4),
                    "direction": direction,
                    "description": template,
                })

        # Sort by absolute attribution descending
        attributions.sort(key=lambda x: abs(x["attribution"]), reverse=True)
        return attributions[:6]

    def fallback_explain(
        self,
        features: np.ndarray,
        feature_names: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Heuristic fallback if booster artifact is momentarily unreadable.
        """
        baselines = np.array([5.0, 12.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.02, 0.02, 0.0, 0.2, 1.0, 0.0, 1.0, 2.0, 0.1], dtype=np.float32)
        diff = features - baselines[:len(features)]
        attributions = []
        for name, val, d in zip(feature_names, features, diff):
            if abs(d) > 0.05:
                direction = "increases_risk" if d > 0 else "decreases_risk"
                attributions.append({
                    "feature": name,
                    "value": round(float(val), 3),
                    "attribution": round(float(d * 0.1), 4),
                    "direction": direction,
                    "description": FEATURE_EXPLANATION_TEMPLATES.get(name, f"Feature {name} contributed to score"),
                })
        attributions.sort(key=lambda x: abs(x["attribution"]), reverse=True)
        return attributions[:5]


explainer = ExplainabilityService()
