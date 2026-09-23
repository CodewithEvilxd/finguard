from typing import Any, Dict, List, Tuple


class RuleEngine:
    def __init__(self, version: str = "v1.0"):
        self.version = version

    def evaluate(self, transaction: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
        amount = float(transaction.get("amount", 0.0))
        tx_type = str(transaction.get("transaction_type", "")).lower()
        country = str(transaction.get("country", "US")).upper()

        rule_score = 0.0
        findings = []

        # Rule 1: High Single Transaction Amount
        if amount >= 10000.0:
            contribution = 35.0 if amount < 50000.0 else 50.0
            rule_score += contribution
            findings.append({
                "rule_id": "RULE_HIGH_AMOUNT",
                "name": "High Single Amount Threshold",
                "contribution": contribution,
                "description": f"Transaction amount ${amount:,.2f} exceeds threshold.",
            })

        # Rule 2: Foreign Wire Transfer
        if tx_type == "wire" and country not in {"US", "CA", "GB"}:
            rule_score += 40.0
            findings.append({
                "rule_id": "RULE_FOREIGN_WIRE",
                "name": "Cross-Border Wire Transfer",
                "contribution": 40.0,
                "description": f"Wire transfer routed to unverified international destination ({country}).",
            })

        # Rule 3: High-Value Night Transaction
        channel = str(transaction.get("channel", "")).lower()
        if channel == "web" and amount > 5000.0 and tx_type in {"wire", "transfer"}:
            rule_score += 15.0
            findings.append({
                "rule_id": "RULE_DIGITAL_OUTFLOW",
                "name": "High Value Digital Outflow",
                "contribution": 15.0,
                "description": f"Substantial online funds outflow via {tx_type}.",
            })

        capped_rule_score = min(rule_score, 100.0)
        return capped_rule_score, findings


rule_engine = RuleEngine()
