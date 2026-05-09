# Uzbekistan (UZ)

Source: https://www.twilio.com/en-us/guidelines/uz/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Uzbekistan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | UZ |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 434 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +998 |

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
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- |
| UCS-2 support | --- | --- | Supported |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | Dynamic Alphanumeric Sender IDs are not fully supported by Uzbekistan mobile operators. Sender IDs may be overwritten with a generic Alphanumeric Sender ID outside the Twilio platform. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | --- | --- | --- |
| Use case restrictions | --- | --- | --- | --- |
| Best practices | --- | --- | Dynamic Numeric Sender IDs are not fully supported by Uzbekistan mobile operators. Sender IDs may be overwritten with a generic Alphanumeric Sender ID outside the Twilio platform and delivery will be attempted on a best effort basis. Kindly prefer using an Alpha Sender ID. | --- |

---

### Uzbekistan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Uzbekistan Phone Number: Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- Uzbekistan Short Code: Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- International Phone Number: Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes (On certain networks like 43405)
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Opt-out Rules : No specific opt-out regulations

---

## uzbekistan
| Key | Value |
| --- | --- |
| MCC | 434 |
| Dialing code | 998 |
| Number portability | Yes |
| Concatenated message | Standard |
| Service restrictions | Sender and content registration is required for local traffic. For international traffic, sender registration is only required on the Ucell network. |
| Service provisioning | 3 days to configure the default account setup. A specific setup may take longer, depending on the supplier. |
| Sender availability | Alphanumeric, Shortcode |
| Sender provisioning | The average sender registration process time depends solely on network providers and exceeds 24 hours. |
| Two-way | No 2-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | International and local traffic are separated. Local traffic is further divided into three categories: transactional, service, and promotional. There is a specific billing for local traffic, so contact [Support](mailto:support@infobip.com) or your dedicated account manager for more information. Opt-ins and opt-outs are mandatory. |
| Country restrictions | Forbidden content: SPAM, information aimed at undermining the state, constitutional and social order, violating the territorial integrity, political independence and state sovereignty of the Republic of Uzbekistan and other states. Promotion of war, terrorism, violence, national exclusivity and religious hatred, racism and its varieties (anti-Semitism, fascism), defaming. The honor and dignity of citizens of the Republic of Uzbekistan, interference in their personal lives, pornographic materials, sending advertising messages, as well as committing other actions entailing legal liability. |
| Country recommendations | Generic senders are not allowed. Description of opt-in and opt-out methods are required for local sender registration. |