# India (IN)

Source: https://www.twilio.com/en-us/guidelines/in/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | India |
| ISO code | The International Organization for Standardization two character representation for the given locale. | IN |
| Region | --- | Asia |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 404, 405 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +91 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | --- | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | 160 characters |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio offers SMS delivery to India through both International and Domestic gateways. International: No DLT registration is required.Messages are transmitted via mobile operators’ International Long Distance Operator (ILDO) connections.Messages are sent using random ILDO-approved short codes in the format 5NNNN—5NNNNNNNN (e.g., 54321).Messages from international customers bypass India’s Do-Not-Disturb (DND) database and are delivered without any time-of-day restrictions. Domestic: Completion of company and Sender ID registration within the mobile operators’ DLT portal is necessary before submitting a registration request to Twilio.Messages will be delivered with the customer’s DLT-registered Alphanumeric Sender ID.Currently, Twilio only supports registration for DLT-registered Alphanumeric Sender IDs but is exploring adding support for promotional messages via DLT-approved 6-digit Sender ID in the near future. Sending firearms, gambling, adult content, money/loan, political, religious, controlled substance, cannabis, and alcohol related content is strictly prohibited. Sending messages with shortened URL is not allowed. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries.Sending gambling related content is strictly prohibited. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | International Pre-registration | Domestic Pre-registration | Dynamic |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Supported | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported Learn more and register via the Console | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | N/A | Mobile operators will append a two-letter prefix to the registered alphanumeric sender ID. For instance, if you send a message from the registered alphanumeric sender ID "TWILIO," it could be delivered as "VM-TWILIO." | No |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | 10 business days | N/A |
| UCS-2 support | --- | N/A | Yes | Yes |
| Use case restrictions | --- | --- | DLT registered alphanumeric Sender IDs must be used strictly according to its DLT approved use-case, such as transactional, service implicit, or service explicit. | Any Alphanumeric Sender ID sent to Indian mobile subscribers will be overwritten with a random short number between five and nine digits long of the format 5NNNN—5NNNNNNN. |
| Best practices | --- | --- | --- | --- |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Supported | Not Supported | Supported |
| Twilio supported | --- | --- | Supported | Supported |
| SenderID Preserved | In some countries sender IDs for certain sender types are not presered adn are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different "from sender ID" than the one sent by you. | --- | No | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 4-6 weeks |
| UCS-2 support | --- | N/A | Supported | Supported |
| Use case restrictions | --- | N/A | Any Numeric Sender ID sent to Indian mobile subscribers will be overwritten with a random short number between five and nine digits long of the format 5NNNN—5NNNNNNN. | N/A |
| Best practices | --- | N/A | N/A | N/A |

---

### India

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes (Note: For international traffic, your sender ID will be changed)
- India Phone Number: Yes (Note: For international traffic, your sender ID will be changed)
- India Short Code: Yes (Note: For international traffic, your sender ID will be changed)
- International Phone Number: Yes (Note: Your sender ID will be changed)
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 21:00-10:00)

Additional Notes :

- This market has Local and International traffic and Marketing and Transactional segmentation
- Sender registration is mandatory only for Local traffic
- Only 6-letter Alphanumeric senders can be registered

Opt-out Rules : No specific opt-out regulations

---

## india
| Key | Value |
| --- | --- |
| MCC | 404 /405 / 406 |
| Dialing code | 91 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | Entities must be DLT compliant before you can sendtraffic locally. Gambling and cryptocurrency traffic forbidden. |
| Service provisioning | Usually it takes 1 day to set up international route set up. |
| Sender availability | For local traffic, ALPHA for transactional traffic, numeric for promo traffic. For international, all senders manipulated into Short Code. |
| Sender provisioning | Local sender registration only, covered in the Country regulation. The sender must be registered with the local MNO (DLT provider). Besides the sender, Principal Entity and Content template also need to be registered before you can start sending the traffic. No sender registration needed for international traffic. |
| Two-way | Tool free Short Code. There's an option for a Virtual Long Number to which end users can reply in a two-way communication. |
| Two-way provisioning | It takes between 2-3 weeks. |
| Country regulations | Local regulation additional inputs: transactional traffic alpha senders, promo traffic numeric senders. Transactional senders to be separated more strictly to OTP, transactional, service implicit, and service explicit. Delivery reports are provided for promotional traffic. International: No promo messages allowed over international gateway. Local traffic: promo messages are sent with a 6 digit numeric number. Delivery reports are provided for promotional traffic. ASTW for promo is 10 AM and 9 PM. International: No promo messages allowed over the international connections. |
| Country restrictions | Gambling and cryptocurrency traffic is forbidden. |
| Country recommendations | Before you apply for the DLT registration, please ensure that your company fits into the parameters of a local entity (local office, local servers for SMS, etc.). For additional info, contact your dedicated account manager or [Support](mailto:support@infobip.com). |