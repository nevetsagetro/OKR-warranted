# Venezuela (VE)

Source: https://www.twilio.com/en-us/guidelines/ve/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Venezuela |
| ISO code | The International Organization for Standardization two character representation for the given locale. | VE |
| Region | --- | South America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 734 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +58 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | No |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required Learn more and Register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 21 days | N/A |
| UCS-2 support | --- | Supported | Supported only for Movilnet |
| Use case restrictions | --- | Alphanumeric Sender ID pre-registration is only supported to Digitel Venezuela. | Any Alpha Sender ID used to send messages to Venezuelan networks will be overwritten with a random short code, long code or generic Alphanumeric Sender ID outside the Twilio platform to facilitate delivery. UCS2 characters toward Movistar may be replaced of flattened. |
| Best practices | --- | N/A | Pre-register an Alphanumeric Sender ID to Digitel Venezuela as delivery of non-registered Sender ID to this network is on best-effort basis only. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported only for Movilnet | N/A |
| Use case restrictions | --- | N/A | Any Numeric Sender ID used to send messages to Venezuelan networks will be overwritten with a random short code, long code or generic Alphanumeric Sender ID outside the Twilio platform to facilitate delivery. UCS2 characters toward Movistar may be replaced of flattened. | N/A |
| Best practices | --- | N/A | Pre-register an Alphanumeric Sender ID to Digitel Venezuela as delivery of non-registered Sender ID to this network is on best-effort basis only. | N/A |

---

### Venezuela

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Alphanumeric only, no pure Alpha)
- Venezuela Phone Number: Yes
- Venezuela Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-08:00)

Additional Notes :

- Only the Only Digital network accepts alphanumeric sender IDs
- For all other networks, sender IDs will be replaced with a short code
- Content restrictions: Gambling, political, and adult content is restricted

Opt-out Rules : No specific opt-out regulations

Last updated 8 months ago

Was this helpful?


---

---

## venezuela
| Key | Value |
| --- | --- |
| MCC | 734 |
| Dialing code | 58 |
| Number portability | No |
| Concatenated message | Concatenated messages supported. |
| Service restrictions | No restrictions. |
| Service provisioning | Available immediately. |
| Sender availability | Digitel - alphanumeric only. Numeric senders will be replaced by a generic alphanumeric sender. Movistar - shared Short Codes only. |
| Sender provisioning | If needed, registration of alphanumeric sender might take up to 1 week. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | No specific country regulations. |
| Country restrictions | Gambling, political and adult content is restricted. |
| Country recommendations | No specific country recommendations. |