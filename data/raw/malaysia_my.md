# Malaysia (MY)

Source: https://www.twilio.com/en-us/guidelines/my/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Malaysia |
| ISO code | The International Organization for Standardization two character representation for the given locale. | MY |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 502 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +60 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Domestic and International Routing Options Twilio supports SMS delivery to Malaysia through both International and Domestic gateways. For domestic customers, registration with Twilio is required before you are able to send through the domestic connections to Malaysia mobile operators. Messages are delivered using random approved domestic shortcodes. International customers do not need to register; messages are by default sent and delivered via international connections to Malaysia mobile operators. Messages are also delivered using random approved shortcodes. Content Compliance Requirements for SMS Delivery to Malaysia Malaysian mobile operators require the content header RM 0.00 to be added to every message sent to Malaysia. This header informs the receiving subscriber that they were not charged for receiving the SMS message. Sending your messages without this header will result in the content being truncated or the message failing entirely. You must also include your brand name to avoid blocking and filtering by mobile operators. Brand names in message content allow mobile operators to identify which organizations are sending messages to their subscribers. The Sender ID of A2P messages to Malaysia is overwritten with a Shortcode Sender ID. Effective September 1, 2024, all SMS messages sent to Malaysia that contain any of the following content in the message body will be blocked: Mobile or fixed-line phone numbers Requests for a person’s personal information (e.g. name, identification number, card number, bank account number, etc.) URLs Previously, customers could send SMS messages containing URLs and phone numbers if they were registered with Twilio before sending. Due to updated regulations to combat fraud, the Malaysian Communications and Multimedia Commission (MCMC) is now restricting the content of SMS messages sent to Malaysian mobile subscribers. In addition, sending firearms, gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. If you are a banking customer, please note that banking regulation restricts the use of SMS OTP in Malaysia. Please seek further advice from your banking regulatory experts about the implications this will have on your business in Malaysia. Time Restrictions for Marketing and Promotional Messages Sending marketing and promotional messages between 8PM to 8AM is prohibited. Concatenated Message Support in Malaysia Concatenated messages are supported by all mobile operators except Digi Malaysia which delivers them as multiple separate messages. Additional Phone Numbers and Sender ID Guidelines Per local regulations, only Person-to-Person (P2P) messages may be sent via Malaysian domestic long codes. If you can guarantee that you only send legitimate P2P messages, please reach out to Twilio Customer Services to ensure the proper domestic long code connectivity is enabled on your account. For Application-to-Person (A2P) messages, you can use any international long codes. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | 2 weeks | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Company has to put their brand name in the content. No generic SMS is allowed. Company has to put RM0 in front of the content e.g RM0 Your Twilio Verification code is 123456 | SenderID will be overwritten with a random operator-approved numeric senderID when the message gets sent to the Malaysian mobile networks. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | Malaysian long codes are limited to 200 messages per day per number and should only be used for Person-to-Person (P2P) messaging. Malaysian long codes will be delivered intact to the target handset. | N/A | N/A |
| Best practices | --- | N/A | SenderID will be overwritten with a random operator-approved numeric senderID when the message gets sent to the Malaysian mobile networks. | N/A |

---

### Malaysia

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Note: Your sender ID will be changed to a random short code by operators)
- Malaysia Phone Number: Yes (Note: Your sender ID will be changed to a random short code by operators)
- Malaysia Short Code: Yes (Note: Your sender ID will be changed to a random short code by operators)
- International Phone Number: Yes (Note: Your sender ID will be changed to a random short code by operators)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): Yes (Note: Your sender ID will be changed to a random short code by operators)

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-08:00)

Additional Notes :

- This market has Local and International traffic segmentation
- All SMS containing URLs and/or phone numbers will be completely blocked by operators, even if previously whitelisted

Opt-out Rules : No specific opt-out regulations

---

## malaysia
| Key | Value |
| --- | --- |
| MCC | 502 |
| Dialing code | 60 |
| Number portability | Yes |
| Concatenated message | Concatenated messages are supported for all networks except DiGi. |
| Service restrictions | If you are planning to terminate messages to Malaysia for the first time, get in touch with your account manager or [Support](mailto:support@infobip.com) so they can set up a specific route. |
| Service provisioning | A few days to configure the default account setup, more if it is a specific setup. |
| Sender availability | Short Codes |
| Sender provisioning | Sender registration process time depends solely on network providers. |
| Two-way | Available as Short Code (dedicated and shared). |
| Two-way provisioning | Short Codes registration process can last up to 2 months (depends on the mobile network operator) with an applicable setup fee and monthly fee. Shared Short Code can be ready in a day or two. |
| Country regulations | The Malaysian telecommunications regulator (MCMC) has announced that, starting September 1, 2024, all SMS messages, whether person-to-person (P2P) or application-to-person (A2P), containing URLs or phone numbers will be completely blocked. Due to Malaysian network regulations, the string "RM0" is added to the beginning of the message text to inform the recipient that the message is free to receive. It is also necessary to include the brand name in all SMS content to comply with the MCMC guidelines. All SMS messages must begin with `RM0 [brand] [message]`. The length of a single SMS is 153 characters. Flash SMS is not supported. DND is not enabled. Opt-out and ASTW are not mandatory. |
| Country restrictions | Spam, phishing, gambling, religious, adult, and racial content is strictly prohibited by law. All traffic must include company name/brand/identity in the SMS content, otherwise the sender faces a penalty imposed by the operator. |
| Country recommendations | No specific country recommendations. |