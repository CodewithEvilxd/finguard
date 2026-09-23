"""
FinGuard AI Model Experiment Runner.
Compares candidate algorithms (Logistic Regression, Random Forest, XGBoost)
on standardized out-of-time test partitions.
"""

import os
import json
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
FEATURES_DIR = os.path.join(ROOT_DIR, "ml-backend/data/features")
EXPERIMENTS_DIR = os.path.join(ROOT_DIR, "ml-backend/training/experiments")


def run_experiment_suite():
    os.makedirs(EXPERIMENTS_DIR, exist_ok=True)
    train_dir = os.path.join(FEATURES_DIR, "train") if os.path.exists(os.path.join(FEATURES_DIR, "train")) else os.path.join(FEATURES_DIR, "training")
    
    X_train = pd.read_parquet(os.path.join(train_dir, "X_train.parquet"))
    y_train = pd.read_parquet(os.path.join(train_dir, "y_train.parquet"))["isFraud"].values
    X_test = pd.read_parquet(os.path.join(FEATURES_DIR, "test/X_test.parquet"))
    y_test = pd.read_parquet(os.path.join(FEATURES_DIR, "test/y_test.parquet"))["isFraud"].values

    experiments = []

    # Experiment 1: Logistic Regression Baseline
    print("Evaluating Experiment 001: Logistic Regression Baseline...")
    lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    lr.fit(X_train, y_train)
    lr_probs = lr.predict_proba(X_test)[:, 1]
    experiments.append({
        "experiment_id": "EXP-001-LOGISTIC-REGRESSION",
        "algorithm": "LogisticRegression",
        "role": "linear_baseline",
        "metrics": {
            "roc_auc": round(float(roc_auc_score(y_test, lr_probs)), 4),
            "pr_auc": round(float(average_precision_score(y_test, lr_probs)), 4),
            "f1": round(float(f1_score(y_test, (lr_probs >= 0.5).astype(int))), 4)
        },
        "status": "archived_baseline"
    })

    # Experiment 2: Random Forest Baseline
    print("Evaluating Experiment 002: Random Forest Baseline...")
    rf = RandomForestClassifier(n_estimators=50, max_depth=8, class_weight="balanced", random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_probs = rf.predict_proba(X_test)[:, 1]
    experiments.append({
        "experiment_id": "EXP-002-RANDOM-FOREST",
        "algorithm": "RandomForestClassifier",
        "role": "ensemble_baseline",
        "metrics": {
            "roc_auc": round(float(roc_auc_score(y_test, rf_probs)), 4),
            "pr_auc": round(float(average_precision_score(y_test, rf_probs)), 4),
            "f1": round(float(f1_score(y_test, (rf_probs >= 0.5).astype(int))), 4)
        },
        "status": "archived_baseline"
    })

    # Experiment 3: XGBoost Champion (from saved metrics)
    xgb_report_path = os.path.join(ROOT_DIR, "ml-backend/training/reports/xgboost_v1_metrics.json")
    if os.path.exists(xgb_report_path):
        with open(xgb_report_path, "r", encoding="utf-8") as f:
            xgb_meta = json.load(f)
        experiments.append({
            "experiment_id": "EXP-003-XGBOOST-V1",
            "algorithm": "XGBClassifier",
            "role": "production_champion",
            "metrics": xgb_meta.get("metrics", {}),
            "status": "active_champion"
        })

    manifest = {
        "suite_name": "FinGuard ML Model Experiments",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "dataset": "IEEE-CIS Fraud Detection (Temporal Split)",
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "experiments": experiments
    }

    out_file = os.path.join(EXPERIMENTS_DIR, "experiment_manifest.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Experiments manifest written to {out_file}")
    return manifest


if __name__ == "__main__":
    run_experiment_suite()
