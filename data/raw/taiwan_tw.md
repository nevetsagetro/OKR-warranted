# Taiwan (TW)

Source: https://www.twilio.com/en-us/guidelines/tw/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Taiwan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | TW |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 466 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +886 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Content Compliance Requirements for SMS Delivery to Taiwan To reduce SMS scams, Taiwan’s National Communications Commission (NCC) has introduced measures that require SMS messages terminating in Taiwan to clearly include the sender’s company, organization, brand, or campaign name at the beginning of the message body. Example: Correct: [MyBrand] Your verification code is 123456.Also correct: MyBrand: Your verification code is 123456.Incorrect: Your verification code is 123456. To make sure your SMS (or your customer's SMS) terminating in Taiwan will not be blocked or uninterrupted, please: Submit your list of brand names for registration through this form. Ensure your Taiwan SMS templates are configured so the content of your messages begins with the same branding that you submitted on this form. If you need help with this process, please reach out to your account team or senderid@twilio.com. URLs (especially shortened URLs) is strictly prohibited in Taiwan. If your SMS content carries a URL, kindly reach out to Twilio Customer Support to get the full-length URL registered/allowlisted to prevent delivery failure. Sending firearms, gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Messages containing WhatsApp/LINE chat links are not allowed. Sender ID Compliance You may use an Alpha and numeric Sender ID to reach mobile phones in Taiwan. However, the Sender ID will be overwritten with a long code outside Twilio’s Platform. Delivery Report Only SMSC delivery reports are supported in Taiwan. Time Restrictions for Marketing and Promotional Messages Sending of promotional/marketing messages from 1230H - 1330H and 2100H until 0900H of the next day is prohibited. Additional Phone Numbers and Sender ID Guidelines Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | --- | You may use an Alphanumeric Sender ID to reach mobile phones in Taiwan. However, the Sender ID will be overwritten with a long code outside Twilio’s Platform. |
| Best practices | --- | --- | You may use an Alphanumeric Sender ID to reach mobile phones in Taiwan. However, the Sender ID will be overwritten with a long code outside Twilio’s Platform. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A | --- |
| UCS-2 support | --- | --- | Supported | --- |
| Use case restrictions | --- | --- | You may use a global SMS-capable number to reach mobile phones in Taiwan. However, the number will be overwritten with a long code outside Twilio’s Platform. | --- |
| Best practices | --- | --- | You may use a global SMS-capable number to reach mobile phones in Taiwan. However, the number will be overwritten with a long code outside Twilio’s Platform. | --- |

---

### Taiwan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: Line (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Note: Your sender ID will be changed to a random numeric sender ID by operators)
- Taiwan Phone Number: Yes (Note: Your sender ID will be changed to a random numeric sender ID by operators)
- Taiwan Short Code: Yes (Note: Your sender ID will be changed to a random numeric sender ID by operators)
- International Phone Number: Yes (Note: Your sender ID will be changed to a random numeric sender ID by operators)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes : URL whitelisting requirements:

- All SMS messages with URLs must be pre-approved
- The URL/domain must belong to a dedicated domain owned by the business (e.g., teamplus.com.tw, e8d.tw)
- Shared or free short URLs are not permitted (e.g., bit.ly, tinyurl, t.co, lihi1, goo.gl)

Opt-out Rules : No specific opt-out regulations

---

## taiwan

| Key | Value |
| --- | --- |
| MCC | 466 |
| Dialing code | 886 |
| Number portability | Yes |
| Concatenated message | Standard for English characters. If Chinese characters are used, maximum per message is 70 characters. Concatenated message is supported. |
| Service restrictions | Before you start sending messages towards Taiwan, contact your dedicated account manager or contact Support . to set up this specific route for you. |
| Service provisioning | 1-2 weeks to configure the default account setup; more if it is a specific setup (depending on the client's needs). |
| Sender availability | All originated senders will be manipulated to Virtual Long Number. |
| Sender provisioning | For more information contact your dedicated account manager or contact Support . |
| Two-way | Available as Virtual Long Number (dedicated and shared). |
| Two-way provisioning |  |
| Country regulations | Generic senders (for example, InfoSMS, GlobalSMS) are not allowed. All SMS messages that include URLs or phone numbers require prior safelisting approval. Contact your dedicated account manager or Support for content safelisting. |
| Country restrictions | Messages that contain or imply gambling, sexual, dating, political, criminal, spamming, or derogatory content are forbidden. All messages must start with the brand name. The brand name can be in any language but must use half-width characters. Full-width characters are not allowed. |
| Country recommendations | Message will be overwritten and manipulated into shared/dedicated VLN at operator side. |