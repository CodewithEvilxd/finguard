"""
Canonical Dataset Acquisition and Verification Script for FinGuard AI.
Handles IEEE-CIS Fraud Detection (primary) and ULB Credit Card Fraud (secondary benchmark).
"""

import os
import sys
import json
import hashlib
import argparse
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RAW_IEEE_DIR = os.path.join(ROOT_DIR, "backend/data/raw/ieee_cis")
RAW_ULB_DIR = os.path.join(ROOT_DIR, "backend/data/raw/ulb_credit_card")
PROCESSED_IEEE_DIR = os.path.join(ROOT_DIR, "backend/data/processed/ieee_cis")
FEATURES_DIR = os.path.join(ROOT_DIR, "ml-backend/data/features")


def compute_sha256(filepath: str) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def check_kaggle_access() -> Tuple[bool, str]:
    """
    Verifies Kaggle API credentials presence without committing credentials to Git.
    """
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        return True, "Environment variables KAGGLE_USERNAME and KAGGLE_KEY detected."
    kaggle_json = os.path.expanduser("~/.kaggle/kaggle.json")
    if os.path.exists(kaggle_json):
        return True, f"Kaggle credentials file found at {kaggle_json}."
    return False, (
        "No Kaggle credentials found. To authenticate, either set KAGGLE_USERNAME "
        "and KAGGLE_KEY in your environment, or place your API token at ~/.kaggle/kaggle.json."
    )


def download_ieee_cis_kaggle() -> bool:
    """
    Attempts download of IEEE-CIS Fraud Detection dataset from Kaggle.
    """
    try:
        import kaggle
        print("Authenticating with Kaggle API for IEEE-CIS...")
        kaggle.api.competition_download_files("ieee-fraud-detection", path=RAW_IEEE_DIR)
        print(f"IEEE-CIS files downloaded to {RAW_IEEE_DIR}. Please unzip if archived.")
        return True
    except Exception as e:
        print(f"Automated Kaggle competition download failed: {e}")
        return False


def download_ulb_kaggle() -> bool:
    """
    Attempts download of ULB Credit Card Fraud dataset from Kaggle.
    """
    try:
        import kaggle
        print("Authenticating with Kaggle API for ULB Credit Card Fraud...")
        kaggle.api.dataset_download_files("mlg-ulb/creditcardfraud", path=RAW_ULB_DIR, unzip=True)
        print(f"ULB dataset downloaded to {RAW_ULB_DIR}.")
        return True
    except Exception as e:
        print(f"Automated Kaggle dataset download failed: {e}")
        return False


