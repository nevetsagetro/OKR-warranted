# Niger (NE)

Source: https://www.twilio.com/en-us/guidelines/ne/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Niger |
| ISO code | The International Organization for Standardization two character representation for the given locale. | NE |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 614 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +227 |

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

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Required | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- |
| UCS-2 support | --- | --- | --- |
| Use case restrictions | --- | --- | Generic Alphanumeric Sender IDs, such as InfoSMS, INFO, Verify and Notify, should be avoided. |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Supported | --- |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | --- | --- |
| UCS-2 support | --- | N/A | Supported | --- |
| Use case restrictions | --- | N/A | --- | --- |
| Best practices | --- | N/A | Dynamic Numeric Sender IDs are not fully supported by the networks Airtel and Orange. Sender IDs of this type will be overwritten with a generic Alphanumeric Sender ID outside the Twilio platform and will be delivered on a best effort basis | --- |

---

### Niger

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: SMS with a two-way short code

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Niger Phone Number: No
- Niger Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

---

## niger
| Key | Value |
| --- | --- |
| MCC | 614 |
| Dialing code | 227 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Prior to sending traffic towards Niger, contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Service provisioning | Depending on the traffic origin and operator, service provisioning might take up to 1 week. |
| Sender availability | Local traffic registration is required on all the major networks. Alpha and numeric senders allowed. Dynamic alpha allowed for traffic with international origin. Numeric senders might get blocked on some networks. |
| Sender provisioning | The average sender registration process time depends solely on network providers and can take up to 1 week. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | No two-way SMS options currently available. |
| Country regulations | No specific regulations for A2P messaging. |
| Country restrictions | No specific restrictions. |
| Country recommendations | Even though there are no specific restrictions, note that person-to-person (P2P) traffic is prohibited and will be blocked, as well as traffic with illegal, adult, religious, and political content. |