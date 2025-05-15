Asymmetric Cryptography and Symmetric Cryptography. These are the two ways of encrypting data that SSL uses.

## Asymmetric Cryptography

Asymmetric Cryptography, also known as Public Key Cryptography, is a way of encrypting data using a public key and a private key pair.

With Public Key is the key that will be shared with the outside for anyone who wants to communicate, and the Private Key is the security key that is kept on the server and is not shared.

When communicating, the sender will use the Public Key to encrypt the data, and the receiver will use the Private Key to decrypt the data that it received.
## Symmetric Cryptography

Symmetric Cryptography is also a way of encrypting data like Asymmetric Cryptography, except that instead of using a key pair, it uses only one key for encrypting and decrypting the data.
## SSL data processing

SSL uses both Asymmetric and Symmetric for encrypting data, the communication between two systems using SSL will have two steps as follows: SSL handshake and Data Transfer.

Asymmetric Cryptography is used in the SSL handshake step. Symmetric Cryptography is used for data transfer after the SSL handshake step.

![[Pasted image 20250508211441.png]]
## SSL Handshake

We will take the example of communication between a browser and a web server.

The SSL connection between the two systems will begin with an SSL handshake using Asymmetric Cryptography. This SSL handshake step is for the browser to authenticate the SSL with the server. The process is as follows:

1. The browser sends a message saying “client hello” to the server
2. The server will reply with the content “server hello”, which contains SSL certificate information and the public key of that SSL
3. The browser will confirm whether the SSL authentication information is real or not, if successful, the browser will generate a Session Key
4. This Session Key will be encrypted with the Public Key and sent to the server
5. The server will receive this encrypted Session Key and use the Private Key to decrypt it and save this Session Key, then it will return a signal to the browser that the Session Key has been received

![[Pasted image 20250508211454.png]]

At the end of the SSL handshake process, both the browser and the server have a Session Key, this is the Key that will be used to encrypt and decrypt data during the communication of the two systems later.

# Data Transfer

This is the process of transferring data between two systems, Symmetric Cryptography will be used in this step, and both use Session Key to encrypt and decrypt data.