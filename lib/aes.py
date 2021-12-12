from base64 import b64encode, b64decode
from typing import Union

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes


def encrypt(plaintext: str, key: str) -> str:
    """
    encrypt text using AES256 GCM and return output in base64
    """
    salt = get_random_bytes(16)
    secret_key = scrypt(key, str(salt), key_len=32, N=2 ** 17, r=8, p=1)
    cipher = AES.new(secret_key, AES.MODE_GCM)
    cipher_text, auth_tag = cipher.encrypt_and_digest(bytes(plaintext, encoding="utf-8"))
    encrypted_bytes = b"".join([salt, cipher.nonce, auth_tag, cipher_text])

    return b64encode(encrypted_bytes).decode("utf-8")

def decrypt(cipher_text: str, key: Union[str, bytes]) -> str:
    """
    decrypt AES256 GCM encrypted base64 text
    """
    encrypted_bytes = b64decode(cipher_text)

    salt = encrypted_bytes[:16]
    nonce = encrypted_bytes[16:32]
    auth_tag = encrypted_bytes[32:48]
    cipher_text = encrypted_bytes[48:]

    secret_key = scrypt(key, str(salt), key_len=32, N=2 ** 17, r=8, p=1)
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce)
    plaintext = cipher.decrypt_and_verify(cipher_text, auth_tag)
    return plaintext.decode("utf-8")
