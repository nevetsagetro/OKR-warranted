# Bangladesh (BD)

Source: https://www.twilio.com/en-us/guidelines/bd/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Bangladesh |
| ISO code | The International Organization for Standardization two character representation for the given locale. | BD |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 470 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +880 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ---- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Sender ID Compliance Sender ID Registration is required in Bangladesh for networks GrameenPhone, Robi/Axiata, and TeleTalk. Starting on September 8, 2025, messages with unregistered Sender IDs to these networks will be blocked. To continue sending messages, you must use a registered Alphanumeric Sender ID. Additional Phone Numbers and Sender ID Guidelines Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required for Robi, Teletalk and Grameenphone | Required | Not Supported for GrameenPhone, Robi/Axiata, and TeleTalk Supported for the rest of Bangladesh networks |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required for Robi, Teletalk and Grameenphone Learn more and register via the Console | Not Supported | Not Supported for GrameenPhone, Robi/Axiata, and TeleTalk Supported for the rest of Bangladesh networks |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A | Yes for the networks that Dynamic Alphanumeric is supported |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | N/A | N/A |
| UCS-2 support | --- | Supported | N/A | Supported |
| Use case restrictions | --- | N/A | N/A | The Bangladesh networks GrameenPhone, Robi/Axiata, and TeleTalk require Sender ID registration. We advise Twilio's customers to register an Alpha Sender ID in Bangladesh for full country coverage. |
| Best practices | --- | Twilio suggests using a pre-registered Alphanumeric Sender ID in Bangladesh | Customers with Domestic traffic are welcome to register their Sender IDs are International ones | Use only registered Alphanumeric Sender ID in Bangladesh |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Not Supported for GrameenPhone, Robi/Axiata, and TeleTalk Supported for the rest of Bangladesh networks | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | The Bangladesh networks GrameenPhone, Robi/Axiata, and TeleTalk require Sender ID registration. We advise Twilio's customers to register an Alpha Sender ID in Bangladesh for full country coverage. | N/A |
| Best practices | --- | N/A | Twilio suggests using a pre-registered Alphanumeric Sender ID in Bangladesh | N/A |

---

### Bangladesh

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- Bangladesh Phone Number: Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- Bangladesh Short Code: No
- International Phone Number: Yes (Note: Your sender ID may be changed to a generic sender on some networks)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes (On certain networks)
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- Sender registration is required for Grameen Phone, Robi and Teletalk networks
- Numeric senders are only fully supported on Teletalk network
- Government, Religion and Gambling content are not allowed

Opt-out Rules : No specific opt-out regulations

---

## bangladesh
| Key | Value |
| --- | --- |
| MCC | 470 |
| Dialing code | 880 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | International traffic: no restrictions. Local traffic: Promo traffic must be in Bengali language. |
| Service provisioning | International 1 day, while for local it takes 3-5 days usually. |
| Sender availability | International traffic: alpha senders only on 3 networks: Teletalk, Robi and Banglalink, while on Grameenphone Alpha and numeric senders are allowed. Local traffic: alpha and numeric senders allowed on all networks. Senders need to be registered with the operator. Alpha senders and VLNs are unique in a country (dedicated to a client). |
| Sender provisioning | Local senders: The average sender registration process completion time depends solely on network providers and exceeds 24 hours. The client needs to have a local entity and needs to submit authorization letter. |
| Two-way | Virtual Long Number (both for international and local) |
| Two-way provisioning | It takes about 2 weeks. There is a standard registration process for local clients. International clients should terminate traffic on most networks with alpha senders and insert VLNs to be able to receive reply from end user. |
| Country regulations | Local regulations: Sending promo message that are not in Bengali language is prohibited. Promo must be sent in Bengali language. |
| Country restrictions | Gambling, betting, and adult content is not allowed, as well as some political and election messages. |
| Country recommendations | No specific country recommendations. |