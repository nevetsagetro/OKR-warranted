# Bulgaria (BG)

Source: https://www.twilio.com/en-us/guidelines/bg/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Bulgaria |
| ISO code | The International Organization for Standardization two character representation for the given locale. | BG |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 284 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +359 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | 4 weeks | N/A |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | No P2P traffic is allowed. Operators will not allow to register international brands SenderIDs as national even if they have local office/company in Bulgaria (Viber, Google, Microsoft etc) Marketing messages: Please notice that for Marketing traffic customers need to have end user approval and they also need to offer some kind of opt out procedure to end user through sms message (Telephone number or unsubscribe link or similar). This is mandatory. | N/A |
| Best practices | --- | N/A | Kindly check International versus Domestic Traffic | Dynamic Alphanumeric Sender IDs are not supported by A1 and Vivacom Bulgaria, and will be overwritten with a generic Alphanumeric Sender ID outside Twilio’s platform. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Dynamic Numeric Sender IDs are not supported and will be overwritten with a generic Alphanumeric Sender ID outside Twilio’s platform. | N/A |

---

### Bulgaria

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Bulgaria Phone Number: No
- Bulgaria Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- On A1 network (28401), only generic sender IDs are allowed
- Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules : No specific opt-out regulations

---

## bulgaria
| Key | Value |
| --- | --- |
| MCC | 284 |
| Dialing code | 359 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions when sending traffic towards Bulgaria. |
| Service provisioning | Sender provisioning should be available within a day, more if it's a specific setup. The process time could depend on the supplier. |
| Sender availability | - Alpha - Short Codes - Virtual Long Numbers. Generic sender is allowed. |
| Sender provisioning | The average sender registration process time depends solely on network providers and it can take up to 30 days. |
| Two-way | Virtual Long Numbers and Short Codes |
| Two-way provisioning | For SC it can take up to 3 months and for VLN is up to 2 weeks. |
| Country regulations | Marketing and transactional traffic are separated. As well as local from international traffic. Promo message must contain the opt-out or unsubscribe option. If the end user unsubscribes from any type of bulk message, it is mandatory to remove them from the recipient list. |
| Country restrictions | Gambling traffic info: The Gambling Act 2014 prohibits the direct advertising of gambling including unsolicited electronic messages containing information about gambling. "Direct advertising" is a defined term and means information distributed in any form and with any means whatsoever, which directly invites customers to take part in gambling games. Not allowed: - Creating the impression that by participating in the game the consumers may solve personal or financial problems or achieve well-being. - Inviting citizens to participate in the game with promises of big winnings. Allowed: - Names of the games. - Registered trade mark of the organizer. - Holding of the drawings (for example, lottery results). - Results of the games or winnings paid |
| Country recommendations | Marketing traffic must have the opt-out option within each message. The client, when sending messages to their customers/end users should add the opt-out option. |