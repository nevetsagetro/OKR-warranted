# Brazil (BR)

Source: https://www.twilio.com/en-us/guidelines/br/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Brazil |
| ISO code | The International Organization for Standardization two character representation for the given locale. | BR |
| Region | --- | South America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 724 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +55 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 140 characters-per-segment for NEXTEL. 160 characters-per-segment for all other carriers. |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | As a best practice when sending SMS to smaller or regional operators, such as Surf Telecom in Brazil, we recommend avoiding the use of special GSM-7 characters. These networks may have limited character set support, which can result in characters being removed, replaced, or messages being encoded differently to ensure delivery. Oi does not support delivery report. Several major carriers in Brazil substitute accented characters for ASCII equivalents. Oi, NEXTEL, and CTBC (Algar) do not support unicode. Sending marketing messages outside the hours of 09:00 and 22:00 local time and all day on Sunday is prohibited. Be aware that Brazil spans three time zones. Messages promoting contests or telecommunication services are prohibited. Sending adult content, controlled substance, and cannabis related content are also strictly prohibited. Message delivery to M2M numbers is on best effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported (Optional) There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported (Optional) Learn more and register via the Console | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 10 weeks | N/A |
| UCS-2 support | --- | Supported | N/A |
| Use case restrictions | --- | The Pre-Registration is optional and available only for TIM, CLARO and VIVO networks | N/A |
| Best practices | --- | We would suggest requesting only an Uppercase Sender ID as VIVO networks only supports Uppercase Sender ID Registration | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 2-4 weeks |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | You can only use Brazil long code phone numbers for person-to-person (P2P) messaging. | N/A | Please refer to Brazil Short Code Best Practices for further information. |
| Best practices | --- | N/A | You may use a global SMS-capable number from another country to send application-to-person (A2P) messaging to mobile phones in Brazil. SenderId is not preserved and may be overwritten with a random shortcode or longcode outside Twilio's platform. | Please refer to Brazil Short Code Best Practices for further information. |

---

### Brazil

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Short Code
- Promotional SMS: Short Code
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Brazil Phone Number: Yes
- Brazil Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes Monday-Saturday: 21:00-08:00 Sunday: All day (no SMS allowed)

Additional Notes :

- All sender IDs are overwritten with a local short code or long code
- Allowed sending times: Monday to Friday: 8:00 AM to 8:00 PM Saturday: 8:00 AM to 2:00 PM Sunday: SMS are not allowed
- Content restrictions: Electoral/political content, religious content, content that breaches intellectual property rights, and content related to termination of pregnancies

Opt-out Rules : No specific opt-out regulations

---

## brazil

| Key | Value |
| --- | --- |
| MCC | 724 |
| Dialing code | 55 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions. |
| Service provisioning | Available within 1 day. |
| Sender availability | Alphanumeric (consult your dedicated account manager or [Support](mailto:support@infobip.com)), Short Codes (dedicated and shared). |
| Sender provisioning | Alpha sender - Up to 3 months. Dedicated Short Code - up to 48h if in stock, otherwise 1-2 months. |
| Two-way | Available. Short Code (shared and dedicated) |
| Two-way provisioning | 1-2 days as two-way needs to be configured by the account manager or [Support](mailto:support@infobip.com) (keyword and forwarding available). |
| Country regulations | No messaging with Virtual Long Numbers allowed, messages with bank and MNO names must be authorized by the companies. Political and gambling not allowed. Marketing must have opt-in from end users. DND is available in Brazil, but the end-user must request it. Alowed send time window: Work days - 8 AM - 8 PM Saturday - 8 AM - 2 PM Sundays - No calls allowed |
| Country restrictions | Gambling and political content is forbidden. Marketing content must have an opt-out option. |
| Country recommendations | When using bank or MNO names, consult [Support](mailto:support@infobip.com) or your account manager to approve and safelist the message content. Otherwise, it will get caught in our filters. MO messages should be set with specific keywords, as generic keywords can lead to the wrong customer receiving the message. Opt-out is mandatory in Brazil so it is recommended to set it on every account. |