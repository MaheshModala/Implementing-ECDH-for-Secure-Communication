# Implementing-ECDH-for-Secure-Communication
Implementing Elliptic Curve Diffie-Hellman for Secure Communication

First, I will try to break down the tasks and try to explain them theoretically before moving on to logical functionality:
1. Key Generation (Initial Setup):
Imagine Mahesh and Satya want to have a completely secret conversation:
Each of them creates two types of keys:
a) ECDH (Elliptic Curve Diffie-Hellman) Keys: Think of this like a special lockbox that can be opened with a unique combination
Each person generates a private key (their secret combination) and a public key (the lockbox itself)
b) RSA Keys: Like a secure wax seal that proves the authenticity of their messages

2. Public Key Exchange
Mahesh and Satya exchange their ECDH public keys. BUT before sending, they sign these keys with their RSA private keys. This is like putting an official seal on an envelope, proving it's really from them.

3. Signature Verification
When Satya receives Mahesh's public key, he checks the signature using Mahesh's RSA public key. This ensures the key truly came from Mahesh and wasn't tampered with. It's like verifying a diplomatic seal's authenticity.

4. Shared Secret Computation
Mahesh uses his private ECDH key and Satya's public ECDH key to compute a shared secret. Satya does the same thing using his private key and Mahesh's public key
Mathematically, they'll arrive at the same secret number. This is like a magical process where they create an identical secret key without ever directly sharing it.

5. Encryption
Once they have the shared secret, they use it to encrypt messages. They use AES-GCM (Advanced Encryption Standard - Galois/Counter Mode).

Example:
Mahesh's Process:
1. Generate ECDH Private/Public Key Pair
2. Generate RSA Private/Public Key Pair
3. Sign his ECDH Public Key with RSA Private Key
4. Send the signed ECDH Public Key to Satya

Satya's Process:
1. Generate ECDH Private/Public Key Pair
2. Generate RSA Private/Public Key Pair
3. Sign his ECDH Public Key with RSA Private Key
4. Send the signed ECDH Public Key to Mahesh

Shared Secret Computation:
- Mahesh uses his ECDH private key + Satya's ECDH public key
- Satya uses his ECDH private key + Mahesh's ECDH public key
- Both compute IDENTICAL shared secret!

Messaging:
Mahesh: "Hey Satya, let's meet at the library."
- Encrypts with shared secret
- Sends encrypted message
- Satya decrypts with the same shared secret

Below is the Process of how to implement this and an expected output from the code:

To run:
**pip install cryptography**
**python secure_communication.py**

Expected Output:
Mahesh's Key Generation:
ECDH Public Key Fingerprint: MFkwEwYHKo

Satya's Key Generation:
ECDH Public Key Fingerprint: MFkwEwYHKo

Mahesh's Signature:
Signature: K1N+4EtXk72L1l1xamLmFR945Dek2NmBvrVgBVgA6nx5iRf0K/pLAGwH2Dh7/FSBqnsAqGHP4pa7ordRmC88dylPVv6/ByOSkxi+Jp0GrG1KY/z7nNWZUwPTQWzDel1TJnttFDBTl6pcoyqqhPoYbWGFuM9PhFq2n9n+nzK0L7XfWVb07z+H3JvgMhJTIkSRNo2s7muhAvogWI2BX4BDSaGstRrZvNgLhMXAJRmKuM4YP7pe7LyoK5d+BlK6bBONKiIQEBM/ai4K/w8WkeJzOVvdPkme3zvu10OcKZz/1deCqPxB9fa98djgZPvi0ezs5rakvfHuLwbJ6LOqaPx4Sw==

Satya's Signature:
Signature: n/4yQ8HjecDn2fN4tHo4txBRXkWjY3RNKXpKw7bhfe9GsNBEr3WS/9v11c4IiHNlXphHCTrkBVO5NXk+aZehZRw1uwebGQlRaH4P9wyf9kS2wlu0FrPEK05SRfJXSPY/0pdzvLLTvgNqLtlpS81q68L36QkpboB9B2KWgp/SkY0oxop2nIZw3MS4Li29nCIRmZapMQ8ODZhLRFh/9wXpJOg3TTpZOgdJ0GnKQUMAedpnii04XKzjNfLAj96zNUOXkx76/4y1lF3gLZJkW5etgB3LXvqJNHSrzIw6YfWWtyDJrN3I73qrcIUZFX+mulB8oWb3HmMRCNgP9BFONavmIQ==
Signature Verification: SUCCESSFUL
Signature Verification: SUCCESSFUL

Mahesh's Shared Secret:
Derived Symmetric Key: CO8cip868vTVpKWX2C+v0ovx6mRGIWHxYniEOUPh38E=

Satya's Shared Secret:
Derived Symmetric Key: CO8cip868vTVpKWX2C+v0ovx6mRGIWHxYniEOUPh38E=

Mahesh's Message Encryption:
Original Message: Hey Satya, let's meet at the library at 3 PM!
Encrypted Message: Dq93vRDswpUoMeTep2xuwrl6HEN8p60L72JpBMoiBfvAFf1xnoAeyZjjLKegx5GkFM1HU06YBc0KUSdPX8xcrvdXQwbqTrHpCQ==

Satya's Message Decryption:
Encrypted Message: Dq93vRDswpUoMeTep2xuwrl6HEN8p60L72JpBMoiBfvAFf1xnoAeyZjjLKegx5GkFM1HU06YBc0KUSdPX8xcrvdXQwbqTrHpCQ==
Decrypted Message: Hey Satya, let's meet at the library at 3 PM!

Satya's Message Encryption:
Original Message: Sure, Mahesh! I'll see you there. Don't be late!
Encrypted Message: CbTt/xb5KoIzN2Yw0ByiYFMBjRqjZmtbZrtj5iW2lpKsyWFTaG2hyIW/OkiGtQTOFtuhJjzGs6zr7FMAKGWlObcGpiiEEAz7XtiCYw==

Mahesh's Message Decryption:
Encrypted Message: CbTt/xb5KoIzN2Yw0ByiYFMBjRqjZmtbZrtj5iW2lpKsyWFTaG2hyIW/OkiGtQTOFtuhJjzGs6zr7FMAKGWlObcGpiiEEAz7XtiCYw==
Decrypted Message: Sure, Mahesh! I'll see you there. Don't be late!
