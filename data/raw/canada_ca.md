# Canada (CA)

Source: https://www.twilio.com/en-us/guidelines/ca/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Canada |
| ISO code | The International Organization for Standardization two character representation for the given locale. | CA |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 302 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +1 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | Inbound long code: GSM 3.38=136, Unicode=70 Outbound long code: GSM 3.38=136, Unicode=70 |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Supported |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | Twilio will not check whether the number is a landline and will attempt to send it to our carrier for delivery. Some carriers will convert the SMS into text-to-speech messages via voice calls. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio recommends sending application-to-person (A2P) traffic over short codes or verified toll-free numbers for optimal delivery results. Canadian mobile carriers enforce strict filtering on A2P messages. Carriers will not cease filtering, but mobile subscribers may wish to reach out to their mobile carrier to petition them to do so. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | --- | --- |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | --- | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | --- | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 12-16 weeks |
| UCS-2 support | --- | Supported | --- | Supported |
| Use case restrictions | --- | High-Risk Financial ServicesPayday LoansShort Term- High Interest LoansAuto LoansMortgage LoansStudent LoansDebt CollectionGambling/SweepstakesStock AlertsCryptocurrency Get Rich Quick SchemesDeceptive Work from Home ProgramsRisk Investment OpportunitiesMulti-Level Marketing 3rd PartyDebt Collection or ConsolidationDebt ReductionCredit Repair ProgramsLead Generation Controlled SubstancesTobaccoVapeFederally Illegal DrugsCannabisCBDAlcohol PornographyProfanityHate SpeechPhishingFraudScamsDeceptive MarketingSnowshoeingFilter EvasionFirearmsAdult ContentFireworks For additional insight into these uses cases, including limitations, and exceptions, visit: Forbidden message categories for SMS and MMS in the US and Canada | N/A | High-Risk Financial ServicesPayday LoansShort Term- High Interest LoansAuto LoansMortgage LoansStudent LoansDebt CollectionGambling/SweepstakesStock AlertsCryptocurrency Get Rich Quick SchemesDeceptive Work from Home ProgramsRisk Investment OpportunitiesMulti-Level Marketing 3rd PartyDebt Collection or ConsolidationDebt ReductionCredit Repair ProgramsLead Generation Controlled SubstancesTobaccoVapeFederally Illegal DrugsCannabisCBDAlcohol PornographyProfanityHate SpeechPhishingFraudScamsDeceptive MarketingSnowshoeingFilter EvasionFirearmsAdult ContentFireworks For additional insight into short code requirements see https://www.twilio.com/en-us/guidelines/ca/short-code |
| Best practices | --- | N/A | N/A | The character limit for Canada short code SMS is 160 Ascii characters. Messages with more than 160 characters will not be delivered. Refer to our FAQ for short code best practices for: + Mobile Marketing Opt-In + Help and Stop Standards + Opt-In S |

## Phone Numbers & Sender ID: Toll-Free

| Field | Description | Toll Free |
| --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | Requires Verification |
| UCS-2 support | --- | --- |
| Use case restrictions | --- | High-Risk Financial ServicesPayday LoansShort Term- High Interest LoansAuto LoansMortgage LoansStudent LoansDebt CollectionGambling/SweepstakesStock AlertsCryptocurrency Get Rich Quick SchemesDeceptive Work from Home ProgramsRisk Investment OpportunitiesMulti-Level Marketing 3rd PartyDebt Collection or ConsolidationDebt ReductionCredit Repair ProgramsLead Generation Controlled SubstancesTobaccoVapeFederally Illegal DrugsCannabisCBDAlcohol PornographyProfanityHate SpeechPhishingFraudScamsDeceptive MarketingSnowshoeingFilter EvasionFirearmsAdult ContentFireworks For additional insight into these uses cases, including limitations, and exceptions, visit: Forbidden message categories for SMS and MMS in the US and Canada |
| Best practices | --- | --- |

---

### Canada

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Toll Free Number
- Promotional SMS: Toll Free Number
- Two-Way Conversations: SMS with Toll Free Number

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Canada Phone Number: Yes (SMS and MMS)
- Canada Short Code: Yes (only SMS)
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-08:00)

Additional Notes

- Also supported: Short Codes, SMS Local Numbers (for testing only)

Opt-out Rules

- Transactional traffic: Opt-out required. Stop language should be included in all registration messages
- Promotional traffic: Opt-out required. Stop language must be included in all registration messages

---

## canada

| Key | Value |
| --- | --- |
| MCC | 302 |
| Dialing code | 1 |
| Number portability | Yes |
| Concatenated message | Standard and long. Concatenated messages are supported. |
| Service restrictions | To send SMS in Canada, you need to set up a dedicated number. |
| Service provisioning | 1-3 days business days targeted for any sender. |
| Sender availability | - Long Code (10DLC available if used in both US & CA) - Toll-Free Number - Short Code Only dedicated options are available in the CA. |
| Sender provisioning | LC: Instant, as can buy over portal (10DLC: 7-10 business days for internal compliance review, secondary DCA review, and approval). TFN: TFN verification can take up to 30 business days. SC: 4-6 weeks dependent upon CTA provisioning cycles. |
| Two-way | LC, TFN, SC |
| Two-way provisioning | All senders in Canada are provisioned for 2-way as part of the service and sender provisioning. |
| Country regulations | Marketing and transactional messages are allowed on all senders, subject to compliance review and carrier approval. |
| Country restrictions | Discouraged A2P sending: •	Grey route messaging •	Number sharing •	Number/URL cycling •	Snowshoe messaging •	Artificial traffic inflation fraud •	Spoofing •	Spam, phishing or malicious messaging DND is enabled. Compliance with mandatory keywords in Canada as well as bilingual support of mandatory keywords. |
| Country recommendations | You can send promotional advertisements and other broadcast messages only to subscribers who have specifically opted-in to receive such messages. It is recommended that messages be sent between 9 a.m. and 9 p.m. only. This applies primarily to marketing messages because informational alerts such as transactional messages, fraud alerts, account recovery/2FA, and appointment reminders should be sent when needed. Organizations involved in the operation of A2P messaging programs in Canada must abide by all applicable laws, rules, and regulations that govern the delivery of these types of messages, including Canada’s Anti-Spam Legislation and applicable privacy laws. Adherence to best practices for Canadian Application-to-Person (A2P) messaging programs is required. |