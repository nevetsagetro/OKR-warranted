# Tanzania (TZ)

Source: https://www.twilio.com/en-us/guidelines/tz/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Tanzania |
| ISO code | The International Organization for Standardization two character representation for the given locale. | TZ |
| Region | --- | Middle East & Africa |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 640 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +255 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 Characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Sender ID Compliance Sender ID Registration is required in Tanzania for networks Tigo, Zantel, Vodacom, and Airtel . Starting on June 16, 2025, messages with unregistered Sender IDs to these networks will be blocked. To continue sending messages, you must use a registered Alphanumeric Sender ID. Additional Phone Numbers and Sender ID Guidelines Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: 1. Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications. 2. Only communicate during an end-user’s daytime hours unless it is urgent. 3. SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language. 4. Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required for Tigo, Zantel, Vodacom, and Airtel | Required | Not Supported for Tigo, Zantel, Vodacom, and Airtel Supported for the rest of Tanzania networks |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Not Supported for Tigo, Zantel, Vodacom, and Airtel Supported for the rest of Tanzania networks |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | Yes for the networks that Dynamic Alphanumeric is supported |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 4 weeks | 3 weeks | --- |
| UCS-2 support | --- | Supported | Supported | --- |
| Use case restrictions | --- | N/A | N/A | The Tanzania networks Tigo, Zantel, Vodacom, and Airtel require Sender ID registration. We advise Twilio's customers to register an Alpha Sender ID in Tanzania for full country coverage. Generic Alphanumeric Sender IDs, such as InfoSMS, INFO, Verify and Notify, should be avoided. |
| Best practices | --- | N/A | --- | Use only registered Alphanumeric Sender ID in Tanzania |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Not Supported for Tigo, Zantel, Vodacom, and Airtel | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | No | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Mobile operators in Tanzania do not support Numeric Sender IDs. | N/A |
| Best practices | --- | N/A | Twilio suggests using a pre-registered Alphanumeric Sender ID in Tanzania | N/A |

---

### Tanzania

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Tanzania Phone Number: No
- Tanzania Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- This market has Local and International traffic segmentation
- Letter of Authorization (LOA) is required for sender ID registration
- Must include brand name inside the SMS content for Airtel network

Opt-out Rules : No specific opt-out regulations

---

## tanzania
| Key | Value |
| --- | --- |
| MCC | 640 |
| Dialing code | 255 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | In Tanzania, there is traffic differentiation based on origin. Registration and supply of proper documentation is required for both sending traffic with local or international origin. Before you start sending any content towards Tanzania for the first time, contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Service provisioning | Depending on the traffic origin and operator, service provisioning might take from 1 day, up to 1 week. |
| Sender availability | Alpha sender allowed. Numeric and generic senders will be blocked. |
| Sender provisioning | Depending on the traffic origin, service provisioning might take from 1 day, up to 1 week. |
| Two-way | Two-way services are available for local traffic only. Available two-way setup: - Short Codes (available with Standard, Premium, and Free to End Users billing models). - USSD |
| Two-way provisioning | Average setup for two-way service is 60 days. |
| Country regulations | Traffic is strictly separated into local (if a company has local offices in Tanzania) and international. Special rates apply for international traffic. To register a sender, you have to provide us with an authorization letter appointing Infobip to register the sender. The letter must be signed and stamped. All numeric senders are forbidden (except Short Code). Generic alpha senders are strictly forbidden and will not be registered. The sender name must be connected with company or product name. |
| Country restrictions | Gambling traffic restrictions: online gambling is legal in Tanzania as long as it is not deemed as spam. Opt ins and opt outs are mandatory. Political traffic restrictions: political campaigns are highly regulated. You are not allowed to register any name related to political party as your sender name. No specific restrictions to promo messages apply. |
| Country recommendations | Prior to sending traffic towards Tanzania, please acquire all necessary documentation to speed up registrations and shorten waiting times. For additional info, contact [Support](mailto:support@infobip.com) or your dedicated account manager. |