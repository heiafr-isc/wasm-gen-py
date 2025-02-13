# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from io import BytesIO

from pydantic import Field

from wasm_gen import instructions as I  # noqa
from wasm_gen.core import Node
from wasm_gen.values import Integer


class Data(Node):

    _data: BytesIO = BytesIO()

    def __bytes__(self):
        raise NotImplementedError


class PassiveData(Data):
    def __bytes__(self):
        v = self._data.getvalue()
        i = bytes(Integer(len(v))) + v
        return b"\x01" + i


class ActiveData(Data):

    memory: int = 0
    offset: int

    expr: list[Node] = Field(default_factory=list)

    def __bytes__(self):
        expr = self.expr.copy()
        if len(expr) == 0 or expr[-1].__class__ != I.End:
            expr.append(I.End())
        e = b"".join([bytes(b) for b in expr])
        v = self._data.getvalue()
        i = bytes(Integer(value=len(v))) + v

        if self.memory == 0:
            return b"\x00" + e + i
        else:
            return b"\x02" + bytes(Integer(self.memory)) + e + i

    def append_expr(self, *expr: Node):
        self.expr.extend(expr)
