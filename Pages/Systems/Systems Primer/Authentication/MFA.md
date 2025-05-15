#auth-system , #authentication 
MFA works by verifying users using authentication factors other than their usernames and passwords.  
These authentication factors may be something they know (knowledge factor), something they have (possession  
factor), and something they are (inheritance factor).

![[Pasted image 20250511170419.png]]

### Knowledge factor:

As the name suggests, the knowledge factor includes information that only the  
authorized user would know. Some common examples are:

- Passwords
- PINs
- Passphrases
- Answers to security questions

Security questions are not usually recommended since attackers might easily crack them.

### Possession factor:

Here, authentication is performed with something the user possesses, like a mobile phone, a physical token,  
or a smart card. For example, it could be a code generated via an app on the phone or communicated to the  
user through an automated call.

### Inheritance factor:

The inheritance factor, being the most secure of the three factors, involves  
verifying identities with the help of inherited biometric means, such as:

- Fingerprint scanning
- Facial scanning
- Retinal scanning
- Voice recognition

In recent times, the location factor and the time factor have also gained importance. The location factor verifies  
whether subsequent access attempts by a user are not from two completely different, impractical locations. The time  
factor checks the user's access request time and challenges them with additional authenticators if the access is  
requested at an odd hour.

## Why is MFA important and  why should you use it?

Securing resources using just passwords does only the bare minimum to secure identities. There are [numerous attacks](https://blogs.manageengine.com/corporate/general/2022/11/15/password-attacks-how-to-combat-them.html) that a hacker can use to breach passwords—like brute-force attacks, phishing attacks, dictionary attacks, and web app attacks—which is why it's important to implement additional layers of authentication to secure resources.

Users happen to be the weakest links of an organization's security chain. They might unknowingly choose weak passwords, repeat passwords for multiple resources, store passwords in plain sight, or retain the same password for an extended duration. Implementing MFA protects against these user vulnerabilities. So, even if an unauthorized person obtains a user's password, they still cannot gain access to the privileged resources since they would need additional information to complete the subsequent [MFA methods](https://www.manageengine.com/products/self-service-password/kb/password-self-service-multi-factor-authentication-techniques.html).

Privileged accounts, such as admin or C-level executive accounts, are often prone to attacks. If an attacker gets hold of the credentials of any of these accounts, they’ll have access to the most important data and resources in the network, and the repercussions could be irreversible. To reduce risk, organizations must protect their high-risk accounts with [additional layers of security.](https://www.manageengine.com/products/self-service-password/multi-factor-authentication-mfa-for-uac.html)

Deploying MFA not only helps organizations fortify access, but also helps them comply with data regulatory norms, like the [PCI DSS](https://www.manageengine.com/products/self-service-password/pci-dss-password-policy-requirements.html), the [GDPR](https://www.manageengine.com/products/self-service-password/gdpr-password-requirements.html), [NIST 800-63B](https://www.manageengine.com/products/self-service-password/nist-password-guidelines.html), [SOX](https://www.manageengine.com/products/self-service-password/sarbanes-oxley-sox-password-requirements.html), and [HIPAA](https://www.manageengine.com/products/self-service-password/hipaa-password-policy-requirements.html).

## What is the difference  between 2FA and MFA?

### 2FA

[Two-factor authentication (2FA)](https://www.manageengine.com/products/self-service-password/two-factor-authentication.html) is quite synonymous to MFA. However, as the name suggests, 2FA includes a total of only two authentication factors, whereas MFA does not have any restriction on the number of authentication factors involved.

### MFA

[MFA](https://www.manageengine.com/products/self-service-password/active-directory-multi-factor-authentication.html) is more widely used, as it secures resources better with multiple authentication methods. But for a legitimate user, having to prove their identity daily using multiple authentication methods can cause MFA fatigue. For simple and intelligent MFA, AI and machine learning have been integrated with MFA, birthing adaptive MFA.

## What is adaptive or risk-based MFA?

[Adaptive MFA](https://www.manageengine.com/products/self-service-password/adaptive-multi-factor-authentication.html), otherwise known as risk-based MFA, provides users with authentication factors that adapt each time a  
user logs in depending on the AI-determined risk level of the user based on contextual information. Contextual  
information includes the following:

![[Pasted image 20250511170433.png]]

- The number of consecutive logon failures
- The user account and user role category
- The physical location (geolocation) of the user requesting access
- The physical distance (geo velocity) between consecutive logon attempts
- The resource to which access is requested
- The type of device
- Third-party threat intelligence data
- The day of the week and the time of the day
- The operating system type
- The IP address

The authentication factors presented to the user are based on the risk level that is calculated using the above contextual factors. For instance, consider a user trying to log in to their work machine at an untimely hour while on a vacation. The user behavior analytics (UBA) tool recognizes that the user's location and time of access are different, and they are automatically prompted with additional authentication factors to prove their identity.

Sometimes, when user login conditions are checked using AI and no risk is detected, the MFA process can be bypassed for the user. And sometimes, if the user's activity seems suspicious, they can also be denied access to the requested resource.

## What are the  
pros and cons of MFA?

### Pros

- Helps secure sensitive data and user identities
- Shields against breached passwords and stolen user devices
- Easy to implement
- Helps build a secure environment, which helps gain customer trust and build a good reputation for the company
- Helps comply with data [compliance regulations](https://www.manageengine.com/products/self-service-password/password-security-compliance.html) like [the GDPR](https://www.manageengine.com/products/self-service-password/gdpr-password-requirements.html), [the PCI DSS](https://www.manageengine.com/products/self-service-password/pci-dss-password-policy-requirements.html), [HIPAA](https://www.manageengine.com/products/self-service-password/hipaa-password-policy-requirements.html), and [NIST 800-63B](https://www.manageengine.com/products/self-service-password/nist-password-guidelines.html)
- Easy for users to adapt to

### Cons

- Authorized users may sometimes be denied access due to a misplaced device carrying the OTP for the second factor of authentication
- Consumes time and hinders users' productivity
- Possibility of wrong judgement in adaptive MFA, thus denying access to legitimate users
- Can be expensive to implement



- [[Pinterest - 2FA]]
- [[Discord - MFA]]
