# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from wasm_gen import (
    ActiveData,
    BaseFunction,
    Export,
    Function,
    FunctionType,
    Import,
    Memory,
    MemoryType,
    Module,
)
from wasm_gen import instructions as I  # noqa
from wasm_gen.type import i32_t

m = Module()

f1 = BaseFunction(
    type=FunctionType(params=[i32_t, i32_t, i32_t, i32_t], results=[i32_t])
)
m.imports.append(Import(node=f1, module="wasi_snapshot_preview1", name="fd_write"))

f2 = Function(type=FunctionType(params=[], results=[]))
f2.body.extend(
    [
        I.I32Const(value=0),
        I.I32Const(value=8),
        I.I32Store(align=2, offset=0),
        I.I32Const(value=4),
        I.I32Const(value=14),
        I.I32Store(align=2, offset=0),
        I.I32Const(value=1),
        I.I32Const(value=0),
        I.I32Const(value=1),
        I.I32Const(value=20),
        I.Call(function=f1),
        I.Drop(),
        I.End(),
    ]
)
m.funcs.append(f2)

m1 = Memory(type=MemoryType(min_pages=1))
m.memories.append(m1)

d = ActiveData(offset=8)
d.expr.append(I.I32Const(value=8))
d._data.write(b"Hello, World!\n")
m.data.append(d)

m.exports.extend(
    [
        Export(node=f2, name="_start"),
        Export(node=m1, name="memory"),
    ]
)

with open("test.wasm", "wb") as f:
    f.write(bytes(m))