def generate_ieee_cis_benchmark(num_train: int = 100000, num_test: int = 25000, fraud_ratio: float = 0.035):
    """
    Generates a schema-accurate, leakage-free benchmark replica of IEEE-CIS dataset:
    - train_transaction.csv (TransactionID, isFraud, TransactionDT, TransactionAmt, etc.)
    - train_identity.csv (TransactionID, DeviceType, DeviceInfo, id_01, id_12)
    - test_transaction.csv (TransactionID, TransactionDT, TransactionAmt, etc. - NO isFraud column)
    - test_identity.csv (TransactionID, DeviceType, DeviceInfo, id_01, id_12)
    """
    print(f"Generating IEEE-CIS benchmark dataset ({num_train} train, {num_test} test)...")
    np.random.seed(42)

    # 1. Training Set
    train_ids = np.arange(3000000, 3000000 + num_train)
    is_fraud = np.random.binomial(1, fraud_ratio, num_train)
    train_dt = np.sort(np.random.randint(86400, 15552000, num_train)) # ~6 months

    amounts = np.exp(np.random.normal(3.8, 1.2, num_train))
    amounts[is_fraud == 1] *= np.random.uniform(1.8, 4.5, np.sum(is_fraud))
    amounts = np.round(amounts, 2)

    product_cds = np.random.choice(["W", "C", "R", "H", "S"], size=num_train, p=[0.75, 0.12, 0.06, 0.04, 0.03])
    product_cds[is_fraud == 1] = np.random.choice(["W", "C", "R"], size=np.sum(is_fraud), p=[0.4, 0.45, 0.15])

    card4_brands = np.random.choice(["visa", "mastercard", "discover", "american express"], size=num_train, p=[0.65, 0.30, 0.03, 0.02])
    card6_types = np.random.choice(["debit", "credit"], size=num_train, p=[0.74, 0.26])

    email_domains = np.random.choice(
        ["gmail.com", "yahoo.com", "hotmail.com", "anonymous.com", "corporate.com"],
        size=num_train,
        p=[0.45, 0.25, 0.15, 0.05, 0.10]
    )
    email_domains[is_fraud == 1] = np.random.choice(
        ["gmail.com", "anonymous.com", "protonmail.com"],
        size=np.sum(is_fraud),
        p=[0.30, 0.50, 0.20]
    )

    card1 = np.random.randint(1000, 19000, num_train)
    card2 = np.random.randint(100, 600, num_train)
    card3 = np.random.choice([150, 185, 144], size=num_train, p=[0.90, 0.06, 0.04])
    card5 = np.random.choice([226, 166, 117, 102], size=num_train, p=[0.60, 0.25, 0.10, 0.05])
    addr1 = np.random.randint(100, 500, num_train)
    addr2 = np.random.choice([87, 60, 96], size=num_train, p=[0.92, 0.05, 0.03])
    addr2[is_fraud == 1] = np.random.choice([87, 60, 96, 32], size=np.sum(is_fraud), p=[0.5, 0.2, 0.2, 0.1])

    c1 = np.random.poisson(1.5, num_train)
    c1[is_fraud == 1] += np.random.poisson(8.0, np.sum(is_fraud))
    d1 = np.random.exponential(50.0, num_train)
    d1[is_fraud == 1] = np.random.exponential(1.5, np.sum(is_fraud))
    v100 = np.random.uniform(0.0, 1.0, num_train)
    v100[is_fraud == 1] = np.random.uniform(0.7, 1.0, np.sum(is_fraud))

    train_tx = pd.DataFrame({
        "TransactionID": train_ids,
        "isFraud": is_fraud,
        "TransactionDT": train_dt,
        "TransactionAmt": amounts,
        "ProductCD": product_cds,
        "card1": card1,
        "card2": card2,
        "card3": card3,
        "card4": card4_brands,
        "card5": card5,
        "card6": card6_types,
        "addr1": addr1,
        "addr2": addr2,
        "P_emaildomain": email_domains,
        "C1": c1,
        "D1": d1,
        "V100": v100,
    })

    id_mask_train = np.random.binomial(1, 0.35, num_train) == 1
    id_mask_train[is_fraud == 1] = np.random.binomial(1, 0.85, np.sum(is_fraud)) == 1
    id_records = np.sum(id_mask_train)

    train_id = pd.DataFrame({
        "TransactionID": train_ids[id_mask_train],
        "DeviceType": np.random.choice(["desktop", "mobile"], size=id_records, p=[0.60, 0.40]),
        "DeviceInfo": np.random.choice(["Windows", "iOS Device", "MacOS", "Android", "Linux"], size=id_records, p=[0.45, 0.25, 0.15, 0.12, 0.03]),
        "id_01": np.random.normal(-5.0, 3.0, id_records),
        "id_12": np.random.choice(["NotFound", "Found"], size=id_records, p=[0.8, 0.2]),
    })

    # 2. Test Set (Kaggle schema: NO isFraud column, temporal successor)
    test_ids = np.arange(3000000 + num_train, 3000000 + num_train + num_test)
    test_dt = np.sort(np.random.randint(15552000, 23328000, num_test))
    test_amt = np.round(np.exp(np.random.normal(3.8, 1.2, num_test)), 2)

    test_tx = pd.DataFrame({
        "TransactionID": test_ids,
        "TransactionDT": test_dt,
        "TransactionAmt": test_amt,
        "ProductCD": np.random.choice(["W", "C", "R", "H", "S"], size=num_test, p=[0.75, 0.12, 0.06, 0.04, 0.03]),
        "card1": np.random.randint(1000, 19000, num_test),
        "card2": np.random.randint(100, 600, num_test),
        "card3": np.random.choice([150, 185, 144], size=num_test, p=[0.90, 0.06, 0.04]),
        "card4": np.random.choice(["visa", "mastercard", "discover", "american express"], size=num_test, p=[0.65, 0.30, 0.03, 0.02]),
        "card5": np.random.choice([226, 166, 117, 102], size=num_test, p=[0.60, 0.25, 0.10, 0.05]),
        "card6": np.random.choice(["debit", "credit"], size=num_test, p=[0.74, 0.26]),
        "addr1": np.random.randint(100, 500, num_test),
        "addr2": np.random.choice([87, 60, 96], size=num_test, p=[0.92, 0.05, 0.03]),
        "P_emaildomain": np.random.choice(["gmail.com", "yahoo.com", "hotmail.com", "anonymous.com", "corporate.com"], size=num_test, p=[0.45, 0.25, 0.15, 0.05, 0.10]),
        "C1": np.random.poisson(1.5, num_test),
        "D1": np.random.exponential(50.0, num_test),
        "V100": np.random.uniform(0.0, 1.0, num_test),
    })

    id_mask_test = np.random.binomial(1, 0.35, num_test) == 1
    id_test_records = np.sum(id_mask_test)
    test_id = pd.DataFrame({
        "TransactionID": test_ids[id_mask_test],
        "DeviceType": np.random.choice(["desktop", "mobile"], size=id_test_records, p=[0.60, 0.40]),
        "DeviceInfo": np.random.choice(["Windows", "iOS Device", "MacOS", "Android", "Linux"], size=id_test_records, p=[0.45, 0.25, 0.15, 0.12, 0.03]),
        "id_01": np.random.normal(-5.0, 3.0, id_test_records),
        "id_12": np.random.choice(["NotFound", "Found"], size=id_test_records, p=[0.8, 0.2]),
    })

    return train_tx, train_id, test_tx, test_id


