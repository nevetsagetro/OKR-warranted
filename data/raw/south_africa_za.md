# South Africa (ZA)

Source: https://www.twilio.com/en-us/guidelines/za/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | South Africa |
| ISO code | The International Organization for Standardization two character representation for the given locale. | ZA |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 655 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +27 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Direct marketing messages are regulated under article 16 of the Wireless Application Service Providers’ Association (WASPA) Code of Conduct. Unless a consumer has expressly or implicitly requested or agreed otherwise, marketing messages should not be sent on: Sundays and public holidays; Saturdays before 9am and after 1pm; and all other days between the hours of 8pm and 8am the following day. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | N/A |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | Domestic numbers are not able to receive inbound messages from the Grapevine network in South Africa. | International longcode sender ID would be overwritten into a random local longcode outside Twilio's platform. | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### South Africa

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- South Africa Phone Number: No
- South Africa Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : This market has Local and International traffic segmentation

Opt-out Rules : No specific opt-out regulations

---

## south-africa
| Key | Value |
| --- | --- |
| MCC | 722 |
| Dialing code | 27 |
| Number portability | Yes |
| Concatenated message | Yes |
| Service restrictions | If you are planning to terminate messages to South Africa for the first time, get in touch with your account manager or [Support](mailto:support@infobip.com) because a specific route setup is required. |
| Service provisioning | 1 day to configure the default account setup, more if it's a specific setup (depending on the client's needs). |
| Sender availability | Virtual Long Numbers are used to deliver SMS to all networks in South Africa. Alpha senders available on demand (subject to registration) only to MTN. |
| Sender provisioning | The average sender registration process completion time depends solely on network providers and exceeds 24 hours |
| Two-way | Virtual Long Number and USSD |
| Two-way provisioning | Up to 2 months. |
| Country regulations | There are several restrictions that need to be taken into consideration when dispatching traffic to South Africa. Rules for opting in and opting out are particularly important: Opt-in In terms of WASPA (https://waspa.org.za/), obligatory opt-in is required before consumers/end users receive marketing communications and must always be able to manage their opt-in status. Opt-out In terms of Consumer Protection act in South Africa an opt-out message must be included in all marketing communications (i.e., ""reply with STOP to 12345""). " The cost of the response needs to be made clear to the recipient. |
| Country restrictions | Since South Africa is highly regulated market. - Time restriction (ASTW is implemented), - Sender ID restrictions - local numbers are used, - Opt-in and opt-out, - DND list (this list is checked for marketing messages before sending). ASTW is implemented and it is not allowed to send in this time frame: - At the consumer’s home on Sundays or public holidays; - On Saturdays before 9:00 AM and after 1:00 PM; - On Mondays to Fridays before 8:00 AM and after 8:00 PM. Do not contact list is implemented in South Africa. It allows the end users to register their phone number on the regulator DND list on a weekly basis to block receiving direct marketing messages. |
| Country recommendations | OTP traffic is allowed, regardless of the traffic type (promotional vs. transactional). Promotional gambling traffic is forbidden. |