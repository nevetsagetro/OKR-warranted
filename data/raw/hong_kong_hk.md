# Hong Kong (HK)

Source: https://www.twilio.com/en-us/guidelines/hk/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Hong Kong |
| ISO code | The International Organization for Standardization two character representation for the given locale. | HK |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 454 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +852 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Effective February 21, 2024, all customers can start using registered Alphanumeric Sender IDs with a hash (#) prefix, such as #twiliocorp, to send SMS messages to Hong Kong (see press release from the Office of the Communications Authority or OFCA). Please note that this does not impact SMS messages sent from Hong Kong domestic longcodes. To use Alphanumeric Sender IDs with a hash (#) prefix, you need to register it first by going on OFCA's website. After registering with OFCA, you need to register it with Twilio by following this link. Sending firearms, gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required for Alphanumeric Sender IDs without a hash (#) prefix There is no segregation between International and Domestic Traffic | Not Supported for China Mobile Hong Kong Supported for the rest of Hong Kong networks |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Not Supported for China Mobile Hong Kong Supported for the rest of Hong Kong networks Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes for the networks that Dynamic Alphanumeric is supported |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 18 days | N/A |
| UCS-2 support | --- | Supported | Supported for the networks that Dynamic is supported |
| Use case restrictions | --- | For Alphanumeric Sender IDs without a hash (#) prefix, registration is only required on mobile operator China Mobile Hong Kong, while other Hong Kong mobile operators support dynamic Alphanumeric Sender IDs. All customers can use registered Alphanumeric Sender IDs with a hash (#) prefix to send to all HK mobile operators starting on February 21, 2024. | The Hong Kong network China Mobile requires Sender ID registration. We advise Twilio's customers to register an Alpha Sender ID in Hong Kong for full country coverage. |
| Best practices | --- | Register your Alphanumeric Sender IDs without a hash (#) prefix with Twilio. Additionally, in an effort to combat SMS spoofing and phishing attacks, the Office of the Communications Authority (OFCA) in Hong Kong now recommends all customers to register their Alphanumeric Sender IDs with a hash (#) prefix. We’ve updated our registration process to comply with this recommendation. | Twilio advises customers to use a registered Alpha Sender ID in Hong Kong. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Not Supported for China Mobile Hong Kong Supported for the rest of Hong Kong networks | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | Supported for the networks that Dynamic is supported | N/A |
| Use case restrictions | --- | N/A | Numeric Sender ID is not supported by mobile operators in Hong Kong and would be overwritten with either a generic Alphanumeric Sender ID or a random domestic Numeric Sender ID. | N/A |
| Best practices | --- | N/A | Twilio advises customers to use a registered Alpha Sender ID in Hong Kong. | N/A |

---

### Hong Kong

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Hong Kong Phone Number: Yes (Note: Your sender ID will be changed to a generic sender by all networks)
- Hong Kong Short Code: Yes (Note: Your sender ID will be changed to a generic sender by all networks)
- International Phone Number: Yes (Note: Your sender ID will be changed to a generic sender by all networks)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules : No specific opt-out regulations

---

## hong-kong
| Key | Value |
| --- | --- |
| MCC | 454 |
| Dialing code | 852 |
| Number portability | Yes |
| Concatenated message | Standard for GSM, 70 for Unicode, concatenated messages supported. |
| Service restrictions | If you are planning to terminate messages to Hong Kong for the first time, contact your account manager or [Support](mailto:support@infobip.com) due to different sender regulations between many networks. |
| Service provisioning | 1 - 3 days. |
| Sender availability | Senders on most networks will be manipulated into numeric without registration. Alpha is available with registration. |
| Sender provisioning | 2 weeks. |
| Two-way | Available as Virtual Long Number. |
| Two-way provisioning | Up to 2 weeks. |
| Country regulations | Message templates and sender details should be shared with your account manager or [Support](mailto:support@infobip.com) to ensure the most suitable solutions are selected, aligning with various options and network regulations. There is a Do Not Call (DNC) list in Hong Kong. Messages to DND numbers will be delivered on a best-effort basis. For marketing traffic, it is mandatory that the message includes a phone number that allows the end user to unsubscribe. Organizations that register their SMS Sender IDs with OFCA's SMS Sender Registry can send SMS messages to local mobile service subscribers in Hong Kong using their registered Sender IDs with the "#" prefix. However, unregistered senders attempting to use the "#" prefix will be blocked. Visit the [OFCA's website](https://www.ofca.gov.hk/en/industry_focus/industry_focus/ssrs/index.html) for more details. |
| Country restrictions | Chinese symbols are not accepted as part of the sender name ID. |
| Country recommendations | No specific country recommendations. |