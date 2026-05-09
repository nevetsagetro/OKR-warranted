# Mexico (MX)

Source: https://www.twilio.com/en-us/guidelines/mx/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Mexico |
| ISO code | The International Organization for Standardization two character representation for the given locale. | MX |
| Region | --- | North America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 334 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +52 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 ASCII characters per message. |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL. |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Message delivery to M2M numbers is on best effort basis only. Dial plan The dial plan in Mexico has recently changed to remove the need to add a 1 after the country code when texting a mobile number, this means that now only the 10-digit subscriber number needs to be dialed after the +52 country prefix, for example +525512345678. Use-case restrictions You must not use SMS as a marketing or research tool in Mexican elections. Carriers will block any numbers used to promote a particular political candidate or cause. You should not use Mexican mobile numbers to send marketing, one-way, or application-to-person (A2P) traffic. URLs and brand names are some of the A2P content likely to be blocked when sending from Mexican numbers. Sending firearms, gambling, adult content, money/loan, lead generation, Text 2 Pay, controlled substance, cannabis, and alcohol related content is strictly prohibited. It is best practice not to send messages between 9PM and 9AM. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported (Optional) | Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported Learn more and register via the Console | Supported Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | Yes | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | 3 weeks | 3 weeks | N/A |
| UCS-2 support | --- | Supported | Supported | Supported |
| Use case restrictions | --- | All promotional traffic must have clear opt out instructions. Pre-registration is only supported for the Telcel and Movistar networks. If traffic is sent to a different MNO or MVNO, it will be delivered with a shared short code. | All promotional traffic must have clear opt out instructions. Pre-registration is only supported for the Telcel, Movistar and AT&T networks. If traffic is sent to a different MNO or MVNO, it will be delivered with a shared short code. | Domestic customers using a Dynamic Alphanumeric Sender ID to submit their messages, should avoid mentioning any international brand names (WhatsApp, Facebook, Instagram, etc) in their SMS content as it could result in message filtering and blocking. In case using such international brand names in the text is required, Twilio suggests pre-registering an Alphanumeric Sender ID so that the message templates get checked and allowlisted. SMS sent with an unregistered Alpha Sender ID will be delivered with the sender ID overwritten with a short code to ensure delivery, though in some cases, it may be replaced with a random local long number. |
| Best practices | --- | --- | Twilio strongly recommends and advises customers who have registered a Domestic Sender ID to exclusively utilize Spanish language within the body content of their SMS messages. This practice ensures compliance with regional regulations. | Customers with Domestic Traffic are suggested registering a Domestic Alphanumeric Sender ID |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported With Limitations | Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | No | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 14 weeks |
| UCS-2 support | --- | Supported | Supported | Supported |
| Use case restrictions | --- | Delivery from Mexican domestic long codes is handled on a best-effort basis and may be unreliable, especially across non-AT&T networks. While AT&T Mexico officially supports these long codes, messages sent to other carriers may still be delivered but will appear from randomized long codes. Additionally, current regulations only allow OTP (One-Time Password) traffic from long codes. If more than nine messages are sent from the same long code within a two-minute window, sender ID rotation will be triggered to help maintain deliverability. For more consistent and reliable performance, we recommend using a +1 number, a registered alphanumeric sender ID, or a dedicated short code. | Domestic customers using an International Longcode to submit their messages, should avoid mentioning any international brand names (WhatsApp, Facebook, Instagram, etc) in their SMS content as it could result in message filtering and blocking. In case using such international brand names in the text is required, Twilio suggests pre-registering an Alphanumeric Sender ID so that the message templates get checked and allowlisted. SMS sent with international long codes will be delivered with the sender ID overwritten with a short code to ensure delivery, though in some cases, it may be replaced with a random local long number. | Refer to our FAQs for short code best practices. |
| Best practices | --- | N/A | --- | Refer to our FAQs for short code best practices. |

---

### Mexico

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric
- Promotional SMS: Alphanumeric
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Mexico Phone Number: Yes
- Mexico Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: Yes (Monday-Thursday 20:00-08:00, Friday-Sunday 20:00-18:00)

Additional Notes :

- If you choose not to maintain the Alpha Sender for your end-users, the messages will default to a Shared Short Code or a Dedicated Short Code if you have previously requested one
- For Mexico, you can request an Alpha Sender registration. If your Alpha Sender sends fewer than 100K messages monthly, there will be a monthly fee of $350 USD
- We have dedicated short codes available for 2-way traffic. It may be more cost-effective for customers to use their own WhatsApp number
- For Promotional Traffic: Allowed from 8:00 AM until 18:00 PM local time

Opt-out Rules : No specific opt-out regulations

---

## mexico
| Key | Value |
| --- | --- |
| MCC | 334 |
| Dialing code | 52 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No restrictions. |
| Service provisioning | Available immediately. |
| Sender availability | Short Codes (shared and dedicated) and alphanumeric senders. |
| Sender provisioning | Shared SC available immediately, dedicated SC and alphanumeric senders can take 4-6 weeks. |
| Two-way | Shared and dedicated Short Code. |
| Two-way provisioning | Shared SC available immediately, dedicated SC can take 4-6 weeks. |
| Country regulations | Promotional content allowed from 8 AM to 6 PM local time. |
| Country restrictions | Adult, political, and religious content is forbidden. |
| Country recommendations | MNOs only allow deliverability over Short Codes. Two-way campaigns need to have a brief approved by the operators. It is mandatory to collect user opt-ins to receive promotional content. |