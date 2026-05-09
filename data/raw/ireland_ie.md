# Ireland (IE)

Source: https://www.twilio.com/en-us/guidelines/ie/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Ireland |
| ISO code | The International Organization for Standardization two character representation for the given locale. | IE |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 272 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +353 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Sending cannabis related content is strictly prohibited. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Global Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required There is no segregation between International and Domestic Traffic | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | N/A |
| UCS-2 support | --- | Supported | Supported |
| Use case restrictions | --- | N/A | Starting from July 3, 2025 messages sent over Twilio with unregistered Alpha Sender IDs will be delivered with the Sender ID Likely Scam. Blocking of unregistered Alpha Sender IDs is not currently enforced but will be introduced at a later stage. Until further notice, unregistered Alpha Sender IDs will continue to be overstamped as 'Likely Scam'. Registration remains recommended to avoid future disruption. You may find more details about the timeline here ___________________________________________________________ Twilio will start blocking on 06/06/2024 messages submitted from MEF-Protected Sender IDs for which customers have not provided an LOA letter. In case you are experiencing delivery issues related to a MEF-Protected Sender ID, please reach out to senderid@twilio.com to provide the LOA proving that you are legitimate and authorised carrier of the traffic related to the specific Sender ID. For more information, visit MEF Protected Sender ID Instructions for IE ___________________________________________________________ The use of generic Sender IDs should be avoided as they are being blocked from the operators. |
| Best practices | --- | N/A | Please refrain from using generic sender IDs like SMS, TEXT, InfoSMS, INFO, Verify, Notify etc to avoid being blocked by network operators. ___________________________________________________________ Twilio suggests using a Registered Alpha Sender ID that is related to the content of the message. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | The networks Meteor Ireland and Three Ireland don't support International Longcodes. Traffic submitted to Twilio with an International longcode will be attempted to be delivered on a best effort basis and the longcode will be replaced from an Alpha Sender ID outside Twilio's platfrom. | N/A |
| Best practices | --- | N/A | It is strongly recommended to use a Registered Alphanumeric Sender ID when sending one-way Application-To-Person (A2P) traffic to Ireland (IE). | N/A |

---

### Ireland

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Ireland Phone Number: Yes
- Ireland Short Code: Yes (Note: May be changed to generic sender on some networks)
- International Phone Number: Yes (Note: May be changed to generic sender on some networks)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-08:00)

Opt-out Rules : No specific opt-out regulations

---

## ireland
| Key | Value |
| --- | --- |
| MCC | 272 |
| Dialing code | 353 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | A registered alphanumeric sender is necessary to send SMS to Ireland. Generic senders cannot be registered. Alphanumeric senders must be registered both with Infobip and with the [Irish regulatory body](https://www.comreg.ie/). Per the latest [update on ComReg’s SMS Sender ID Blocking](https://www.comreg.ie/industry/electronic-communications/nuisance-communications/sms-sender-id-registry/#1), the blocking of unregistered Sender IDs has been postponed to a later date yet to be determined. |
| Service provisioning | For Sender ID Owners (SIDO) or Third-Party (wholesale and reseller clients) sender registration is mandatory. For Participating Aggregators, sender registration is not mandatory. Contact Infobip to create an exception to this process.
        For more information about the regulations, see [ComReg SMS Sender ID Registry](https://www.comreg.ie/industry/electronic-communications/nuisance-communications/sms-sender-id-registry/registry-qa/). Sender ID Owners must first create an account on the [ComReg portal](https://senderid.comreg.ie/), and then:
        - Request the sender registration on the ComReg portal, and select Infobip as the chosen Participating Aggregator.
        - When the sender is approved by ComReg and you have authorized Infobip to carry your traffic with the sender(s), contact Infobip to internally register these senders. Numbers have no specific restrictions when sending SMS to Ireland. |
| Sender availability | - Alpha - Virtual Long Number - Dynamic |
| Sender provisioning | Within 5 days. For customized setups, the process may require additional time. |
| Two-way | Virtual Long Numbers |
| Two-way provisioning | 5 days |
| Country regulations | There is a set country level sender ID manipulation replacing the country prefix 353 with 0. This affects all accounts. All marketing traffic should have opt-ins and opt-out options within the message. |
| Country restrictions | No special restrictions. |
| Country recommendations | No specific country recommendations. |