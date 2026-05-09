# Tunisia (TN)

Source: https://www.twilio.com/en-us/guidelines/tn/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Tunisia |
| ISO code | The International Organization for Standardization two character representation for the given locale. | TN |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 605 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +216 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | No |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | Yes | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | 18 days | N/A |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | --- | --- |
| Best practices | --- | N/A | --- | Avoid the use of generic Alphanumeric Sender IDs as they tend to be blocked and filtered by mobile operators. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | International Long Code preservation is not supported for Tunisian networks. The Long Code will be overwritten with a generic Alphanumeric Sender ID outside the Twilio platform. | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Tunisia

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Tunisia Phone Number: No
- Tunisia Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

---

## tunisia
| Key | Value |
| --- | --- |
| MCC | 605 |
| Dialing code | 216 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | The only restriction is that to send local traffic, your business must be a registered sender. International traffic GWs are fully dynamic. |
| Service provisioning | 1 day to configure the default account setup, more if it's a specific setup, could also depend on the supplier. |
| Sender availability | For local traffic registered alpha-numeric senders (alphas) are allowed. International traffic is fully dynamic. |
| Sender provisioning | The average sender registration process time depends solely on network providers. Currently it is under 3 days (local SMS termination). |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | A2P SMS traffic is divided into local and international. Sender registration is mandatory only for local traffic. (Generic senders are not allowed, traffic with cryptocurrency, SPAM is not allowed) Sender registration for international traffic is not needed. There isn't a separation of transactional and promotional traffic. |
| Country restrictions | Gambling and adult traffic is forbidden. There are no specific rules and regulations for promotional SMS traffic. |
| Country recommendations | No specific recommendations. |