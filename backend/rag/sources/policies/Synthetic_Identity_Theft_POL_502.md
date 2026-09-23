# Synthetic Identity Fraud Detection Framework (POL-502)

## 1. Regulatory Context
Under the USA PATRIOT Act and FinCEN Customer Due Diligence (CDD) requirements, financial institutions are obligated to establish reasonable belief regarding the true identity of each customer.

## 2. Typology of Synthetic Identity Construction
Synthetic identities are fabricated by combining legitimate Social Security Numbers (often belonging to minors or deceased individuals) with fabricated names, addresses, and birthdates to construct artificial credit histories.

## 3. High-Confidence Detection Signals
1. **SSN Randomization Anomaly**: Social Security Numbers issued after June 25, 2011 paired with credit files alleging trade lines predating the issuance date.
2. **Authorized User Piggybacking**: Rapid inflation of credit limits through paid tradeline leasing without direct kinship with primary account holders.
3. **Multiple Names at Identical Residential Address**: Detection of 4 or more unrelated account holders sharing a single residential address or commercial mail drop.
4. **Dormancy Followed by Bust-Out**: An account remaining largely dormant for 6 to 12 months that suddenly utilizes 95% or more of available credit lines followed by payment defaults.

## 4. Remediation Steps
When synthetic fraud is suspected, the investigator must place the account in "Hold - Identity Verification", freeze outbound withdrawals, and require documentary proof of identity (government passport, physical utility statement, and in-person or certified digital verification).
