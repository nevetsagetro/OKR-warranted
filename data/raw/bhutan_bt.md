# Bhutan (BT)

Source: https://www.twilio.com/en-us/guidelines/bt/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Bhutan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | BT |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 402 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +975 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | SMS delivery to B-Mobile Bhutan is at best effort. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Bhutan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Bhutan Phone Number: Yes
- Bhutan Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Opt-out Rules : No specific opt-out regulations

---

## bhutan
| Key | Value |
| --- | --- |
| MCC | 402 |
| Dialing code | 975 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions. |
| Service provisioning | Since no prior registration of senders is necessary, service provisioning should be available within a day. |
| Sender availability | Sender ID preregistration not required. Senders are dynamic and any acceptable alphanumeric term can be set. |
| Sender provisioning | Available immediately. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | Subscribers should be provided the choice to unsubscribe to SMS-CB services. Broadcast messages should be only to the intended recipients by geographical area. Any picture or video in any format not permitted for broadcasting. Ensure that the subscriber is not charged for receiving A2P services. Ensure that the content providers bear the cost of broadcasting such service, as approved by the Authority. The Service Providers shall ensure that promotion or advertisement of any product or service: a) Be thoroughly reviewed and broadcasted only to the subscribers of an intended geographical area or target, and b) Be in accordance with the Advertisement policy, Rules on Contents and any other relevant Rules/Regulations of the government. |
| Country restrictions | The Service Provider shall not broadcast any messages that: a) Are political and religious in nature. b) Create social disharmony and is detrimental to the peace, stability and well being of the nation. c) Incite religious, ethnic, regional, or communal conflicts. |
| Country recommendations | No specific country recommendations. |