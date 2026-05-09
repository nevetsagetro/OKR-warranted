# France (FR)

Source: https://www.twilio.com/en-us/guidelines/fr/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | France |
| ISO code | The International Organization for Standardization two character representation for the given locale. | FR |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 208 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +33 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | Inbound: GSM 3.38=160, Unicode=70 Outbound: GSM 3.38=160, Unicode=70 |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Marketing SMS traffic can be sent between 8am and 10pm on working days. If messages are sent outside these times they will be queued and sent at an appropriate time The use of URL shorteners such as bit.ly or tiny.url is strictly forbidden in France, and may trigger SMS filtering and fines from the operator for non compliance. Twilio recommends that customers use the full, unshortened form of URLs to ensure message delivery. Sending adult content, controlled substance, and cannabis related content is strictly prohibited. As part of the new Telemarketing law in France, from July 1, 2025, organizations are prohibited from contacting customers by SMS for the aim of offering services, selling equipment or carrying out work relating to housing with a view to achieving energy savings, producing renewable energy or adapting them to aging or disability. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to ensure compliance with all applicable laws and the requirements of AF2M's Code of Conduct (https://af2m.org/charte-business-messaging/). The table below provides some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.SMS marketing campaigns must support HELP/STOP messages and similar keywords in the end-user’s local language. In France, including a web link in the message is also an acceptable method for OPT-OUT. The use of a mobile phone number as an opt-out mechanism is strictly forbidden and may result in fines from operators for non-compliance.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | Alphanumeric sender IDs containing special characters are strictly forbidden and may result in non delivery and fines from operators for non-compliance. For some sensitive Sender IDs, French mobile operators may ask for Letter Of Authorization to prove the legitimacy of traffic coming in from Twilio. Messages submitted to the NRJ Mobile and Truephone networks will be overwritten with random shortcodes outside the Twilio platform. |
| Best practices | --- | N/A | You must use Alphanumeric Sender IDs to send A2P messages. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 8-10 |
| UCS-2 support | --- | Supported | Supported | Supported |
| Use case restrictions | --- | Refer to our Regulatory Guidelines for Prescribed/Prohibited use cases. | French mobile operators do not support message delivery via international Numeric Sender ID. Submission by International Long Codes will be attempted on a best-effort basis. The Long Code will be overwritten with a generic Alphanumeric Sender ID or Short Code outside the Twilio platform. | Refer to our FAQs for short code best practices. |
| Best practices | --- | N/A | You must use Alphanumeric Sender IDs to send A2P messages | Refer to our FAQs for short code best practices. |

---

### France

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- France Phone Number: No
- France Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: Yes (Monday-Saturday 22:00-08:00 and all days on Sunday and during French public holidays)

Additional Notes :

- For NRJ Mobile network (20826), all sender IDs will be changed to short codes
- Messages sent during quiet hours will be queued and delivered during open hours
- Short URLs not supported
- Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules :

- Transactional traffic: Opt-out not required. Open 24/7
- Promotional traffic: Must include opt-out method. Only accepted method is texting "STOP xxxxx" or "STOP au xxxxx" (where xxxxx will be the short code set by the operator)

---

## france

| Key | Value |
| --- | --- |
| MCC | 208 |
| Dialing code | 33 |
| Number portability | Yes |
| Concatenated message | Standard, concatenated messages supported. |
| Service restrictions | No specific restrictions. |
| Service provisioning | 1 day to configure the default account setup, more if it is a specific setup (it could also depend on the supplier). |
| Sender availability | Dynamic alpha (except on NRJ Mobile), Short Code, and Virtual Long Number. |
| Sender provisioning | No sender registration needed. |
| Two-way | Available two-way setup: - Virtual Long Number - Short Code (dedicated/shared) |
| Two-way provisioning | VLN and shared SC can be ready in a day or two. Dedicated SC setup can take up to 4 months (because the number needs to be registered on all networks and special gateway should be created on each network). |
| Country regulations | In France, you are not allowed to send marketing traffic: on Sundays, during French holidays, and between 9:30 PM and 8 AM on other days. Marketing traffic must have an opt-out option within a text message. The opt-out option will be added automatically to all marketing messages, if not already done so by the client. |
| Country restrictions | There is a differentiation between promotional, transactional traffic, and ASTW. Adult and gambling traffic is forbidden. All promo messages must have an opt-out option. All connections allow alpha senders, except NRJ mobile (SC only). Due to new country regulations in France, starting January 1, 2025, the use of alphanumeric senders will be restricted. Sender names containing spaces or special characters will no longer be allowed. |
| Country recommendations | No specific country recommendations. |