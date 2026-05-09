# Ukraine (UA)

Source: https://www.twilio.com/en-us/guidelines/ua/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Ukraine |
| ISO code | The International Organization for Standardization two character representation for the given locale. | UA |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 255 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +380 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Required | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | N/A |
| UCS-2 support | --- | --- | Supported |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | Avoid the use of generic Alphanumeric Sender IDs because mobile operators tend to block or filter such IDs. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Network operators in Ukraine do not support Numeric Sender IDs. SMS submissions with Numeric Sender IDs will be attempted on a best effort basis by replacing the Numeric Sender ID with a generic Alpha one outside Twilio's platfrom. Additionally for the network Trimob those messages will fail completely. Twilio recommends using Alphanumeric Sender IDs to ensure message delivery. | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Ukraine

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Note: Your sender ID may be changed on some networks)
- Ukraine Phone Number: Yes (Note: Your sender ID may be changed on some networks)
- Ukraine Short Code: Yes (Note: Your sender ID may be changed on some networks)
- International Phone Number: Yes (Note: Your sender ID may be changed on some networks)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: No

Additional Notes : Sender registration is mandatory on specific networks

Opt-out Rules : No specific opt-out regulations

---

## ukraine

| Key | Value |
| --- | --- |
| MCC | 255 |
| Dialing code | 380 |
| Number portability | Yes |
| Concatenated message | Yes |
| Service restrictions | If you are planning to terminate to Ukrainian networks, please get in touch with your account manager or [Support](mailto:support@infobip.com) to set a specific route. Special registration setup needed for international traffic. |
| Service provisioning | 1 day to configure the default account setup, more if it's a specific setup (depending on the client's needs) |
| Sender availability | - Alpha sender - Virtual Long Number (ordering through your account manager or [Support](mailto:support@infobip.com)) |
| Sender provisioning | - Alpha Sender sends orders to the MNOs three times a month - on the 5th, 15th, and 25th. Once the request is sent to the MNO, the estimated time of arrival is 13 days. - Virtual Long Number (immediate, for larger orders up to 6 weeks) |
| Two-way | Available 2-way setup: - requested VLN with a monthly fee |
| Two-way provisioning | VLN: Immediate. For orders larger than 5 numbers, it can take up to 6 weeks |
| Country regulations | For registration of brand names, the operator may ask for documents that can prove the right to use the name of trademark/brand, including the company registration documents. Local sender names are allowed only for residents. |
| Country restrictions | Gambling, alcohol, adult content, violence. |
| Country recommendations | We recommend using the registered sender IDs to ensure throughput and reliability, handset delivery reports and brand recognition. |