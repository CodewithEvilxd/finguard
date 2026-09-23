import pytest
from app.features.pipeline import feature_pipeline
from app.risk.scorer import risk_scorer


def test_feature_pipeline_dimensions():
    sample = {
        "amount": 250.0,
        "transaction_type": "purchase",
        "channel": "web",
        "country": "US",
        "timestamp": "2026-09-22T14:30:00Z",
    }
    vec = feature_pipeline.transform(sample)
    assert len(vec) == len(feature_pipeline.feature_names)
    assert vec[0] > 0.0  # log1p(250) > 0


def test_risk_scorer_boundaries():
    # Cold start (only rule score)
    score1, level1 = risk_scorer.compute_score(None, None, 40.0)
    assert 0.0 <= score1 <= 100.0
    assert level1 == "medium"

    # Extreme high fraud
    score2, level2 = risk_scorer.compute_score(0.99, 0.95, 90.0)
    assert score2 >= 85.0
    assert level2 == "critical"

    # Extreme low fraud
    score3, level3 = risk_scorer.compute_score(0.01, 0.02, 0.0)
    assert score3 < 35.0
    assert level3 == "low"
