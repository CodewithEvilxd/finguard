"""
Reproducible Model Evaluation Suite for FinGuard AI.
Calculates imbalanced classification metrics without relying on raw accuracy:
ROC-AUC, PR-AUC, Precision, Recall, F1, Confusion Matrix, FPR, FNR, Precision@K.
"""

import os
import json
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
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
REPORTS_DIR = os.path.join(ROOT_DIR, "ml-backend/training/reports")


def evaluate_binary_classifier(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float = 0.5,
    top_k: int = 100,
) -> Dict[str, Any]:
    """
    Computes rigorous evaluation metrics tailored for severely imbalanced fraud detection.
    """
    y_pred = (y_prob >= threshold).astype(int)

    roc_auc = float(roc_auc_score(y_true, y_prob))
    pr_auc = float(average_precision_score(y_true, y_prob))
    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = [int(v) for v in cm.ravel()]

    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

    # Precision@K
    order = np.argsort(y_prob)[::-1]
    p_at_k = float(y_true[order[:top_k]].mean()) if len(order) >= top_k else 0.0

    return {
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "calibrated_threshold": round(threshold, 4),
        "precision_at_k": {
            f"precision_at_{top_k}": round(p_at_k, 4)
        },
        "confusion_matrix": {
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp
        },
        "false_positive_rate": round(fpr, 4),
        "false_negative_rate": round(fnr, 4),
        "primary_metric_note": "Precision-Recall AUC and Precision@K are primary; raw accuracy is omitted due to extreme class imbalance."
    }


def find_optimal_threshold(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """
    Finds threshold that maximizes F1 score on validation distribution.
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_prob)
    f1_scores = np.divide(
        2 * (precisions * recalls),
        (precisions + recalls),
        out=np.zeros_like(precisions),
        where=(precisions + recalls) != 0,
    )
    best_idx = np.argmax(f1_scores)
    optimal_th = float(thresholds[best_idx]) if best_idx < len(thresholds) else 0.5
    return max(0.15, min(0.85, optimal_th))
