# Yemen (YE)

Source: https://www.twilio.com/en-us/guidelines/ye/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Yemen |
| ISO code | The International Organization for Standardization two character representation for the given locale. | YE |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 421 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +967 |

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
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A |
| UCS-2 support | --- | --- | Supported |
| Use case restrictions | --- | --- | Dynamic Alpha Sender ID is not fully supported in Yemen. Depending the network that the number belongs to, messages may be delivered with the original Sender ID preserved or with a generic Alpha Sender ID |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | Numeric sender IDs are not fully supported in Yemen. Submission with Numeric Sender ID will be attempted on best effort basis and may be successful by having the Sender ID replaced with a generic one outside Twilio's platform or may fail completely. Prefer using an Alpha Sender ID in Yemen | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Yemen

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Yemen Phone Number: Yes
- Yemen Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Yemen Mobile requires registration otherwise sender ID will be overwritten to INFO
- On Ytelecom network, all senders will be received with A2PSMS

Opt-out Rules : No specific opt-out regulations

Last updated 1 year ago

Was this helpful?


---

# SMS Country Information Guide: North America

Fuente: https://docs.bird.com/applications/channels/channels/supported-channels/sms/concepts/choose-the-right-sender-availability-and-restrictions-by-country/sms-country-information-guide-north-america

---

## yemen
| Key | Value |
| --- | --- |
| MCC | 421 |
| Dialing code | 967 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | For Yemen Mobile, only registered alpha senders allowed. Other networks have no restrictions. |
| Service provisioning | 1 day to configure the default account setup, more if it's a specific setup, could depend on the supplier. |
| Sender availability | Alpha and numeric senders supported. Full dynamic connections, except for Yemen Mobile network (registered Alpha). |
| Sender provisioning | Only for Yemen Mobile: The average sender registration process time depends solely on network provider. Usually takes up to 5 days. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | No separation into local and international traffic in place. No separation on transactional and promotional traffic in place. Sender registration is needed only towards Yemen Mobile network. There is no sender registration needed for other networks. No specific regulations for promotional traffic. |
| Country restrictions | Gambling, betting as well as SPAM, loan traffic, Crypto, Forex, adult and political content is likely to be blocked by the Yemen operators. |
| Country recommendations | No specific recommendations. |