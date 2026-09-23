# AML and KYC Red Flags Identification Policy (POL-305)

## 1. Regulatory Context and Scope
Under the Bank Secrecy Act (BSA) and Financial Crimes Enforcement Network (FinCEN) mandates, all covered financial institutions must detect, investigate, and report suspicious activities indicative of money laundering, terrorist financing, and illicit capital flight.

## 2. Mandatory Surveillance Triggers
The FinGuard surveillance engine flags the following transactional typologies under POL-305:

1. **Transaction Structuring (Smurfing)**: Multiple currency deposits or electronic fund transfers structured just below the $10,000 regulatory reporting threshold (e.g., $9,000 to $9,950) executed across a 24-hour to 72-hour window.
2. **Rapid Velocity of High-Value Transfers**: Accounts exhibiting a 300% or greater spike in transaction frequency over a rolling 7-day period compared to baseline historical transaction patterns.
3. **High-Risk Non-Cooperative Jurisdictions**: Inbound or outbound transfers routing through Financial Action Task Force (FATF) blacklisted or greylisted jurisdictions without clear legitimate commercial purpose.
4. **Politically Exposed Persons (PEP) Activity**: Uncharacteristic transfer volume or beneficiary additions linked to PEP profiles or state-owned commercial entities.
5. **Dormant Account Awakening**: Immediate large-scale outward wire activity initiated from accounts that have recorded zero operational transactions for more than 180 calendar days.

## 3. Mandatory Investigator Protocol
- **Immediate Escrow Hold**: Transactions meeting two or more POL-305 triggers must be placed in a provisional hold state pending tier-2 compliance review.
- **Beneficial Ownership Verification**: Analysts must demand verified Ultimate Beneficial Owner (UBO) documentation for corporate accounts before clearing funds.
- **SAR Recommendation**: If the account holder fails to provide verifiable legitimate documentation within 48 hours, a Suspicious Activity Report (SAR) must be drafted in accordance with REG-04.
