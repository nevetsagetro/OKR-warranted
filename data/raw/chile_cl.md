# Chile (CL)

Source: https://www.twilio.com/en-us/guidelines/cl/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Chile |
| ISO code | The International Organization for Standardization two character representation for the given locale. | CL |
| Region | --- | South America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 730 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +56 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | --- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to ensure they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Yes |
| Use case restrictions | --- | N/A | Alpha Sender ID would be overwritten with a random longcode outside the Twilio platform to ensure delivery |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | - Marketing messages are not allowed over domestic long codes - Political related messages are not allowed - Sending of 10 identical message within 60 seconds from the same domestic long code is not allowed - Sending of 10 messages within 60 seconds from the same domestic long code is not allowed -Concatenated messages are not supported over domestic longcodes | International longcode would be overwritten with a random longcode outside the Twilio platform to ensure delivery | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Chile

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Long Code (Phone Number)
- Promotional SMS: Long Code (Phone Number)
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Chile Phone Number: Yes
- Chile Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 21:30-10:30)

Additional Notes :

- Allowed SMS window: 8:30 AM to 7:30 PM local time
- Long Codes are strongly recommended for one-way traffic
- By default, all traffic will be changed to a Long Code unless a Short Code is specifically requested

Opt-out Rules : No specific opt-out regulations

---

## chile
| Key | Value |
| --- | --- |
| MCC | 730 |
| Dialing code | 56 |
| Number portability | Yes |
| Concatenated message | Standard. Long message supported over Short Code. |
| Service restrictions | There is a local/international traffic separation on some Chilean networks. Note that international traffic is more expensive. |
| Service provisioning | 1 day to configure the default account setup. More if it's a specific setup (depending on the client's needs). |
| Sender availability | Virtual Long Number and Short Codes. |
| Sender provisioning | Short Codes work immediately after route configuration. Virtual Long Numbers take 1 day to configure. |
| Two-way | - Virtual long numbers - Short code Both dedicated and shared options. |
| Two-way provisioning | Virtual Long Number takes 1 day to configuration. Request keyword registration for shared options is a must. Short Code provisioning may take up to 180 days. However, it's immediately available over a shared Short Code. |
| Country regulations | In Chile, there's a differentiation between local and international traffic. Chile has DND, requested by end user. ASTW: 8:30 AM to 7:30 PM. Messages with MNO names, financial, and other messages that are content sensitive must be carefully reviewed. Political, drug, alcohol content is forbidden. |
| Country restrictions | Political, drug, alcohol content is forbidden. |
| Country recommendations | If you plan to send local traffic, contact [Support](mailto:support@infobip.com) or your account manager to confirm that this type of content is considered local. |