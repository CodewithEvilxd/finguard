# Standard Operating Procedure: SOP-104
## Rapid Multi-Hop Wire Verification

### Scope and Purpose
This document governs compliance protocol when an international wire transfer exceeding $25,000 is initiated from any electronic channel (web, mobile, or open banking API).

### Mandatory Verification Steps
1. **Device Identification**: Verify whether the initiating device fingerprint has previously transacted on the source account within the past 90 days.
2. **Multi-Factor Authentication (MFA)**: If the initiating device is unverified or operates from a non-standard subnet/proxy, confirm that step-up MFA was completed.
3. **Corridor Divergence**: Compare the beneficiary country code against the account holder's registered primary trade corridors. If the corridor is novel, secondary verification via registered phone or authorized representative callback is mandatory.
4. **Hold Protocol**: Initiate a temporary 60-minute settlement pause if the transaction amount exceeds 300% of the account's 30-day moving average single wire size.

### Human Analyst Authority
Autonomous systems are restricted to advisory flagging and automated queue triage. Final approval or irreversible account suspension must be executed exclusively by a credentialed fraud risk analyst.
