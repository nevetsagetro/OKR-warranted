# Bosnia and Herzegovina (BA)

Source: https://www.twilio.com/en-us/guidelines/ba/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Bosnia and Herzegovina |
| ISO code | The International Organization for Standardization two character representation for the given locale. | BA |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 218 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +387 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

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
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | International Long Code Sender ID is not fully supported in Bosnia and Herzegowina so we suggest using an Alpha Sender ID instead. Messages submitted with an International LongCode Sender ID will be delivered on a best effort basis and the Sender ID will chane to a generic Alpha one outside Twilio's platform | N/A |

---

### Bosnia and Herzegovina

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Bosnia and Herzegovina Phone Number: No
- Bosnia and Herzegovina Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes : Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules : No specific opt-out regulations

---

## bosnia-and-herzegovina

| Key | Value |
| --- | --- |
| MCC | 218 |
| Dialing code | 387 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is a required. The needed documentation depends on traffic origin and network. Before you start sending any content towards Bosnia and Herzegovina for the first time, contact your dedicated account manager or [Support](mailto:support@infobip.com) so they can set up a specific route for you. |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). |
| Sender availability | Alpha senders only. |
| Sender provisioning | It takes about 7 days. |
| Two-way | Short Code |
| Two-way provisioning | It takes one month at least. For more details, contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Country regulations | No specific regulations. |
| Country restrictions | No specific restrictions. |
| Country recommendations | No specific recommendations. |