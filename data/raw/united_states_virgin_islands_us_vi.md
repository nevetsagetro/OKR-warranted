# United States Virgin Islands (US) (VI)

Source: https://www.twilio.com/en-us/guidelines/vi/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | United States Virgin Islands (US) |
| ISO code | The International Organization for Standardization two character representation for the given locale. | VI |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | The US Virgin Islands shares the US MCCs 310, and 311, in addition to the assigned MCC 332. |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +1340 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | No |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. Twilio’s customers, including their end users and clients, must comply with applicable laws, regulations, Twilio's policies, including but not limited to, the Twilio Acceptable Use Policy and the Twilio Messaging Policy, and industry standards, including but not limited to, telecommunications providers’ policies. U.S. telecommunications providers may assess fees for non-compliant A2P traffic, and Twilio will pass these fees onto you. To date, T-Mobile is the first U.S. telecommunications provider to announce non-compliance fees for violations of T-Mobile’s Code of Conduct. Twilio will update these guidelines accordingly if/when additional U.S. telecommunications providers announce non-compliance fees. T-Mobile non-compliance fees are as follows: 10DLC Long Code Messaging Program Evasion: A $1,000 pass-through fee if a program/campaign is found to be using techniques such as snowshoeing, or unauthorized number replacement/recycling. Content Violation: After prior warning, a $10,000 pass-through fee may be imposed for each unique instance of content violating the T-Mobile Code of Conduct involving the same sender/content provider. This includes SHAFT (Sex, Hate, Alcohol, Firearms, Tobacco) violations, spam, phishing, and messaging that meets the Severity 0 violation as defined in the CTIA Short Code Monitoring Handbook. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- |
| UCS-2 support | --- | --- | --- |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | --- | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | --- | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | Requires Registration* | --- | Requires a US Shortcode |
| UCS-2 support | --- | --- | --- | --- |
| Use case restrictions | --- | Some US Operators offer local service in the US Virgin Islands. For those Operators you would need to follow the US Guidelines, including 10DLC Registration. | --- | Some US Operators offer local service in the US Virgin Islands. For those Operators you would need to follow the US Guidelines. |
| Best practices | --- | Refer to our FAQ for long code best practices. | --- | US Operators with local service in the US Virgin Islands will support US shortcodes. Local US Virgin Islands Operators will have their sender id preserved for most US shortcodes and support 2-way messaging. |

## Phone Numbers & Sender ID: Toll Free

| Field | Description | Toll Free |
| --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | Requires Verification |
| UCS-2 support | --- | Supported |
| Use case restrictions | --- | High-Risk Financial Services Payday Loans Short Term- High Interest Loans Auto Loans Mortgage Loans Student Loans Debt Collection Gambling/SweepstakesStock AlertsCryptocurrency Get Rich Quick Schemes Deceptive Work from Home ProgramsRisk Investment Opportunities Multi-Level Marketing 3rd Party Debt Collection or ConsolidationDebt ReductionCredit Repair Programs Lead Generation Controlled Substances Tobacco Vape Federally Illegal Drugs Pornography Profanity Hate Speech Phishing Fraud Scams Deceptive Marketing Snowshoeing Filter Evasion Fireworks For additional insight into these uses cases, including limitations, and exceptions, visit: Forbidden message categories for SMS and MMS in the US and Canada |
| Best practices | --- | Note: The euro symbol (€) is not supported; avoid using this character in message submission toward the US Virgin Islands |
