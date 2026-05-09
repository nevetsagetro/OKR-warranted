# Dominican Republic (DO)

Source: https://www.twilio.com/en-us/guidelines/do/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Dominican Republic |
| ISO code | The International Organization for Standardization two character representation for the given locale. | DO |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 370 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +1829 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | Dynamic Alphanumeric Sender IDs are not fully supported by Dominican Republic mobile operators. Sender IDs may be overwritten with a random shortcode outside the Twilio platform. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 4 weeks |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | N/A | Refer to our FAQs for short code best practices. |
| Best practices | --- | N/A | Dynamic Numeric Sender IDs are not fully supported by Dominican Republic mobile operators. Sender IDs may be overwritten with a random shortcode outside the Twilio platform. | Refer to our FAQs for short code best practices. |

---

### Dominican Republic

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: SMS with a two-way short code

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Dominican Republic Phone Number: Yes
- Dominican Republic Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: No
- Content Restrictions: Gambling, political and adult content are restricted

Additional Notes : Some messages from alphanumeric and long code senders may be changed to random short codes by local operators

Opt-out Rules : No specific opt-out regulations

---

## dominican-republic
| Key | Value |
| --- | --- |
| MCC | 370 |
| Dialing code |  |
| Number portability | Yes |
| Concatenated message | Concatenated messages supported. |
| Service restrictions | Before you start sending messages towards the Dominican Republic, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | 1 day to configure default account setup. More if it's a specific setup (depending on the client's needs). |
| Sender availability | Alphanumeric, Virtual Long Numbers and Short Code |
| Sender provisioning |  |
| Two-way | It may be available. Short Code. |
| Two-way provisioning | Contact your account manager or [Support](mailto:support@infobip.com) to check the availability for two-way solutions. It might take up to 3 months to provision a Short Code. |
| Country regulations | No specific country regulations. |
| Country restrictions | Gambling, political and adult content are restricted. |
| Country recommendations | No specific country recommendations. |