from typing import Optional, Tuple


class RiskScorer:
    def __init__(
        self,
        weight_supervised: float = 0.45,
        weight_unsupervised: float = 0.25,
        weight_rules: float = 0.30,
        version: str = "v1.0",
    ):
        self.w_sup = weight_supervised
        self.w_unsup = weight_unsupervised
        self.w_rules = weight_rules
        self.version = version

    def compute_score(
        self,
        fraud_probability: Optional[float],
        anomaly_score: Optional[float],
        rule_score: float,
    ) -> Tuple[float, str]:
        """
        Combines model probabilities, anomaly distances, and rule outputs into a unified [0, 100] score.
        If a component is None (e.g. cold start), remaining components are reweighted proportionally.
        """
        active_weights = 0.0
        weighted_sum = 0.0

        if fraud_probability is not None:
            weighted_sum += self.w_sup * (fraud_probability * 100.0)
            active_weights += self.w_sup

        if anomaly_score is not None:
            weighted_sum += self.w_unsup * (anomaly_score * 100.0)
            active_weights += self.w_unsup

        weighted_sum += self.w_rules * rule_score
        active_weights += self.w_rules

        final_score = weighted_sum / active_weights if active_weights > 0 else rule_score
        
        # When severe deterministic rules fire (e.g. wire laundering / high-value spikes),
        # enforce a rule-based risk floor so that critical policy breaches are not diluted by cold models.
        if rule_score >= 80.0:
            final_score = max(final_score, rule_score * 0.75)
        elif rule_score >= 50.0:
            final_score = max(final_score, rule_score * 0.60)

        final_score = max(0.0, min(100.0, round(final_score, 1)))

        if final_score >= 85.0:
            level = "critical"
        elif final_score >= 65.0:
            level = "high"
        elif final_score >= 35.0:
            level = "medium"
        else:
            level = "low"

        return final_score, level


risk_scorer = RiskScorer()
