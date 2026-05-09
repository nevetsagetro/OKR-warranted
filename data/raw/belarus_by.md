# Belarus (BY)

Source: https://www.twilio.com/en-us/guidelines/by/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Belarus |
| ISO code | The International Organization for Standardization two character representation for the given locale. | BY |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 257 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +375 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | For companies based in Belarus, Twilio does not support domestic Alphanumeric Sender ID pre-registration because of local regulations. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Not Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | N/A | --- |
| UCS-2 support | --- | Supported | N/A | --- |
| Use case restrictions | --- | The content of the messages needs to be related with the Sender ID that is being used otherwise the network operator may block the message. Generic Sender IDs are not allowed. Due to the circumstances in the region, the regulatory body (government) started to control traffic on the MTS Belarus network and some senders although properly registered in the past can fail or be manipulated into generic PhoneSMS. This will happen outside Twilio platfrom and unfortunately we have no influence on this. Person-To-Person (P2P) messages are prohibited and these messages would be blocked/filtered by the mobile operators. | For companies based in Belarus, Twilio does not support domestic Alphanumeric Sender ID pre-registration because of local regulations. | --- |
| Best practices | --- | The suffix "by" may be added in the Sender ID outside Twilio's platform if the Sender ID is recognised as a Domestic one from Twilio's downstream provide | --- | Dynamic Alphanumeric Sender ID is not supported by mobile operators in Belarus. Send only with pre-registered sender Id. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Numeric Sender ID is not supported by mobile operators in Belarus. It is overwritten with generic Alphanumeric Sender ID outside the Twilio platform and delivery is on best effort basis only. Twilio recommends sending only from registered sender Id. Person-To-Person (P2P) messages are prohibited and these messages would be blocked/filtered by the mobile operators. | N/A |

---

### Belarus

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Belarus Phone Number: No
- Belarus Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Mandatory registration required
- Generic Sender IDs not allowed
- Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules : No specific opt-out regulations

---

## belarus

| Key | Value |
| --- | --- |
| MCC | 257 |
| Dialing code | 375 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is required. |
| Service provisioning | 3 days to configure the default account setup. More if it's a specific setup (it could depend on the supplier). |
| Sender availability | Alpha |
| Sender provisioning | The average sender registration process time depends solely on network providers and exceeds 24 hours. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | Traffic is separated into local and international. Only alpha senders are allowed and sender registration is mandatory. Opt ins and opt outs are mandatory. ASTW is 9:00 AM to 9:00 PM every day. |
| Country restrictions | Political content is forbidden. |
| Country recommendations | Generic alphanumeric senders are forbidden. |