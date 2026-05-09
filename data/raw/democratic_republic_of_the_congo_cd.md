# Democratic Republic of the Congo (CD)

Source: https://www.twilio.com/en-us/guidelines/cd/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Democratic Republic of the Congo |
| ISO code | The International Organization for Standardization two character representation for the given locale. | CD |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 630 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +243 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A |
| UCS-2 support | --- | --- | Supported |
| Use case restrictions | --- | --- | Generic Alphanumeric Sender IDs, such as InfoSMS, INFO, Verify and Notify, should be avoided. |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A | --- |
| UCS-2 support | --- | --- | Supported | --- |
| Use case restrictions | --- | --- | --- | --- |
| Best practices | --- | --- | Numeric Sender IDs are not supported by Airtel network. Messages submitted with a Numeric Sender ID towards subscribers of this network will not be delivered. Twilio suggests using an Alphanumeric Sender ID for this country. | --- |

---

## democratic-republic-of-the-congo
| Key | Value |
| --- | --- |
| MCC | 630 |
| Dialing code | 243 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | There's traffic differentiation based on origin on certain networks. Sender registration is required for traffic with local origin (for major networks). Before you start sending any content towards Democratic Republic of the Congo for the first time, contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Service provisioning | Depending on the traffic origin and operator, service provisioning might take from 1 day, up to 1 week. |
| Sender availability | Local traffic registration is required on the major networks. Maximum length is 11 characters with no special characters, numbers are not allowed. |
| Sender provisioning | The average sender registration process time depends solely on network providers and can take up to 1 week. |
| Two-way | No two-way services are available for local traffic only and only through Short Code. Other details available upon request. |
| Two-way provisioning | Reach out to your dedicated account manager or [Support](mailto:support@infobip.com) for more information. |
| Country regulations | No specific regulations for A2P messaging. |
| Country restrictions | No specific restrictions. |
| Country recommendations | Before you start sending local-origin traffic to the Democratic Republic of the Congo, register you senders to avoid failing traffic. For additional info, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |