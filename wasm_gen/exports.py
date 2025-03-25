# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from wasm_gen.core import Node
from wasm_gen.function import BaseFunction
from wasm_gen.globals import Global
from wasm_gen.memory import Memory
from wasm_gen.values import Name, UnsignedInt

func = b"\x00"
table = b"\x01"
mem = b"\x02"
global_ = b"\x03"


class Export(Node):

    node: Node
    name: str

    def __bytes__(self):
        desc = None
        if isinstance(self.node, BaseFunction):
            desc = func + bytes(UnsignedInt(value=self.node._index))
        elif isinstance(self.node, Memory):
            desc = mem + bytes(UnsignedInt(value=self.node._index))
        elif isinstance(self.node, Global):
            desc = global_ + bytes(UnsignedInt(value=self.node._index))
        else:
            raise Exception("Unknown import type")

        return bytes(Name(value=self.name)) + desc
