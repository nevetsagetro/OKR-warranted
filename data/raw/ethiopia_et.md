# Ethiopia (ET)

Source: https://www.twilio.com/en-us/guidelines/et/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Ethiopia |
| ISO code | The International Organization for Standardization two character representation for the given locale. | ET |
| Region | --- | Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 636 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | 251 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Required |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 10 days | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | Local banking and/or promotional traffic are forbidden. | Local banking and/or promotional traffic are forbidden. |
| Best practices | --- | --- | The ETH-MTN network does not support Dynamic Alphanumeric Sender IDs in Ethiopia. Twilio suggests using a pre-registered alphanumeric Sender ID in Ethiopia |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A | --- |
| UCS-2 support | --- | --- | Supported | --- |
| Use case restrictions | --- | --- | Local banking and/or promotional traffic are forbidden. | --- |
| Best practices | --- | --- | The ETH-MTN network does not support Numeric Sender IDs in Ethiopia. The ETH-MTN network does not support Dynamic Alphanumeric Sender IDs in Ethiopia. Twilio suggests using a pre-registered alphanumeric Sender ID in Ethiopia. | --- |

---

### Ethiopia

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Ethiopia Phone Number: No
- Ethiopia Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

---

## ethiopia
| Key | Value |
| --- | --- |
| MCC | 636 |
| Dialing code | 251 |
| Number portability | No |
| Concatenated message | Standard. |
| Service restrictions | No specific service restrictions apply to sending traffic to Ethiopia. |
| Service provisioning | Sender registration is needed. Estimated time to provision a new sender is 2 working days. |
| Sender availability | Alphanumeric |
| Sender provisioning | Up to 2 working days. |
| Two-way | Yes. Short Codes. |
| Two-way provisioning | Yes. |
| Country regulations | There's traffic segmentation. To send local traffic, the business has to be registered in the country. |
| Country restrictions | Local banking and promotional traffic are forbidden. Promotional messages are not allowed.Local banking traffic is not allowed. SPAM, fraud, etc. is forbidden. |
| Country recommendations |  |