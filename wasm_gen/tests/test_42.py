# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

import hashlib
from pathlib import Path

from wasm_gen import (
    BaseFunction,
    BaseGlobal,
    BaseMemory,
    Export,
    Function,
    FunctionType,
    GlobalType,
    Import,
    MemoryType,
    Module,
)
from wasm_gen import instructions as I  # noqa
from wasm_gen.type import i32_t


def test_42():

    m = Module()

    open_input = BaseFunction(type=FunctionType(params=[], results=[]))
    read_int = BaseFunction(type=FunctionType(params=[i32_t], results=[]))
    eot = BaseFunction(type=FunctionType(params=[], results=[i32_t]))
    write_char = BaseFunction(type=FunctionType(params=[i32_t], results=[]))
    write_int = BaseFunction(type=FunctionType(params=[i32_t, i32_t], results=[]))
    write_ln = BaseFunction(type=FunctionType(params=[], results=[]))

    m.imports.extend(
        [
            Import(node=open_input, module="sys", name="OpenInput"),
            Import(node=read_int, module="sys", name="ReadInt"),
            Import(node=eot, module="sys", name="eot"),
            Import(node=write_char, module="sys", name="WriteChar"),
            Import(node=write_int, module="sys", name="WriteInt"),
            Import(node=write_ln, module="sys", name="WriteLn"),
        ]
    )

    m1 = BaseMemory(type=MemoryType(min_pages=1))
    m.imports.append(Import(node=m1, module="env", name="memory"))

    sp = BaseGlobal(type=GlobalType(type=i32_t, mutable=True))
    m.imports.append(Import(node=sp, module="env", name="__stack_pointer"))

    say42 = Function(type=FunctionType(params=[], results=[]))

    say42.body.extend(
        [
            I.I32Const(value=42),
            I.I32Const(value=5),
            I.Call(function=write_int),
            I.Call(function=write_ln),
        ]
    )

    say42.body.append(I.End())

    m.funcs.append(say42)

    m.exports.extend(
        [
            Export(node=say42, name="say42"),
        ]
    )

    sig = hashlib.sha256()
    sig.update(bytes(m))

    target = Path(__file__).parent / "test_say42.wasm"

    with open(target, "wb") as f:
        f.write(bytes(m))

    assert (
        sig.hexdigest()
        == "2b74aa60b199f96382ff779d467e21b70fad40cf7fa1674f8c423f3a34039c6a"
    )
