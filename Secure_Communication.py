import os
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecureComm:
    def __init__(self, name):
        self.name = name
        self.curve = ec.SECP256R1()
        self.shared_secret = None

    def generate_keys(self):
        ecdh_private = ec.generate_private_key(self.curve)
        ecdh_public = ecdh_private.public_key()
        rsa_private = rsa.generate_private_key(public_exponent=65537,
                                               key_size=2048)
        rsa_public = rsa_private.public_key()

        print(f"\n{self.name}'s Key Generation:")
        print(
            "ECDH Public Key Fingerprint:",
            base64.b64encode(
                ecdh_public.public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo))
            [:10].decode())
        return ecdh_private, ecdh_public, rsa_private, rsa_public

    def sign_key(self, rsa_private, ecdh_public):
        ecdh_public_bytes = ecdh_public.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

        signature = rsa_private.sign(
            ecdh_public_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

        print(f"\n{self.name}'s Signature:")
        print("Signature:", base64.b64encode(signature).decode())
        return signature, ecdh_public_bytes

    def verify_signature(self, rsa_public, signature, ecdh_public_bytes):
        # Verify the signature
        try:
            rsa_public.verify(
                signature, ecdh_public_bytes,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())
            print("Signature Verification: SUCCESSFUL")
            return True
        except:
            print("Signature Verification: FAILED")
            return False

    def compute_shared_secret(self, ecdh_private, peer_ecdh_public):
        shared_secret = ecdh_private.exchange(ec.ECDH(), peer_ecdh_public)

        self.shared_secret = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'shared secret derivation').derive(shared_secret)

        print(f"\n{self.name}'s Shared Secret:")
        print("Derived Symmetric Key:",
              base64.b64encode(self.shared_secret).decode())
        return self.shared_secret

    def encrypt_message(self, message):
        if not self.shared_secret:
            raise ValueError("Shared secret not established")
        aesgcm = AESGCM(self.shared_secret)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, message.encode(), None)

        encrypted = base64.b64encode(nonce + ciphertext).decode()

        print(f"\n{self.name}'s Message Encryption:")
        print("Original Message:", message)
        print("Encrypted Message:", encrypted)
        return encrypted

    def decrypt_message(self, encrypted_message):
        if not self.shared_secret:
            raise ValueError("Shared secret not established")
        decoded = base64.b64decode(encrypted_message.encode())
        nonce = decoded[:12]
        ciphertext = decoded[12:]

        aesgcm = AESGCM(self.shared_secret)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        print(f"\n{self.name}'s Message Decryption:")
        print("Encrypted Message:", encrypted_message)
        print("Decrypted Message:", plaintext.decode())

        return plaintext.decode()

def main():
    # Mahesh's setup
    Mahesh = SecureComm("Mahesh")
    Mahesh_ecdh_private, Mahesh_ecdh_public, Mahesh_rsa_private, Mahesh_rsa_public = Mahesh.generate_keys(
    )
    # Satya's setup
    Satya = SecureComm("Satya")
    Satya_ecdh_private, Satya_ecdh_public, Satya_rsa_private, Satya_rsa_public = Satya.generate_keys(
    )
    # Key signing and verification
    Mahesh_signature, Mahesh_ecdh_public_bytes = Mahesh.sign_key(
        Mahesh_rsa_private, Mahesh_ecdh_public)
    Satya_signature, Satya_ecdh_public_bytes = Satya.sign_key(
        Satya_rsa_private, Satya_ecdh_public)
    # Verify signatures
    Satya.verify_signature(Mahesh_rsa_public, Mahesh_signature,
                           Mahesh_ecdh_public_bytes)
    Mahesh.verify_signature(Satya_rsa_public, Satya_signature,
                            Satya_ecdh_public_bytes)
    # Compute shared secrets
    Mahesh.compute_shared_secret(Mahesh_ecdh_private, Satya_ecdh_public)
    Satya.compute_shared_secret(Satya_ecdh_private, Mahesh_ecdh_public)
    # Message Exchange
    # Mahesh sends a message to Satya
    Mahesh_message = "Hey Satya, let's meet at the library at 3 PM!"
    encrypted_message_1 = Mahesh.encrypt_message(Mahesh_message)
    # Satya decrypts Mahesh's message
    Satya.decrypt_message(encrypted_message_1)
    # Satya sends a reply to Mahesh
    Satya_message = "Sure, Mahesh! I'll see you there. Don't be late!"
    encrypted_message_2 = Satya.encrypt_message(Satya_message)
    # Mahesh decrypts Satya's message
    Mahesh.decrypt_message(encrypted_message_2)

if __name__ == "__main__":
    main()