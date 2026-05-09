# Zimbabwe (ZW)

Source: https://www.twilio.com/en-us/guidelines/zw/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Zimbabwe |
| ISO code | The International Organization for Standardization two character representation for the given locale. | ZW |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 648 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +263 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | It is highly recommended for best deliverability that you use an Alphanumeric sender ID to send to any network in Zimbabwe. The use of generic Alphanumeric Sender IDs is strictly prohibited. The network Telecel Zimbabwe does not support Numeric Sender ID and only allows OTT/OTP messages. Sender ID and content registration is required but is currently not supported by Twilio. Delivery to M2M numbers is on best-effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required Learn more and register via the Console | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 1 week | N/A |
| UCS-2 support | --- | Supported | --- |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Telcel Zimbabwe does not support Numeric Sender IDs. Use an Alphanumeric Sender ID for better deliverability. | N/A |

---

### Zimbabwe

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Zimbabwe Phone Number: No
- Zimbabwe Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

Was this helpful?


---

# SMS Country Information Guide: Asia (A-K)

Fuente: https://docs.bird.com/applications/channels/channels/supported-channels/sms/concepts/choose-the-right-sender-availability-and-restrictions-by-country/sms-country-information-guide-asia-a-k

---

## zimbabwe

| Key | Value |
| --- | --- |
| MCC | 648 |
| Dialing code | 263 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | There's traffic differentiation based on origin (local or international). You need to be registered before you can send local traffic. The same rule does not apply for international traffic. Note that you may not be able to send traffic with a generic or numeric sender because some networks have certain restrictions. Before you send any type of traffic towards Zimbabwe, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |
| Service provisioning | Depending on the traffic origin and operator, service provisioning might take from 10 days to up to 30 days. Traffic with international origin does not have to be pre-registered but to assure that your traffic is delivered delivered, do not use generic and numeric senders. |
| Sender availability | Local traffic registration is required on all networks, maximum length 11 characters with special characters. |
| Sender provisioning | The average sender registration process time depends solely on network providers and can take up to 30 days. |
| Two-way | Available 2-way setup: Short Codes. The two-way option is available via Short Code only and only on Econet. |
| Two-way provisioning | Provisioning time for Econet can take up to 6 months to complete. |
| Country regulations | A2P messaging is differentiated based on its origin (local or international).Special rates apply for international traffic. |
| Country restrictions | Political, adult, and gambling content is forbidden. |
| Country recommendations | Before you start sending any traffic to Zimbabwe, register your senders to avoid failing traffic. Do not use generic or numeric senders because some networks have certain restrictions. For additional information, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |