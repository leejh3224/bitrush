import lib.aes as aes


def test_aes():
    plaintext = "hello world"

    cipher_text = aes.encrypt(plaintext, key="1234")
    decrypted = aes.decrypt(cipher_text, key="1234")

    assert decrypted == plaintext
