# Romania (RO)

Source: https://www.twilio.com/en-us/guidelines/ro/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Romania |
| ISO code | The International Organization for Standardization two character representation for the given locale. | RO |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 226 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +40 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Mobile operators Vodafone and Orange in Romania do not support Dynamic Sender IDs. These IDs will be overwritten with either a generic short code or an Alphanumeric Sender ID to ensure delivery. Romanian mobile operators are blocking and filtering SMS content containing web addresses (URLs). If your SMS content carries a web URL, kindly reach out to Twilio customer services to get your SMS content added to an allow list to prevent delivery failure. When content registration is complete, you must send the messages with an International Long Code Sender ID or an Alphanumeric Sender ID. Sending messages using Domestic Long Code Sender ID may result in messages containing a web URL being filtered. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required only for Telekom Romania Supported optionally for all the rest Romanian Networks There is no segregation between International and Domestic Traffic | Supported except for Telekom Romania |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required only for Telekom Romania (Free of cost) Supported optionally for all the rest Romanian Networks (Registration Fees are applied) Learn more and register via the Console | Supported for Telekom Romania Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 4 weeks | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | N/A | Messages with alphanumeric Sender IDs sent to the Orange, Vodafone or Digi.Mobil networks will be overwritten with either a generic short code or an Alphanumeric Sender ID outside the Twilio platform. Starting from the 15th of January of 2025, messages with unregistered Alpha Sender IDs will not be supported for Telekom Romania. |
| Best practices | --- | Romania is a country very sensitive to URLs. Even if the Sender ID gets registered, sending messages containing a URL that is not checked and allowlisted may produce issues in the delivery so we would like to suggest our customers to proactively provide us with the full list of ULRs they intend to use during Sender ID Registration procedure as sample SMS messages. Twilio will check them and make sure they are allowlisted. In case new URLs need to be used in the future please reach out to Twilio customer services to get the new URL allowlisted alongside the sender ID you have registered. Additionally starting from the 20th of November of 2024 the URL Registration needs to be combined with an Alpha Sender ID Registration otherwise messages sent to Telekom Romania will fail. Learn more and register via the Console. To prevent blocking or message filtering of promotional gambling traffic in Romania, we recommend completing full sender ID registration across all networks. | Twilio suggests using a Registered Alpha Sender ID in Romania. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | International Numeric Sender IDs will be overwritten with either a generic short code or an Alphanumeric Sender ID outside the Twilio platform. Starting from the 20th of November of 2024, messages with Numeric Sender IDs will not be supported for Telekom Romania. | N/A |
| Best practices | --- | N/A | Twilio suggests using a Registered Alpha Sender ID in Romania. | N/A |

---

### Romania

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Romania Phone Number: Yes (Requires registration or will be converted to short code)
- Romania Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes (For some networks)
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- Short URLs not supported
- You can register sender IDs for a fee or use free short codes generated by operators
- Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules : No specific opt-out regulations

---

## romania
| Key | Value |
| --- | --- |
| MCC | 226 |
| Dialing code | 40 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions. |
| Service provisioning | 1 day to configure the default account setup. More if it's a specific setup (it could depend on the supplier). |
| Sender availability | - Alpha - Short Code |
| Sender provisioning | Sender registration can take up to 15 days. |
| Two-way | Virtual Long Number and Short Code |
| Two-way provisioning | For VLN, it takes about 2-3 days and for Short Code, it can take up between 2-4 weeks. |
| Country regulations | No specific country regulations. |
| Country restrictions | Gambling is fully legal in Romania, but in order to promote bonuses (for example, "Log in in today to get 10 free spins."), players must have already opted in to receive such messages. Players who opted out cannot receive promotional messages from the online gambling operator. Online operators must restrict access to their gambling platform to minors. |
| Country recommendations | No specific country recommendations. |