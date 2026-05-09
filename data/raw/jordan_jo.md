# Jordan (JO)

Source: https://www.twilio.com/en-us/guidelines/jo/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Jordan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | JO |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 416 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +962 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Operators Zain and Orange are currently blocking any generic Sender IDs. Pre-registered Sender IDs: Due to filtering for Zain, traffic needs to be pre-registered to ensure delivery. Application-to-Person (A2P): Carriers in Jordan have implemented spam filters to prevent A2P traffic from reaching their networks. Spam filters can return fake delivery receipts in some cases and don’t discriminate between spam and legitimate traffic. Marketing: When sending advertising/marketing messages, you are required to add the prefix “adv” before the Sender ID (for example, FROM=”adv xxxx”) to be compliant with the Telecom Regulation Commission of Jordan. You may not send these promotional messages after 9:00 PM Amman time (GMT+3). Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 12 days | 12 days | N/A |
| UCS-2 support | --- | Supported | Supported | Supported |
| Use case restrictions | --- | If you are using an Alphanumeric Sender ID for promotional purposes, you must add the prefix “adv” before the Sender ID (for example, FROM=”adv xxxx”) to be compliant with the Telecom Regulation Commission of Jordan. You cannot send promotional messages after 9:00 PM Amman time (GMT+3). Failure to adhere to this rule will result in messages being blocked and the potential denylisting of the account. | N/A | Jordan mobile operators do not support Dynamic Alphanumeric Sender ID and these are overwritten with a generic Alphanumeric Sender ID outside the Twilio platform to attempt delivery on a best-effort basis. |
| Best practices | --- | N/A | N/A | Twilio suggests using a pre-registered Sender ID in Jordan. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Jordan mobile operators do not support Numeric Sender ID and these are overwritten with a generic Alphanumeric Sender ID outside the Twilio platform to attempt delivery on a best-effort basis. | N/A |
| Best practices | --- | N/A | Twilio highly recommends pre-registering Alphanumeric Sender IDs to avoid blocking and filtering by mobile operators. | N/A |

---

### Jordan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Jordan Phone Number: Yes
- Jordan Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Promotional traffic: Only allowed from 7AM to 9PM local time
- SMS traffic is divided into local/international and transactional/promotional
- Two-way SMS is not available
- Gambling, betting, spam, loan traffic, crypto, forex, and adult content are likely to be blocked

Opt-out Rules : No specific opt-out regulations

---

## jordan

| Key | Value |
| --- | --- |
| MCC | 416 |
| Dialing code | 962 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration required only for local A2P SMS traffic. Required documentation depends on the traffic origin and network. Before you start sending traffic towards Jordan, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | Depends on sender provisioning time (depending on the network). |
| Sender availability | Alpha, alphanumeric with registration. |
| Sender provisioning | For local SMS traffic, up to 3 days. For international SMS traffic, sender registration is not required. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | General regulation: A2P SMS traffic is divided into local and international, and transactional and promotional. Allowed Send Time for promotional traffic: 7 AM to 9 PM local time. You can send only one advertising message per day per and brand is allowed for individual end user. Sender for promotional SMS termination needs to have the "ADV" prefix |
| Country restrictions | Gambling, betting as well as SPAM, loan traffic, crypto, Forex, and adult content is likely to be blocked by the operators. |
| Country recommendations | No specific recommendations. |