# American Samoa (AS)

Source: https://www.twilio.com/en-us/guidelines/as/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | American Samoa |
| ISO code | The International Organization for Standardization two character representation for the given locale. | AS |
| Region | --- | Oceania |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 544 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +1684 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to ensure they comply with all applicable laws. The following are some general best practices Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Required | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A |
| UCS-2 support | --- | --- | N/A |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A | --- |
| UCS-2 support | --- | --- | N/A | --- |
| Use case restrictions | --- | --- | --- | --- |
| Best practices | --- | --- | --- | --- |

## Phone Numbers & Sender ID: Toll Free

| Field | Description | Toll Free |
| --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | Requires Verification |
| UCS-2 support | --- | Supported |
| Use case restrictions | --- | High-Risk Financial Services Payday Loans Short Term- High Interest Loans Auto Loans Mortgage Loans Student Loans Debt Collection Gambling/SweepstakesStock AlertsCryptocurrency Get Rich Quick Schemes Deceptive Work from Home ProgramsRisk Investment Opportunities Multi-Level Marketing 3rd Party Debt Collection or ConsolidationDebt ReductionCredit Repair Programs Lead Generation Controlled Substances Tobacco Vape Federally Illegal Drugs Pornography Profanity Hate Speech Phishing Fraud Scams Deceptive Marketing Snowshoeing Filter Evasion Fireworks For additional insight into these uses cases, including limitations, and exceptions, visit: Forbidden message categories for SMS and MMS in the US and Canada |
| Best practices | --- | Note: The euro symbol (€) is not supported; avoid using this character in message submission toward American Samoa |

---

### American Samoa

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- American Samoa Phone Number: Yes
- American Samoa Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

---

## american-samoa
| Key | Value |
| --- | --- |
| MCC | 544 |
| Dialing code | 1684 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Before you start sending messages towards American Samoa, contact your dedicated account manager or [Support](mailto:support@infobip.com) because of specific regulations. |
| Service provisioning | 1-3 days for default setup. |
| Sender availability | Alpha, VLN , SC , dynamic. |
| Sender provisioning | Not available |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | Get opt-in consent from each end user before sending any messages, particularly for marketing or other non-essential communications. Only communicate during an end-user’s daytime hours, unless it is urgent. |
| Country restrictions | No spam. |
| Country recommendations | No specific country recommendations. |