# Kazakhstan (KZ)

Source: https://www.twilio.com/en-us/guidelines/kz/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Kazakhstan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | KZ |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 401 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +7 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries.Gambling content is not allowed.Religious content is not allowed. Strict enforcement of the Law “On Advertising” in Kazakhstan prohibits sending promotional SMS related to bookmakers, sweepstakes, and totalizators. Sending this type of traffic may result in regulatory action including fines, penalties and sanctions which may lead to action taken on your account, pursuant to our Terms of Service and accompanying documents and guides available in the folllowing links: [https://www.twilio.com/en-us/legal/tos https://www.twilio.com/docs] |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | N/A |
| UCS-2 support | --- | Supported | N/A |
| Use case restrictions | --- | You may only send promotional and marketing messages if end-users have provided their prior written consent to receive these messages, i.e., they have actively opted into your service. Unsolicited messages will not be sent. You should not contact any users on the do-not-call registry. There is a policy of stopping traffic to operators Tele 2 (40177) and Altel (40107), according to which a “curfew” is imposed to ban the sending of advertising traffic from 22:00 to 9:00 local time (GMT +6). | N/A |
| Best practices | --- | N/A | Sender ID registration is required in Kazakhstan. We highly recommend our customers use pre-registered Alphanumeric Sender IDs. Delivery over Numeric Sender ID will be attempted on a best-effort basis. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | --- | N/A |
| Best practices | --- | N/A | Sender ID registration is required in Kazakhstan. We highly recommend our customers use pre-registered Alphanumeric Sender IDs. Delivery over Numeric Sender ID will be attempted on a best-effort basis. | N/A |

---

### Kazakhstan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Kazakhstan Phone Number: No
- Kazakhstan Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 21:00-09:00)

Additional Notes :

- Promotional traffic: Only allowed between 9AM and 9PM (GMT +6) on K'Cell network
- Sender registration is mandatory on all Kazakhstan networks

Opt-out Rules : No specific opt-out regulations

---

## kazakhstan

| Key | Value |
| --- | --- |
| MCC | 401 |
| Dialing code | 7 |
| Number portability | Yes |
| Concatenated message | Standard |
| Service restrictions | Traffic is split based on origination on all networks. T2 and Alter have an additional split on transactional, service, and advertising traffic. |
| Service provisioning | Sender registration is required. |
| Sender availability | - Alpha - Short Codes - Some MNOs (generics) |
| Sender provisioning | The average sender registration process completion time depends solely on network providers and exceeds 24 hours. |
| Two-way provisioning | Setup can take around 1 month. Available for local entities only. |
| Country regulations | Local traffic (all operators): - Night-time restrictions apply. - Opt-ins are mandatory. - ASTW implemented: 09:00 AM - 09:00 PM (local connections). International traffic (**Tele2** and **Altel only**): ASTW applies from 09:00 to 21:00 local time (GMT+6). From 21:00 until 09:00, as well as on weekends and holidays, SMS may only be sent in these cases: - When the end user requests an OTP within the specified period. - When the end user has explicitly requested to receive the information at that time. Penalty of 1,000,000 KZT may be applied by the MNO, but only if the operator receives a direct end-user complaint. From June 2025 , for both one-way and two-way traffic, it is strictly prohibited to send any advertising related to gambling or betting over SMS. Violating this rule may result in penalty fines and the risk of service termination. |
| Country restrictions | Sender provisioning. |
| Country recommendations | Only registered senders are allowed. Note that there is a separation into local and international traffic. International traffic is forbidden on local connections due to big fines. Get the opt-in consent from each end user before sending any traffic to them, particular for marketing or other non-essential communications. |