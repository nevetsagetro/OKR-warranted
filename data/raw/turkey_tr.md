# Turkey (TR)

Source: https://www.twilio.com/en-us/guidelines/tr/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Turkey |
| ISO code | The International Organization for Standardization two character representation for the given locale. | TR |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 286 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +90 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | GSM7 Encoding: 155 characters instead of 160 characters. UCS2 Encoding: 65 characters instead of 70 characters. (In Turkey, messages have an additional 5 characters reserved for operator identifiers, effectively reducing the character limit by 5). |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Effective April 1 2026 companies WITHOUT a local entity in Turkey can no longer send messages with URLs in their content to Turkish numbers. Because Turkish carriers filter traffic with Numeric and unregistered Alphanumeric Sender IDs, be sure to pre-register your Alphanumeric Sender ID to ensure message delivery. Person-to-person (P2P) traffic, as well as content related to gambling, politics, and religion are prohibited. From February 15, 2021 — and until further notice — submission of promotional traffic to Turkey will be prohibited. Please do not submit such traffic as it may result in your messages and your registered Sender ID being blocked. It may also result in financial penalties. Message delivery to M2M numbers is on best-effort basis only. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | P2P, gambling, political, or religious content is prohibited. Unsolicited messages will not be sent to end-users. SMS delivery to the Turkish Republic of Northern Cyprus is not supported. | Sender ID Registration is required in Turkey. Messages sent from unregistered alphanumeric Sender IDs will be delivered on a best effort basis. |
| Best practices | --- | N/A | Twilio suggests using a pre-registered alphanumeric Sender ID in Turkey. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | SMS delivery to the Turkish Republic of Northern Cyprus is not supported. Sender ID Registration is required in Turkey. Messages sent from international longcodes will be delivered on a best effort basis. | N/A |
| Best practices | --- | N/A | Twilio suggests using a pre-registered alphanumeric Sender ID in Turkey. | N/A |

---

### Turkey

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Turkey Phone Number: No
- Turkey Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Mandatory registration required; generic senders not allowed
- Short URLs not supported
- Financial organizations: Letter of Authorization (LOA) required for all sender ID registration

Opt-out Rules : No specific opt-out regulations