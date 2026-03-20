# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: MIT

"""
This is an example of how to use the WASM Generator to generate a simple
WebAssembly module that adds two numbers and prints the result. The
generated module imports some functions from the host environment (e.g.,
for reading input and writing output) and defines a function that
performs the addition and prints the result.
"""

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

# Substract 12 from the stack pointer
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Const(value=12),
        I.I32Sub(),
        I.GlobalSet(global_=sp),
    ]
)

# Open the input stream
add.body.extend(
    [
        I.Call(function=open_input),
    ]
)

# Push the address of z (the result of the addition) onto the stack
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Const(value=8),
        I.I32Add(),
    ]
)

# Read x and y
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Const(value=0),
        I.I32Add(),
        I.Call(function=read_int),
        I.GlobalGet(global_=sp),
        I.I32Const(value=4),
        I.I32Add(),
        I.Call(function=read_int),
    ]
)
#  Do the addition of two numbers
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Const(value=0),
        I.I32Add(),
        I.I32Load(),
        I.GlobalGet(global_=sp),
        I.I32Const(value=4),
        I.I32Add(),
        I.I32Load(),
        I.I32Add(),
    ]
)

# Save the result of the addition in z
add.body.extend(
    [
        I.I32Store(),
    ]
)

# Write the result of the addition
add.body.extend(
    [
        I.GlobalGet(global_=sp),
        I.I32Const(value=8),
        I.I32Add(),
        I.I32Load(),
        I.I32Const(value=5),
        I.Call(function=write_int),
        I.Call(function=write_ln),
    ]
)

# Restore the stack pointer
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

with open("add.wasm", "wb") as f:
    f.write(bytes(m))
