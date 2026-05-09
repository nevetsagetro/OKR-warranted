# Indonesia (ID)

Source: https://www.twilio.com/en-us/guidelines/id/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Indonesia |
| ISO code | The International Organization for Standardization two character representation for the given locale. | ID |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 510 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +62 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | All SMS messages sent via domestic Sender IDs to Indonesia must include a brand name, service program, or community in the message body in order to avoid rejection of message. This requirement aligns with Twilio's ongoing commitment to ensuring compliance in Indonesia. Message delivery to M2M numbers is on best effort basis only. Sending firearms, gambling, adult content, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. It is best practice not to include phone numbers in message body. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices. Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 4 weeks | 3 weeks | N/A |
| UCS-2 support | --- | Supported | Not Supported UCS2-encoded messages are only supported over International Registered Sender IDs | Supported |
| Use case restrictions | --- | Please refrain from requesting generic alphanumeric sender IDs to avoid being blocked by network operators. Messages must not contain: SPAM-related materials.Anything that is misleading, deceiving, obscene, offensive, or defamatory against any person.Content that infringes on the rights of any third-party or may give rise to any legal claim by any person. | All SMS messages sent via domestic Sender IDs to Indonesia must include a brand name, service program, or community in the message body in order to avoid rejection of message. This requirement aligns with Twilio's ongoing commitment to ensuring compliance in Indonesia. Messages must not contain: SPAM-related materials.Anything that is misleading, deceiving, obscene, offensive, or defamatory against any person.Content that infringes on the rights of any third-party or may give rise to any legal claim by any person. | Twilio will start blocking on the 21st of September of 2024 any traffic submitted to the networks Telkomsel, Axiata, and Smart from Sender IDs that are not pre-registered. Please Register an Alpha Sender ID in Indonesia to avoid having your messages blocked. |
| Best practices | --- | Separate procedures are in place for registering Domestic and International Sender IDs, this may require different documents to be submitted. The major Indonesian network operators follow strict policies regarding the validity of registered Sender IDs which don't produce traffic. Every 3 months each network operator is checking the traffic that is sent to them and Alphanumeric Sender IDs with less than 1000 SMS per 3 month and per network are deprovisioned. | We strongly suggest our Domestic customers who intend to register their Alpha Sender IDs to send at least 5000 SMS, spread to all Indonesian networks | Twilio suggests using a pre-registered Alphanumeric Sender ID in Indonesia |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | No | No | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Delivery of messages submitted with Numeric Sender IDs is on a best-effort basis and will be overwritten with either random Numeric or Alphanumeric Sender IDs. Pre-registration of Alphanumeric Sender IDs is required. Twilio will start blocking on the 21st of September of 2024 any traffic submitted to the networks Telkomsel, Axiata, and Smart from Sender IDs that are not pre-registered. Please Register an Alpha Sender ID in Indonesia to avoid having your messages blocked. | N/A |
| Best practices | --- | N/A | Twilio suggests using a pre-registered Alphanumeric Sender ID in Indonesia | N/A |

---

### Indonesia

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Indonesia Phone Number: No
- Indonesia Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- This market has Local and International traffic segmentation
- Letter of Authorization (LOA) required for sender ID registration

Opt-out Rules : No specific opt-out regulations

---

## indonesia
| Key | Value |
| --- | --- |
| MCC | 510 |
| Dialing code | 62 |
| Number portability | No |
| Concatenated message | Concatenated messages are not guaranteed to be delivered to all networks. The recommendation is to limit message to one singular message. Usually because of the handset limitation. |
| Service restrictions | Sender registration is required. Documentation depends on traffic origin and network. Before you start sending messages towards Indonesia, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | Setup depends on sender provisioning time (different on each network). |
| Sender availability | Alpha senders only. Sender should be brand-related senders, generic senders are mainly not allowed. |
| Sender provisioning | The average sender registration process completion time depends solely on network providers. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | Indonesian message traffic is separated into local and international. Local traffic has further separation into OTP and notification. Opt-out and ASTW are not implemented. DND is not enabled. Local promotional messages have specific routing set internally. |
| Country restrictions | Gambling, religious, adult, and racial content is prohibited by law. |
| Country recommendations | Maximum sender length is 11 characters for all operators. To have optimal routing and to secure delivery to all networks,  sender registration is necessary. Used sender should clearly indicate the brand/company to avoid interruption of service. |