# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

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

m = Module()

open_input = BaseFunction(type=FunctionType(params=[], results=[]))
read_int = BaseFunction(type=FunctionType(params=[], results=[i32_t]))
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

#  Do the addition of two numbers
add.body.extend(
    [
        I.Call(function=open_input),
        I.Call(function=read_int),
        I.Call(function=read_int),
        I.I32Add(),
    ]
)

# Write the result of the addition
add.body.extend(
    [
        I.I32Const(value=5),
        I.Call(function=write_int),
        I.Call(function=write_ln),
    ]
)

# Substract 4 from the stack pointer
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Const(value=4),
        I.I32Sub(),
        I.GlobalSet(global_=sp),
    ]
)

# Store 42 into memory (at stack pointer)
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Const(value=42),
        I.I32Store(),
    ]
)

# Write the value of the stack pointer
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Const(value=5),
        I.Call(function=write_int),
        I.Call(function=write_ln),
    ]
)

# Print the value on the top of the stack
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Load(),
        I.I32Const(value=5),
        I.Call(function=write_int),
        I.Call(function=write_ln),
    ]
)

add.body.append(I.End())


m.funcs.append(add)

m.exports.extend(
    [
        Export(node=add, name="add"),
    ]
)

with open("add.wasm", "wb") as f:
    f.write(bytes(m))
