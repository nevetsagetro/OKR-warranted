# El Salvador (SV)

Source: https://www.twilio.com/en-us/guidelines/sv/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | El Salvador |
| ISO code | The International Organization for Standardization two character representation for the given locale. | SV |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 706 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +503 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | --- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 1 week | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | Alphanumeric Sender ID pre-registration is only supported to Claro El Salvador. | N/A |
| Best practices | --- | N/A | You may use an Alphanumeric Sender ID to reach mobile phones in El Salvador. However, the Sender ID will be overwritten with a short code. Pre-register an Alphanumeric Sender ID to Claro El Salvador as delivery of non-registered Sender ID to this network is on best-effort basis only. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Dynamic Sender ID is not supported by El Salvador mobile operators. Sender ID is overwritten either into a shortcode or longcode outside the Twilio platform | N/A |

---

### El Salvador

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Short Code
- Promotional SMS: Short Code
- Two-Way Conversations: SMS with a two-way short code

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- El Salvador Phone Number: Yes
- El Salvador Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Senders are classified by local and international
- Long Code are supported only by Claro and Tigo

Opt-out Rules : No specific opt-out regulations

---

## el-salvador
| Key | Value |
| --- | --- |
| MCC | 706 |
| Dialing code | 503 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Local/international separation present in Claro, international route is the default. |
| Service provisioning | Default route available immediately, specific route adjustments might take up to 2 days. |
| Sender availability | Alphanumeric - for international traffic in Claro Dynamic - available in Digicel and Tigo VLN - for local traffic in Claro and all traffic in Movistar |
| Sender provisioning | Sender registration for Claro can take up to 2 weeks. |
| Two-way | Available two-way setup: Virtual Long Number. MO or MT initiated. |
| Two-way provisioning | It can take up to 2 months. |
| Country regulations | Marketing traffic not allowed for two-way traffic. |
| Country restrictions | No specific country restrictions. |
| Country recommendations | There are monthly costs for two-way service. For these details, contact your dedicated account manager or [Support](mailto:support@infobip.com) before you start the provisioning process. |