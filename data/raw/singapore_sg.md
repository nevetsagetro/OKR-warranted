# SINGAPORE (SG)

Source: https://www.twilio.com/en-us/guidelines/sg/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Singapore |
| ISO code | The International Organization for Standardization two character representation for the given locale. | SG |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 525 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +65 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 ASCII characters per message |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Alphanumeric, Shortcode, Twilio Domestic Longcode must be registered with SGNIC (https://sgnic.sg/smsregistry/overview). International Longcode Sender IDs cannot be registered with SGNIC. Participating Aggregators like Twilio are required to ensure Registered Sender IDs are only received from the same organization who has registered with SGNIC, a Participating Aggregator, or a third party representative. In line with this regulatory requirement, customers must complete the registration with Twilio to provide proof of registration with SGNIC and all other necessary details before they start sending SMS. From 30 January 2023, all non-registered Sender IDs will be overwritten with Alphanumeric Sender ID ‘Likely-SCAM’. Sending firearms, gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Messages containing WhatsApp/LINE chat links are not allowed. Message delivery to M2M numbers is on best effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. Note: It is crucial to de-register the number from the SSIR/SGNIC portal after releasing it from your Twilio account, to ensure the number no longer has any relation to your organisation. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 5 business days | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | N/A | Only Alphanumeric Sender ID registered with SGNIC and Twilio will be preserved. From 30 January 2023 all non-registered Alphanumeric Sender IDs. |
| Best practices | --- | All customers must pre-register Alphanumeric Sender ID in the SGNIC portal. After registration, customers must register an Alphanumeric Sender ID directly in the Twilio Console and provide the necessary proof of registration and other details. | Only send from pre-registered Sender IDs. Please review the Compliance Considerations for more details. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | Supported | Supported | N/A |
| Use case restrictions | --- | Only Domestic Longcodes registered with SGNIC and Twilio will be preserved. From 30 January 2023, all non-registered Domestic Longcodes are overwritten with 'Likely-SCAM'. | From 30 January 2023 all International Longcodes are overwritten with 'Likely-SCAM'. Take note that International Longcodes can't be registered with SGNIC and Twilio. | N/A |
| Best practices | --- | All customers must pre-register Long code domestic in the SGNIC portal. After registration, customers must complete the registration with Twilio (https://twlo.my.salesforce-sites.com/SenderId) to provide proof of registration with SGNIC and all other necessary details before they start sending SMS. Avoid sending Person-To-Person messages over SGNIC and Twilio registered Domestic Longcodes as this is not allowed. Please review the Compliance Considerations for more details. | It is recommended to send one-way messages through a pre-registered Alphanumeric Sender ID. Please review the Compliance Considerations for more details. | N/A |

---

### Singapore

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Singapore Phone Number: Yes
- Singapore Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 22:30-07:00)

Additional Notes :

- All unregistered senders will be delivered as "Likely-SCAM"
- Must register on the SSIR portal
- After registration, you need two separate approvals: Request approval for sending to Singapore Upload the Proof of Registration on the SSIR as an attachment or LOA for the sender ID
- Short URLs are not supported

Opt-out Rules : No specific opt-out regulations

---

## singapore
| Key | Value |
| --- | --- |
| MCC | 525 |
| Dialing code | 65 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Before you start sending messages towards Singapore, contact your dedicated account manager or [Support](mailto:support@infobip.com) to set up this specific route for you. |
| Service provisioning | Between 1 and 3 days. |
| Sender availability | Default sender available for networks where registration is required (StarHub, Singtel). - Alpha - Numeric There are different setups and monthly fees depending on the operator, sender type (alphanumeric, numeric). Purpose and description should be provided for every required sender ID which should be used in the exact form in which they are approved since they are case sensitive. |
| Sender provisioning | The average sender registration process time depends solely on network providers and is usually finished within 3 working days. |
| Two-way | Available as Virtual Long Number. |
| Two-way provisioning | Between 7 and 10 working days. |
| Country regulations | The Infocomm Media Development Authority (“IMDA”) Singapore has announced an implementation of the Full SMS Sender ID Registration (“Full SSIR Regime”) starting from 31 January 2023. All organisations wishing to send SMS messages to Singapore must register their Sender IDs directly with the Singapore SMS Sender ID Registry (“SSIR”). With effect from 31 January 2023, only Sender IDs that have been registered with SSIR are allowed in Singapore. All SMS carrying non-registered Sender IDs will be marked as “Likely-SCAM” as a default for a transition period of 6 months. Thereafter, messages with non-registered Sender IDs will be blocked and not delivered to end users. For more information, see: https://www.sgnic.sg/faq/sms-sender-id-registry# |
| Country restrictions | Unsolicited SMS or calls from unknown sources that are related to loans, financial assistance, adult content or online gambling/betting are prohibited. |
| Country recommendations | No specific country recommendations. |