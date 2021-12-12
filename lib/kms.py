from os import environ
from typing import Tuple

import boto3
from botocore.config import Config
from base64 import b64encode

class Kms:
    region = environ.get("AWS_REGION")
    config = Config(region_name=region if region is not None else "ap-northeast-2")
    kms = boto3.client("kms", config=config)
    crypto_key_alias = "alias/crypto-key"

    def create_data_key(self) -> Tuple[bytes, bytes]:
        response = self.kms.generate_data_key(KeyId=self.crypto_key_alias, KeySpec="AES_256")
        return response.get("CiphertextBlob"), b64encode(response.get("Plaintext"))

    def decrypt_data_key(self, blob: bytes) -> bytes:
        response = self.kms.decrypt(CiphertextBlob=blob)
        return b64encode(response["Plaintext"])
