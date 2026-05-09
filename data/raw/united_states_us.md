# United States (US)

Source: https://www.twilio.com/en-us/guidelines/us/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | United States |
| ISO code | The International Organization for Standardization two character representation for the given locale. | US |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 310, 311 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +1 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 1600 characters. |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Supported |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | Twilio will not check whether the number is a landline and will attempt to send it to our carrier for delivery. Some carriers will convert the SMS into text-to-speech messages via voice calls. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio’s customers, including their end users and clients, must comply with applicable laws, regulations, Twilio's policies, including, but not limited, to the Twilio Acceptable Use Policy and the Twilio Messaging Policy, and industry standards, including, but not limited to, telecommunications providers’ policies. U.S. telecommunications providers may assess fees for non-compliant A2P traffic, and Twilio will pass these fees onto you. To date, T-Mobile is the first U.S. telecommunications provider to announce non-compliance fees for violations of T-Mobile’s Code of Conduct. Twilio will update these guidelines accordingly if/when additional U.S. telecommunications providers announce non-compliance fees. T-Mobile non-compliance fees are as follows: 10DLC Long Code Messaging Program Evasion: A $1,000 pass-through fee if a program/campaign is found to be using techniques such as snowshoeing, or unauthorized number replacement/recycling. Content Violation: After prior warning, a $10,000 pass-through fee may be imposed for each unique instance of content violating the T-Mobile Code of Conduct involving the same sender/content provider. This includes SHAFT (Sex, Hate, Alcohol, Firearms, Tobacco) violations, spam, phishing, and messaging that meets the Severity 0 violation as defined in the CTIA Short Code Monitoring Handbook. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | No | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- |
| UCS-2 support | --- | --- | --- |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | Note: The euro symbol (€) is not supported; avoid using this character in message submission toward the United States. | Note: The euro symbol (€) is not supported; avoid using this character in message submission toward the United States. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Not Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | Requires registration | --- | 6 - 10 weeks |
| UCS-2 support | --- | --- | --- | --- |
| Use case restrictions | --- | Loan Advertisements - Third Party Lenders “Get rich quick” schemes Work from Home ProgramsSecret ShopperThird Party Job AlertsRisk Investment Opportunities Illegal substances Lead Generation Hate Speech Dynamic Routing Snowshoeing Filter Evasion Shared Phone Numbers URL Cycling URL Redirects Number Cycling Spam Fraud or Deceptive Messaging Inapproriate Content Profanity High Risk Financial Payday LoansShort Term-High Interest LoansThird Party Mortgage LoanStudent LoansThird Party Auto LoansGambling/Sweepstakes Debt Forgiveness or Debt Collection Debt ConsolidationDebt ReductionThird Party Debt CollectionCredit Repair Phishing Gambling Vape Fireworks For additional insight into these uses cases, including limitations, and exceptions, visit: Forbidden message categories for SMS and MMS in the US and Canada | --- | Loan Advertisements - Third Party Lenders “Get rich quick” schemes Work from Home ProgramsSecret ShopperThird Party Job AlertsRisk Investment Opportunities Illegal substances Lead Generation Hate Speech Dynamic Routing Snowshoeing Filter Evasion Shared Short Codes URL Cycling URL Redirects Number Cycling Spam Fraud or Deceptive Messaging Inapproriate Content Profanity High Risk Financial Payday LoansShort Term-High Interest LoansThird Party Mortgage LoanStudent LoansThird Party Auto Loans Debt Forgiveness or Debt Collection Debt ConsolidationDebt ReductionThird Party Debt CollectionCredit Repair Phishing Gambling Vape Fireworks For additional insight into short code requirements see https://www.twilio.com/guidelines/us/short-code |
| Best practices | --- | Refer to our FAQ for long code best practices. Note: The euro symbol (€) is not supported; avoid using this character in message submission toward the United States. | Note: The euro symbol (€) is not supported; avoid using this character in message submission toward the United States. | Refer to our FAQ for short code best practices. Note: The euro symbol (€) is not supported; avoid using this character in message submission toward the United States. |

## Phone Numbers & Sender ID: Toll Free

| Field | Description | Toll Free |
| --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | Requires Verification |
| UCS-2 support | --- | --- |
| Use case restrictions | --- | High-Risk Financial Services Payday Loans Short Term- High Interest Loans Auto Loans Mortgage Loans Student Loans Debt Collection Gambling/SweepstakesStock AlertsCryptocurrency Get Rich Quick Schemes Deceptive Work from Home ProgramsRisk Investment Opportunities Multi-Level Marketing 3rd Party Debt Collection or ConsolidationDebt ReductionCredit Repair Programs Lead Generation Controlled Substances Tobacco Vape Federally Illegal Drugs Pornography Profanity Hate Speech Phishing Fraud Scams Deceptive Marketing Snowshoeing Filter Evasion Fireworks For additional insight into these uses cases, including limitations, and exceptions, visit: Forbidden message categories for SMS and MMS in the US and Canada |
| Best practices | --- | Note: The euro symbol (€) is not supported; avoid using this character in message submission toward the United States. |

---

## united-states
| Key | Value |
| --- | --- |
| MCC | 310 - 316 |
| Dialing code | 1 |
| Number portability | Yes |
| Concatenated message | Standard and long-concatenated messages are supported. |
| Service restrictions | A dedicated sender is necessary to send SMS in USA. |
| Service provisioning | 1-3 days business days targeted for any sender. |
| Sender availability | - 10 Digit Long Code - Toll-Free Number - Short Code Only dedicated options are available in the US. Shared senders are not allowed. |
| Sender provisioning | 10DLC: 7-10 business days for an internal compliance review, secondary DCA review, and approval. TFN: TFN verification can take up to 14 business days. SC: 2-4 weeks |
| Two-way | 10DLC, TFN, SC |
| Two-way provisioning | All senders in the USA are provisioned for 2-way as part of the service and sender provisioning. |
| Country regulations | Marketing and transactional messages are allowed on all senders, subject to compliance review and carrier approval. All senders in the US require opt-in. DND is enabled. |
| Country restrictions | Prohibited content - SPAM - Fraudulent or misleading messages - Depictions or endorsement of violence - Inappropriate content - Profanity or hate speech - Endorsement of illegal drugs (including cannabis/CBD/marijuana) - Loan advertisements for payday loans or non-direct lenders - Debt relief programs - Credit repair programs - Work and investment opportunities such as job alerts from third-party recruiting firms or risk investment opportunities - Lead generation or sharing of collected information with third parties - Distribution or malware or app downloads from non-secure locations Prohibited practices - Phishing - Fraud or scams - Deceptive marketing - Sharing, selling, or renting consent - Snowshoe sending - Filter evasion - Dynamic routing - URL cycling - Number cycling |
| Country recommendations | You can send messages only to subscribers who have specifically opted-in to receive such messages. Message senders shall also provide proper methods for subscribers who have opted in to opt out in the future. SMS campaigns must support HELP/STOP messages, and similar messages, in the end user's local language. Do not contact end users on do-not-call or do-not-disturb registries. It is recommended not to send promotional traffic during quiet hours (before 8 a.m. and after 9 p.m. in recipients local time). |