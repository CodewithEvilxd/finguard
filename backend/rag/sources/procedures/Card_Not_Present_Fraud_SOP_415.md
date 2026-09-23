# Card-Not-Present (CNP) Fraud and Velocity Mitigation Protocol (SOP-415)

## 1. Scope and Applicability
This Standard Operating Procedure applies to all payment card surveillance teams monitoring e-commerce, digital wallet, and recurring billing transactions.

## 2. Threshold Triggers and Real-Time Traps
The real-time decision engine monitors the following high-risk indicators:
1. **Rapid Transaction Velocity (C1 Spike)**: More than 5 distinct authorization attempts within a rolling 60-minute window across varying merchant categories.
2. **Device and Identity Mismatch**: Device telemetry indicating foreign IP, Tor exit nodes, or headless browser automation coupled with newly added card details.
3. **Micro-Testing Followed by High-Value Purchase**: A series of low-value authorization attempts ($1.00 - $5.00) followed immediately by an attempt exceeding $2,500.00.
4. **Foreign Corridor Deviation**: Cardholder resident in domestic market transacting with high-risk offshore merchant aggregators without documented travel notices.

## 3. Intervention Protocol
- **Score 60 - 79**: Temporary authorization challenge; trigger step-up multi-factor authentication (MFA) via 3D Secure 2.2.
- **Score >= 80**: Automatic authorization decline, place temporary security freeze on card profile, and create an urgent priority alert for manual investigation.
