# Kenya (KE)

Source: https://www.twilio.com/en-us/guidelines/ke/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Kenya |
| ISO code | The International Organization for Standardization two character representation for the given locale. | KE |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 639 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +254 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Required | Not Supported for Kenya Safaricom Supported for the rest of Kenyan networks |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Not Supported | Not Supported for Kenya Safaricom Supported for the rest of Kenyan networks |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A | Yes for the networks that Dynamic Alphanumeric is supported |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 4 weeks | N/A | N/A |
| UCS-2 support | --- | Supported | N/A | Supported for the networks that Dynamic Alphanumeric is supported |
| Use case restrictions | --- | Kenya operates an opt-in policy, and you must be able to demonstrate your users have chosen to receive messages from you. The following content is not allowed: AdultPoliticalGamblingPerson-to-person (P2P) messaging Additionally subscribers are allowed to opt-out of all promotional broadcast or per sender ID so promotional messages sent to those subscribers will fail. | N/A | The largest Kenyan network (Safaricom) requires Sender ID registration. We advise Twilio's customers to register an Alpha Sender ID in Kenya for full country coverage. |
| Best practices | --- | Generic Alphanumeric Sender IDs, such as InfoSMS, INFO, Verify, Notify, etc., should be avoided. | Customers with Domestic Traffic are welcome to register their Sender IDs are International ones | Twilio advises customers to use a registered Alpha Sender ID in Kenya. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | N/A | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Twilio advises customers to use a registered Alpha Sender ID in Kenya. | N/A |

---

### Kenya

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Kenya Phone Number: No
- Kenya Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : Certificate of Incorporation or business license is required for sender ID registration

Opt-out Rules : No specific opt-out regulations

---

## kenya
| Key | Value |
| --- | --- |
| MCC | 639 |
| Dialing code | 254 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | There's traffic differentiation based on origin (local or international). For sending local or international traffic, you need to register and file proper documentation. Note that there are setup and monthly fees for each registered sender. If you send both promotional and transactional content, you cannot use the same sender. Before you start sending traffic towards Kenya, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |
| Service provisioning | Depending on the traffic origin and operator, service provisioning might take from 1 day up to 1 week. |
| Sender availability | Local traffic registration is required on all networks. Maximum length of 11 characters including special characters, numbers are not allowed. You need an authorization letter. The sender name needs to match the name of the company/person (initials allowed). Otherwise you need a brand/trademark certificate. There are special requirements for political, betting and natural person/private person name senders (notarized ID required). For international traffic, you need a sender ID registration. The authorization letter might be required as well. Operator's registration fees apply. |
| Sender provisioning | The average sender registration process time depends solely on network providers and can take up to 1 week. |
| Two-way | Standard, zero rated and premium |
| Two-way provisioning | Local entity is required for the setup of Short Codes. It can take up to 2 weeks provisioning time |
| Country regulations | A2P messaging is differentiated based on its origin (local or international). Special rates apply for international traffic. Marketing traffic is allowed between 8:00 AM - 6:00 PM only. Generic sender IDs are forbidden. Gaming and political traffic require additional attention and approvals from operators. Necessary DND register (enables subscribers to opt out form receiving any kind of promotional content) for promotional messages. Necessary "Allowed send time window" which prohibits sending promotional content between 8:00 PM to 6:00 AM. Note that promotional messages have to have an opt out so subscribers can limit receiving promotional content. Because of this, the length of a single SMS is reduced to 150 characters (rather than the default 160). This means additional charges will apply if the dispatched SMS is longer than 150 characters. There's a DND register set up for promotional message types.This DND register enables subscribers to opt out form receiving any kind of promotional content. There is also an "Allowed send time window" which prohibits sending promotional content from 8 PM to 6 AM. For Safaricom, each client will be required to confirm they have validated databases and that subscriber consent has duly been obtained prior to sending targeted promotional messages by submitting either of the following: - Sign up forms with confirmation to receive promo traffic - App with Opt in/out capability - Consent of terms of conditions with clause to receipt of promotional content |
| Country restrictions | Gambling traffic is allowed. However, before sending such traffic, you are required to file certain paperwork. Sending promotional messages to subscribers who opted out is forbidden. The form needs to be signed and stamped. |
| Country recommendations | Before sending traffic to Kenya, please acquire all the necessary documentation to speed up registrations and waiting times. For additional information, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |