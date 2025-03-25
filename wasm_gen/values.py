# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from wasm_gen.core import Node


class UnsignedInt(Node):

    value: int

    def to_bytes(self, min_len: int = 0) -> bytes:
        res = b""
        value = self.value
        while True:
            byte = value & 0x7F
            value >>= 7
            if (len(res) + 1 >= min_len) and (value == 0):
                res += byte.to_bytes(1, "little")
                return res
            res += (byte | 0x80).to_bytes(1, "little")

    def __bytes__(self) -> bytes:
        return self.to_bytes()


class SignedInt(Node):

    value: int

    def to_bytes(self, min_len: int = 0) -> bytes:
        res = b""
        value = self.value
        while True:
            byte = value & 0x7F
            value >>= 7
            if (len(res) + 1 >= min_len) and (
                (value == 0 and (byte & 0x40) == 0)
                or (value == -1 and (byte & 0x40) != 0)
            ):
                res += byte.to_bytes(1, "little")
                return res
            res += (byte | 0x80).to_bytes(1, "little")

    def __bytes__(self) -> bytes:
        return self.to_bytes()


class FloatingPoint(Node):

    value: float
    size: int = 4

    def __bytes__(self) -> bytes:
        return self.value.to_bytes(self.size, "little")


class Name(Node):

    value: str

    def __bytes__(self) -> bytes:
        value = self.value.encode("utf-8")
        return bytes(UnsignedInt(value=len(value))) + value


class Vector(Node):

    values: list

    def __bytes__(self):
        res = bytes(UnsignedInt(value=len(self.values)))
        for value in self.values:
            res += bytes(value)
        return res
