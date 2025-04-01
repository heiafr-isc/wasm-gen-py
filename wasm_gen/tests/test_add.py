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


def test_add():

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

    add = Function(type=FunctionType(params=[], results=[]))

    # Substract 12 from the stack pointer for x, y and z
    add.body.extend(
        [
            I.GlobalGet(global_=sp),
            I.I32Const(value=12),
            I.I32Sub(),
            I.GlobalSet(global_=sp),
        ]
    )

    # call OpenInput
    add.body.append(I.Call(function=open_input))

    #  put the address of z (sp + 8) on the stack
    add.body.extend(
        [
            I.GlobalGet(global_=sp),
            I.I32Const(value=8),
            I.I32Add(),
        ]
    )

    # put the address of x (sp+0) on the stack and call ReadInt
    add.body.extend(
        [
            I.GlobalGet(global_=sp),
            I.I32Const(value=0),
            I.I32Add(),
            I.Call(function=read_int),
        ]
    )

    # put the address of y (sp+4) on the stack and call ReadInt
    add.body.extend(
        [
            I.GlobalGet(global_=sp),
            I.I32Const(value=4),
            I.I32Add(),
            I.Call(function=read_int),
        ]
    )

    # load x from memory
    add.body.extend(
        [
            I.GlobalGet(global_=sp),
            I.I32Const(value=0),
            I.I32Add(),
            I.I32Load(),
        ]
    )

    # load y from memory
    add.body.extend(
        [
            I.GlobalGet(global_=sp),
            I.I32Const(value=4),
            I.I32Add(),
            I.I32Load(),
        ]
    )

    # add x and y
    add.body.append(I.I32Add())

    # store the result in z
    add.body.append(I.I32Store())

    # load z from memory
    add.body.extend(
        [
            I.GlobalGet(global_=sp),
            I.I32Const(value=8),
            I.I32Add(),
            I.I32Load(),
        ]
    )

    # put 5 on the stack and call WriteInt and WriteLn
    add.body.extend(
        [
            I.I32Const(value=5),
            I.Call(function=write_int),
            I.Call(function=write_ln),
        ]
    )

    # free stack space
    add.body.extend(
        [
            I.GlobalGet(global_=sp),
            I.I32Const(value=12),
            I.I32Add(),
            I.GlobalSet(global_=sp),
        ]
    )

    add.body.append(I.End())

    m.funcs.append(add)

    m.exports.extend(
        [
            Export(node=add, name="add"),
        ]
    )

    sig = hashlib.sha256()
    sig.update(bytes(m))

    target = Path(__file__).parent / "test_add.wasm"

    with open(target, "wb") as f:
        f.write(bytes(m))

    assert (
        sig.hexdigest()
        == "ec3f432554fccc55d3ad293caf179de958e6e787119470e50f2573ee7a27a4c4"
    )
