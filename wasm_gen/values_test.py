# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from wasm_gen.values import Integer, Name


def test_integers():
    n = Integer(value=624485)
    assert bytes(n) == b"\xe5\x8e\x26"

    n = Integer(value=-123456, signed=True)
    assert bytes(n) == b"\xc0\xbb\x78"

    n = Integer(value=1)
    assert bytes(n) == b"\x01"
    assert n.to_bytes(5) == b"\x81\x80\x80\x80\x00"


def test_names():
    n = Name(value="foo")
    assert bytes(n) == b"\x03foo"

    n = Name(value="français")
    assert bytes(n) == b"\x09fran\xc3\xa7ais"
