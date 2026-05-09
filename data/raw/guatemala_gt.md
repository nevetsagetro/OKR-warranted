# Guatemala (GT)

Source: https://www.twilio.com/en-us/guidelines/gt/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Guatemala |
| ISO code | The International Organization for Standardization two character representation for the given locale. | GT |
| Region | --- | Central America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 704 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +502 |

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
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported There is no segregation between International and Domestic Traffic | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 2 weeks | N/A |
| UCS-2 support | --- | Supported | N/A |
| Use case restrictions | --- | Alphanumeric Sender ID pre-registration is only supported to Claro Guatemala. | Dynamic Alphanumeric Sender IDs are not fully supported by Guatemalan mobile operators. Sender IDs may be overwritten with a random domestic longcode or shortcode outside the Twilio platform. |
| Best practices | --- | N/A | You may use an Alphanumeric Sender ID to reach mobile phones in Guatemala. However, the Sender ID will be overwritten with a short code. Pre-register an Alphanumeric Sender ID to Claro Guatemala as delivery of non-registered Sender ID to this network is on best-effort basis only. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported | --- |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | Dynamic Numeric Sender IDs are not fully supported by Guatemalan mobile operators. Sender IDs may be overwritten with a random domestic longcode or shortcode outside the Twilio platform. | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### Guatemala

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Short Code
- Promotional SMS: Short Code
- Two-Way Conversations: SMS with a two-way short code

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Guatemala Phone Number: Yes
- Guatemala Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- SMS traffic is allowed only from 8 AM to 8 PM local time
- Senders are classified by local and international
- Gambling, political, adult content are restricted

Opt-out Rules : No specific opt-out regulations

---

## guatemala
| Key | Value |
| --- | --- |
| MCC | 704 |
| Dialing code | 502 |
| Number portability | No |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Traffic is segmented based on origin. International traffic is more expensive. Before you start sending any local traffic, contact your dedicated account manager or [Support](mailto:support@infobip.com). |
| Service provisioning | Immediately after the account and route configuration is done. |
| Sender availability | Shared Long Numeric |
| Sender provisioning | Shared numbers are immediately available after account and route setup. |
| Two-way | Shared or dedicated Virtual Long Number (local) and Short Code (international). |
| Two-way provisioning | 1-2 days for shared Virtual Long Number and 1-2 months for dedicated Virtual Long Number or Short Code. |
| Country regulations | You can send messages from 8 AM to 8 PM local time. |
| Country restrictions | Gambling, political, adult content, and MNO promotions for other MNOs is restricted. |
| Country recommendations | If you plan to send local traffic (company has headquarters in Guatemala), contact your dedicated account manager or [Support](mailto:support@infobip.com) to ensure your traffic is compliant. |