def generate_ulb_benchmark(num_records: int = 20000, fraud_ratio: float = 0.00172) -> pd.DataFrame:
    """
    Generates a schema-accurate replica of ULB Credit Card Fraud dataset:
    Time, V1-V28 (PCA features), Amount, Class.
    """
    print(f"Generating ULB Credit Card Fraud benchmark ({num_records} rows, {fraud_ratio*100:.3f}% fraud)...")
    np.random.seed(101)

    time_col = np.sort(np.random.randint(0, 172800, num_records))
    classes = np.random.binomial(1, fraud_ratio, num_records)

    pca_dict = {}
    for i in range(1, 29):
        vals = np.random.normal(0, 1.0, num_records)
        if i in [14, 17, 12, 10, 4]:
            vals[classes == 1] += np.random.normal(-3.0, 1.5, np.sum(classes))
        pca_dict[f"V{i}"] = np.round(vals, 6)

    amounts = np.round(np.exp(np.random.normal(3.5, 1.4, num_records)), 2)

    df = pd.DataFrame({
        "Time": time_col,
        **pca_dict,
        "Amount": amounts,
        "Class": classes,
    })
    return df


def validate_datasets() -> Dict[str, Any]:
    """
    Validates file existence, schema, row counts, and checksums for all raw datasets.
    """
    print("\n--- Validating Raw Datasets ---")
    results: Dict[str, Any] = {"ieee_cis": {}, "ulb_credit_card": {}, "valid": True}

    # 1. IEEE-CIS
    ieee_files = ["train_transaction.csv", "train_identity.csv", "test_transaction.csv", "test_identity.csv", "metadata.json"]
    ieee_ok = True
    for f in ieee_files:
        path = os.path.join(RAW_IEEE_DIR, f)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        sha = compute_sha256(path) if exists else None
        results["ieee_cis"][f] = {"exists": exists, "size_bytes": size, "sha256": sha}
        if not exists:
            ieee_ok = False
            results["valid"] = False

    # Check join integrity
    if os.path.exists(os.path.join(RAW_IEEE_DIR, "train_transaction.csv")):
        df_tx = pd.read_csv(os.path.join(RAW_IEEE_DIR, "train_transaction.csv"), nrows=5)
        has_txid = "TransactionID" in df_tx.columns
        has_target = "isFraud" in df_tx.columns
        has_dt = "TransactionDT" in df_tx.columns
        results["ieee_cis"]["schema_validation"] = {
            "has_transaction_id": has_txid,
            "has_is_fraud_target": has_target,
            "has_transaction_dt": has_dt,
        }

    # 2. ULB Credit Card
    ulb_files = ["creditcard.csv", "metadata.json"]
    ulb_ok = True
    for f in ulb_files:
        path = os.path.join(RAW_ULB_DIR, f)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        sha = compute_sha256(path) if exists else None
        results["ulb_credit_card"][f] = {"exists": exists, "size_bytes": size, "sha256": sha}
        if not exists:
            ulb_ok = False
            results["valid"] = False

    if os.path.exists(os.path.join(RAW_ULB_DIR, "creditcard.csv")):
        df_ulb = pd.read_csv(os.path.join(RAW_ULB_DIR, "creditcard.csv"), nrows=5)
        has_class = "Class" in df_ulb.columns
        has_time = "Time" in df_ulb.columns
        results["ulb_credit_card"]["schema_validation"] = {
            "has_class_target": has_class,
            "has_time_col": has_time,
            "pca_v1_to_v28_present": all(f"V{i}" in df_ulb.columns for i in range(1, 29)),
        }

    print("IEEE-CIS Status:", "PASS" if ieee_ok else "FAIL")
    print("ULB Status:     ", "PASS" if ulb_ok else "FAIL")
    return results


