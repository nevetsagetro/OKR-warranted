# China (CN)

Source: https://www.twilio.com/en-us/guidelines/cn/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | China |
| ISO code | The International Organization for Standardization two character representation for the given locale. | CN |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 460 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +86 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | We recommend a maximum of 500 characters or 8 segments for UCS2 encoding for better delivery rate. |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Not Available |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Chinese networks have very strict regulations about the type of SMS content which can be sent to subscribers on their network. The networks impose heavy fines and cut off connections if these rules are breached. Customers that send messages to, from, and within China must follow all applicable laws and regulations. Broadly speaking, China messaging restrictions do not allow URLs in the content, content that is political, illegal, pornographic, fraudulent, or finance-related, including but not limited to marketing content from banks or insurance companies, loans, credit cards, securities, stocks, crude oil, futures, gold, and cryptocurrency. Restrictions include messages that violate basic principles of the China Constitution, the Ministry of lndustry and Information Technology’s “Nine Prevention Rules”, and the Ministry of Public Security’s “Five categories”. Twilio can deliver SMS to China on a best-effort basis, without guaranteed delivery. M2M Number Delivery Message delivery to Machine-to-Machine (M2M) numbers is on a best-effort basis only and is not guaranteed. General guidance Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | Overwritten | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Supported | N/A |
| Best practices | --- | N/A | Twilio can deliver SMS to China on a best-effort basis, without guaranteed delivery | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | N/A | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | Best Effort Delivery Only | N/A |
| Best practices | --- | N/A | Twilio can deliver SMS to China on a best-effort basis, without guaranteed delivery | N/A |

---

### China

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Long Code (Phone Number)
- Promotional SMS: Long Code (Phone Number)
- Two-Way Conversations: WeChat (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Note: Your sender ID will be changed by operators)
- China Phone Number: No
- China Short Code: No
- International Phone Number: Yes (Note: Your sender ID will be changed by operators)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- This market has Marketing and Transactional traffic segmentation
- Two-way SMS is not available
- Sender registration and content whitelisting is mandatory

Opt-out Rules : No specific opt-out regulations

---

## china
| Key | Value |
| --- | --- |
| MCC | 460 |
| Dialing code | 86 |
| Number portability | Yes |
| Concatenated message | Concatenated messages are supported. Unicode is a standard format with single message length of up to 70 characters. |
| Service restrictions | If you are planning to terminate messages to China for the first time, contact your dedicated account manager or [Support](mailto:support@infobip.com) because a specific set of regulations, especially regarding senders, needs to be met. Signature registration is needed for quality terminations. It is required for using two-way solutions. One numeric sender can have only one signature. It is strongly recommended to use a Chinese signature, as English signatures are highly likely to be rejected by suppliers. The signature must be consistent with the registered trademark, company name, or ICP filing to ensure compliance. |
| Service provisioning | 1-3 days to configure the default account setup, more if it is a specific setup, could depend on the supplier. |
| Sender availability | All originating senders will be manipulated into a VLN starting with 106. |
| Sender provisioning | The average sender registration (signature) process time is usually 1 week. |
| Two-way | LC/VLN |
| Two-way provisioning | It takes between 1 and 3 working days. |
| Country regulations | Signature and template safelisting is required (signature serves as a sender name and is usually displayed at the beginning of the message within []). Opt-out text "拒收请回复R" is by default added by Infobip, translated in English as "Reply R to unsubscribe". Customers can use a different opt-out message if the default one is not suitable. Check the details with your account manager or [Support](mailto:support@infobip.com). In accordance with the "Notice on Further Clarifying the Relevant Requirements for Port Short Message Services" and the "Implementation Rules for the Operation and Access Management of Port Short Message Services" issued by the Ministry of Industry and Information Technology which aims to safeguard the legitimate rights and interests of users and ensure effective governance. Effective immediately, Chinese telecom operators have implemented stricter content controls over SMS. Chinese networks, together with all administrative regions in China, are now directed to quickly enforce stringent regulations on SMS content, including cleaning and purifying the short message service market environment. Violations can result in heavy fines and disconnection. Customers sending messages to, from, or within China must comply with all applicable laws and regulations.  Generally, China messaging restrictions prohibit: - URLs in the content - Political, pornographic, or fraudulent content which is deemed illegal in China - Finance-related content, including any form or hint of marketing and or promotional messages from banks, insurance companies, loans, credit cards, securities, stocks, crude oil, futures, cryptocurrency, and gold - Marketing/promo traffic regarding real estate, stocks, loans, investment banking, education, immigration, politics, adult supplies, pornography, violence, gambling, and other illegal information - Messages that directly violate China's law and constitution - Any messages that can be considered harmful to its citizens' morality and public order - Any messages promoting gambling, alcohol, tobacco, and certain health products Due to the existing regulations, there is a possibility of traffic blocking occurring randomly and without prior notice. This may have an impact on legitimate and registered customer traffic. As a result of these potential disruptions, Infobip is committed to guaranteeing traffic on a best-effort basis. As for those getting blocked, we may at some point require you to provide supporting documents, including Chinese-issued documents as proof of business and economic activity in China. It is important to note that these regulations are subject to change at any time, and such changes could result in significant disruptions that may impact the reliability of our services. We understand the importance of maintaining seamless communication and are dedicated to ensuring minimal impact on our customers during such occurrences. |
| Country restrictions | Marketing/promo traffic regarding real estate, stocks, loans, investment banking, education, immigration, politics, adult supplies, pornography, violence, gambling and other illegal information is strictly prohibited. |
| Country recommendations | For reliable termination of SMS, registration is recommended along with signature and templates. To use two-way solutions, registration is a prerequisite. |