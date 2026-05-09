# Philippines (PH)

Source: https://www.twilio.com/en-us/guidelines/ph/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Philippines |
| ISO code | The International Organization for Standardization two character representation for the given locale. | PH |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 515 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +63 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Sender ID Compliance Sender ID Registration is required in the Philippines. Starting on April 07, 2025, messages with unregistered Sender IDs will be blocked. To continue sending messages, you must use a registered Alphanumeric Sender ID. Sender IDs containing the words “TEST”, “MESSAGE”, “SMS”, and/or permuations based on those words are not allowed. Sender IDs that portray other networks as “SMART” and/or “SUN” and/or permuations based on those words — for example, “SMARTMONEY”, “SUNCELL”, “SMARTLIVE”, “SMARTLOAD”, etc.) are not allowed. Content Compliance Requirements for SMS Delivery to the Philippines You may send commercial and promotional advertisements, surveys, and other broadcast/push messages only to subscribers who have specifically opted-in to receive such messages. PTEs and content providers shall also provide methods for subscribers who have opted-in to opt-out in the future. Regular opt-out instructions must be sent once per week for daily subscriptions or once per month for weekly subscriptions. Spam messages are those which promote or offer financial loans, real estate, products and services, and sometimes relate to elections and other political messages. Sending firearms, adult content, money/loan, political, religious, controlled substance, cannabis, tobacco, and alcohol related content is strictly prohibited. Content related to gaming and gambling is prohibited for all offshore gaming operators. It is permitted for registered Philippine Inland Gaming Operators (PIGO) and only when it is registered. Shortened URLs in message content are strictly not allowed, and customers sending banking related content with a URL must ensure that message templates are allow-listed. Sending a URL that is not allow-listed will result in message failure. Phone numbers in message content is also not allowed. URLs are not permitted when sending messages from Domestic Longcodes to the Philippines. If your message content includes a URL, it can only be delivered if the URL is registered and the message is sent using a registered Alphanumeric Sender ID. If you need to send URLs, learn more on how to register an Alphanumeric Sender ID via the Console. Delivery to M2M Numbers Message delivery to M2M numbers is on best effort basis only. Additional Phone Numbers and Sender ID Guidelines Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | 2 weeks | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | Messages that appear to be person-to-person (P2P) based on their content will be filtered. Sender IDs containing the words “TEST”, “MESSAGE”, “SMS”, and/or permuations based on those words are not allowed. Sender IDs that portray other networks as “SMART” and/or “SUN” and/or permuations based on those words are not allowed. See above for examples. Commercial and promotional advertisements, surveys, and other broadcast/push messages may be sent only to subscribers who have specifically opted-in to receive such messages. Messages sent must provide methods for subscribers who have opted-in to opt-out in the future. Regular opt-out instructions must be sent once a week for daily subscriptions and once a month for weekly subscriptions. Financial loans, real estate offers, product and service promotions, and political messages will be blocked. Adult content and any mention of alcohol, drugs, politics, and tobacco is prohibited. Content related to gaming and gambling is prohibited for all offshore gaming operators. It is permitted for registered Philippine Inland Gaming Operators (PIGO) and only when it is registered. | Messages that appear to be person-to-person (P2P) based on their content will be filtered. Sender IDs containing the words “TEST”, “MESSAGE”, “SMS”, and/or permuations based on those words are not allowed. Sender IDs that portray other networks as “SMART” and/or “SUN” and/or permuations based on those words are not allowed. See above for examples. Commercial and promotional advertisements, surveys, and other broadcast/push messages may be sent only to subscribers who have specifically opted-in to receive such messages. Messages sent must provide methods for subscribers who have opted-in to opt-out in the future. Regular opt-out instructions must be sent once a week for daily subscriptions and once a month for weekly subscriptions. Financial loans, real estate offers, product and service promotions, and political messages will be blocked. Adult content and any mention of alcohol, drugs, politics, and tobacco is prohibited. Content related to gaming and gambling is prohibited for all offshore gaming operators. It is permitted for registered Philippine Inland Gaming Operators (PIGO) and only when it is registered. | N/A |
| Best practices | --- | N/A | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | N/A | N/A |
| Use case restrictions | --- | You can only use local longcodes for 2-way messaging. URLs cannot be sent with Long code domestic sender ID. You must send it with a registered alphanumeric sender ID. If you need to send URLs, learn more on how to register an Alphanumeric Sender ID via the Console. | N/A | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Philippines

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Philippines Phone Number: No
- Philippines Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- This market has Local and International traffic segmentation
- Registered sender IDs are only valid within the validity period stated in the LOA
- Before end of validity period, customer must submit a new LOA with a new validity period
- URL whitelisting is required
- Letter of Authorization (LOA) is required for sender ID registration
- Online gambling content prohibited for all Offshore Gaming Operators, but permitted for Philippine Inland Gaming Operators (PIGO) under certain conditions

Opt-out Rules : No specific opt-out regulations

---

## philippines

| Key | Value |
| --- | --- |
| MCC | 515 |
| Dialing code | 63 |
| Number portability | No |
| Concatenated message | Standard, concatenated messages (long SMS) supported. |
| Service restrictions | Before you start sending messages towards the Philippines, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | 1 day to configure the default account setup, more if it's a specific setup (depending on client). |
| Sender availability | Alpha, Virtual Long Number, Short Code |
| Sender provisioning | The average sender registration process completion time depends solely on network providers. |
| Two-way | Available as Short Code (numbers are available for Globe and Smart networks). |
| Two-way provisioning | 20 days |
| Country regulations | Long SMS is limited to 3 messages, which amounts to 459 characters. |
| Country restrictions | Forbidden content: adult, alcohol, drugs, gambling, election, tobacco. Spam and scam messages are strictly forbidden. Any advertisement promoting nudity, profanity, violence, and substance abuse is illegal under Philippine Law. Additionally, operators block all SMS templates with URL Shorteners (short URLs), regardless of the client's industry, to protect subscribers from fraudulent attacks (it is recommended to use full URL format in SMS). |
| Country recommendations | For specific sender ID's it should be indicated if its promotional or transactional traffic. Avoid forbidden words related to adult, alcohol, drugs, gambling, election, and tobacco. Sending the same message 6 or more consecutive times to the same destination within an hour will be blocked. |