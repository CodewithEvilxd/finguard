"""
XGBoost Supervised Fraud Classification Training Pipeline.
Trains, validates, evaluates, and persists production artifacts with metrics and SHAP support.
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
FEATURES_DIR = os.path.join(ROOT_DIR, "ml-backend/data/features")
MODELS_DIR = os.path.join(ROOT_DIR, "ml-backend/models/xgboost/v1")
REPORTS_DIR = os.path.join(ROOT_DIR, "ml-backend/training/reports")


def compute_sha256(filepath: str) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def train_and_evaluate():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    print("Loading feature matrices from ml-backend/data/features/...")
    train_dir = os.path.join(FEATURES_DIR, "train") if os.path.exists(os.path.join(FEATURES_DIR, "train")) else os.path.join(FEATURES_DIR, "training")
    X_train = pd.read_parquet(os.path.join(train_dir, "X_train.parquet"))
    y_train = pd.read_parquet(os.path.join(train_dir, "y_train.parquet"))["isFraud"].values

    X_val = pd.read_parquet(os.path.join(FEATURES_DIR, "validation/X_validation.parquet"))
    y_val = pd.read_parquet(os.path.join(FEATURES_DIR, "validation/y_validation.parquet"))["isFraud"].values

    X_test = pd.read_parquet(os.path.join(FEATURES_DIR, "test/X_test.parquet"))
    y_test = pd.read_parquet(os.path.join(FEATURES_DIR, "test/y_test.parquet"))["isFraud"].values

    feature_names = list(X_train.columns)
    print(f"Features ({len(feature_names)}): {feature_names}")
    print(f"Training set: {len(X_train)} samples, Fraud count: {int(np.sum(y_train))} ({y_train.mean()*100:.2f}%)")

    # Handling Class Imbalance
    neg_count = len(y_train) - np.sum(y_train)
    pos_count = np.sum(y_train)
    scale_pos_weight = float(neg_count / max(1, pos_count))
    print(f"Calculated scale_pos_weight: {scale_pos_weight:.2f}")

    # XGBoost Classifier
    params = {
        "n_estimators": 250,
        "max_depth": 5,
        "learning_rate": 0.05,
        "scale_pos_weight": scale_pos_weight,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "objective": "binary:logistic",
        "eval_metric": ["auc", "aucpr"],
        "random_state": 42,
        "n_jobs": -1,
    }

    print("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(**params)
    model.fit(
        X_train,
        y_train,
        eval_set=[(X_val, y_val)],
        verbose=False,
    )

    # Predictions on Validation Set for Threshold Tuning
    val_probs = model.predict_proba(X_val)[:, 1]
    precisions, recalls, thresholds = precision_recall_curve(y_val, val_probs)
    
    # Avoid divide-by-zero
    f1_scores = np.divide(
        2 * (precisions * recalls),
        (precisions + recalls),
        out=np.zeros_like(precisions),
        where=(precisions + recalls) != 0,
    )
    best_idx = np.argmax(f1_scores)
    optimal_threshold = float(thresholds[best_idx]) if best_idx < len(thresholds) else 0.5
    optimal_threshold = max(0.20, min(0.80, optimal_threshold))
    print(f"Optimal classification threshold (calibrated on Val F1): {optimal_threshold:.4f}")

    # Evaluation on Out-of-Time Test Set
    test_probs = model.predict_proba(X_test)[:, 1]
    test_preds = (test_probs >= optimal_threshold).astype(int)

    roc_auc = float(roc_auc_score(y_test, test_probs))
    pr_auc = float(average_precision_score(y_test, test_probs))
    precision = float(precision_score(y_test, test_preds, zero_division=0))
    recall = float(recall_score(y_test, test_preds, zero_division=0))
    f1 = float(f1_score(y_test, test_preds, zero_division=0))

    cm = confusion_matrix(y_test, test_preds)
    tn, fp, fn, tp = [int(v) for v in cm.ravel()]

    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

    # Precision@K
    order = np.argsort(test_probs)[::-1]
    p_at_100 = float(y_test[order[:100]].mean()) if len(order) >= 100 else 0.0

    print("\n--- Test Set Evaluation Results ---")
    print(f"ROC-AUC:       {roc_auc:.4f}")
    print(f"PR-AUC:        {pr_auc:.4f}")
    print(f"Precision:     {precision:.4f} (at threshold {optimal_threshold:.2f})")
    print(f"Recall:        {recall:.4f}")
    print(f"F1 Score:      {f1:.4f}")
    print(f"Precision@100: {p_at_100:.4f}")
    print(f"Confusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")
    print(f"FPR: {fpr:.4f}, FNR: {fnr:.4f}")

    # Feature Importance
    booster = model.get_booster()
    importance_gain = booster.get_score(importance_type="gain")
    sorted_importance = sorted(importance_gain.items(), key=lambda x: x[1], reverse=True)

    # Save Model Artifacts
    model_json_path = os.path.join(MODELS_DIR, "model.json")
    model.save_model(model_json_path)
    model_hash = compute_sha256(model_json_path)
    print(f"\nSaved XGBoost model to {model_json_path} (SHA256: {model_hash[:16]}...)")

    # Save Feature Schema
    schema_path = os.path.join(MODELS_DIR, "feature_schema.json")
    schema_info = {
        "model_version": "1.0.0",
        "feature_count": len(feature_names),
        "features": feature_names,
        "optimal_threshold": optimal_threshold,
    }
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema_info, f, indent=2)

    # Save Metadata
    meta_path = os.path.join(MODELS_DIR, "metadata.json")
    meta_info = {
        "model_id": "finguard-xgboost-v1",
        "algorithm": "XGBClassifier",
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
        "training_samples": len(X_train),
        "validation_samples": len(X_val),
        "test_samples": len(X_test),
        "scale_pos_weight": scale_pos_weight,
        "hyperparameters": params,
        "calibrated_threshold": optimal_threshold,
        "metrics": {
            "roc_auc": roc_auc,
            "pr_auc": pr_auc,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "precision_at_100": p_at_100,
            "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
            "fpr": fpr,
            "fnr": fnr,
        },
        "evaluation_metrics": {
            "roc_auc": roc_auc,
            "pr_auc": pr_auc,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "precision_at_100": p_at_100,
            "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
            "fpr": fpr,
            "fnr": fnr,
        },
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, indent=2)

    # Save Full Evaluation Report
    report_path = os.path.join(REPORTS_DIR, "xgboost_v1_metrics.json")
    eval_report = {
        **meta_info,
        "top_features_by_gain": sorted_importance[:10],
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(eval_report, f, indent=2)
    print(f"Saved evaluation report to {report_path}")

    return eval_report


if __name__ == "__main__":
    train_and_evaluate()
