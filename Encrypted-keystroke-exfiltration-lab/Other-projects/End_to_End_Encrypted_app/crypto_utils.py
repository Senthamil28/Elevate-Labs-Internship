import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
        )
    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
        )
    return private_key, public_pem


def load_public_key(public_pem):
    return serialization.load_pem_public_key(public_pem)

def encrypt_message(message, receiver_public_key):
     aes_key = os.urandom(32)
     aesgcm = AESGCM(aes_key)

     nonce = os.urandom(12)
     ciphertext = aesgcm.encrypt(nonce, message.encode(), None)

     encrypted_key = receiver_public_key.encrypt(
         aes_key,
         padding.OAEP(
             mgf = padding.MGF1(algorithm = hashes.SHA256()),
             algorithm = hashes.SHA256(),
             label = None
             )
         )

     return {
         "key": base64.b64encode(encrypted_key).decode(),
         "nonce": base64.b64encode(nonce).decode(),
         "cipher": base64.b64encode(ciphertext).decode()
         }
def decrypt_message(data, private_key):

    encrypted_key = base64.b64decode(data["key"])
    nonce = base64.b64decode(data["nonce"])
    ciphertext = base64.b64decode(data["cipher"])

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
            )
        )

    aesgcm = AESGCM(aes_key)
    message = aesgcm.decrypt(nonce, ciphertext, None)

    return message.decode()

def get_fingerprint(public_pem):
    digest = hashlib.sha256(public_pem).hexdigest()
    return ":".join(digest[i:i+2] for i in range(0, len(digest), 2))


def sign_message(message, private_key):

    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
            ),
        hashes.SHA256())

    return base64.b64encode(signature).decode()


def verify_signature(message, signature, public_key):

    signature = base64.b64decode(signature)

    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
                ),
            hashes.SHA256()
        )

        return True
    except:
        return False
