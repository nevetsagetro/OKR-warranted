# Argentina (AR)

Source: https://www.twilio.com/en-us/guidelines/ar/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Argentina |
| ISO code | The International Organization for Standardization two character representation for the given locale. | AR |
| Region | --- | South America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 722 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +54 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications. Only communicate during an end user's daytime hours unless it is urgent. SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language. Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | Local networks do not support dynamic Sender ID. Messages will be delivered with random shortcode outside the Twilio platform. |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 6-15 weeks |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | N/A | Refer to our FAQs for short code best practices. |
| Best practices | --- | N/A | Local networks do not support dynamic Sender ID. Messages will be delivered with random shortcode outside the Twilio platform. | Refer to our FAQs for short code best practices. |

---

### Argentina

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Short Code
- Promotional SMS: Short Code
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Argentina Phone Number: Yes
- Argentina Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Generic Sender IDs are not allowed; registration is mandatory
- Content restrictions: Gambling, political, and adult content is forbidden
- Mobile operators block promotional messages from other operators to their subscribers
- Messages with operator names are flagged as spam
- Messages containing bank and mobile operator names will be flagged as spam

Opt-out Rules : No specific opt-out regulations

---

## argentina
| Key | Value |
| --- | --- |
| MCC | 722 |
| Dialing code | 54 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | The traffic is separated into local and international. International traffic is a bit more expensive. |
| Service provisioning | Immediately available once account and route configuration is set up. |
| Sender availability | Short Code (dedicated or shared) |
| Sender provisioning | Shared: immediately after account and route setup is done. Dedicated: up to 3 months. |
| Two-way | Short Codes (dedicated or shared) |
| Two-way provisioning | 1-2 days for shared, up to 3 months for dedicated. |
| Country regulations | Messages containing bank and mobile operators names will be identified as spam so avoid using those names. |
| Country restrictions | Gambling and political traffic and messages containing adult content is forbidden. Mobile operators do not allow promotional messages from other operators to be delivered to their subscribers. Messages with operator names are identified as spam. |
| Country recommendations | Use international format for destination numbers, do not add 9 or 15. If you are unsure whether your traffic is considered local, contact [Support](mailto:support@infobip.com) or your account manager before you start sending messages. |