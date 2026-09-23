# Risk Surveillance Policy: POL-201
## Unusual Velocity & Geo-IP Deviations

### Objective
Define criteria for detecting automated credential stuffing, session hijacking, and fast-flux proxy laundering across multi-channel consumer and commercial accounts.

### Key Risk Triggers
- **Impossible Travel**: Two or more transactions executed within 30 minutes across geographic jurisdictions separated by greater than 300 statute miles.
- **Subnet Rotation**: More than three unique public IP subnets executing transactions on the same account within a single calendar hour.
- **Bursty Volume**: Transaction frequency accelerating beyond 4.0 standard deviations from the account's historical weekday velocity distribution.

### Remediation Protocol
- Generate an expedited high-priority risk alert in the FinGuard surveillance queue.
- Attach all observed IP addresses, ASN numbers, and device telemetry to the case facts.
- Require analyst sign-off before unfreezing outbound digital channels.
