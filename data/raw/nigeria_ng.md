# Nigeria (NG)

Source: https://www.twilio.com/en-us/guidelines/ng/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Nigeria |
| ISO code | The International Organization for Standardization two character representation for the given locale. | NG |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 621 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +234 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Sending gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Dynamic Alphanumeric Sender IDs are supported, although sending with Numeric Sender IDs will be attempted on a best-effort basis. We recommend sending with an Alphanumeric Sender ID specific to your brand and content. The Nigerian Communication Commission mandates that Nigerian telecom operators implement a do-not-disturb (DND) registry which allows customers to opt out of either receiving promotional messages or unsolicited messages via SMS in general. Depending on the DND features that the subscriber has selected, attempts to send promotional and unsolicited SMS to those numbers may fail. Twilio provides special routes with permission to contact phone numbers on the DND list by SMS when the traffic is classified as One-Time Password (OTP). Please consider: Unsolicited messages are not allowed via this route. Your recipients must have expressed permission (i.e., opted in) to be contacted via SMS.A phone number on the DND list might also be switched off, out of network coverage, or simply dead. The delivery report will indicate the status of messages sent to phone numbers on the DND. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Supported only for the major Nigerian Networks (MTN, Airtel, Glo and Etisalat). | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported only for the major Nigerian Networks (MTN, Airtel, Glo and Etisalat) Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | 2-3 weeks | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | Promotional content is not allowed to be registered. | Twilio supports the registration of the following two categories of Domestic Sender IDs: - Banking - Promotional | Sender ID Registration is Required. Submission with unregistered Sender IDs will be attempted on a best effort basis. Generic Alphanumeric Sender IDs, such as InfoSMS, INFO, Verify and Notify, should be avoided. Google as a Sender ID is prohibited in Nigeria. Messages using this Sender ID may be blocked or filtered by the local operators. |
| Best practices | --- | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Numeric International sender ID is not supported to the MTN, Airtel and 9 Mobile networks in Nigeria. Messages submitted with numeric would result in delivery failure. Twilio strongly suggests submitting traffic only with a Pre-Registered alphanumeric sender ID in Nigeria. | N/A |
| Best practices | --- | N/A | --- | N/A |

---

### Nigeria

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Nigeria Phone Number: Yes
- Nigeria Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Local traffic requires registration
- International traffic is Alpha dynamic
- Letter of Authorization (LOA) is required for Banking and Financial traffic

Opt-out Rules : No specific opt-out regulations

---

## nigeria

| Key | Value |
| --- | --- |
| MCC | 621 |
| Dialing code | 234 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | There's traffic differentiation based on origin. For sending local or international traffic, you need to register and file proper documentation. If you send both promotional and transactional content, you cannot use the same sender. Before you start sending traffic towards Nigeria, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |
| Service provisioning | Depending on the traffic origin, service provisioning might take from 1 day up to 4 weeks. |
| Sender availability | Alpha and Short Code. |
| Sender provisioning | The average sender registration process time depends solely on network providers and can take up to 4 weeks. |
| Two-way | Available two-way options: Short Codes and USSD. Standard, zero rated and premium |
| Two-way provisioning | To use Short Codes, you need to have a local entity. Provisioning time can take up to 3 months. |
| Country regulations | A2P messaging is differentiated based on its origin (local or international). Necessary DND register (enables subscribers to opt out form receiving any kind of promotional content) for promotional messages. For traffic with local origin, sender names have to be connected to the company name, its product, brand or application. If the client can't provide any reference connecting it to the chosen sender, the sender application will be rejected. |
| Country restrictions | There are no specific restrictions regarding the type of traffic. However, traffic containing operator names, VLNs, keywords such as "Promo", "Congratulations", "Win", etc. might be affected. We advise you to avoid such words/phrases in messages. |
| Country recommendations | Before you start sending traffic towards Nigeria, acquire all necessary documentation to speed up registrations and waiting times. For additional information, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |