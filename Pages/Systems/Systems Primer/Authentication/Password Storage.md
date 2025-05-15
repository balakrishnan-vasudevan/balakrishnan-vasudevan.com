> [!question] How to Store Passwords in the Database

https://newsletter.systemdesign.one/p/how-to-store-passwords-in-database
https://iorilan.medium.com/a-basic-question-in-security-interview-how-do-you-store-passwords-in-the-database-676c125cff64

And here’s how you can answer it:

### 1. Hashing

A hacker can retrieve the passwords easily if they’re stored in plaintext form.

So they transform the password using a hash function.



Hash Function Transforming a Password

A hash function creates a unique string value from a password - **fingerprint**. Also the transformation is one-sided. Put simply, it’s impossible to find the password from a fingerprint.

A popular choice for the hash function is [bcrypt](https://en.wikipedia.org/wiki/Bcrypt) because: (1) it’s slow. (2) it needs a ton of computing power. (3) it needs a lot of memory. Thus making it difficult to run many password-cracking attempts for the hacker.



Hashing Explained With an Analogy

Think of the **[hash function](https://en.wikipedia.org/wiki/Hash_function)** as mixing colors - it’s difficult to find the original colors from the new color.



Workflow for Hashing a Password

Here’s how it works:

- The server generates a fingerprint from the given password when the user creates an account.
    
- The password isn’t stored in the database, instead the fingerprint is.
    
- The fingerprint is regenerated whenever the user enters the password.
    

The regenerated fingerprint gets compared against the value in the database. And the user is given access only if the values are equal.

Ready for the best part?

### 2. Salting

A hacker might crack the password from the fingerprint using a rainbow table.

So they add salt to the password.


Rainbow Table

Think of the **[rainbow table](https://en.wikipedia.org/wiki/Rainbow_table)** as a map between _pre-computed_ _fingerprints_ and passwords.

While **[salt](https://en.wikipedia.org/wiki/Salt_\(cryptography\))** is a random string.


Adding Salt to the Password to Create a Unique Fingerprint

And each user gets a unique salt, thus generating different fingerprints. Put simply, 2 users with the same password will have different fingerprints.

Also the rainbow table wouldn’t work after salting because of unique fingerprints. It invalidates the pre-computed values in the rainbow table.

Workflow for Salting a Password

Here’s what happens when the user creates an account:

- The server creates a unique salt for the user.
    
- The server combines the salt with the given password and hashes it.
    

They store the salt alongside the fingerprint in the database.



Workflow for Validating the Password

Here’s what happens when the user enters a password:

- The server retrieves the salt for the specific user from the database.
    
- The server combines the entered password with salt to generate a fingerprint.
    

The server checks if the fingerprints are the same.

Ready for the next technique?

### 3. Stretching

The hacker might do a brute force attack to crack the password.

Imagine **brute forcing** as trying out all number combinations on a number lock.

So they do stretching.


How Key Stretching Works

Think of **[stretching](https://en.wikipedia.org/wiki/Key_stretching)** as applying the same hash function many times. Thus brute forcing becomes slower and more difficult.