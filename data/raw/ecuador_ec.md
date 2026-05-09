# Ecuador (EC)

Source: https://www.twilio.com/en-us/guidelines/ec/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Ecuador |
| ISO code | The International Organization for Standardization two character representation for the given locale. | EC |
| Region | --- | South America |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 740 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +593 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | No |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. Ecuador Movistar does not support Concatenated SMS. Messages may be delivered, but only the first segment. To ensure successful delivery, keep message content under 160 characters. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Not Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Required | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- |
| UCS-2 support | --- | --- | --- |
| Use case restrictions | --- | --- | --- |
| Best practices | --- | --- | In general, submission with an Alphanumeric Sender ID in Ecuador is not supported. An exception to this rule is the network CNT Mobile, which does support dynamic Alphanumeric Sender IDs. |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | --- | Supported | --- |
| Twilio supported | Whether Twilio supports the feature for the given country. | Not Supported | Supported | Not Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | No | --- |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | --- | --- | --- |
| UCS-2 support | --- | --- | Yes except for he network Movistar | --- |
| Use case restrictions | --- | --- | --- | --- |
| Best practices | --- | --- | You may use a global SMS-capable number to reach mobile phones in Ecuador. Any numeric Sender ID will be overwritten with either a short code or a long code. An exception to this is the network CNT Mobile, which will preserve the Alphanumeric Sender ID. | --- |

---

### Ecuador

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Short Code
- Promotional SMS: Short Code
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): No
- Ecuador Phone Number: No
- Ecuador Short Code: Yes
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: Yes
- Quiet Hours/Do Not Disturb: No

Additional Notes :

- For Promotional Traffic: Messages must be sent Monday to Friday between 9 AM and 6 PM
- Every SMS must clearly identify the sender, including the sender's name or company name

Opt-out Rules : No specific opt-out regulations

---

## ecuador
| Key | Value |
| --- | --- |
| MCC | 740 |
| Dialing code | 593 |
| Number portability | Yes |
| Concatenated message | Concatenated messages supported. |
| Service restrictions | There is local/international and promo/transactional traffic separation within the country. Template registration is needed for Claro. Contact your dedicated account manager or [Support](mailto:support@infobip.com) for more details. All traffic will be considered international, by default. |
| Service provisioning | Default setup is available immediately. Additional takes 1-2 weeks depending on the exact configuration and template registration. |
| Sender availability | Short Codes (dedicated and shared) |
| Sender provisioning | Dedicated Short Codes are requested directly from the operator and there are two types: Gold - easy to remember. Example: 444, 555, etc. Regular - not easy to remember, 1439,5297, etc. |
| Two-way | Available as dedicated Short Code. |
| Two-way provisioning | Usually takes 1-2 months. |
| Country regulations | Whitelisting and template registration are needed on Claro for all marketing traffic. Only template registration for transactional traffic. Marketing and promotional traffic Template Registration requires: - Templates (they should comply with the requirements from the MNO): - Identifying name of the company and sender of the messages should be visible over the templates. - Indicate the dynamic variables with following format: `{DYNAMIC VARIABLE}` - Company name - Estimated monthly traffic volume - Opt-in case described and opt-out case as well. They should have this (is mandatory). - List of phone numbers (only the numbers) of the end users that opted in the campaign - In case the campaign is done with an opt-in method of Keywords, where end users opt in themselves, then the list of phone numbers is not needed Transactional traffic Template Registration requires: - Templates (they should comply with the requirements from the MNO): - Identifying name of the company and sender of the messages should be visible over the templates. - Indicate the dynamic variables with following format: `{DYNAMIC VARIABLE}` - Company name - Estimated monthly traffic volume Marketing content must have opt-out option. Promotional messages have an ASTW from Monday to Friday 9 AM to 6 PM and Saturday 9 AM to 12 PM (needs approval by e-mail). Each message can't be sent to an end-user more than once a day. |
| Country restrictions | Gambling, political and adult content is restricted. |
| Country recommendations | Before sending any traffic, Contact your account manager or [Support](mailto:support@infobip.com) to assess what category (local/international and transactional/promotional) your content falls into. Make sure you have message templates ready for registration to make that process faster. |