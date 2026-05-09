# Cuba (CU)

Source: https://www.twilio.com/en-us/guidelines/cu/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Cuba |
| ISO code | The International Organization for Standardization two character representation for the given locale. | CU |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 368 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +53 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | No |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Notice: Discontinuation of SMS Delivery to Cuba In compliance with applicable regulations and requirements, and to reinforce our commitment as a trusted partner for our customer communication needs, Twilio will stop supporting SMS message delivery to Cuba effective September 15, 2025. We strongly encourage customers to discontinue sending SMS traffic to Cuba through Twilio before this date to avoid delivery failures. After September 15, 2025 onward, all SMS messages to Cuba will be blocked by Twilio. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | N/A |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Not Supported | --- |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | N/A | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Cuba

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Cuba Phone Number: Yes
- Cuba Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No
- Content Restrictions: Gambling, political and adult content is forbidden

Additional Notes : Two-way SMS not available

Opt-out Rules : No specific opt-out regulations

---

## cuba
| Key | Value |
| --- | --- |
| MCC | 368 |
| Dialing code | 53 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is not required for international traffic. |
| Service provisioning | Alphanumeric senders and dedicated VLNs are not supported. |
| Sender availability | International registration for alphanumeric senders is not supported. |
| Sender provisioning | Estimated time to register is 180 days. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | No specific country regulations. |
| Country restrictions | Gambling, political and adult content is forbidden. |
| Country recommendations | Contact your dedicated account manager or [Support](mailto:support@infobip.com) for more information about default senders and sender registration. |