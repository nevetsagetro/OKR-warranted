# Costa Rica (CR)

Source: https://www.twilio.com/en-us/guidelines/cr/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Costa Rica |
| ISO code | The International Organization for Standardization two character representation for the given locale. | CR |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 712 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +506 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | No |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | Although the Twilio API supports long messages, operators in Costa Rica do not generally support concatenated SMS. When Twilio receives a long message for Costa Rica, we will split the message into individual messages and cannot guarantee their order. |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Required | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- |
| UCS-2 support | --- | --- | --- |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | --- | --- | --- |
| Use case restrictions | --- | --- | --- | --- |
| Best practices | --- | --- | You may use a global SMS-capable number to reach mobile phones in Costa Rica. However, the the number will be overwritten with either a short code or a long code. | --- |

---

### Costa Rica

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Long Code
- Promotional SMS: Long Code
- Two-Way Conversations: SMS with a two-way long number

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Costa Rica Phone Number: Yes
- Costa Rica Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Senders are classified as local or international
- Gambling, political and adult content is forbidden

Opt-out Rules : No specific opt-out regulations

---

## costa-rica
| Key | Value |
| --- | --- |
| MCC | 712 |
| Dialing code | 506 |
| Number portability | Yes |
| Concatenated message | Standard. |
| Service restrictions | There is local/international traffic separation within the country. International traffic is more expensive. All traffic is considered international, by default. |
| Service provisioning | For local traffic, provisioning may take up to 3 days. |
| Sender availability | Shared Virtual Long Number (shared and dedicated) |
| Sender provisioning | Shared VLN available immediately after the route configuration is done. |
| Two-way | Available for local traffic. Shared and dedicated Virtual Long Numbers. |
| Two-way provisioning | 1-2 days for shared VLN, and up to 1 month for dedicated VLN. |
| Country regulations | Traffic is segmented based on origin. If messages are sent from within Costa Rica, they will be considered local. |
| Country restrictions | Gambling, political, adult content, and MNO promotions for other MNOs are restricted in Costa Rica. Promotional messages can be sent from 8 AM to 8 PM, Costa Rica time. |
| Country recommendations | If you are planning to send local traffic, contact your dedicated account manager or [Support](mailto:support@infobip.com) to confirm whether this traffic is considered local. |