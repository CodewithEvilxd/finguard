# Account Takeover Incident Response Protocol (SOP-210)

## 1. Purpose and Objective
Standard Operating Procedure SOP-210 establishes the operational sequence required when an account displays telemetry consistent with credential compromise, session hijacking, or malicious account takeover (ATO).

## 2. Detection Criteria & Technical Signals
Investigations are triggered under SOP-210 upon detection of the following composite indicators:
1. **Unrecognized Device Footprint**: Transaction initiated from a device identifier or browser fingerprint not seen in the preceding 90 days of account history.
2. **Geographical Velocity Impossibility**: Authentication or payment initiation from two distinct geographical locations where travel between the points within the elapsed time interval is physically impossible.
3. **Immediate Beneficiary Addition & Transfer**: Outward transfer executed to a newly registered external beneficiary within 15 minutes of profile modification or password change.
4. **Behavioral Deviation Threshold**: Transaction amount exceeding 4.0 standard deviations from the account holder's rolling 30-day mean transaction magnitude.

## 3. Required Mitigation Steps
- **Step 1 - Automated Session Termination**: Revoke all active authentication tokens, cookies, and OAuth authorizations across all platforms.
- **Step 2 - Temporary Debit Block**: Apply an administrative block on all outgoing settlement rails while permitting inbound deposits.
- **Step 3 - Out-of-Band Controller Contact**: Perform voice or cryptographically signed out-of-band verification with the designated primary corporate contact using registered offline phone numbers.
- **Step 4 - Forensic Evidence Logging**: Export raw HTTP headers, user-agent strings, client IP traces, and ML prediction scores to the immutable audit ledger.
- **Step 5 - Release or Resolution**: An administrative block may only be cleared with written sign-off from a Compliance Officer grade 3 or above.
