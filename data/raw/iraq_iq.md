# Iraq (IQ)

Source: https://www.twilio.com/en-us/guidelines/iq/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Iraq |
| ISO code | The International Organization for Standardization two character representation for the given locale. | IQ |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 418 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +964 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | Although Alphanumeric Sender ID registration is not required in Iraq, we recommend that you avoid using generic Alphanumeric Sender IDs and instead submit messages with Alphanumeric Sender IDs that correctly represent the content of your messages. The submission of messages with generic Sender IDs will be attempted on best-effort basis and will most likely result in delivery failure. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | The use of Numeric Sender IDs is not supported by Zain and Korek networks. Such IDs will be overwritten with a generic Alphanumeric Sender ID outside the Twilio platform. For the network Zain specifically the expected behaviour is SMS failure when a Numeric Sender ID is used so Twilio recommends submitting messages only with Alphanumeric Sender IDs for better deliverability. | N/A |
| Best practices | --- | N/A | Twilio recommends submitting messages only with Alphanumeric Sender IDs for better deliverability. | N/A |

---

### Iraq

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Iraq Phone Number: Yes
- Iraq Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : Zain network does not support numeric senders

Opt-out Rules : No specific opt-out regulations

---

## iraq

| Key | Value |
| --- | --- |
| MCC | 418 |
| Dialing code | 964 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is required only on Asiacell (Ooredoo Group), while it is not required on other network providers. There are few specific requirements that need to be fulfilled to register senders. Company HQ must be in Iraq to be considered domestic and there is no specific documentation needed nor are there specific sender name restrictions. International SMS termination towards Iraq does not require sender registrations, they are dynamic. |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). |
| Sender availability | Alpha senders only. No specific sender name restrictions. |
| Sender provisioning | For local SMS traffic on Asiacell Network, usually around 5-7 days. |
| Two-way | No specific regulations for A2P messaging. |
| Two-way provisioning | / |
| Country regulations | Generally, A2P SMS traffic is divided on local and international only for Asiacell and there is no traffic separation of any kind for other networks. |
| Country restrictions | Gambling, betting as well as SPAM, loan traffic, Crypto, Forex and adult content is likely to be blocked by the Iraq operators. No specific restrictions for promo SMS traffic. |
| Country recommendations | No specific recommendations. |