# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from wasm_gen.core import Node
from wasm_gen.values import UnsignedInt


@dataclass
class MemoryType(Node):
    min_pages: int
    max_pages: int | None = None

    def __bytes__(self) -> bytes:
        if self.max_pages is None:
            return b"\x00" + bytes(UnsignedInt(value=self.min_pages))
        else:
            return (
                b"\x01"
                + bytes(UnsignedInt(value=self.min_pages))
                + bytes(UnsignedInt(value=self.max_pages))
            )


@dataclass
class BaseMemory(Node):
    type: MemoryType
    _index: int = -1


@dataclass
class Memory(BaseMemory):
    def __bytes__(self) -> bytes:
        return bytes(self.type)
