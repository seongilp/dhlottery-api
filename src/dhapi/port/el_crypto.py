import base64

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

_BLOCK_SIZE = 16
_ITERATION_COUNT = 1000
_SALT_SIZE = 32
_IV_SIZE = 16


def _derive_key(key_code: str, salt: bytes) -> bytes:
    passphrase = key_code[:32].ljust(32, "0")
    return PBKDF2(passphrase, salt, _BLOCK_SIZE, count=_ITERATION_COUNT, hmac_hash_module=SHA256)


def _pad(data: bytes) -> bytes:
    pad_len = _BLOCK_SIZE - len(data) % _BLOCK_SIZE
    return data + bytes([pad_len]) * pad_len


def _unpad(data: bytes) -> bytes:
    return data[: -data[-1]]


def encrypt_el_payload(plain_text: str, key_code: str) -> str:
    """el.dhlottery.co.kr(연금복권) 요청의 q 파라미터 암호화. 포맷: hex(salt 32B) + hex(iv 16B) + base64(ciphertext)"""
    salt = get_random_bytes(_SALT_SIZE)
    iv = get_random_bytes(_IV_SIZE)
    aes = AES.new(_derive_key(key_code, salt), AES.MODE_CBC, iv)
    encrypted = aes.encrypt(_pad(plain_text.encode("utf-8")))
    return salt.hex() + iv.hex() + base64.b64encode(encrypted).decode("ascii")


def decrypt_el_payload(enc_text: str, key_code: str) -> str:
    salt = bytes.fromhex(enc_text[0 : _SALT_SIZE * 2])
    iv = bytes.fromhex(enc_text[_SALT_SIZE * 2 : _SALT_SIZE * 2 + _IV_SIZE * 2])
    aes = AES.new(_derive_key(key_code, salt), AES.MODE_CBC, iv)
    decrypted = _unpad(aes.decrypt(base64.b64decode(enc_text[_SALT_SIZE * 2 + _IV_SIZE * 2 :])))
    return decrypted.decode("utf-8")
