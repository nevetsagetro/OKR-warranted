# Norway (NO)

Source: https://www.twilio.com/en-us/guidelines/no/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Norway |
| ISO code | The International Organization for Standardization two character representation for the given locale. | NO |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 242 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +47 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Gambling and lottery-related content is strictly prohibited by mobile operators in Norway. Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Norway

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Norway Phone Number: Yes
- Norway Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- On Telenor network, Alpha senders are not supported and will be converted to local numeric numbers
- Short URLs not supported
- Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules : No specific opt-out regulations

---

## norway

| Key | Value |
| --- | --- |
| MCC | 242 |
| Dialing code | 47 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions when sending traffic towards Norway. |
| Service provisioning | Sender provisioning should be available within a day, more if it's a specific setup. |
| Sender availability | - Alpha - Short Code - Virtual Long Number |
| Sender provisioning | Sender registration process can take up to 3 days. |
| Two-way | Virtual Long Numbers and Short Codes |
| Two-way provisioning | 1-2 working days for VLN and shared SC, and up to 2 weeks for dedicated SC. |
| Country regulations | Senders can contain max 11 characters. Strict regulation regarding spam traffic. Opt-out options are mandatory within messages. Especially when sending promotional traffic. Generic senders are not allowed. |
| Country restrictions | General anti spam regulation. Links in SMS are examined by Norwegian networks and operators require URL whitelisting due to spam. Gambling traffic is allowed with mandatory opt-in info available at request. In 2010, Norway implemented payment-blocking to stop money transfers between foreign gambling operators and Norwegian customers. Refer to Gambling Laws and Regulations: [https://iclg.com/practice-areas/gambling-laws-and-regulations/norway](https://iclg.com/practice-areas/gambling-laws-and-regulations/norway) |
| Country recommendations | Mobile operators are filtering and blocking traffic which contains URLs. Only URLs that are whitelisted and legit won't be blocked. Before sending any traffic to customers and end users, get opt-in consent from each end user. Opt-in info needs to be available upon request. |