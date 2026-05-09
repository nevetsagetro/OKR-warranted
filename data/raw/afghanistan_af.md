# Afghanistan (AF)

Source: https://www.twilio.com/en-us/guidelines/af/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Afghanistan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | AF |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 412 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +93 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to ensure they comply with all applicable laws. The following are some general best practices Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not required There is no segregation between International and Domestic Traffic | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Twilio recommends registering an Alpha Sender ID Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 1 week | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | Promotional content is not allowed to be registered | --- |
| Best practices | --- | Please refrain from using generic sender IDs like InfoSMS, INFO, Verify, Notify etc to avoid being blocked by network operators. | Twilio recommends registering an Alpha Sender ID |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | No | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | --- | --- | --- |
| Use case restrictions | --- | --- | Numeric sender IDs are prohibited for Etisalat, MTN and Salaam (Afghan Telecom). Use an alphanumeric sender ID to this network for better deliverability. | --- |
| Best practices | --- | --- | --- | --- |

---

### Afghanistan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Afghanistan Phone Number: Yes (Note: Your sender ID may be changed on AWCC network)
- Afghanistan Short Code: No
- International Phone Number: Yes (Note: Your sender ID may be changed on AWCC network)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: No

Additional Notes : MTN network requires mandatory sender registration. Both local and international numeric formats are allowed

Opt-out Rules : No specific opt-out regulations

---

## afghanistan
| Key | Value |
| --- | --- |
| MCC | 412 |
| Dialing code | 93 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions. |
| Service provisioning | 1 day to configure default account setup, more if it's a specific setup (depending on the client's needs). |
| Sender availability | Alpha sender available on all networks. For numeric senders additional adjustment is needed. Contact your account manager or [Support](mailto:support@infobip.com). |
| Sender provisioning | Alpha sender, immediately. Numeric senders 7-14 days. |
| Two-way | Virtual Long Number. (use case overview needed) |
| Two-way provisioning | It can take up to 30 days. |
| Country regulations | No specific regulations. |
| Country restrictions | No specific restrictions. |
| Country recommendations | No specific recommendations. |