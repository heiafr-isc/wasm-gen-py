# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from pydantic import Field

from wasm_gen import instructions as I  # noqa
from wasm_gen.core import Node
from wasm_gen.values import Integer, Vector


class LocalVariables(Node):

    count: int
    type: bytes

    def __bytes__(self) -> bytes:
        return bytes(Integer(value=self.count)) + self.type


class FunctionType(Node):

    params: list[bytes] = Field(default_factory=list)
    results: list[bytes] = Field(default_factory=list)
    _index: int = -1

    def __bytes__(self):
        return (
            b"\x60"
            + bytes(Vector(values=self.params))
            + bytes(Vector(values=self.results))
        )


class BaseFunction(Node):

    type: FunctionType
    _index: int = -1


class Function(BaseFunction):

    local_vars: list[bytes] = Field(default_factory=list)
    # The body is actually a list of Instructions, but if we ask for
    # Instructions here, we get a nasty circular import
    body: list[Node] = Field(default_factory=list)

    def __bytes__(self) -> bytes:
        if len(self.body) == 0:
            raise Exception("Function body is empty")
        if bytes(self.body[-1]) != bytes(I.End()):
            raise Exception("Function body does not end with End instruction")

        bv = bytes(Vector(values=[bytes(v) for v in self.local_vars])) + b"".join(
            [bytes(b) for b in self.body]
        )
        return bytes(Integer(value=len(bv))) + bv
