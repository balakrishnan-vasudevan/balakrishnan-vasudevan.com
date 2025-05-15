#auth-system 
0. Admin inserts username and password into the Kerberos DB.
1. User logs in with the credentials.
2. After a user has logged in, when they want to access a service, the client will generate a secret key from the password.
3. Client sends "user 1, service (or service ID)" in plaintext to the auth service
4. Auth service checks if user exists, fetches encrypted password from the DB.
5. Auth service responds with session key (encrypted by user's secret key from (2) and TGT (Ticket granting ticket) which is encrypted by the session key, expiry date, and user ID.
6. Client decrypts session key using secret key, then decrypts TFT info using session key.
7. Client sends info (TFT, serverIP, userID, timestamp) encrypted by session key to TGS (Ticket granting service) to get service ticket.
8. TGS decrypts TGT and checks validity in the DB.
9. Service Ticket issued to client
10. Client decrypts the session key and get a service ticket
11. Client uses a service ticket to access the service.



![[Pasted image 20231127174627.png]]