# Colombia (CO)

Source: https://www.twilio.com/en-us/guidelines/co/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Colombia |
| ISO code | The International Organization for Standardization two character representation for the given locale. | CO |
| Region | --- | South America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 732 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +57 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Ascii character limit for a single message |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | Yes. The network Virgin Mobile doesn’t support sender ID preservation, messages via dedicated short code will have the sender ID replaced with a shared code. |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 4 - 10 weeks |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | N/A | Refer to our FAQs for short code best practices. |
| Best practices | --- | N/A | You may use a global SMS-capable number to reach mobile phones in Colombia. However, the number will be overwritten with a short code. | Refer to our FAQs for short code best practices. |

---

### Colombia

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric
- Promotional SMS: Alphanumeric
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No*
- Colombia Phone Number: No*
- Colombia Short Code: Yes**
- International Phone Number: No*
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No* No* - means you can configure the channel with an Alphanumeric Sender ID, but the operators will deliver them with a random short code Yes** - means that the short code is supported, but only a random one assigned by operators. Dedicated short codes are available only for local entities.

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No
- URL whitelisting required: Yes
- Quiet Hours/Do Not Disturb: Yes - Marketing traffic only (Monday-Sunday 22:00-08:00)

Additional Notes :

- For Promotional Traffic: Allowed from 8:00 AM until 9:00 PM local time
- All senders will be overwritten to a shared short code
- Dedicated short codes can be requested directly from the CRC (Telecommunications Regulator in Colombia), but only if your company is a Colombian-registered legal entity

Opt-out Rules : No specific opt-out regulations

---

## colombia
| Key | Value |
| --- | --- |
| MCC | 732 |
| Dialing code | 57 |
| Number portability | Yes |
| Concatenated message | Concatenated messages supported. |
| Service restrictions | No restrictions. |
| Service provisioning | Available immediately |
| Sender availability | Short Code (shared or dedicated) |
| Sender provisioning | Shared Short Codes are available immediately. 4-8 weeks for a dedicated Short Code. Contact your dedicated account manager or [Support](mailto:support@infobip.com) for a consultation if you need a dedicated Short Code. |
| Two-way | Shared Short Code. |
| Two-way provisioning | Dedicated Short Code - up to 3 months, depending on the MNOs. Shared Short Code - 2 day to configure. |
| Country regulations | To send SMS notifications (transactional, marketing, debt collectors, etc.), you must collect end users opt ins. Debt collectors and marketing content restrictions imposed by CRC (Telecommunications Regulator) from 8:00 AM until 9:00 PM. Opt-ins are required. |
| Country restrictions | NLI is not supported. Clients must have opt ins from their end user to send political content. Every political message must contain a Spanish version of „paid political ad“. |
| Country recommendations | Short code can be removed by the regulator if they are not being used. |