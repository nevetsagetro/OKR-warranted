# Italy (IT)

Source: https://www.twilio.com/en-us/guidelines/it/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Italy |
| ISO code | The International Organization for Standardization two character representation for the given locale. | IT |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 222 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +39 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | ----- |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | You cannot send SMS to a landline destination number: the Twilio REST API will throw a 400 response with error code 21614, the message will not appear in the logs, and the account will not be charged. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | Sending cannabis related content is strictly prohibited. Sending marketing and promotional messages between 10PM to 8AM, and all day on Sunday is prohibited. In compliance with Italian Communications Authority resolution 42/13/CIR, Twilio Ireland Limited (Twilio) has adopted this Code of Conduct regarding the use of Aliases (i.e., alphanumeric senderIDs) for Business Messaging Services. In this context, an “Alias” is a string of alphanumeric characters shown in the CLI field for SMS/MMS and data transfer communications. Article 5, paragraph 4 of AGCOM (Italian Communications Authority) resolution 42/13/CIR regarding “Regulations for using alphanumeric caller identification indicators in SMS/MMS used for business messaging services” states that messaging service providers must adopt a Code of Conduct in advance, establishing, among other things, the rules for creating an Alias and the measures taken to protect End Users. The Code of Conduct will be regularly updated by Twilio, including but not limited to ensure compliance with any future changes to the regulatory regime applicable to the use of Aliases. +++++++++ In ottemperanza alla delibera 42/13/CIR dell'Autorità per le Garanzie nelle Comunicazioni, Twilio Ireland Limited (Twilio) ha adottato un codice di condotta in merito all'utilizzo di ALIAS (cosiddetti SenderID alfanumerici) per i servizi di messaggistica aziendale. In questo contesto, un "Alias" è una stringa di caratteri alfanumerici visualizzata nel campo dell'indirizzo per SMS/MMS e comunicazioni di trasferimento dati. L'articolo 5, comma 4, della delibera AGCOM 42/13/CIR recante “Regolamento per l'utilizzo degli indicatori alfanumerici di identificazione del chiamante negli SMS/MMS utilizzati per i servizi di messaggistica aziendale” prevede che i fornitori di servizi di messaggistica debbano adottare uno specifico codice di comportamento in anticipare, stabilendo, tra l'altro, le regole per la creazione degli Alias e le misure adottate a tutela degli utenti finali. Il codice di condotta sarà periodicamente aggiornato da Twilio come e laddove necessario per garantire il rispetto di eventuali future modifiche al regime normativo applicabile all'utilizzo degli Alias. ------------------ Messages sent from international mobile numbers to Italy may be replaced with an Alphanumeric Sender ID or a Local Numeric Sender ID. Message delivery to M2M numbers is on best-effort basis only. Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end-user before sending any communication to them, particularly for marketing or other non-essential communications.Only communicate during an end-user’s daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end-user’s local language.Do not contact end-users on do-not-call or do-not-disturb registries. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | --- | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | N/A |
| Best practices | --- | N/A | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Not Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | N/A | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 7-9 weeks |
| UCS-2 support | --- | N/A | N/A | Supported |
| Use case restrictions | --- | N/A | N/A | Please refer to our Italy Short Code Best Practises for further details. |
| Best practices | --- | N/A | N/A | Please refer to our Italy Short Code Best Practises for further details. |

---

### Italy

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- Italy Phone Number: Yes (Only if provided by Bird)
- Italy Short Code: No
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: No
- Generic URL Shortening: No (Only branded URL shortening like yourbrand.link is allowed)
- Quiet Hours/Do Not Disturb: No

Additional Notes : Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules : No specific opt-out regulations

---

## italy

| Key | Value |
| --- | --- |
| MCC | 222 |
| Dialing code | 39 |
| Number portability | Yes |
| Concatenated message | Standard, concatenated messages supported. |
| Service restrictions | No specific restrictions for sending traffic towards Italy. |
| Service provisioning | 1 day to configure the default account setup, more if it's a specific setup. |
| Sender availability | - Alpha - Virtual Long Number Generic senders are not allowed. |
| Sender provisioning | Sender registration process time can take up to 7 days. |
| Two-way | Virtual Long Numbers |
| Two-way provisioning | Between 2-3 working days. |
| Country regulations | Using generic senders is forbidden. Opt-in is not mandatory. |
| Country restrictions | No specific country restrictions. |
| Country recommendations | No specific country recommendations. |