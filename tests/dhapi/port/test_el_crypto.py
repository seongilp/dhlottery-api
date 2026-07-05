import base64

from dhapi.port.el_crypto import decrypt_el_payload, encrypt_el_payload


def test_roundtrip():
    key_code = "ABCDEF0123456789ABCDEF0123456789EXTRA"
    plain = "ROUND=323&round=323&LT_EPSD=323&SEL_NO=&BUY_CNT=&AUTO_SEL_SET=SA&SEL_CLASS=&BUY_TYPE=A&ACCS_TYPE=01"
    assert decrypt_el_payload(encrypt_el_payload(plain, key_code), key_code) == plain


def test_roundtrip_korean():
    key_code = "shortkey"
    plain = '{"resultMsg": "구매 성공", "selLotNo": "354094"}'
    assert decrypt_el_payload(encrypt_el_payload(plain, key_code), key_code) == plain


def test_encrypted_format():
    encrypted = encrypt_el_payload("hello", "key")
    salt_hex, iv_hex, ciphertext_b64 = encrypted[:64], encrypted[64:96], encrypted[96:]
    bytes.fromhex(salt_hex)
    bytes.fromhex(iv_hex)
    assert len(base64.b64decode(ciphertext_b64)) % 16 == 0


def test_wrong_key_does_not_reveal_plaintext():
    encrypted = encrypt_el_payload("hello", "key1")
    try:
        assert decrypt_el_payload(encrypted, "key2") != "hello"
    except (ValueError, UnicodeDecodeError):
        pass  # 잘못된 키는 대부분 패딩/디코딩 오류를 일으킴


def test_encryption_is_salted():
    assert encrypt_el_payload("hello", "key") != encrypt_el_payload("hello", "key")
