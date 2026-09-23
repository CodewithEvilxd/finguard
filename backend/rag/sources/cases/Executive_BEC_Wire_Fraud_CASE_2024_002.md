# Case Study: Executive Business Email Compromise and Diverted Vendor Remittance (CASE-2024-002)

## 1. Incident Synopsis
On August 14, 2024, a sophisticated Business Email Compromise (BEC) attack targeted Meridian Infrastructure Corp. Adversaries registered a look-alike domain (`meridian-infrastructre.com`) and spoofed the Chief Financial Officer's identity to issue an urgent wire redirect of $340,000.00 intended for heavy equipment supplier Caterpillar Finance.

## 2. Technical and Behavioral Indicators Observed
1. **Urgency Pretext**: Email demanded immediate payment before 17:00 EDT to avoid contractual penalties, discouraging standard voice verification.
2. **Beneficiary Bank Diversion**: Original domestic correspondent bank in Illinois was substituted with an offshore financial institution in Cyprus.
3. **Session IP Incongruity**: The client corporate portal session initiating the transfer originated from an IP geolocated in Lagos, Nigeria, while the corporate headquarters operated from Denver, Colorado.
4. **SHAP Attribution Dominance**: In the FinGuard risk model, the primary risk drivers were `is_foreign_corridor (+0.42)`, `amount_log (+0.31)`, and `c1_velocity (+0.28)`.

## 3. Investigation Findings and Resolution
The automated FinGuard surveillance engine flagged the transaction at unified risk score 94.2 (Critical Risk). Under SOP-104 Section 2, the wire queue was halted. Out-of-band voice contact with the CFO confirmed the email was illegitimate. No corporate funds were lost.
