# Sri Lanka (LK)

Source: https://www.twilio.com/en-us/guidelines/lk/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Sri Lanka |
| ISO code | The International Organization for Standardization two character representation for the given locale. | LK |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 413 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +94 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | 3 weeks | N/A |
| UCS-2 support | --- | Supported | Supported | Supported |
| Use case restrictions | --- | The network Mobitel in Sri Lanka only allows OTP, OTT, and transactional traffic, such as banking and payment messages. SMS submitted with a registered Sender ID carrying non-OTP or non-transactional traffic will be blocked by the operator. | --- | To ensure your Alphanumeric Sender IDs are preserved, be sure to pre-register them. Delivery of messages with non pre-registered Alphanumeric Sender IDs is on a best-effort basis only. |
| Best practices | --- | N/A | N/A | Twilio suggests using a pre-registered Alphanumeric Sender ID in Sri Lanka. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Dynamic Numeric Sender IDs are not supported and will be overwritten with a random Sender ID outside the Twilio platform. Delivery is on a best-effort basis only. | N/A |
| Best practices | --- | N/A | Twilio suggests using a pre-registered Alphanumeric Sender ID in Sri Lanka. | N/A |

---

### Sri Lanka

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Sri Lanka Phone Number: No
- Sri Lanka Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: No

Additional Notes : Sender registration is mandatory on Dialog, Etisalat and Hutch networks

Opt-out Rules : No specific opt-out regulations

---

## sri-lanka
| Key | Value |
| --- | --- |
| MCC | 413 |
| Dialing code | 94 |
| Number portability | No |
| Concatenated message | Standard |
| Service restrictions | Sender registration is required for domestic and international traffic. Documentation depends on the network. For more details, contact [Support](mailto:support@infobip.com) or your dedicated account manager |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). |
| Sender availability | International traffic is delivered with Alpha 6 character sender, Domestic can be terminated with Alpha or Numeric sender. |
| Sender provisioning | The average sender registration takes one week. |
| Two-way | Available for domestic traffic with Virtual Long Number. |
| Two-way provisioning | Local entity can send two-way communication. It depends on the MNO how fast they will provide all needed information. |
| Country regulations | Promotional traffic allowed only for domestic traffic. To be considered domestic, the client must have all infrastructure in Sri Lanka and data cannot leave the country. DND is not active, opt-out option is mandatory for promo domestic traffic, and it must be inserted in message template with VLN or link for opt-out. Allowed sender time window is set from 8-20 for local promotional traffic. International promotional traffic is not allowed. |
| Country restrictions | To be considered as a local entity all servers should be in Sri Lanka, no data should leave the country and it has to be pre-approved by MNO. |
| Country recommendations | Before you start sending traffic to Sri Lanka, be sure to get the necessary documentation to speed up the registrations process. For additional info, contact your dedicated account manager or [Support](mailto:support@infobip.com). Note that opt outs are mandatory with VLN or link in message template for domestic promo traffic. |