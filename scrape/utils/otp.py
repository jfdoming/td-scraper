import struct


def pack_otp(otp: str) -> bytes:
    assert len(otp) == 6
    return struct.pack(">I", int(otp))[-3:]


def unpack_otp(otp: bytes) -> str:
    return str(struct.unpack(">I", b"\x00" + otp)[0]).zfill(6)
