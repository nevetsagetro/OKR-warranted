# SUDAN (SD)

Source: https://www.twilio.com/en-us/guidelines/sd/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Sudan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | SD |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 634 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +249 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | Promotional content is not allowed to be registered | For the MTN Sudan network specifically, Alphanumeric Sender IDs must be pre-registratered. Please refrain from using generic Sender IDs like InfoSMS, INFO, Verify, Notify, etc. to avoid being blocked by network operators. |
| Best practices | --- | Please refrain from requesting the pre-registration of generic sender IDs like InfoSMS, INFO, Verify, Notify etc to avoid being blocked by network operators. | Twilio suggests using a pre-registered Alphanumeric Sender ID in Sudan. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Not Supported | --- |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Numeric International Sender ID is not supported by the MTN and Sudani One networks in Sudan. Messages submitted with a Numeric Sender ID will not be delivered. Prefer submitting messages only with a registered Alphanumeric Sender ID to this network. | N/A |
| Best practices | --- | N/A | Twilio suggests using a pre-registered Alphanumeric Sender ID in Sudan. | N/A |

---

### Sudan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Sudan Phone Number: No
- Sudan Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : This market has Local and International traffic segmentation

Opt-out Rules : No specific opt-out regulations

---

## sudan
| Key | Value |
| --- | --- |
| MCC | 634 |
| Dialing code | 249 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions apply to sending traffic to Sudan. |
| Service provisioning | Since no prior registration of senders is necessary, service provisioning should be available within a day. |
| Sender availability | Dynamic Alpha or numeric senders allowed. |
| Sender provisioning | Sender provisioning should be available within a day. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | No two-way SMS options currently available. |
| Country regulations | No specific regulations for A2P messaging. |
| Country restrictions | No specific restrictions. |
| Country recommendations | Even though there are no specific restrictions, note that person-to-person (P2P) traffic is prohibited and will be blocked, as well as traffic with illegal, adult, religious, and political content.