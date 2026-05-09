# Honduras (HN)

Source: https://www.twilio.com/en-us/guidelines/hn/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Honduras |
| ISO code | The International Organization for Standardization two character representation for the given locale. | HN |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 708 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +504 |

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

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | --- |
| UCS-2 support | --- | Supported | --- |
| Use case restrictions | --- | --- | For Claro network specifically, Alphanumeric Sender IDs are only supported through pre-registration. |
| Best practices | --- | --- | Dynamic Alphanumeric Sender IDs are not fully supported for Honduras mobile operators. Sender IDs may be overwritten with a local long code or short code outside the Twilio platform. Twilio suggests using a pre-registered Sender ID to submit SMS Traffic in Honduras. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | --- |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | --- | --- | --- |
| Use case restrictions | --- | --- | --- | --- |
| Best practices | --- | --- | Dynamic Numeric Sender IDs are not fully supported for Honduras mobile operators. Sender IDs may be overwritten with a local long code or short code outside the Twilio platform. | --- |

---

### Honduras

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Long Code
- Promotional SMS: Long Code
- Two-Way Conversations: SMS with a two-way long number

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Honduras Phone Number: Yes
- Honduras Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-08:00)

Additional Notes :

- Senders are classified as local or international
- Senders will be overwritten with a long code
- Gambling, political and adult content is forbidden

Opt-out Rules : No specific opt-out regulations

---

## honduras
| Key | Value |
| --- | --- |
| MCC | 708 |
| Dialing code | 504 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | There is a separation between local and international traffic with a difference in supported sender types - local VLN for local traffic and alphanumeric for international. |
| Service provisioning | Available immediately. Additional sender registration might be required for international traffic to Claro. |
| Sender availability | International traffic - Alphanumeric Local traffic - VLN |
| Sender provisioning | Sender registration for international traffic to Claro might take up to 1 week. |
| Two-way | Available set up: VLN (MO and MT initiated) |
| Two-way provisioning | Two-way provisioning might take up to 2 months. |
| Country regulations | No specific country regulations. |
| Country restrictions | Gambling, political and adult content is restricted. |
| Country recommendations | Contact [Support](mailto:support@infobip.com) or your dedicated account manager if you plan to send local traffic just to confirm whether it qualifies as local. For international traffic, check whether your sender needs to be registered. Note that there are monthly costs for two-way messaging. Check these details with your account manager or [Support](mailto:support@infobip.com) before starting the provisioning process. |