# New Zealand (NZ)

Source: https://www.twilio.com/en-us/guidelines/nz/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | New Zealand |
| ISO code | The International Organization for Standardization two character representation for the given locale. | NZ |
| Region | --- | Oceania |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 530 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +64 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Due to local carrier restrictions, NZ Operators have mandated Dedicated Short Codes . For compliance, New Zealand’s mobile operators require the content “Reply to this SMS will be charged” to be added to every message sent to New Zealand. Please contact Twilio to learn how to get dedicated shortcodes. Sending firearms, gambling, adult content, money/loan, political, religious, controlled substance, and cannabis related content is strictly prohibited. Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | N/A | N/A |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | N/A |
| Use case restrictions | --- | N/A | Mobile operators in New Zealand require SMS messages to be delivered through dedicated short code Sender ID only. |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | N/A | Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 5-6 weeks |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | Mobile operators in New Zealand require SMS messages to be delivered through dedicated short code Sender ID only. | Refer to our FAQs for short code best practices. |
| Best practices | --- | N/A | N/A | Refer to our FAQs for short code best practices. |

---

### New Zealand

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Short Code
- Promotional SMS: Short Code
- Two-Way Conversations: SMS with a two-way short code

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- New Zealand Phone Number: No
- New Zealand Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- Alphanumeric Sender IDs are best-effort only
- For reliable delivery, purchasing a short code is recommended

Opt-out Rules : No specific opt-out regulations

---

## new-zealand
| Key | Value |
| --- | --- |
| MCC | 530 |
| Dialing code | 64 |
| Number portability | Yes |
| Concatenated message | Standard |
| Service restrictions | All sender IDs are overwritten by operators to local Short Codes. |
| Service provisioning | Available within 1 working day. |
| Sender availability | Short Code |
| Sender provisioning | Not available. |
| Two-way | Dedicated Short Code (Standard or FTEU Billing for transactional traffic) (Only FTEU Billing for transactional + marketing/marketing only) |
| Two-way provisioning | 40 days |
| Country regulations | Promo/marketing traffic is strictly regulated with the high penalties and restrictive measures for not following all regulations. More info: https://www.consumerprotection.govt.nz/general-help/consumer-laws/online-safety-laws-and-rules/. Opt-in and Opt-out options are required for promo/marketing messages and two-way communication. Sometimes, even if the client manages to submit a decent proof of Opt-In, the MNO's tend to ask for an immediate block of certain traffic content. Usually, gambling traffic (even from more established online services) tends to be blocked in these situations for the preservation of our connections. |
| Country restrictions | Spam, political, religious, and adult content is strictly forbidden. The Gambling Act of 2003 bans online gambling with the exception of some strictly regulated lotteries and sports betting games. The government of New Zealand has not prohibited the use of foreign gambling websites for its citizens and allows players to use them freely. The New Zealand Gambling Act nor any other New Zealand's law makes using overseas gambling websites a crime, but is illegal to advertise these websites and the penalty is $5,000 per offense. |
| Country recommendations | Infobip highly recommends not to send promo/marketing traffic on New Zealand. Namely, because of the strict regulations and situations where the supplier can lose expensive Short Codes in case of any unwanted traffic appears. |