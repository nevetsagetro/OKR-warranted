# Japan (JP)

Source: https://www.twilio.com/en-us/guidelines/jp/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Japan |
| ISO code | The International Organization for Standardization two character representation for the given locale. | JP |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 440 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +81 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Not Available |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio provides SMS delivery services to Japan via two distinct gateways: International and Domestic. For the International gateway: There's no need for registration.Both dynamic longcodes and alphanumeric sender IDs are supported. For the Domestic gateway: Registration is mandatory.Messages wil be delivered using either a longcode or a shortcode.Customers have the option to select either a dedicated or shared sender ID. Please contact the sales team to use domestic gateway for Japan. Sending firearms, gambling, adult content, money/loan, lead generation, Text 2 Pay, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Phone numbers in message content is not allowed. Message delivery to M2M numbers is on best-effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | When you need to deliver SMS via the Domestic gateway, please contact the sales team from here. | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | 5 weeks | N/A |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | --- | SMS message to the KDDI network in Japan with over five (5) segments may experience delivery delay due to a network limitation on KDDI Japan's platform. |
| Best practices | --- | N/A | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | N/A |
| UCS-2 support | --- | N/A | Supported | N/A |
| Use case restrictions | --- | N/A | N/A | N/A |
| Best practices | --- | N/A | SMS message to the KDDI network in Japan with over five (5) segments may experience delivery delay due to a network limitation on KDDI Japan's platform. International Numeric Sender Id would also be prepended with 010 (eq 01044XX) as per KDDI Japan policy | N/A |

---

### Japan

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: Line (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Japan Phone Number: Yes (Can only be used for local traffic)
- Japan Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- This market has Local and International traffic segmentation
- Sender registration is mandatory only for local traffic

Opt-out Rules : No specific opt-out regulations

---

## japan

| Key | Value |
| --- | --- |
| MCC | 440 |
| Dialing code | 81 |
| Number portability | Yes |
| Concatenated message | Long SMS is supported. |
| Service restrictions | Before you send any kind of traffic towards Japan, contact [Support](mailto:support@infobip.com) or your dedicated account manager to set up this specific route for you. |
| Service provisioning | 1 day to configure default account setup, more if it's a specific setup (depending on the client's needs) |
| Sender availability | Alpha, alphanumeric, numeric. |
| Sender provisioning | Sender registration is not required but there will be some forbidden senders on each network which are not allowed to use. |
| Two-way | Available two-way setup: VLN only (numbers can be used via Softbank, NTT Docomo and au(KDDI) |
| Two-way provisioning | 3-4 weeks for order + time for setup on our side and order form should be filled by your account manager or [Support](mailto:support@infobip.com). |
| Country regulations | No international/local and promotional/transactional traffic type separation. Client belongs to financial sector, traffic is only allowed between 7:00 AM to 8:00 PM |
| Country restrictions | Gambling traffic is prohibited by law in Japan. No fraud or threat contents are allowed. Promotional messages need user opt-ins. |
| Country recommendations | Docomo supports only alpha sender and international numeric senders. Local numeric and short codes will be manipulated by MNO to alpha sender "Reject". KDDI supports only local numeric and alpha senders. SoftBank supports alpha senders and international numeric. Local numeric senders and short codes will be manipulated to a number +44 xxxx xxxx. |