# SAUDI ARABIA (SA)

Source: https://www.twilio.com/en-us/guidelines/sa/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Saudi Arabia |
| ISO code | The International Organization for Standardization two character representation for the given locale. | SA |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 420 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +966 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Saudi Arabian networks have implemented strong filtering that blocks messages coming from Numeric Sender IDs, messages that contain objectionable content, and messages that contain URLs. Messages sent with identical content to a recent message will also be blocked. To avoid the possibility of messages to users in Saudi Arabia being blocked, be sure to pre-register your Alphanumeric Sender IDs. Promotional messages should only be sent between 09:00am and 08:00pm local time. Messages sent to mobile numbers registered in the DND list will be filtered. Sending gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Messages containing WhatsApp/LINE chat links, and phone number in body are not allowed. Twilio is unable to register Sender IDs on behalf of domestic brands based in Saudi Arabia or Qatar because of a new regulation that prohibits the re-selling of domestic traffic. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | N/A | N/A |
| UCS-2 support | --- | Supported | N/A | N/A |
| Use case restrictions | --- | Starting from April of 2024, the network MOBILY has stopped supporting Promotional Sender ID Registration. Twilio will continue supporting this type of Registration only for the rest Saudi Arabian networks. If you use Alphanumeric Sender IDs for promotional purposes such as advertising or marketing, you must affix -AD to the Sender ID. For example, Twilio-AD instead of just Twilio. If you use an existing Alphanumeric Sender ID for transactional purposes, but choose to use it for promotional purposes too, then you have to register another Account SID and register a new Sender ID which will be dedicated to promotional traffic only. You must also affix -AD to the Sender ID: for example, Twilio-AD instead of just Twilio. Shortened URLs, adult content, and gambling or virtual gambling content is prohibited. Messages containing such content will be blocked, and the account may be blacklisted. Due to limitations related to the local infrastructure we suggest our clients to use UCS2 encoding when submitting messages containing the EURO symbol "€". | Twilio is unable to register Sender IDs on behalf of domestic brands in Saudi Arabia or Qatar due to a new regulation that prohibits the re-selling of domestic traffic. | N/A |
| Best practices | --- | URLs in the message content must first be allowlisted. Sending messages with URLs without adding them to an allowlist may result in delivery failure. If the requested Sender ID is different to the name of or not affiliated with the company requesting the Sender ID, you must submit documentation that proves the company is allowed to use the Sender ID’s brand name. For example, Twilio owns the brand ‘Authy’. When Twilio submits a registration request for Authy, it needs to provide a document which proves that Twilio owns the rights to use the Authy brand name. | N/A | Twilio requires customers to use a registered Alpha Sender ID in Saudi Arabia. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Twilio requires customers to use a registered Alpha Sender ID in Saudi Arabia. | N/A |

---

### Saudi Arabia

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Saudi Arabia Phone Number: No
- Saudi Arabia Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 22:00-08:00)

Additional Notes :

- This market has Local/International and Transactional/Promotional traffic segmentation
- Only international traffic supported
- For Promotional traffic: Sender name must start with prefix AD- (e.g., AD-YourBrand) Allowed only between 8AM-8PM (summer) or 8AM-7PM (winter) Messages sent outside allowed hours will be queued and delivered at 8AM Opt-out is automatically added Local enterprise clients need opt-ins from end users on operator's DND base Racism, sex, and alcoholic promo content is strictly forbidden
- For Transactional traffic: No time restriction (delivered instantly)
- Sender ID is case sensitive
- Letter of Authorization (LOA) and Certificate of Incorporation required for sender ID registration
- URL whitelisting is required

Opt-out Rules : No specific opt-out regulations

---

## saudi-arabia
| Key | Value |
| --- | --- |
| MCC | 420 |
| Dialing code | 966 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is a required. The needed documentation depends on traffic origin and network. Before you start sending any content towards KSA for the first time, contact your dedicated account manager or [Support](mailto:support@infobip.com) so they can set up a specific route for you. |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). |
| Sender availability | - Alphanumeric - Alpha |
| Sender provisioning | The average sender registration processing time depends solely on network providers. For local senders, it can take up to 30 days. For international senders, up to 15 days. |
| Two-way | No. |
| Two-way provisioning | / |
| Country regulations | A2P SMS traffic is divided into local and international and transactional and promotional. For local SMS termination, your company must have a local presence and provide documentation to prove this. |
| Country restrictions | Gambling, betting, SPAM, loan traffic, crypto, Forex, and adult content is likely to be blocked by the Saudi Arabian operators. URL shorteners (bit.ly, goo.gl etc) are strictly forbidden. Other URLs in the message content needs to be safelisted beforehand. You can send promotional traffic only between 8 AM and 10 PM local KSA timezone. Companies need to add a suffix -AD to the sender name when sending promotional traffic. |
| Country recommendations | Highly regulated country. Before you send any traffic towards Saudi Arabia, acquire all the necessary documentation to speed up registration and waiting time. For more details, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |
---