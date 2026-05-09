# Algeria (DZ)

Source: https://www.twilio.com/en-us/guidelines/dz/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Algeria |
| ISO code | The International Organization for Standardization two character representation for the given locale. | DZ |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 603 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +213 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | SMS cannot be sent to landline destination number. The Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications. Only communicate during an end-user’s daytime hours unless it is urgent. SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language. Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | Yes | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | 2 weeks | --- |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | --- | Generic Alpha Sender IDs should be avoided in Algeria. Especially for the network Mobilis, messages will be rejected if submitted from a Generic Sender ID. |
| Best practices | --- | N/A | --- | We suggest our customers using an Alpha Sender ID that properly represents the service or product related to the content of the message they are submitting. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | --- | Supported | --- |
| Use case restrictions | --- | --- | Numeric Sender ID is not fully supported in Algeria. Depending on the network, messages with Numeric Sender IDs will be delivered on a best-effort basis, and the Numeric Sender ID may be changed to a Generic Alphanumeric Sender ID outside the Twilio platfrom. Specifically for the network Mobilis messages are expected to fail if submitted from a Numeric Sender ID and not an Alpha Sender one. We strongly advise you to use only an Alphanumeric Sender ID when sending messages to Algeria. | --- |
| Best practices | --- | --- | --- | --- |

---

### Algeria

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Algeria Phone Number: Yes
- Algeria Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

---

## algeria
| Key | Value |
| --- | --- |
| MCC | 603 |
| Dialing code | 213 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restriction. |
| Service provisioning | No prior registration of senders is necessary. Service provisioning should be available within a day. |
| Sender availability | Dynamic Alpha sender allowed. Numeric senders might get blocked on some networks. |
| Sender provisioning | Sender provisioning should be available within a day. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | No two-way SMS options currently available. |
| Country regulations | There are no specific regulations for A2P messaging. |
| Country restrictions | Gambling traffic is forbidden. |
| Country recommendations | Even though there are no specific restrictions, note that person-to-person (P2P) traffic is prohibited and will be blocked, as well as traffic with illegal, adult, religious, and political content. |