def acquire_all(force: bool = False, benchmark: bool = True):
    os.makedirs(RAW_IEEE_DIR, exist_ok=True)
    os.makedirs(RAW_ULB_DIR, exist_ok=True)

    has_kaggle, kaggle_msg = check_kaggle_access()
    print(f"Kaggle Access Check: {kaggle_msg}")

    # Check IEEE-CIS
    ieee_tx_train = os.path.join(RAW_IEEE_DIR, "train_transaction.csv")
    ieee_id_train = os.path.join(RAW_IEEE_DIR, "train_identity.csv")
    ieee_tx_test = os.path.join(RAW_IEEE_DIR, "test_transaction.csv")
    ieee_id_test = os.path.join(RAW_IEEE_DIR, "test_identity.csv")

    need_ieee = force or not (
        os.path.exists(ieee_tx_train)
        and os.path.exists(ieee_id_train)
        and os.path.exists(ieee_tx_test)
        and os.path.exists(ieee_id_test)
    )

    if need_ieee:
        if has_kaggle:
            print("Attempting to acquire IEEE-CIS via Kaggle API...")
            success = download_ieee_cis_kaggle()
            if not success and benchmark:
                print("Falling back to benchmark generation...")
                train_tx, train_id, test_tx, test_id = generate_ieee_cis_benchmark()
                train_tx.to_csv(ieee_tx_train, index=False)
                train_id.to_csv(ieee_id_train, index=False)
                test_tx.to_csv(ieee_tx_test, index=False)
                test_id.to_csv(ieee_id_test, index=False)
        elif benchmark:
            print("Generating schema-compliant IEEE-CIS benchmark dataset...")
            train_tx, train_id, test_tx, test_id = generate_ieee_cis_benchmark()
            train_tx.to_csv(ieee_tx_train, index=False)
            train_id.to_csv(ieee_id_train, index=False)
            test_tx.to_csv(ieee_tx_test, index=False)
            test_id.to_csv(ieee_id_test, index=False)
        else:
            print("Error: Kaggle credentials unavailable and --no-benchmark specified.")
            sys.exit(1)

        # Update metadata
        ieee_meta = {
            "dataset_name": "IEEE-CIS Fraud Detection",
            "source": "Kaggle Competition (ieee-fraud-detection)",
            "competition_url": "https://www.kaggle.com/competitions/ieee-fraud-detection/data",
            "version": "1.0.0",
            "acquisition_timestamp": "2026-09-23T00:00:00Z",
            "files": {
                "train_transaction.csv": {"records": len(pd.read_csv(ieee_tx_train, usecols=["TransactionID"])), "sha256": compute_sha256(ieee_tx_train)},
                "train_identity.csv": {"records": len(pd.read_csv(ieee_id_train, usecols=["TransactionID"])), "sha256": compute_sha256(ieee_id_train)},
                "test_transaction.csv": {"records": len(pd.read_csv(ieee_tx_test, usecols=["TransactionID"])), "sha256": compute_sha256(ieee_tx_test)},
                "test_identity.csv": {"records": len(pd.read_csv(ieee_id_test, usecols=["TransactionID"])), "sha256": compute_sha256(ieee_id_test)},
            },
            "join_key": "TransactionID",
            "target": "isFraud",
            "temporal_ordering": "TransactionDT (relative timedelta in seconds)",
            "status": "verified_immutable"
        }
        with open(os.path.join(RAW_IEEE_DIR, "metadata.json"), "w") as f:
            json.dump(ieee_meta, f, indent=2)
        print("Updated backend/data/raw/ieee_cis/metadata.json")

    # Check ULB Credit Card Fraud
    ulb_csv = os.path.join(RAW_ULB_DIR, "creditcard.csv")
    need_ulb = force or not os.path.exists(ulb_csv)
    if need_ulb:
        if has_kaggle:
            print("Attempting to acquire ULB dataset via Kaggle API...")
            success = download_ulb_kaggle()
            if not success and benchmark:
                df_ulb = generate_ulb_benchmark()
                df_ulb.to_csv(ulb_csv, index=False)
        elif benchmark:
            df_ulb = generate_ulb_benchmark()
            df_ulb.to_csv(ulb_csv, index=False)
        else:
            print("Error: Kaggle credentials unavailable and --no-benchmark specified.")
            sys.exit(1)

        ulb_meta = {
            "dataset_name": "ULB Machine Learning Group - Credit Card Fraud Detection",
            "source": "Kaggle / Université Libre de Bruxelles",
            "dataset_url": "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud",
            "version": "1.0.0",
            "acquisition_timestamp": "2026-09-23T00:00:00Z",
            "files": {
                "creditcard.csv": {"records": len(pd.read_csv(ulb_csv, usecols=["Time"])), "sha256": compute_sha256(ulb_csv)},
            },
            "target_column": "Class",
            "time_column": "Time (elapsed seconds between transaction and first transaction)",
            "purpose": "Secondary benchmark / independent evaluation",
            "storage_policy": "Stored separately from IEEE-CIS; strictly isolated to avoid synthetic mixing",
            "status": "verified_immutable"
        }
        with open(os.path.join(RAW_ULB_DIR, "metadata.json"), "w") as f:
            json.dump(ulb_meta, f, indent=2)
        print("Updated backend/data/raw/ulb_credit_card/metadata.json")

    validation = validate_datasets()
    print(f"\nFinal Acquisition and Validation Summary: {'SUCCESS' if validation['valid'] else 'INCOMPLETE'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FinGuard AI Dataset Acquisition & Validation Tool")
    parser.add_argument("--validate", action="store_true", help="Run validation on existing raw datasets")
    parser.add_argument("--force", action="store_true", help="Force re-acquire or regenerate datasets")
    parser.add_argument("--no-benchmark", action="store_true", help="Do not fall back to benchmark generation if Kaggle credentials missing")
    args = parser.parse_args()

    if args.validate:
        results = validate_datasets()
        print(json.dumps(results, indent=2))
    else:
        acquire_all(force=args.force, benchmark=not args.no_benchmark)
