# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from dataclasses import dataclass, field

from wasm_gen.core import Node
from wasm_gen.values import UnsignedInt


@dataclass
class GlobalType(Node):

    type: bytes
    mutable: bool

    def __bytes__(self) -> bytes:
        if self.mutable:
            return self.type + bytes(UnsignedInt(value=1))
        else:
            return self.type + bytes(UnsignedInt(value=0))


@dataclass
class BaseGlobal(Node):
    type: GlobalType
    _index: int = -1


@dataclass
class Global(BaseGlobal):

    expr: list[Node] = field(default_factory=list)

    def __bytes__(self) -> bytes:
        return bytes(self.type) + b"".join([bytes(e) for e in self.expr])
