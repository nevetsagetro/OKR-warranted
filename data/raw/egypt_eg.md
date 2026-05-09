# Egypt (EG)

Source: https://www.twilio.com/en-us/guidelines/eg/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Egypt |
| ISO code | The International Organization for Standardization two character representation for the given locale. | EG |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 602 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +20 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Mobile operators in Egypt are known to block and filter messages, so it is highly recommended that you send messages using pre-registered Alphanumeric Sender IDs. Due to technical limitations with our partner mobile operator’s platform, delivery reports may be delayed for domestic registered traffic. However, actual delivery is not impacted. Moreover, although concatenated messages to domestic customers are supported and delivered properly, a DLR will be provided only for the first part of those concatenated messages. For Marketing messages: Message curfew for marketing campaigns: 21:00 -09:00 local time (GMT + 02:00). No messages should be sent on Fridays, Saturdays or official holidays. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Twilio recommends registering an Alpha Sender ID Learn more and register via the Console | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 1 week | 3 weeks | N/A |
| UCS-2 support | --- | Supported | N/A | Supported |
| Use case restrictions | --- | Sending gambling, political, medicine/drug related, religious, and adult-related, alcohol, tobacco content is strictly prohibited | Sending gambling, political, medicine/drug related, religious, and adult-related, alcohol, tobacco content is strictly prohibited | The following Sender IDs have been denylisted from Orange Egypt CloudOTP FACEBOOK Facebook facebook GOOGLE Google google META and Meta MICROSOFT NOTICE VerifyOTP WASMSOTP |
| Best practices | --- | We suggest our customers selecting simple sender IDs as the operators tend to reject requests to register sender IDs that include special characters. | We suggest our customers selecting simple sender IDs as the operators tend to reject requests to register sender IDs that include special characters. For local traffic, we suggest including the local brand or service name in the text, since we observe rejections of generic text (such as Your verification code is XXXXXX), particularly with the Etisalat network. | Twilio recommends registering an Alpha Sender ID |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Messages sent with International Longcodes towards the network Etisalat will be delivered with a generic Alpha Sender ID. This is a replacement taking place outside Twilio's platform. | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Egypt

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Egypt Phone Number: Yes
- Egypt Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : This market has Local and International traffic segmentation. Local traffic requires sender ID registration

Opt-out Rules : No specific opt-out regulations

---

## egypt
| Key | Value |
| --- | --- |
| MCC | 602 |
| Dialing code | 20 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is required with proper documentation. Before you start sending traffic to Egypt, contact your dedicated account manager or [Support](mailto:support@infobip.com) for them to set up this specific route for you. |
| Service provisioning | Depends on sender provisioning time (depending on the network). |
| Sender availability | Alpha senders supported with registration. Numeric senders are not supported on all networks in Egypt. |
| Sender provisioning | Usually 7-15 days for local SMS traffic (local documents are need). 1-2 days for international SMS traffic. |
| Two-way | No two-way SMS options currently available. |
| Two-way provisioning | / |
| Country regulations | Egypt MNOs divide traffic into local and international SMS traffic. OTP traffic is not allowed on local connections. Therefore OTP traffic should be routed over international connections. |
| Country restrictions | No specific restrictions. |
| Country recommendations | Before you send any kind of traffic (local or international) towards and from Egypt, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |