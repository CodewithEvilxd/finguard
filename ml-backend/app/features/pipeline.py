"""
Runtime Feature Engineering Pipeline.
Transforms incoming transaction payloads into the exact 17-dimensional feature vector
expected by the trained XGBoost and Isolation Forest models.
"""

import math
from datetime import datetime, timezone
from typing import Any, Dict, List
import numpy as np


class FeaturePipeline:
    def __init__(self, version: str = "1.0.0"):
        self.version = version
        self.feature_names = [
            "amount_log",
            "hour_of_day",
            "day_of_week",
            "is_night",
            "is_weekend",
            "product_code_encoded",
            "card4_brand_encoded",
            "card6_type_encoded",
            "card1_freq",
            "addr1_freq",
            "is_foreign_corridor",
            "email_domain_risk",
            "has_identity",
            "is_mobile_device",
            "c1_velocity",
            "d1_recency",
            "v100_masked_signal",
        ]

    def transform(self, transaction: Dict[str, Any]) -> np.ndarray:
        # 1. Amount Log
        amount = float(transaction.get("amount", transaction.get("TransactionAmt", 0.0)))
        amount_log = math.log1p(max(amount, 0.0))

        # 2. Time & Calendar Features
        timestamp_raw = transaction.get("timestamp")
        dt_val = transaction.get("TransactionDT")

        hour_of_day = 12.0
        day_of_week = 2.0
        is_night = 0.0
        is_weekend = 0.0

        if timestamp_raw:
            try:
                dt = datetime.fromisoformat(str(timestamp_raw).replace("Z", "+00:00"))
                hour_of_day = float(dt.hour)
                day_of_week = float(dt.weekday())
                is_night = 1.0 if (dt.hour >= 23 or dt.hour <= 5) else 0.0
                is_weekend = 1.0 if dt.weekday() >= 5 else 0.0
            except Exception:
                pass
        elif dt_val is not None:
            sec = int(dt_val)
            hour_of_day = float((sec // 3600) % 24)
            day_of_week = float((sec // (3600 * 24)) % 7)
            is_night = 1.0 if (hour_of_day <= 5 or hour_of_day >= 23) else 0.0
            is_weekend = 1.0 if day_of_week >= 5 else 0.0
        elif transaction.get("hour_of_day") is not None:
            hour_of_day = float(transaction.get("hour_of_day", 12))
            is_night = 1.0 if (hour_of_day <= 5 or hour_of_day >= 23) else 0.0
            is_weekend = float(transaction.get("is_weekend", 0))

        # 3. Product Code
        tx_type = str(transaction.get("transaction_type", transaction.get("ProductCD", "W"))).upper()
        product_code_map = {"W": 0.0, "C": 1.0, "R": 2.0, "H": 3.0, "S": 4.0, "WIRE": 1.0, "TRANSFER": 2.0, "PURCHASE": 0.0}
        product_code_encoded = product_code_map.get(tx_type, 0.0)

        # 4. Card Brand and Type
        card4 = str(transaction.get("card4", "visa")).lower()
        card4_map = {"visa": 0.0, "mastercard": 1.0, "discover": 2.0, "american express": 3.0}
        card4_brand_encoded = card4_map.get(card4, 0.0)

        card6 = str(transaction.get("card6", "debit")).lower()
        card6_map = {"debit": 0.0, "credit": 1.0}
        card6_type_encoded = card6_map.get(card6, 0.0)

        # 5. Entity Frequency Baselines
        card1_freq = float(transaction.get("card1_freq", 0.015))
        addr1_freq = float(transaction.get("addr1_freq", 0.020))

        # 6. Foreign Corridor
        is_foreign = float(transaction.get("is_foreign", 0.0))
        if "addr2" in transaction:
            is_foreign = 1.0 if transaction.get("addr2") != 87 else 0.0
        country = str(transaction.get("country", "US")).upper()
        if country not in {"US", "CA", "USA"}:
            is_foreign = 1.0

        # 7. Email Domain Risk
        email = str(transaction.get("email", transaction.get("P_emaildomain", "gmail.com"))).lower()
        if "anonymous" in email or "proton" in email:
            email_domain_risk = 2.0
        elif "hotmail" in email:
            email_domain_risk = 1.0
        elif "yahoo" in email:
            email_domain_risk = 0.5
        elif "corporate" in email or ".gov" in email:
            email_domain_risk = 0.0
        else:
            email_domain_risk = 0.2

        # 8. Device / Identity
        channel = str(transaction.get("channel", "web")).lower()
        has_identity = 1.0 if (transaction.get("device_id") or transaction.get("DeviceInfo") or channel in {"web", "mobile"}) else 0.0
        is_mobile_device = 1.0 if (channel == "mobile" or transaction.get("DeviceType") == "mobile") else 0.0

        # 9. Velocity and Masked Signals
        if "velocity_zscore" in transaction:
            c1_vel = float(transaction["velocity_zscore"])
        elif amount > 25000.0 or is_foreign:
            c1_vel = 4.5
        else:
            c1_vel = float(transaction.get("C1", 1.0))
        c1_velocity = math.log1p(max(c1_vel, 0.0))

        if "d1_recency" in transaction or "D1" in transaction:
            d1_rec = float(transaction.get("d1_recency", transaction.get("D1", 10.0)))
        elif amount > 25000.0 and is_foreign:
            d1_rec = 0.5  # rapid succession on anomalous foreign wires
        else:
            d1_rec = 10.0
        d1_recency = math.log1p(max(d1_rec, 0.0))

        v100_masked_signal = float(transaction.get("V100", 0.85 if (amount > 25000.0 and is_foreign) else 0.15))

        features = [
            amount_log,
            hour_of_day,
            day_of_week,
            is_night,
            is_weekend,
            product_code_encoded,
            card4_brand_encoded,
            card6_type_encoded,
            card1_freq,
            addr1_freq,
            is_foreign,
            email_domain_risk,
            has_identity,
            is_mobile_device,
            c1_velocity,
            d1_recency,
            v100_masked_signal,
        ]

        return np.array(features, dtype=np.float32)


feature_pipeline = FeaturePipeline()
