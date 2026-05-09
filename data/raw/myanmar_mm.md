# Myanmar (MM)

Source: https://www.twilio.com/en-us/guidelines/mm/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Myanmar |
| ISO code | The International Organization for Standardization two character representation for the given locale. | MM |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 414 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +95 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not required There is no segregation between International and Domestic Traffic | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Twilio recommends registering an Alpha Sender ID Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 1 week | N/A |
| UCS-2 support | --- | Yes | Yes |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | --- | Twilio recommends registering an Alpha Sender ID |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | N/A | N/A |
| Use case restrictions | --- | Myanmar domestic Long Codes can only be used for Person-To-Person (P2P) messages. The use of Myanmar domestic Long Codes for Application-To-Person (A2P) messages will result in delivery failure. | N/A | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Myanmar

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Myanmar Phone Number: Yes (Note: Your sender ID may be changed by some networks)
- Myanmar Short Code: Yes (Note: Your sender ID may be changed by some networks)
- International Phone Number: Yes (Note: Your sender ID may be changed by some networks)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : MPT network additionally supports numeric senders and short codes

Opt-out Rules : No specific opt-out regulations

---

## myanmar
| Key | Value |
| --- | --- |
| MCC | 414 |
| Dialing code | 95 |
| Number portability | No |
| Concatenated message | Long SMS is supported. |
| Service restrictions | Before you start sending messages towards Myanmar, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | 1 day to configure the default account setup, more if it's a specific setup (depending on the client's needs). |
| Sender availability | Alpha, VLN, and SC. |
| Sender provisioning | Between 2 and 15 working days. |
| Two-way | Available as Virtual Long Number. |
| Two-way provisioning | 10 days to order and 3 days to configure. |
| Country regulations | No specific country regulations. |
| Country restrictions | Gambling, political, tobacco, alcohol, religious, and adult content is forbidden. |
| Country recommendations | Due to political instability in Myanmar, sender registration is required for all local and international traffic. |