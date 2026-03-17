# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: MIT

from wasm_gen.values import FloatingPoint, Name, SignedInt, UnsignedInt


def test_integers() -> None:
    uInt = UnsignedInt(value=624485)
    assert bytes(uInt) == b"\xe5\x8e\x26"

    sInt = SignedInt(value=-123456)
    assert bytes(sInt) == b"\xc0\xbb\x78"

    sInt = SignedInt(value=64)
    assert bytes(sInt) == b"\xc0\x00"

    uInt = UnsignedInt(value=64)
    assert bytes(uInt) == b"\x40"

    uInt = UnsignedInt(value=1)
    assert bytes(uInt) == b"\x01"
    assert uInt.to_bytes(5) == b"\x81\x80\x80\x80\x00"


def test_floats() -> None:
    f = FloatingPoint(value=3.14)
    assert bytes(f) == b"\xc3\xf5\x48\x40"


def test_double() -> None:
    f = FloatingPoint(value=3.14, size=8)
    assert bytes(f) == b"\x1f\x85\xeb\x51\xb8\x1e\x09\x40"


def test_names() -> None:
    n = Name(value="foo")
    assert bytes(n) == b"\x03foo"

    n = Name(value="français")
    assert bytes(n) == b"\x09fran\xc3\xa7ais"
