# Thailand (TH)

Source: https://www.twilio.com/en-us/guidelines/th/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Thailand |
| ISO code | The International Organization for Standardization two character representation for the given locale. | TH |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 520 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +66 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Sender ID Compliance Sender ID Registration is required in Thailand. The enforcement of complete blocking of unregistered Sender IDs in Thailand is on October 06, 2025. Twilio highly recommends sending from a registered Alphanumeric Sender ID to avoid having your messages blocked. Content Compliance Requirements for SMS Delivery to Thailand If your SMS content carries a URL, please contact senderid@twilio.com to get the full-length URL registered/allowlisted in connection with your Sender ID to prevent delivery failure. Shortened URLs are considered prohibited content in Thailand and can not be registered/allowlisted. Thailand's telecom regulator has very strict regulations about the type of SMS content which can be sent to mobile subscribers. They may impose heavy fines and cut off connections if these rules are breached. Customers that send messages to Thailand must follow all applicable laws and regulations and must avoid sending firearms, gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content. Customers in bank and financial services should not send messages containing URLs. In addition, authorities in Thailand apply URL criteria, which customers will need to follow to be compliant with local regulation/avoid the blocking of SMS containing URL. This criteria includes: (a) URLs must direct users to legitimate and verified destinations; (b) URLs must not lead to interactive platforms (such as direct download sites, or forms requiring user input); and (c) the purpose of the URL must be transparent and lawful. Time Restrictions for Marketing and Promotional Messages Sending marketing and promotional messages between 9PM to 9AM is prohibited. Additional Phone Numbers and Sender ID Guidelines AIS in Thailand has a feature that prevents subscribers from receiving SMS from non-Thai numbers. Customers can opt-out of this feature by dialing *137. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: 1. Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications. 2. Only communicate during an end-user’s daytime hours unless it is urgent. 3. SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language. 4. Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required Learn more and register via the Console | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | N/A |
| UCS-2 support | --- | Supported | --- |
| Use case restrictions | --- | Customers who intend to register and send loan related content must be able to provide a license from the Bank Of Thailand. | N/A |
| Best practices | --- | Local network operators tend to deactivate Sender IDs which were registered in the past but are not used for a considerable period of time. We suggest our clients to make sure that they keep sending traffic periodically to the specific destination once they register their Alpha Sender IDs. If the Sender ID is deactivated due to inactivity then the customer needs to reinitiate the registration procedure. | Twilio suggests using a pre-registered Alphanumeric Sender ID in Thailand. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | National Broadcasting and Telecommunications Commission of Thailand (NBTC) requires URLs in all A2P message content to be registered. | N/A | N/A |
| Best practices | --- | N/A | Twilio suggests using a pre-registered Alphanumeric Sender ID in Thailand | N/A |

---

### Thailand

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: Line (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Thailand Phone Number: No
- Thailand Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes (21:00-09:00)

Additional Notes :

- Sender ID is case sensitive and must match brand name or company name
- DND blocking enabled
- Strictly no political, religious, racial, unsolicited promotion, adult, part-time, gambling, fake loan, fake job or fake crypto content

Opt-out Rules : No specific opt-out regulations

---

## thailand
| Key | Value |
| --- | --- |
| MCC | 520 |
| Dialing code | 66 |
| Number portability | Yes |
| Concatenated message | Standard (70 for unicode Thai). Concatenated messages supported - 3 SMS (201 Thai character, 459 English characters). |
| Service restrictions | Gambling, phishing, and spam traffic are not allowed. |
| Service provisioning | Immediate availability after the account and route configuration is set up. |
| Sender availability | Alpha and numeric (Thailand number) senders are supported. Note that all senders need sender registration and URL safelisting before sending traffic. |
| Sender provisioning | Sender registration process is usually done within 7 working days. |
| Two-way | Available. VLN and SC through AIS. VLN is already tested and we have working numbers. |
| Two-way provisioning | It can take up to 30 days. |
| Country regulations | DND exists. The opt-out process is managed by the mobile network operator (MNO), where each subscriber can choose not to receive promotional messages by dialing a short number and selecting the opt-out option. Thailand National Broadcasting and Telecommunications Commission (NBTC) has announced that all SMS traffic containing URLs must be submitted for safelisting along with the sender IDs before being sent to Thailand. Any messages with non-registered URLs will be blocked from reaching the end users. The regulation will take effect on February 1st, 2025. |
| Country restrictions | Gambling, phishing, and spam traffic are not allowed. |
| Country recommendations | For larger traffic campaigns, we recommended you contact your dedicated account manager or [Support](mailto:support@infobip.com) to secure optimal TPS and quality. As Thailand has DND registry, OTP traffic senders need to be internally approved. |