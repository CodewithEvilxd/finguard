# Global Sanctions and OFAC Compliance Regulation (REG-12)

## 1. Statutory Mandate
Federal regulations enforced by the Office of Foreign Assets Control (OFAC) mandate 100% pre-settlement screening of all wire transfers, ACH entries, and real-time payments against Specially Designated Nationals (SDN) and Blocked Persons lists.

## 2. Real-Time Screening Rules
1. **Fuzzy Name Matching**: All beneficiary, originator, and intermediary bank names are scanned against official sanctions databases using Jaro-Winkler and Levenshtein algorithms. Any match scoring >= 85.0% confidence triggers an automatic hard stop.
2. **Prohibited Geographic Corridors**: Direct or correspondent wire transfers originating from or destined for comprehensively sanctioned territories are rejected immediately by automated rule engines.
3. **Secondary Sanctions & Maritime Screening**: Cross-border trade settlements referencing vessels or entities named on the OFAC Non-SDN Menu-Based Sanctions lists must be frozen immediately.

## 3. Escalation and Regulatory Disclosures
- **Immediate Asset Block**: Funds matched to an active SDN profile must be segregated into an interest-bearing blocked funds account within 24 hours.
- **Reporting Requirement**: Formal blocking or rejection reports must be transmitted to OFAC via the compliance portal within 10 business days.
- **Strict Human Oversight**: Machine learning systems and rule engines cannot clear a suspected sanctions match autonomously. Every false-positive disposition requires two-analyst consensus sign-off.
