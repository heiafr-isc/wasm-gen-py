# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from wasm_gen.core import Node
from wasm_gen.values import UnsignedInt


class MemoryType(Node):
    min_pages: int
    max_pages: int = None

    def __bytes__(self):
        if self.max_pages is None:
            return b"\x00" + bytes(UnsignedInt(value=self.min_pages))
        else:
            return (
                b"\x01"
                + bytes(UnsignedInt(value=self.min_pages))
                + bytes(UnsignedInt(value=self.max_pages))
            )


class BaseMemory(Node):
    type: MemoryType
    _index: int = -1


class Memory(BaseMemory):
    def __bytes__(self):
        return bytes(self.type)
