# United Kingdom (GB)

Source: https://www.twilio.com/en-us/guidelines/gb/sms

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | United Kingdom |
| ISO code | The International Organization for Standardization two character representation for the given locale. | GB |
| Region | --- | Europe |
| Mobile country code | A three digit code associated with the given locale and used in conjunction with a Mobile Network Code to uniquely identify mobile networks. | 234, 235 |
| Dialing code | The dialing prefix used to establish a call or send an SMS from one locale to the given locale. | +44 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | Whether Twilio supports two-way SMS in the given locale. | Yes |
| Number portability available | Whether number portability is available in the given locale. | Yes |
| Twilio concatenated message support | Concatenation refers to the capability of splitting a message that is too long to be sent in one SMS into smaller pieces and then joining the pieces at the receiving end so that the receiver sees the message as one. | Yes* For certain sender ID types this may not be supported. Where messages are split and rejoined may vary based on character encoding. |
| Message length | How many characters can be sent given a particular message encoding before the message will be split into concatenated segments. | Inbound: GSM 3.38=160, Unicode=70 Outbound: GSM 3.38=160, Unicode=70 |
| Twilio MMS support | Multimedia Messaging Service (MMS) provides a standards-based means to send pictures and video to mobile phones. | Converted to SMS with embedded URL |
| Sending SMS to landline numbers | How Twilio handles an SMS message destined for landline telephone number. | Twilio will not check whether the number is a landline and will attempt to send it to our carrier for delivery. Some carriers will convert the SMS into text-to-speech messages via voice calls. |
| Compliance considerations | Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. This table lists some general best practices. | SMS-to-voice functionality is in widespread use in the UK, and as a result, Twilio will not reject messages sent to landlines. Please be aware of this fact because it may not be the desired behavior for your application. If this is not the desired behavior, Twilio Support can help. ________________________________________________ Sending cannabis related content is strictly prohibited. CBD related content is however permissible in the UK _________________________________________________ Twilio recommends testing your message templates before launching campaigns or sending live messages to the UK, as certain characters – such as letters with a diaeresis (commonly known as umlauts, e.g., ü, ö, ä) – may not be delivered intact and could be automatically replaced to facilitate delivery. _________________________________________________ Message delivery to M2M numbers is on best-effort basis only. _________________________________________________ Twilio strongly encourages customers to review proposed use cases with qualified legal counsel to make sure that they comply with all applicable laws. The following are some general best practices: Get opt-in consent from each end user before sending any communication to them, particular for marketing or other non-essential communications.Only communicate during an end user's daytime hours unless it is urgent.SMS campaigns should support HELP/STOP messages, and similar messages, in the end user's local language.Do not contact end users on do-not-call or do-not-disturb registries. _________________________________________________ BT introduced within 2023 strict regulations in order to reduce fraudulent messaging and smishing attempts. Messages sent to BT subscribers with sender IDs related to specific brands will be blocked by default so customers are required to allowlist Alpha Sender IDs related to the specific brands before sending messages with them. Please find more details in BT Protected Brands |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Not Required | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Required only for Protected Sender IDs. Learn more and register via the Console | Supported Learn more |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | --- | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A |
| UCS-2 support | --- | N/A | Supported |
| Use case restrictions | --- | N/A | Protected Sender IDs: In case you need to submit messages using a "MEF protected Sender ID" or a "BT Protected Sender ID" you need to first pre-register it with Twilio. You can register your Protected Sender ID via the Console ___________________________________________________________ The use of generic Sender IDs should be avoided as they are being blocked from the operators. ___________________________________________________________ UK operators have begun restricting Sender IDs that contain special characters (such as ?, ', +, etc.), we recommend using only the following special character set for your alphanumeric Sender IDs: A to Z (Upper case) A to Z (Lower case) . (Period) - (Dash) 0 to 9 (Numeric) _ (Underscore) (Space) & (Ampersand) |
| Best practices | --- | N/A | Generic Sender IDs: Please refrain from using generic sender IDs like SMS, TEXT, InfoSMS, INFO, Verify, Notify etc to avoid being blocked by network operators. Twilio suggests using an Alpha Sender ID that is related to the content of the message. Starting from the 1st November of 2023 the following Alphanumeric Sender IDs will be added to the above list: 1TimePin , 2FA, Accept, Access, Account, Active, Admin, Advise, Alert, Allow, Allowance, App, Appointment, Approve, Approved, Auth, AuthMsg, Authorise, AuthSMS, Aware, Bank, Banking, Bill, Billing, Call, Card, Caution, Certify, Check, CloudOTP, Code, Collect, Collection, Confirm, Contact, Control, Courier, Delay, Deliver, Delivery, Discount, Energy, Fraud, Help, Info, InfoSMS, ISA, Key, Loan, Login, Logistics,, LogMeIn, Logon, Malware, Message, Mobile, Mortgage, MSG, MsgAuth, Network, NoReply, Notify, OneTimePin, Order, OTP, OTPSMS, Package, Parcel, Pay, Payment, Pin, PinCode, Post, Protocol, Purchase, Ratify, Rebate, Receipt, Refund, Reminder, Repayment, Reply, Respond, Save, Saving, Scam, Savings, Schedule, Secure, Security, Service, Shipping, Sign, Signin, Signon, SMS, SMSAuth, SMSCode, SMSlnfo, SMSOTP, SMSVerfiy, Support, System, Text, Trace, Track, Tracking, Trust, TXT, Update, Updates, Validate, Verify, VerifySMS, VerifyMe, Virus, Warn, Warning, Winner |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Operator network capability | Whether mobile operators in the given country support the feature. | Supported | Not Supported | Supported |
| Twilio supported | Whether Twilio supports the feature for the given country. | Supported | Not Supported | Supported |
| Sender ID preserved | In some countries sender IDs for certain sender types are not preserved and are changed for compliance and/or deliverability reasons. In these countries mobile subscribers will see a different ‘from sender ID’ than the one sent by you. | Yes | N/A | Yes |
| Provisioning time | Provisioning is the process of getting the sender ID approved and registered with mobile networks (depending on country requirements). Provisioning time is how long this process takes in the given country. | N/A | N/A | 8-12 weeks |
| UCS-2 support | --- | Supported | N/A | Supported |
| Use case restrictions | --- | Virgin Mobile no longer support SMS to UK landline numbers | N/A | Short codes can only message users on carriers within the countries in which they are provisioned. AlthoughTwilio can provision short codes in multiple countries, if your customers are not located in the UK, you should not obtain a UK short code. Short codes require express consent from end users before any SMS can be sent; if you cannot obtain consent then you should not use a short code. Twilio and/or the carriers will not support certain types of campaigns, including: Those in which express end-user consent cannot be obtained. This includes friend-to-friend invite-based campaigns, as well as opt-ins obtained through lead generation.Those containing cannabis related content. Note: Campaigns dealing with age-restricted content (alcohol, gambling, etc.) are allowed, but will be evaluated on a case-by-case basis by UK carriers. |
| Best practices | --- | N/A | N/A | Refer to our FAQ for short code best practices: https://support.twilio.com/hc/en-us/articles/223134887-Requirements-for-UK-short-codes. |

---

### United Kingdom

Best Messaging Channels by Use Case (Bird's Recommendations)

- Transactional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Promotional SMS: Alphanumeric Sender ID (e.g., "YourBrand")
- Two-Way Conversations: WhatsApp (You can use your existing number or get a new one from Bird)

Sender Types Supported

- Alphanumeric Sender ID (Business names like "Bird" or "Netflix" that send one-way messages): Yes
- United Kingdom Phone Number: Yes
- United Kingdom Short Code: Yes (Only when provisioned by Bird)
- International Phone Number: No
- Generic Sender ID (Sender IDs that don't clearly identify your brand): No

Restrictions

- Operator Registration Required: Yes
- Generic URL Shortening: No (URL whitelisting required)
- Quiet Hours/Do Not Disturb: Yes (Monday-Sunday 20:00-09:00)

Additional Notes :

- Short URLs not supported; URLs must be whitelisted to avoid being blocked
- Financial organizations: Letter of Authorization (LOA) required for financial content to ensure delivery

Opt-out Rules :

- Transactional traffic: Opt-out not required
- Promotional traffic: Must include an opt-out method (URL or Local number)
- If you can't implement opt-out, Bird will add an opt-out URL for you
- If you manage opt-outs yourself, inform Bird to remove their opt-out URL to prevent dual opt-out features

Was this helpful?


---

# SMS Country Information Guide: Middle East

Fuente: https://docs.bird.com/applications/channels/channels/supported-channels/sms/concepts/choose-the-right-sender-availability-and-restrictions-by-country/sms-country-information-guide-middle-east

---

## united-kingdom

| Key | Value |
| --- | --- |
| MCC | 234 |
| Dialing code | 44 |
| Number portability | Yes |
| Concatenated message | Standard. Concatenated messages supported. |
| Service restrictions | No specific restrictions. |
| Service provisioning | 1 day  to configure the default account setup. More if it's a specific setup (it could depend on the supplier). |
| Sender availability | - Alpha - Virtual Long Number - Short Code Only the following special characters are allowed: **.** (dot), **-** (dash), **_** (underscore), **space**, **&** (ampersand), and **'** (apostrophe). Special characters cannot be used as the first character of any Sender ID. Sender registration is mandatory. Generic senders are not allowed. It is possible to request dynamic senders. |
| Sender provisioning | Sender registration can take 2-3 days. |
| Two-way | Virtual Long Number and Short Code |
| Two-way provisioning | The setup for VLN is 2-3 days and for SC is about 1 month. |
| Country regulations | Alpha senders can range from 3-11 in character length (3 is minimum). Shorter senders will be rejected, as well as alpha senders with more than 11 characters. Marketing traffic must be opted in and needs to contain an opt-out capability (STOP to VLNs or unsubscribe URL). |
| Country restrictions | Gambling is legal and well regulated. All forms of online gambling are licensed by the Gambling Commission and therefore can be legally provided in the country under a license from the Commission. The Commission's site has details of both licensed operators and applicants. You can check whether a company is registered and licensed to operate in the UK using the [UK Gambling Commission public register](https://www.gamblingcommission.gov.uk/public-register/businesses). |
| Country recommendations | No specific country recommendations. |