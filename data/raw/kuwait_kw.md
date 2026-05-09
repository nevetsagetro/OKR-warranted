# Kuwait (KW)

Source: https://www.twilio.com/en-us/guidelines/kw/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Kuwait |
| ISO code | The International Organization for Standardization two character representation for the given locale. | KW |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 419 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +965 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required Learn more and register via the Console | Not Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 4 weeks | N/A | N/A |
| UCS-2 support | --- | Supported | N/A | Supported |
| Use case restrictions | --- | Include opt-in and opt-out instructions for all promotional and marketing messages. Promotional Sender IDs must contain the letters "AD" The following content is strictly prohibited: PoliticalGamblingAdultSPAM SMS message delivery to numbers registered in the Do-Not-Disturb (DND) registry is not supported. | N/A | Sender ID Registration is required in Kuwait. Messages submitted without a pre-registered Sender ID will be delivered on a best effort basis |
| Best practices | --- | N/A | N/A | Twilio strongly suggests registering an alphanumeric Sender ID in Kuwait |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Numeric sender ID towards the network Viva Kuwait would be rejected as it is not supported by the mobile operator and messages submitted with generic alphanumeric sender ID is likely to fail. Numeric sender ID to other networks in Kuwait would be overwritten with generic alphanumeric sender ID outside the Twilio platform and delivery would be attempted on best effort basis only. SMS message delivery to numbers registered in the Do-Not-Disturb (DND) registry is not supported. | N/A |
| Best practices | --- | N/A | Twilio strongly suggests registering an alphanumeric Sender ID in Kuwait | N/A |

---

### Kuwait

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Kuwait Phone Number: No
- Kuwait Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- STC network additionally supports local/international numeric and short code senders
- Sender registration is mandatory on all networks except STC

Opt-out Rules : No specific opt-out regulations

---

## kuwait
| Key | Value |
| --- | --- |
| MCC | 419 |
| Dialing code | 965 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is required for all networks. Generic senders are not allowed. There are few specific requirements that need to be fulfilled in order to register senders. To register sender as local, company HQ must be in Kuwait to be considered domestic. |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). Prior to sending traffic towards Kuwait, contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Sender availability | Alpha (registered, not dynamic) |
| Sender provisioning | Sender registration is mandatory. The average sender registration process time depends solely on network providers. Usually lasts up to 7 days. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | A2P SMS traffic is divided into local and international. (Only companies with HQ in Kuwait are considered as local companies.) Sender registration is mandatory for both local and international traffic. Different senders need to be used for different types of traffic (transactional/promotional). |
| Country restrictions | Gambling, betting as well as SPAM, loan traffic, Crypto, Forex, adult and political content is likely to be blocked by the Kuwait operators. No specific restrictions for promo SMS termination. |
| Country recommendations | Before you send any traffic towards Kuwait, acquire all the necessary documentation to speed up registration and waiting time. For more details, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |