# FinGuard AI Demo Runbook

## Demo goal
Show one coherent story rather than every feature: a suspicious transaction enters, the system detects it, explains it, helps investigate it, and records the analyst decision.

## Preparation
1. Start all services.
2. Verify health/readiness endpoints.
3. Load synthetic demo data.
4. Confirm the dashboard loads.
5. Confirm at least one low-risk and one high-risk transaction exist.
6. Confirm the AI assistant has access to approved demo knowledge documents.

## Demo sequence
1. Open `/` and show the product interface.
2. Enter `/demo`.
3. Open the risk dashboard.
4. Submit or simulate a suspicious transaction.
5. Show the new alert.
6. Open the alert and show the unified risk score.
7. Expand “Why flagged?” and show top factors.
8. Open related account activity.
9. Ask the investigation assistant why the alert was produced.
10. Show retrieved evidence/source references.
11. Record an analyst decision.
12. Open the audit history and show the recorded action.

## Demo safety
Use only synthetic data. Do not imply connection to a real bank or payment network unless a separately authorized sandbox integration exists.
