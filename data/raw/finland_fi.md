# Finland (FI)

Source: https://www.twilio.com/en-us/guidelines/fi/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Finland |
| ISO code | The International Organization for Standardization two character representation for the given locale. | FI |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 244 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +358 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Gambling and lottery-related content is strictly prohibited by mobile operators in Finland. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Required | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | For some Protected Sender IDs, Finnish mobile operators require specific documents to successfully deliver SMS messages to subscribers. Please check the following list as provided from The Finnish Transport and Communications Agency Traficom to find those Protected Sender IDs. |
| Best practices | --- | N/A | In case you need to submit messages via one of the protected Sender ID please reach out to our Customer Support and provide Twilio with a Letter Of Authorization as well as the Numbering Decision which was acquired from Traficom following the registration of the Protected Sender ID. In case you are not the owner of the specific protected Sender ID we suggest using a different Alpha Sender ID which is not protected. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | Numeric Sender ID is not supported in FInland. Messages with the specific type of Sender ID will be delivered on a best effort basis while the Sender ID is expected to change to a generic Alpha one outside Twilio's platform | N/A |

---

### Finland

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Finland Phone Number: Yes
- Finland Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- Short URLs not supported
- Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules : No specific opt-out regulations

---

## finland
| Key | Value |
| --- | --- |
| MCC | 244 |
| Dialing code | 358 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | / |
| Service provisioning | Sender provisioning should be available within a day, more if it's a specific setup. |
| Sender availability | - Alpha - Virtual Long Number - Short Code |
| Sender provisioning | No sender registration needed. |
| Two-way | Available as Virtual Long Numbers and Short Codes. |
| Two-way provisioning | For VLN is takes 2-4 days and up to 3 weeks for SC. |
| Country regulations | Opt-in info must be available on operator's demand, opt-out option must be inserted within the message. |
| Country restrictions | General anti spam restrictions. |
| Country recommendations | Before sending any traffic to customers and end users, get opt-in consent from each end user. Especially when sending marketing content. |