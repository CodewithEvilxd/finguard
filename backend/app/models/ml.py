from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid, get_utc_now


class ModelVersion(Base, TimestampMixin):
    __tablename__ = "model_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    version = Column(String(50), unique=True, index=True, nullable=False)
    model_name = Column(String(100), nullable=False)  # xgboost-fraud-v1, isolation-forest-v1
    model_type = Column(String(50), nullable=False)  # supervised, unsupervised, hybrid
    parameters = Column(Text, nullable=True)  # JSON serialized
    metrics = Column(Text, nullable=True)  # JSON serialized
    checksum = Column(String(64), nullable=True)
    is_active = Column(String(20), default="active", nullable=False)

    predictions = relationship("ModelPrediction", back_populates="model_version")


class ModelPrediction(Base, TimestampMixin):
    __tablename__ = "model_predictions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    transaction_id = Column(String(36), ForeignKey("transactions.id"), unique=True, index=True, nullable=False)
    model_version_id = Column(String(36), ForeignKey("model_versions.id"), nullable=True)

    fraud_probability = Column(Float, nullable=True)
    anomaly_score = Column(Float, nullable=True)
    rule_score = Column(Float, nullable=True)
    final_risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)  # low, medium, high, critical

    feature_version = Column(String(50), default="v1.0", nullable=False)
    scoring_version = Column(String(50), default="v1.0", nullable=False)
    model_version_name = Column(String(100), default="finguard-xgboost-v1.0.0", nullable=True)
    explanation_payload = Column(Text, nullable=True)  # JSON serialized SHAP factors and rule matches
    predicted_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)

    transaction = relationship("Transaction", back_populates="prediction")
    model_version = relationship("ModelVersion", back_populates="predictions")

    __table_args__ = (
        Index("idx_predictions_transaction_created", "transaction_id", "created_at"),
    )
