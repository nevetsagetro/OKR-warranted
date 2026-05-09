# Morocco (MA)

Source: https://www.twilio.com/en-us/guidelines/ma/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Morocco |
| ISO code | The International Organization for Standardization two character representation for the given locale. | MA |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 604 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +212 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | 3 weeks | N/A |
| UCS-2 support | --- | Supported | Supported | Supported |
| Use case restrictions | --- | --- | --- | The Wana Telecom network does not support dynamic Alphanumeric Sender IDs — they will be overwritten with a generic Alphanumeric Sender ID outside the Twilio platform. Twilio suggests using a pre-registered Alphanumeric Sender ID in Morocco |
| Best practices | --- | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A | N/A |
| UCS-2 support | --- | --- | Supported | N/A |
| Use case restrictions | --- | --- | Numeric Sender ID is not supported by the Maroc Telecom and Wana Telecom networks. Numeric Sender IDs will be overwritten with a generic Alphanumeric Sender ID outside the Twilio platform. Delivery is on a best-effort basis. | N/A |
| Best practices | --- | --- | Use non-generic Alphanumeric Sender IDs to send messages to Morocco for better delivery. Twilio suggests using a pre-registered Alphanumeric Sender ID in Morocco | N/A |

---

### Morocco

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Morocco Phone Number: Yes
- Morocco Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): Yes

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : This market has Local and International traffic segmentation

Opt-out Rules : No specific opt-out regulations

---

## morocco
| Key | Value |
| --- | --- |
| MCC | 604 |
| Dialing code | 212 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | There's traffic differentiation based on origin. Sender registration is required. As well as providing proper documentation for sending both traffic for local and international origin. Before you start sending any content towards Morocco for the first time, contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Service provisioning | Depending on the traffic origin and operator, service provisioning might take up to 2 weeks. |
| Sender availability | Sender registration is required on all networks, maximum length 11 characters with no special characters, numbers and generic senders are not allowed and no spaces. |
| Sender provisioning | Depending on the traffic origin, service provisioning might take  up to 2 weeks. |
| Two-way | Two-way services are available for local traffic only. Only premium Short Code available on demand. |
| Two-way provisioning | Estimated provisioning time is 4 to 6 months |
| Country regulations | No specific regulations for A2P messaging. ASTW is implemented so marketing traffic is allowed only from 10 AM to 8 PM hours every day. (9:00 to 19:00 UTC) |
| Country restrictions | No specific restrictions. |
| Country recommendations | Before you start sending local-origin traffic to the Morocco, register you senders to avoid failing traffic. For additional info, reach out to [Support](mailto:support@infobip.com) or your dedicated account managers. |