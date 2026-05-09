# Ghana (GH)

Source: https://www.twilio.com/en-us/guidelines/gh/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Ghana |
| ISO code | The International Organization for Standardization two character representation for the given locale. | GH |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 620 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +233 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Sender ID Compliance Sender ID Registration is required in Ghana for MTN network. Starting on July 8, 2026, messages with unregistered Sender IDs to these networks will be blocked. To continue sending messages, you must use a registered Alphanumeric Sender ID. Additional Phone Numbers and Sender ID Guidelines Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required for MTN | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | 2 weeks | N/A |
| UCS-2 support | --- | Supported | Supported | Supported |
| Use case restrictions | --- | Promotional content is not allowed to be registered. | Only the following characters are supported via GSM-7 encoding: %&'()*+,-./0123456789:;<=>? ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz# The use of any other GSM-7 character will result in the character getting replaced or removed. | Dynamic Alphanumeric Sender ID is not supported for MTN network. Please refrain from using generic sender IDs to avoid being blocked by network operators. |
| Best practices | --- | --- | --- | Twilio suggests using an alphanumeric pre-registered Sender ID in Ghana |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | Numeric International sender ID is not supported to the Airtel, MTN and Glo networks in Ghana. Messages submitted with numeric would result in delivery failure. Send only with alphanumeric sender ID to these networks. | N/A |
| Best practices | --- | N/A | Twilio suggests using an alphanumeric pre-registered Sender ID in Ghana | N/A |

---

### Ghana

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Ghana Phone Number: No
- Ghana Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

---

## ghana
| Key | Value |
| --- | --- |
| MCC | 620 |
| Dialing code | 233 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | If you are planning to terminate to Ghana networks, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up a specific route for you. Sender registration is needed for local traffic. |
| Service provisioning | 1 day to configure the default account setup + sender registration if needed (local traffic) |
| Sender availability | Alpha, Short Code |
| Sender provisioning | The average sender registration process completion time depends solely on network providers and can take up to 48h (weekends not included). |
| Two-way | Available 2-way setup: - USSD - Short Code Standard and zero-rated billing for two-way Short Codes. Reverse billing for USSD codes. |
| Two-way provisioning | The official „time to market“ is 7 days after all SCs fees are paid, but usually takes up to 2 months. Not applicable for international traffic. |
| Country regulations | The SMS designed to promote, directly or indirectly, goods, services, commercial images of people pursuing a commercial activity or exercising a regulated profession (such as dentists, accountants, lawyers) is forbidden. Unsolicited promotional messages are not allowed. DND is handled on the MNO side. |
| Country restrictions | Gambling traffic is allowed. No specific regulations apply to promo messages, but network MTN has a DND service which blocks messages froma a specific shortcode. This is not mandated by  regulator, but applied at MNO's discretion. |
| Country recommendations | Even though there are no specific restrictions, note that person-to-person (P2P) traffic is prohibited and will be blocked, as well as traffic with illegal, adult, religious, and political content. |