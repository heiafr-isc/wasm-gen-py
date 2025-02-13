# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from pydantic import Field

from wasm_gen.core import Node
from wasm_gen.values import Integer


class GlobalType(Node):

    type: bytes
    mutable: bool

    def __bytes__(self):
        if self.mutable:
            return self.type + bytes(Integer(value=1))
        else:
            return self.type + bytes(Integer(value=0))


class BaseGlobal(Node):
    type: GlobalType
    _index: int = -1


class Global(BaseGlobal):

    expr: list[Node] = Field(default_factory=list)

    def __bytes__(self):
        return bytes(self.type) + b"".join([bytes(e) for e in self.expr])
