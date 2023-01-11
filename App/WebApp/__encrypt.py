from os import path as _path
from typing import Any as _Any

from Crypto.PublicKey import RSA as _RSA
from Crypto.Cipher import PKCS1_v1_5 as _PKCS1_v1_5, PKCS1_OAEP as _PKCS1_OAEP

PRIVATE_KEY_FILE_NAME = "key.rsa"
PUBLIC_KEY_FILE_NAME = "key.rsa.pub"
_keyDir: str = "temp/"
_pathPhrase: str = ""

def _rsaKeyGen(pathPhrase: str) -> None:
    key = _RSA.generate(2048)
    encryptedKey = key.export_key(passphrase=pathPhrase,
                                  pkcs=8,
                                  protection="scryptAndAES128-CBC")
    with open(_path.join(_keyDir, PRIVATE_KEY_FILE_NAME), "wb") as f:
        f.write(encryptedKey)
    with open(_path.join(_keyDir, PUBLIC_KEY_FILE_NAME), "wb") as f:
        f.write(key.publickey().export_key())

def decrypt(data: bytes) -> dict[str, _Any]:
    if not (_path.exists(_path.join(_keyDir, PRIVATE_KEY_FILE_NAME)) and _path.exists(_path.join(_keyDir, PUBLIC_KEY_FILE_NAME))):
        _rsaKeyGen(_pathPhrase)
    with open(_path.join(_keyDir, PRIVATE_KEY_FILE_NAME), "rb") as f:
        key = _RSA.import_key(f.read(), passphrase=_pathPhrase)
    cipher = _PKCS1_OAEP.new(key)
    return cipher.decrypt(data).decode()