# Peru (PE)

Source: https://www.twilio.com/en-us/guidelines/pe/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Peru |
| ISO code | The International Organization for Standardization two character representation for the given locale. | PE |
| Region | --- | South America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 716 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +51 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | --- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | You may use an Alpha Sender ID to submit SMS messages in Peru, however it will be overwritten with either a short or long code outside the Twilio platform. |
| Best practices | --- | N/A | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | You may use a Numeric Sender ID to submit SMS messages in Peru, however it will be overwritten with either a short or long code outside the Twilio platform. | N/A |
| Best practices | --- | N/A | --- | N/A |

---

### Peru

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Short Code
- Promotional SMS: Short Code
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Peru Phone Number: Yes
- Peru Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: Yes Monday-Friday: 20:00-08:00 Saturday: 13:00-08:00 Sunday: All day (no SMS allowed)

Additional Notes :

- Allowed times for Promotional/Marketing Traffic: Monday to Friday: 8 AM to 8 PM Saturday: 9 AM to 1 PM (local time)
- Senders are classified as local or international
- All sender IDs will be overwritten with a short code
- Content restrictions: Gambling, political, and adult content is forbidden

Opt-out Rules : No specific opt-out regulations

---

## peru
| Key | Value |
| --- | --- |
| MCC | 716 |
| Dialing code | 51 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Traffic is segmented by origin (local and international). International traffic is more expensive. Before you start sending traffic within Peru, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | Immediate available after account and route configuration. |
| Sender availability | Short Code (dedicated or shared). Non-registered senders will be manipulated into a default Short Code. |
| Sender provisioning | For shared, immediately after account and route setup is done. For dedicated, it may take up to 2 months. |
| Two-way | Shared or dedicated Short Code. |
| Two-way provisioning | 1-2 days for shared, up to 3 months for dedicated. |
| Country regulations | End-user should opt-in for marketing and promotion traffic. Allowed time for marketing, debt collections, promotions: Monday to Friday from 8 AM to 8 PM. Saturday from 9 AM to 1 PM. |
| Country restrictions | Political and promotional traffic from competing MNOs is not allowed. |
| Country recommendations | If you plan to send local traffic (company has headquarters in Peru), contact [Support](mailto:support@infobip.com) or your account manager to make sure your traffic is considered local. |