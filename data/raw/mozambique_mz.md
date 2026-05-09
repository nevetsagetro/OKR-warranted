# Mozambique (MZ)

Source: https://www.twilio.com/en-us/guidelines/mz/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Mozambique |
| ISO code | The International Organization for Standardization two character representation for the given locale. | MZ |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 643 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +258 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | SMS sent to Mozambique should contain the brand name or application name in the message body. Any SMS sent to Mozambique that doesn’t contain a brand name or application name may be undelivered or blocked. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not required There is no segregation between International and Domestic Traffic | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Twilio recommends registering an Alpha Sender ID Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 1 week | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | Twilio recommends registering an Alpha Sender ID |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Not Supported | --- |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A | --- |
| UCS-2 support | --- | --- | Supported | --- |
| Use case restrictions | --- | --- | International Longcode Sender ID is not supported for Mozambique Movitel | --- |
| Best practices | --- | --- | Twilio suggests using a pre-registered Alphanumeric Sender ID in Mozambique | --- |

---

### Mozambique

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Mozambique Phone Number: Yes
- Mozambique Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): Yes

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : This market has Local and International traffic segmentation. Local traffic requires sender ID registration

Opt-out Rules : No specific opt-out regulations

---

## mozambique
| Key | Value |
| --- | --- |
| MCC | 643 |
| Dialing code | 258 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is required. Before you start sending any content towards Mozambique for the first time, contact your dedicated account manager or [Support](mailto:support@infobip.com) so they can set up a specific route for you. |
| Service provisioning | Since sender registration is required and obtaining of sender, service provision depends on the time of sender provisioning. |
| Sender availability | Alpha, numeric, Short Code |
| Sender provisioning | Alpha - 20 days Numeric - up to 45 days Short Code - up to 45 days |
| Two-way | Short Codes and alpha senders; depends on the network. |
| Two-way provisioning | 3 months |
| Country regulations | No specific regulations for A2P messaging. |
| Country restrictions | Gambling traffic is allowed. |
| Country recommendations | Even though there are no specific restrictions, note that person-to-person (P2P) traffic is prohibited and will be blocked, as well as traffic with illegal, adult, religious, and political content. |