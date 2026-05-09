# South Korea (KR)

Source: https://www.twilio.com/en-us/guidelines/kr/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | South Korea |
| ISO code | The International Organization for Standardization two character representation for the given locale. | KR |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 450 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +82 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Long messages are no longer supported and will be delivered and displayed on the handset as multiple separate segments. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | One SMS segment can contain up to 140 bytes. This is equivalent to either 140 characters using the GSM 8-bit unpacked (commonly known as ASCII) encoding or 70 characters using the UCS2 16-bit encoding. |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | SMS messages toward South Korea would be automatically appended with [Web 발신] which means the message is A2P or [국제발신] which means the message is sent from abroad. Only numeric senderId is supported and it would be automatically prefixed with 009 or 006. Only EUC-KR characters are supported by the South Korean mobile operators so carefully review your content and only use characters that are on the list. Sending of adult and gambling related content is strictly prohibited. Message delivery to M2M numbers is on best-effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | N/A |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Please take note that international longcode would be appended with 009 or 006 as regulation by the mobile operators | N/A |

---

### South Korea

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: KakaoTalk (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Note: Your sender ID will be changed to a random numeric sender ID by operators)
- South Korea Phone Number: Yes (Note: Your sender ID will be changed to a random numeric sender ID by operators)
- South Korea Short Code: Yes (Note: Your sender ID will be changed to a random numeric sender ID by operators)
- International Phone Number: Yes (Note: Your sender ID will be changed to a random numeric sender ID by operators)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Opt-out Rules : No specific opt-out regulations

---

## south-korea  
| Key | Value |
| --- | --- |
| MCC | 450 |
| Dialing code | 82 |
| Number portability | Yes |
| Concatenated message | Different types of traffic (local and international) have their own settings. Reach out to your dedicated account manager or [Support](mailto:support@infobip.com) for more information. |
| Service restrictions | Before you start sending messages towards South Korea, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | 1 day to configure the default account setup, more if it is a specific setup (depending on the client's needs). |
| Sender availability | Virtual Long Number |
| Sender provisioning | Up to 7 days. |
| Two-way | Available VLN for local clients only. Special setup is applied. Contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Two-way provisioning | 2 weeks. The business needs to have a local entity. |
| Country regulations | There is a distinction between local and international traffic, as well as between SMS and LMS (long messages). Businesses operating in Korea can use the local route to send both SMS and LMS after completing sender registration. Separate commercials are applied. For marketing traffic, the SMS template must include the following opt-out information: 1. Insert (광고) at the beginning of the message. (광고) means advertisement. 2. Indicate the company name and add a contact number. If the contact number is the same as the sender’s number, it can be omitted. 3. Users need to be opted in before sending. 4. Add 무료거부/무료수신거부 - a free 10 digit opt-out number (080-XXX-XXXX) the end clients can use to opt out with a call. Example: 무료거부 080-XXX-XXXX or 무료수신거부 080-XXX-XXXX The 080 number needs to be purchased. It is not allowed to send marketing traffic from 9 pm to 8 am KR local time. |
| Country restrictions | Only numeric senders are allowed. Spam traffic is strictly forbidden. Content that includes gambling, illegal loans, adult/obscene material, unauthorized game of chance and medical ads without proper approval (for example, unauthorized procedures or clinics) are strictly illegal. |
| Country recommendations | No specific country recommendations. |