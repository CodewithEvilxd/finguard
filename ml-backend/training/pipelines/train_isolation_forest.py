"""
Isolation Forest Unsupervised Anomaly Detection Training Pipeline.
Trains on normal baseline transaction distribution to learn behavioral deviations.
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
FEATURES_DIR = os.path.join(ROOT_DIR, "ml-backend/data/features")
MODELS_DIR = os.path.join(ROOT_DIR, "ml-backend/models/isolation-forest/v1")
REPORTS_DIR = os.path.join(ROOT_DIR, "ml-backend/training/reports")


def compute_sha256(filepath: str) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def train_and_evaluate_isolation_forest():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    print("Loading feature matrices for Isolation Forest...")
    train_dir = os.path.join(FEATURES_DIR, "train") if os.path.exists(os.path.join(FEATURES_DIR, "train")) else os.path.join(FEATURES_DIR, "training")
    X_train = pd.read_parquet(os.path.join(train_dir, "X_train.parquet"))
    y_train = pd.read_parquet(os.path.join(train_dir, "y_train.parquet"))["isFraud"].values

    X_test = pd.read_parquet(os.path.join(FEATURES_DIR, "test/X_test.parquet"))
    y_test = pd.read_parquet(os.path.join(FEATURES_DIR, "test/y_test.parquet"))["isFraud"].values

    feature_names = list(X_train.columns)

    # Train Isolation Forest primarily on legitimate/normal transactions
    normal_mask = (y_train == 0)
    X_train_normal = X_train[normal_mask]
    print(f"Training Isolation Forest on {len(X_train_normal)} legitimate transactions...")

    params = {
        "n_estimators": 150,
        "max_samples": 0.8,
        "contamination": 0.035,
        "random_state": 42,
        "n_jobs": -1,
    }

    model = IsolationForest(**params)
    model.fit(X_train_normal)

    # Decision function on test set (more negative = more anomalous)
    raw_scores = model.decision_function(X_test)
    
    # Min-max normalization of anomaly scores to [0.0, 1.0] (higher = more anomalous)
    # Using percentile clipping for robust bounds
    p1 = np.percentile(raw_scores, 1)
    p99 = np.percentile(raw_scores, 99)
    clipped = np.clip(raw_scores, p1, p99)
    normalized_anomaly_scores = 1.0 - (clipped - p1) / (p99 - p1 + 1e-6)
    normalized_anomaly_scores = np.round(normalized_anomaly_scores, 4)

    # Evaluate anomaly distribution
    mean_normal_anomaly = float(normalized_anomaly_scores[y_test == 0].mean())
    mean_fraud_anomaly = float(normalized_anomaly_scores[y_test == 1].mean())

    print("\n--- Isolation Forest Anomaly Analysis on Test Set ---")
    print(f"Legitimate Transactions Mean Anomaly Score: {mean_normal_anomaly:.4f}")
    print(f"Fraudulent Transactions Mean Anomaly Score: {mean_fraud_anomaly:.4f}")
    print(f"Anomaly Separation Delta:                   {mean_fraud_anomaly - mean_normal_anomaly:+.4f}")

    # Save Model Artifact
    joblib_path = os.path.join(MODELS_DIR, "model.joblib")
    joblib.dump(model, joblib_path, compress=3)
    model_hash = compute_sha256(joblib_path)
    print(f"\nSaved Isolation Forest model to {joblib_path} (SHA256: {model_hash[:16]}...)")

    # Save Feature Schema
    schema_path = os.path.join(MODELS_DIR, "feature_schema.json")
    schema_info = {
        "model_version": "1.0.0",
        "feature_count": len(feature_names),
        "features": feature_names,
        "score_normalization": {
            "p1": float(p1),
            "p99": float(p99),
            "formula": "1.0 - (clip(raw, p1, p99) - p1) / (p99 - p1)"
        }
    }
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema_info, f, indent=2)

    # Save Metadata
    meta_path = os.path.join(MODELS_DIR, "metadata.json")
    meta_info = {
        "model_id": "finguard-isolation-forest-v1",
        "algorithm": "IsolationForest",
        "version": "1.0.0",
        "model_version": "1.0.0",
        "dataset_identifier": "ieee_cis_kaggle_v1.0.0_100k",
        "preprocessing_version": "1.0.0",
        "feature_schema_version": "1.0.0",
        "training_seed": 42,
        "training_timestamp": datetime.now(timezone.utc).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sha256": model_hash,
        "artifact_checksum": model_hash,
        "training_samples": len(X_train_normal),
        "contamination": params["contamination"],
        "hyperparameters": params,
        "metrics": {
            "mean_normal_anomaly": mean_normal_anomaly,
            "mean_fraud_anomaly": mean_fraud_anomaly,
            "anomaly_separation_delta": mean_fraud_anomaly - mean_normal_anomaly,
        },
        "evaluation_metrics": {
            "mean_normal_anomaly": mean_normal_anomaly,
            "mean_fraud_anomaly": mean_fraud_anomaly,
            "anomaly_separation_delta": mean_fraud_anomaly - mean_normal_anomaly,
        },
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, indent=2)

    # Save Evaluation Report
    report_path = os.path.join(REPORTS_DIR, "isolation_forest_v1_metrics.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, indent=2)
    print(f"Saved evaluation report to {report_path}")

    return meta_info


if __name__ == "__main__":
    train_and_evaluate_isolation_forest()
