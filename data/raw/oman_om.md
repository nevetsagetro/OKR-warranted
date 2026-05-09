# Oman (OM)

Source: https://www.twilio.com/en-us/guidelines/om/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Oman |
| ISO code | The International Organization for Standardization two character representation for the given locale. | OM |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 422 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +968 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | We recommend that you test Unicode-encoded content before sending it, although Unicode characters should be supported. Sender IDs are overwritten with either random Alphanumeric or long numbers to avoid carrier blocking and filtering. Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Temporarily Suspended | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 18 days | 14 days | N/A |
| UCS-2 support | --- | Supported | Supported | Supported |
| Use case restrictions | --- | N/A | N/A | Oman requires Sender ID pre-registration. Delivery via unregistered Sender IDs will be attempted on a best-effort basis but may not succeed. |
| Best practices | --- | N/A | N/A | Twilio Suggests using a pre-registered Sender ID to submit SMS messages in Oman |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Oman requires Sender ID pre-registration. Delivery via unregistered Sender IDs will be attempted on a best-effort basis but may not succeed. | N/A |
| Best practices | --- | N/A | Twilio Suggests using a pre-registered Sender ID to submit SMS messages in Oman | N/A |

---

### Oman

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Oman Phone Number: No
- Oman Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- This market has Local and International traffic segmentation
- Sender registration is mandatory for all Oman networks
- Letter of Authorization (LOA) is required for sender ID registration only for Local traffic

Opt-out Rules : No specific opt-out regulations

---

## oman
| Key | Value |
| --- | --- |
| MCC | 422 |
| Dialing code | 968 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is required on both network providers, Oman Mobile and Ooredoo as well. There are few specific requirements that need to be fulfilled in order to register senders. Authorization letter from client to Infobip. Also, in NOC there should be a description for each sender and Trade license is needed. International GWs towards Oman require sender registrations as well, otherwise unregistered International senders will be replaced to generic sender NOTICE. |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). |
| Sender availability | Alpha and numeric. Generic senders are not allowed for local SMS termination. |
| Sender provisioning | The average sender registration process time depends solely on network providers. Registration of local senders can lasts up to 20 days, while international are usually done in 10 days period. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | A2P SMS traffic is divided into local and international. The company must have local presence (provision of local Trade License needed) to be considered for local SMS termination. |
| Country restrictions | No spam, political, religious or adult content. Allowed Send Time Window for promotional traffic: 8:00 AM – 8:00 PM. Monday to Sunday, local timezone. |
| Country recommendations | Highly regulated country. Before sending any type of traffic towards Oman for the first time, contact your account manager or [Support](mailto:support@infobip.com). |