# Belgium (BE)

Source: https://www.twilio.com/en-us/guidelines/be/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Belgium |
| ISO code | The International Organization for Standardization two character representation for the given locale. | BE |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 206 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +32 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Gambling, Betting and Casino traffic is permitted only for licensed companies. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Required | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- |
| UCS-2 support | --- | --- | --- |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | Supported | --- | --- |
| Use case restrictions | --- | --- | Numeric sender ID would be overwritten with random shortcode or numeric sender ID to ensure delivery | --- |
| Best practices | --- | --- | --- | --- |

---

### Belgium

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Belgium Phone Number: Yes (Only if provided by Bird)
- Belgium Short Code: Yes (Note: All sender IDs will be converted to numeric by operators)
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- We recommend whitelisting sender IDs with support for different services
- Short URLs not supported
- Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules :

- Transactional traffic: Opt-out not required. Marketing content forbidden on transactional routes (penalty fees apply)
- Promotional traffic: Marketing content cannot be delivered to opted-out numbers

---

## belgium
| Key | Value |
| --- | --- |
| MCC | 206 |
| Dialing code | 32 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions to sending traffic towards Belgium. |
| Service provisioning | Sender provisioning should be available within a day, more if it's a specific setup. |
| Sender availability | Virtual Long Numbers and Short Codes. Alphanumeric senders are not allowed. |
| Sender provisioning | No sender registration needed. |
| Two-way | Virtual Long Numbers and Short Codes. |
| Two-way provisioning | The setup can take up to 6 weeks. |
| Country regulations | No specific country regulations. |
| Country restrictions | Regulatory authorities in Belgium block all alphanumeric originator/source address for all networks in Belgium. Alphanumeric senders are manipulated into Short Codes. |
| Country recommendations | No specific country recommendations. |