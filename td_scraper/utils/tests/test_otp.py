from scrape.utils.otp import pack_otp, unpack_otp


def test_pack_unpack():
    assert unpack_otp(pack_otp("123456")) == "123456"
    assert unpack_otp(pack_otp("654321")) == "654321"
    assert unpack_otp(pack_otp("012345")) == "012345"
    assert unpack_otp(pack_otp("000000")) == "000000"


def test_unpack_pack():
    assert pack_otp(unpack_otp(b"\x01\x23\x45")) == b"\x01\x23\x45"
    assert pack_otp(unpack_otp(b"\x05\x43\x21")) == b"\x05\x43\x21"
    assert pack_otp(unpack_otp(b"\x00\x00\x12")) == b"\x00\x00\x12"
    assert pack_otp(unpack_otp(b"\x00\x00\x00")) == b"\x00\x00\x00"
