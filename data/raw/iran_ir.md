# Iran (IR)

Source: https://www.twilio.com/en-us/guidelines/ir/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Iran |
| ISO code | The International Organization for Standardization two character representation for the given locale. | IR |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 432 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +98 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Not Available |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Notice: Discontinuation of SMS Delivery to Iran In compliance with applicable regulations and requirements, and to reinforce our commitment as a trusted partner for our customer communication needs, Twilio will stop supporting SMS message delivery to Iran effective March 15, 2025. We strongly encourage customers to discontinue sending SMS traffic to Iran through Twilio before this date to avoid delivery failures. After March 15, 2025 onward, all SMS messages to Iran will be blocked by Twilio |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | N/A |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | N/A | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Iran

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Iran Phone Number: No
- Iran Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: No

Additional Notes : Sender registration is mandatory on all Iran networks

Opt-out Rules : No specific opt-out regulations

---

## iran
| Key | Value |
| --- | --- |
| MCC | 432 |
| Dialing code | 98 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is a required only for MCI Iran Network and MTN Irancell. For MCI Iran, senders are case-sensitive and generic senders are not allowed. Also, there is no specific documentation needed for registration. If you are planning to terminate messages to Iran for the first time, contact your account manager or [Support](mailto:support@infobip.com) to set up a specific route for you. |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). |
| Sender availability | Alpha senders only. For MCI Iran, senders are case-sensitive and generic senders are not allowed. |
| Sender provisioning | Up to 10 days. |
| Two-way | / |
| Two-way provisioning | / |
| Country regulations | Gambling, betting, as well as SPAM, loan traffic, Crypto, Forex and adult content is likely to be blocked by the Iranian operators. |
| Country restrictions | Gambling, spamming, and adult content is forbidden. No specific restrictions for promo SMS traffic. |
| Country recommendations | No specific recommendations. |