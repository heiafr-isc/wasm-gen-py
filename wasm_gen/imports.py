# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from wasm_gen.core import Node
from wasm_gen.function import BaseFunction
from wasm_gen.globals import BaseGlobal
from wasm_gen.memory import BaseMemory
from wasm_gen.values import Name, UnsignedInt

func = b"\x00"
table = b"\x01"
mem = b"\x02"
global_ = b"\x03"


class Import(Node):

    node: Node
    module: str
    name: str

    def __bytes__(self):
        desc = None
        if isinstance(self.node, BaseFunction):
            desc = func + bytes(UnsignedInt(value=self.node.type._index))
        elif isinstance(self.node, BaseMemory):
            desc = mem + bytes(self.node.type)
        elif isinstance(self.node, BaseGlobal):
            desc = global_ + bytes(self.node.type)
        else:
            raise Exception("Unknown import type")

        return bytes(Name(value=self.module)) + bytes(Name(value=self.name)) + desc
