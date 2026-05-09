# Nicaragua (NI)

Source: https://www.twilio.com/en-us/guidelines/ni/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Nicaragua |
| ISO code | The International Organization for Standardization two character representation for the given locale. | NI |
| Region | --- | Central America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 710 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +505 |

## Guidelines keep

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported There is no segregation between International and Domestic Traffic | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | --- |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | Alphanumeric Sender ID pre-registration is only supported to Claro Nicaragua. | The character Ñ is not supported in the network Telefonica unless the encoding UCS2 is utilised |
| Best practices | --- | --- | You may use an Alphanumeric Sender ID to reach mobile phones in Nicaragua. However, the Sender ID will be overwritten with a short code, with the exception of the Movistar network where the Alpha senderID is preserved. Pre-register an Alphanumeric Sender ID to Claro Nicaragua as delivery of non-registered Sender ID to this network is on best-effort basis only. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | --- | --- |
| UCS-2 support | --- | N/A | Supported | --- |
| Use case restrictions | --- | N/A | The character Ñ is not supported in the network Telefonica unless the encoding UCS2 is utilised | --- |
| Best practices | --- | N/A | You may use a global SMS-capable number to reach mobile phones in Nicaragua. However, the number will be overwritten with a short code. | --- |

---

### Nicaragua

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Short Code
- Promotional SMS: Short Code
- Two-Way Conversations: SMS with a two-way short code

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Nicaragua Phone Number: No
- Nicaragua Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : Gambling, political and adult content is forbidden

Opt-out Rules : No specific opt-out regulations

---

## nicaragua

| Key | Value |
| --- | --- |
| MCC | 710 |
| Dialing code | 505 |
| Number portability | No |
| Concatenated message | Concatenated messages supported. |
| Service restrictions | Some networks have a local/international traffic separation. |
| Service provisioning | The default route is available immediately, while additional sender registration might take up to 1 week. |
| Sender availability | Mostly manipulated to default numeric senders, possibility to use alphanumeric senders for some traffic. |
| Sender provisioning | Alphanumeric sender registration for Claro international traffic might take up to 1 week. |
| Two-way | Available set up: VLN, MT and MO initiated |
| Two-way provisioning | It might take up to 2 months. |
| Country regulations | No specific country regulations. |
| Country restrictions | Gambling, political and adult content is restricted. |
| Country recommendations | If you want to use an alphanumeric sender, registration is required. Make sure you've done that before you start sending messages. Note that there are monthly costs for two-way messaging. Check these details with your dedicated account manager or [Support](mailto:support@infobip.com) before starting the provisioning process. |