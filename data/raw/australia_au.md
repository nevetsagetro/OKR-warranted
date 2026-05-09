# Australia (AU)

Source: https://www.twilio.com/en-us/guidelines/au/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Australia |
| ISO code | The International Organization for Standardization two character representation for the given locale. | AU |
| Region | --- | Oceania |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 505 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +61 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in a given locale | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | Inbound: GSM 3.38=160, Unicode=70 Outbound: GSM 3.38=160, Unicode=70 |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Supported |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Effective April 25, 2023, dynamic Alphanumeric Sender IDs won’t be allowed in Australia. All Alphanumeric Sender IDs must be pre-registered to send messages in Australia. Messages sent using Alphanumeric Sender IDs that aren’t pre-registered by April 25, 2023 may be blocked. To pre-register with Twilio, head over to https://console.twilio.com/us1/develop/phone-numbers/sender-ids/applications/create to provide the necessary proof that you are entitled to use the Alphanumeric Sender ID and other documents. Message delivery to M2M numbers is on best effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to ensure they comply with all applicable laws. Sending gambling, firearms, and cannabus related content is strictly prohibited in Australia. Unsolicited Communication: All commercial electronic messages sent to an electronic address in Australia are beholden to the SPAM Act (2003). It is a partner’s responsibility to familiarize yourself with this legislation and ensure your compliance; the key rules relating to this can be found at https://www.acma.gov.au/theACMA/spam-industry-obligations and below: - Permission (consent)—messages can only be sent with the permission of the person who owns the account for the address (usually the recipient). - Identification—messages must contain the name and contact details of the person or business that authorized the message (sender identification). - Unsubscribe—messages must contain a low (or no cost) way for the recipient to stop getting messages (to ‘opt out’ or unsubscribe). The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 5 business days | N/A |
| UCS-2 support | --- | Supported | --- |
| Use case restrictions | --- | N/A | Only Alphanumeric Sender ID registered with Twilio will be allowed from 25 April 2023. All non-registered Alphanumeric Sender IDs will be blocked. |
| Best practices | --- | All customers must pre-register Alphanumeric Sender ID with Twilio, providing the necessary proof that they are entitled to use the Alphanumeric Sender ID | Only send from pre-registered Alphanumeric Sender IDs. Please review the Compliance Considerations for more details. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Australia

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: SMS with a two-way long number

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Australia Phone Number: Yes
- Australia Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-11:00)

Additional Notes : Registration required for Alphanumeric Sender IDs

Opt-out Rules : No specific opt-out regulations

---

## australia
| Key | Value |
| --- | --- |
| MCC | 505 |
| Dialing code | 61 |
| Number portability | Yes |
| Concatenated message | Standard |
| Service restrictions | Before you start sending messages towards Australia, reach out to your dedicated account manager or [Support](mailto:support@infobip.com) due to specific regulations. |
| Service provisioning | Available within 1 day. |
| Sender availability | Alpha, Virtual Long Number, Short Code |
| Sender provisioning | 1 working day. |
| Two-way | Available as VLN. |
| Two-way provisioning | Between 1 to 5 working days. The business does not need to have a local entity. |
| Country regulations | No specific regulations. |
| Country restrictions | No adult, religious, political, or gambling content. Gambling traffic restrictions are: - Anyone providing a regulated interactive gambling service in Australia must hold a license under Australian State or Territory laws. - Gambling promotional messaging is strictly prohibited to new users unless the user specifically opted-in with the gambling company prior to the actual SMS termination. - No inducement in the message content to get users to gamble – for both new or existing users. - Opt in/opt out functions are required for all promotional or transactional gambling messages. - Online sports betting is legal in Australia through licensed operators with numerous additional restrictions. - Online lotteries are legal, except for "instant-win" games. Promotional traffic must include an opt-out mechanism. Make sure to add it when sending such messages. For all additional restrictions, please contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Country recommendations | In the case of alphanumeric sender ID usage, prior to live traffic, the sender must be registered with ACMA **before 1 July 2026**. Any message sent using an unregistered sender ID will have the sender replaced with "Unverified". To register your sender, see [Australia registration guidelines](https://www.infobip.com/docs/essentials/australia-registration/australia-registration-guidelines). |