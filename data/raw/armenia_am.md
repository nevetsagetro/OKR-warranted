# Armenia (AM)

Source: https://www.twilio.com/en-us/guidelines/am/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Armenia |
| ISO code | The International Organization for Standardization two character representation for the given locale. | AM |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 283 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +374 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | SMS cannot be sent to landline destination number. The Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications. Only communicate during an end-user’s daytime hours unless it is urgent. SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language. Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | Person-To-Person (P2P) messages are prohibited and will be blocked/filtered by mobile operators. Content related to gambling, politics, drugs, or pornography and adult material is forbidden. | Person-To-Person (P2P) messages are prohibited and will be blocked/filtered by mobile operators. Content related to gambling, politics, drugs, or pornography and adult material is forbidden. |
| Best practices | --- | N/A | Using Generic Sender IDs to send to the networks Beeline and Vivacell is not supported. The sender ID will be overwritten with an Alphanumeric Sender ID outside the Twilio platform. Delivery will be attempted on a best-effort basis only. Twilio highly recommends sending messages with pre-registered Alphanumeric Sender IDs. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Person-To-Person (P2P) messages are prohibited and will be blocked/filtered by mobile operators. Content related to gambling, politics, drugs, or pornography and adult material is forbidden. | N/A |
| Best practices | --- | N/A | Using Numeric Sender IDs to send to the networks Beeline and Vivacell is not supported. The sender ID will be overwritten with an Alphanumeric Sender ID outside the Twilio platform. Delivery will be attempted on a best-effort basis only. Twilio highly recommends sending messages with pre-registered Alphanumeric Sender IDs. | N/A |

---

## armenia

| Key | Value |
| --- | --- |
| MCC | 283 |
| Dialing code | 374 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is required for local traffic only. |
| Service provisioning | 3 days to configure the default account setup. More if it's a specific setup (it could depend on the supplier). |
| Sender availability | Alphanumeric |
| Sender provisioning | The average sender registration time depends solely on network providers and exceeds 24 hours. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | No specific country regulations. |
| Country restrictions | Political content is forbidden. Infobip does not have coverage over Karabakh Telecom network from region Naghorno Karabakh. |
| Country recommendations | No specific country recommendations. |