# United Arab Emirates (AE)

Source: https://www.twilio.com/en-us/guidelines/ae/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | United Arab Emirates |
| ISO code | The International Organization for Standardization two character representation for the given locale. | AE |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 424 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +971 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Mobile carriers in the United Arab Emirates require all SMS messages to be submitted from registered Sender ID only. Any SMS sent from unregistered Sender ID will be blocked. All promotional Alphanumeric Sender IDs must carry an AD- prefix, and this counts towards the 11-character limit. Promotional messages to the UAE can not be sent between 09:00pm to 07:00am local time. Messages sent during the restricted time period will be queued outside the Twilio platform and will only be processed for delivery during the allowed time period. Sending gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Messages containing URL, WhatsApp/LINE chat links, and phone number in body are also not allowed. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | --- | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | 2 weeks | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | Messages containing adult, gambling, or religious content are strictly forbidden. URL shortners should be avoided as the local networks tend to filter messages containing them. Please note that Promotional messaging is only supported for Domestic Entities and Promotional Content is not permitted for International Entities. Due to limitations related to the local infrastructure we suggest our clients to use UCS2 encoding when submitting messages containing the EURO symbol "€". | Messages containing adult, gambling, or religious content are strictly forbidden. All promotional Alphanumeric Sender IDs must carry an AD- prefix. Promotional messages to the UAE can not be sent between 09:00pm to 07:00am local time. Messages sent during the restricted time period will be queued outside the Twilio platform and will only be processed for delivery during the allowed time period. URL shortners should be avoided as the local networks tend to filter messages containing them. Due to limitations related to the local infrastructure we suggest our clients to use UCS2 encoding when submitting messages containing the EURO symbol "€". | Alphanumeric Sender IDs are only supported through pre-registration. |
| Best practices | --- | For all health services related Sender ID registration requests, we will require an approval letter from the UAE health authorities. UAE is a country very sensitive to URLs. Even if the Sender ID gets registered, sending messages containing a URL that is not checked and allowlisted may produce issues in the delivery so we would like to suggest our customers to proactively provide us with the full list of URLs they intend to use during Sender ID Registration procedure as sample SMS messages. | For all health services related Sender ID registration requests, we will require an approval letter from the UAE health authorities. UAE is a country very sensitive to URLs. Even if the Sender ID gets registered, sending messages containing a URL that is not checked and allowlisted may produce issues in the delivery so we would like to suggest our customers to proactively provide us with the full list of URLs they intend to use during Sender ID Registration procedure as sample SMS messages. | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Not Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | N/A | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### United Arab Emirates

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: WhatsApp (You can use your existing number or get a new one from Bird)
- Promotional SMS: WhatsApp (You can use your existing number or get a new one from Bird)
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- UAE Phone Number: No
- UAE Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:30-07:30)

Additional Notes :

- All promotional sender IDs must be prefixed by AD (e.g., AD-YourBrand)
- Letter of Authorization (LOA) and Certificate of Incorporation required for sender ID registration

Opt-out Rules : No specific opt-out regulations

---

## united-arab-emirates

| Key | Value |
| --- | --- |
| MCC | 424 |
| Dialing code | 971 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Sender registration is required. The needed documentation depends on traffic original and network. Before you start sending messages towards United Arab Emirates, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | Setup depends on sender provisioning time (depending on the network). |
| Sender availability | - Short Codes - Alphanumeric |
| Sender provisioning | The average sender registration processing time depends solely on network providers. For transactional senders (local and international), it can take up to 15 days. For promotional senders there is a specific process of registration and end users consent provisioning directly over MNO portals. |
| Two-way | Short Code |
| Two-way provisioning | For dedicated Short Code it can take around 1-2 weeks. For shared Short Code, 1 day. |
| Country regulations | A2P SMS traffic is divided into local and international and on transactional and promotional. |
| Country restrictions | Crpytocurrency traffic is not allowed. Notifications are considered as transactional traffic. Opt-out is automatically added, as part of message content, within every promotional message. For example, to stop, send "b AD-Brand:" to 7726. You can send promotional traffic only between 7 AM and 9 PM local time. Promotional sender name must start with prefix AD- (example – AD-Brand). All local enterprise clients need to add opt-ins from end users on operator's DND base. |
| Country recommendations | Highly regulated country. Before sending any traffic towards UAE, acquire all necessary documentation to speed up the registration and waiting time. For more details, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |