from lib import aes
from lib.kms import Kms


def test_envelope_encryption():
    kms = Kms()
    plaintext = "hello world"

    data_key, plain_key = kms.create_data_key()

    enc = aes.encrypt(plaintext, key=plain_key.decode("utf-8"))

    plain_key = kms.decrypt_data_key(blob=data_key)

    dec = aes.decrypt(enc, key=plain_key)

    print(dec)
    assert dec == plaintext

