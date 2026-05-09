# Pakistan (PK)

Source: https://www.twilio.com/en-us/guidelines/pk/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Pakistan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | PK |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 410 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +92 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Per local regulations, peer-to-peer (P2P) traffic is prohibited from being sent via operators in Pakistan. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | Dynamic Alphanumeric Sender IDs are not supported by all mobile operators in Pakistan. Sender IDs may be overwritten with a random Short Code or a generic Alphanumeric Sender ID outside the Twilio platform to ensure deliverability. Messages related to gambling are not allowed by all mobile operators in Pakistan. |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Dynamic Numeric Sender IDs are not supported by all mobile operators in Pakistan. Sender IDs may be overwritten with a random Short Code or a Generic Alphanumeric Sender ID outside the Twilio platform to ensure deliverability. Messages related to gambling are not allowed by all mobile operators in Pakistan. | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Pakistan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- Pakistan Phone Number: Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- Pakistan Short Code: Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- International Phone Number: Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes (On certain networks)
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- This market has Local and International traffic segmentation
- Different networks have different requirements: Mobilink & Warid: Alpha senders need registration or will be changed to generic sender ZONG & SCO Mobile: All sender types supported Telenor & Ufone: All senders will be changed to short codes regardless of registration status

Opt-out Rules : No specific opt-out regulations

---

## pakistan
| Key | Value |
| --- | --- |
| MCC | 410 |
| Dialing code | 92 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | For local traffic, sender registration is required. The needed documentation depends on traffic origin and network. Before you start sending messages towards Pakistan, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). |
| Sender availability | For international traffic, Jazz and Zong networks deliver with Alpha. Ufone and Telenor delivers with numeric. For Telenor, all senders will be manipulated into random 5 or 6-digits Short Code. For Ufone, all senders will be manipulated into 56789 Short Code. For Jazz, there is sender registration. For Zong, no sender registration needed. |
| Sender provisioning | The average sender registration process depends solely on network providers. For local SMS termination, it usually takes about 15 days. Note that you must have the documentation to confirm your company's local presence. For international SMS termination (only Jazz Network), it can around 5 days. |
| Two-way | Virtual Long Number, for local companies only. |
| Two-way provisioning | Only available for local companies. It can take up to 10 days. |
| Country regulations | No specific regulations. |
| Country restrictions | No specific restrictions. |
| Country recommendations | Before you send any kind of traffic towards Pakistan, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |