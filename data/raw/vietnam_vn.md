# Vietnam (VN)

Source: https://www.twilio.com/en-us/guidelines/vn/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Vietnam |
| ISO code | The International Organization for Standardization two character representation for the given locale. | VN |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 452 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +84 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Not available |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Sender ID Compliance Vietnam mobile operators require pre-registration of Alphanumeric Sender IDs and message templates. Numeric Sender IDs are overwritten with generic Alphanumeric Sender IDs outside Twilio’s platform. Quality is lower and delivery is on a best-effort basis because generic Alphanumeric Sender IDs are likely to be blocked or filtered by mobile operators. Twilio therefore recommends using pre-registered Alphanumeric Sender IDs and message templates only. Sending promotional traffic (non transactional) is not currently supported. The enforcement of complete blocking of unregistered Sender IDs in Vietnam is on August 25, 2025. Twilio highly recommends sending from a registered Alphanumeric Sender ID to avoid having your messages blocked. Please ensure you pass your exact registered Alphanumeric Sender ID in the “From” parameter when you send a message. Keep in mind that registered senders are case-sensitive. Content Compliance Requirements for SMS Delivery to Vietnam Starting August 12, 2024, all SMS messages to Vietnam must include a brand name or application name in the message body. This name should be similar or identical to the alphanumeric SenderID header you use to send the SMS message. For example, an OTP message from Company ABC could appear like this: [Company ABC] Your verification code is 123456. Any SMS message to Vietnam that doesn’t contain a brand name or application name may be undelivered or blocked after the start date. Mobile operators prohibit sending virtual currency-related content. You must have a license from the State Bank of Vietnam to send finance-related content via Sender ID. Delivery reports are SMSC-acknowledgment only and are not guaranteed. Sending firearms, gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Messages containing URLs, WhatsApp/LINE chat links, and phone numbers in the body are not allowed. Sending marketing and promotional messages between 8PM to 8AM is prohibited. Additional Phone Numbers and Sender ID Guidelines Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Required | Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | N/A |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 5 weeks | 5 weeks | N/A |
| UCS-2 support | --- | Supported | N/A | N/A |
| Use case restrictions | --- | Mobile operators prohibit sending virtual currency-related content. You must have a license from the State Bank of Vietnam to send finance-related content using a Sender ID. Delivery reports are not supported by all mobile networks other than VietnaMobile. Sending adult, gambling, charity or political content is prohibited. Sending promotional traffic (non transactional) is not currently supported. | Mobile operators prohibit sending virtual currency-related content. You must have a license from the State Bank of Vietnam to send finance-related content using a Sender ID. Delivery reports are not supported by all mobile networks other than VietnaMobile. Sending adult, gambling, charity or political content is prohibited. Sending promotional traffic (non transactional) is not currently supported. | Delivery of messages submitted with unregistered Sender IDs is on a best-effort basis and will be overwritten with either a random Numeric or Alphanumeric Sender ID outside the Twilio platform. The enforcement of complete blocking of unregistered Sender IDs in Vietnam is on August 25, 2025. Twilio highly recommends sending from a registered Alphanumeric Sender ID to avoid having your messages blocked. Please ensure you pass your exact registered Alphanumeric Sender ID in the “From” parameter when you send a message. Keep in mind that registered senders are case-sensitive. |
| Best practices | --- | On receiving your registration request, the Sender ID team will ask you to upload a colored copy of your business registration certificate. This is a legal document issued by the government or a government-related body that legitimizes the formation of a company or corporation. If the Sender ID you requested is different from or is not affiliated with the company requesting the Sender ID, you will need to submit documentation that proves the company is allowed to use the Sender ID’s brand name. For example, Twilio owns the brand ‘Authy’. When Twilio submits a registration request for Authy, it needs to submit a document that proves Twilio owns the rights to use the Authy brand name. | On receiving your registration request, the Sender ID team will ask you to upload a colored copy of your business registration certificate. This is a legal document issued by the government or a government-related body that legitimizes the formation of a company or corporation. If the Sender ID you requested is different from or is not affiliated with the company requesting the Sender ID, you will need to submit documentation that proves the company is allowed to use the Sender ID’s brand name. For example, Twilio owns the brand ‘Authy’. When Twilio submits a registration request for Authy, it needs to submit a document that proves Twilio owns the rights to use the Authy brand name. | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Delivery of messages submitted with Numeric Sender IDs is on a best-effort basis and will be overwritten with either a random Numeric or Alphanumeric Sender ID outside the Twilio platform. The enforcement of complete blocking of unregistered Sender IDs in Vietnam is on August 25, 2025. Twilio highly recommends sending from a registered Alphanumeric Sender ID to avoid having your messages blocked. Please ensure you pass your exact registered Alphanumeric Sender ID in the “From” parameter when you send a message. Keep in mind that registered senders are case-sensitive. | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Vietnam

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Vietnam Phone Number: No
- Vietnam Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- This market has Local and International traffic segmentation
- Local traffic is further divided into industry sectors (e.g., e-commerce, education, banking, and general)
- For local brands, Vietnam business license is required but doesn't guarantee sender ID will be categorized as local
- Content whitelisting required
- Letter of Authorization (LOA) and Certificate of Incorporation required for sender ID registration

Opt-out Rules : No specific opt-out regulations

Was this helpful?


---

# SMS Country Information Guide: Caribbean

Fuente: https://docs.bird.com/applications/channels/channels/supported-channels/sms/concepts/choose-the-right-sender-availability-and-restrictions-by-country/sms-country-information-guide-caribbean

---

## vietnam
| Key | Value |
| --- | --- |
| MCC | 452 |
| Dialing code | 84 |
| Number portability | Yes |
| Concatenated message | Standard |
| Service restrictions | Sender ID registration is required by all operators for local and international brands, for all traffic types. Registration demands more time and documentation than usual. |
| Service provisioning | 1 day to configure the default account setup. More if it is a specific setup (could depend on the supplier). |
| Sender availability | Alpha (numeric IDs are not supported) |
| Sender provisioning | Between 7 and 17 days. |
| Two-way | Shared Short Code is available. |
| Two-way provisioning | Local entity not required. The client needs to register the keyword and MT SMS to reply to the MO SMS. |
| Country regulations | International promotional traffic is not allowed. ASTW is essential for local promotional traffic, with a restriction on evening transmissions. Enabling DND DB is mandatory for promotional traffic. Contact your account manager or [Support](mailto:support@infobip.com) to configure your account appropriately for specific needs related to promotional or marketing communications. It is advisable to obtain opt-in consent from each recipient before sending any communication, especially for marketing or non-essential messages. If a user subscribes or registers on the client's website/app, consent is already included. Opt-out is required for promo traffic. More info here: - [Law and regulations](https://english.mic.gov.vn/law-regulations.htm) - [Trang homepage](https://english.vnta.gov.vn/Trang/default.aspx) Finance sector clients need to provide a financial license from the State Bank. E-commerce clients need to have a stamp of MOIT on their website. Generic senders are not allowed, and they will be blocked by the operator. |
| Country restrictions | Gambling, gaming, sex, politics, tobacco, alcohol, and beer content is forbidden. |
| Country recommendations | We suggest to reach out to your account manager or [Support](mailto:support@infobip.com) to adequately set up your account for your specific requirements. |