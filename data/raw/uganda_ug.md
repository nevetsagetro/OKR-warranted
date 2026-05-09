# Uganda (UG)

Source: https://www.twilio.com/en-us/guidelines/ug/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Uganda |
| ISO code | The International Organization for Standardization two character representation for the given locale. | UG |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 641 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +256 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user’s local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | Promotional content is not allowed to be registered | Generic Alphanumeric Sender IDs, such as InfoSMS, INFO, Verify and Notify, should be avoided. For MTN network specifically, Alphanumeric Sender IDs are only supported through pre-registration. |
| Best practices | --- | Please refrain from requesting generic sender IDs like InfoSMS, INFO, Verify, Notify etc to avoid being blocked by network operators. | Twilio suggests using a pre-registered Alphanumeric Sender ID in Uganda. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | Yes | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | The networks MTN, Airtel, Africel and Smart in Uganda do not support numeric sender ID. For better deliverability, send only with an Alphanumeric Sender ID that is related to your content. | N/A |
| Best practices | --- | N/A | Twilio suggests using a pre-registered Alphanumeric Sender ID in Uganda. | N/A |

---

### Uganda

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Uganda Phone Number: Yes
- Uganda Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

---

## uganda
| Key | Value |
| --- | --- |
| MCC | 641 |
| Dialing code | 256 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | There's traffic differentiation based on origin (local or international). For sending local traffic, you need to register and file proper documentation. There are setup and monthly fees for each registered sender. Before you start sending any traffic towards Uganda, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |
| Service provisioning | Depending on traffic origin and operator, service provisioning might take from 1 day to up to 2 weeks. |
| Sender availability | Local traffic registration is required on all the major networks. The maximum length 11 characters, no space or special characters. You need an authorization letter stating that the company is authorized to send traffic. The letter must be signed and stamped. Each message sent must include a recognized accurate identifier. This must enable the recipient to identify who sent the message. Additionally, within the message, you must include information how can the recipient contact the sender. If an organization is sending these messages, include the name of the organization. Operator's registration fees apply. |
| Sender provisioning | The average sender registration process time depends solely on network providers and can take up to 2 weeks. |
| Two-way | Two-way services are available for local traffic only and only using Short Code. Available two-way setup: standard and zero rated. |
| Two-way provisioning | To use Short Codes, you need to have a local entity. Provisioning time can take up to 3 months. |
| Country regulations | Each message must have the unsubscribe option or opt-out option. Use the keyword "STOP" for recipients to unsubscribe. |
| Country restrictions | Any content that is objectionable on the grounds of public interest, public morality, public order, public security or national harmony are prohibited. These include sexual content, acts of violence, ethnic, racial or religious hatred, unreasonable invasion of privacy, inducing dangerous practices or harmful substance or debases, degrades or demeans in any form. |
| Country recommendations | Before you start sending traffic towards Uganda, acquire all necessary documentation to speed up registrations and waiting times. For additional information, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |