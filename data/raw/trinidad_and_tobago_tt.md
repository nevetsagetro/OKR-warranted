# Trinidad and Tobago (TT)

Source: https://www.twilio.com/en-us/guidelines/tt/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Trinidad and Tobago |
| ISO code | The International Organization for Standardization two character representation for the given locale. | TT |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 374 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +1868 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | No |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | No |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- |
| UCS-2 support | --- | --- | --- |
| Use case restrictions | --- | --- | Alpha sender IDs are being overwritten to random numeric for bMobile network. |
| Best practices | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | --- |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Not Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | --- | --- | --- |
| Use case restrictions | --- | Numeric sender IDs are being overwritten to random numeric when sending to bMobile network. | Numeric sender IDs are being overwritten to random numeric when sending to bMobile network. | --- |
| Best practices | --- | You may use a global SMS-capable number to reach mobile phones in Trinidad and Tobago. | --- | --- |

---

### Trinidad and Tobago

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Trinidad and Tobago Phone Number: Yes
- Trinidad and Tobago Short Code: Yes
- International Phone Number: Yes
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes : Two-way SMS not available

Opt-out Rules : No specific opt-out regulations

---

## trinidad-and-tobago

| Key | Value |
| --- | --- |
| MCC | 374 |
| Dialing code | 1868 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No restrictions. |
| Service provisioning | Available immediately. |
| Sender availability | Dynamic to Digicel, VLN to bmobile. |
| Sender provisioning | A dedicated VLN can be obtained for bmobile, it can take up to 3 days. |
| Two-way | Might be available in the set up of Virtual Long Number. |
| Two-way provisioning | It can take up to 2 months. |
| Country regulations | No specific country regulations. |
| Country restrictions | No specific country restrictions. |
| Country recommendations | Contact [Support](mailto:support@infobip.com) or your account manager if you want to get a two-way number for Trinidad and Tobago. |