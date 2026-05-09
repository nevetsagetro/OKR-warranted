# Cameroon (CM)

Source: https://www.twilio.com/en-us/guidelines/cm/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Cameroon |
| ISO code | The International Organization for Standardization two character representation for the given locale. | CM |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 624 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +237 |

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

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Not Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | N/A | N/A |
| UCS-2 support | --- | Supported | N/A | Supported |
| Use case restrictions | --- | Promotional content is not allowed to be registered | N/A | For MTN network specifically, Alphanumeric Sender IDs are only supported through pre-registration. Google as a Sender ID is prohibited in Cameroon. Messages using this Sender ID may be blocked or filtered by the local operators. |
| Best practices | --- | Please refrain from requesting generic sender IDs to avoid being blocked by network operators. | Customers with Domestic Traffic are welcome to register their Sender IDs are International ones | Twilio suggests using a preregistered Alphanumeric Sender ID in Cameroon |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Not Supported | --- |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | --- | --- | --- |
| Use case restrictions | --- | --- | Numeric International sender ID is not supported to the MTN network in Cameroon. Messages submitted with numeric would result in delivery failure. Send only with alphanumeric sender ID to this network. | --- |
| Best practices | --- | --- | Twilio suggests using a preregistered Alphanumeric Sender ID in Cameroon | --- |

---

### Cameroon

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Cameroon Phone Number: Yes
- Cameroon Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : This market has Local and International traffic segmentation

Opt-out Rules : No specific opt-out regulations

---

## cameroon

| Key | Value |
| --- | --- |
| MCC | 624 |
| Dialing code | 237 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | In Cameroon, traffic is segmented based on origin and type, depending on the network. Registration is required for local traffic. For Orange, registration is needed for all traffic. Before you start sending traffic towards Cameroon, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |
| Service provisioning | Service provisioning is up to 1 week. For networks which don't require businesses to register to send international traffic, service provisioning should be available within a day. |
| Sender availability | Alpha sender allowed. Numeric senders are blocked. |
| Sender provisioning | Up to 1 week for traffic of local origin. For international origin traffic, sender provisioning should be available within a day. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | No two-way SMS options currently available. |
| Country regulations | No specific regulations. |
| Country restrictions | No specific restrictions. |
| Country recommendations | Even though there are no specific restrictions, note that person-to-person (P2P) traffic is prohibited and will be blocked, as well as traffic with illegal, adult, religious, and political content. |