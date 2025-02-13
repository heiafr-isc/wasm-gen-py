# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from wasm_gen.core import Node
from wasm_gen.function import BaseFunction
from wasm_gen.globals import BaseGlobal
from wasm_gen.values import Integer


class Instruction(Node):
    def __bytes__(self):
        raise NotImplementedError


class Unreachable(Instruction):
    def __bytes__(self):
        return b"\x00"


class Nop(Instruction):
    def __bytes__(self):
        return b"\x01"


class Block(Instruction):
    def __bytes__(self):
        return b"\x02"


class Loop(Instruction):
    def __bytes__(self):
        return b"\x03"


class If(Instruction):
    def __bytes__(self):
        return b"\x04"


class Else(Instruction):
    def __bytes__(self):
        return b"\x05"


class End(Instruction):
    def __bytes__(self):
        return b"\x0b"


class Br(Instruction):

    label: int

    def __bytes__(self):
        return b"\x0c" + bytes(Integer(value=self.label))


class BrIf(Instruction):

    label: int

    def __bytes__(self):
        return b"\x0d" + bytes(Integer(value=self.label))


class BrTable(Instruction):
    def __bytes__(self):
        return b"\x0e"


class Return(Instruction):
    def __bytes__(self):
        return b"\x0f"


class Call(Instruction):

    function: BaseFunction

    def __bytes__(self):
        return b"\x10" + bytes(Integer(value=self.function._index))


class CallIndirect(Instruction):

    typeidx: int
    tableidx: int

    def __bytes__(self):
        return (
            b"\x11"
            + bytes(Integer(value=self.typeidx))
            + bytes(Integer(value=self.tableidx))
        )


class Drop(Instruction):
    def __bytes__(self):
        return b"\x1a"


class Select(Instruction):
    def __bytes__(self):
        return b"\x1b"


class LocalGet(Instruction):

    localidx: int

    def __bytes__(self):
        return b"\x20" + bytes(Integer(value=self.localidx))


class LocalSet(Instruction):

    localidx: int

    def __bytes__(self):
        return b"\x21" + bytes(Integer(value=self.localidx))


class LocalTee(Instruction):

    localidx: int

    def __bytes__(self):
        return b"\x22" + bytes(Integer(value=self.localidx))


class GlobalGet(Instruction):

    global_: BaseGlobal

    def __bytes__(self):
        return b"\x23" + bytes(Integer(value=self.global_._index))


class GlobalSet(Instruction):

    global_: BaseGlobal

    def __bytes__(self):
        return b"\x24" + bytes(Integer(value=self.global_._index))


class TableGet(Instruction):

    tableidx: int

    def __bytes__(self):
        return b"\x25" + bytes(Integer(value=self.tableidx))


class TableSet(Instruction):

    tableidx: int

    def __bytes__(self):
        return b"\x26" + bytes(Integer(value=self.tableidx))


class I32(Instruction):

    align: int = 2
    offset: int = 0

    def __bytes__(self):
        raise NotImplementedError


class I32Load(I32):
    def __bytes__(self):
        return (
            b"\x28"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I32Load8S(I32):
    def __bytes__(self):
        return (
            b"\x2c"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I32Load8U(I32):
    def __bytes__(self):
        return (
            b"\x2d"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I32Load16S(I32):
    def __bytes__(self):
        return (
            b"\x2e"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I32Load16U(I32):
    def __bytes__(self):
        return (
            b"\x2f"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I32Store(I32):
    def __bytes__(self):
        return (
            b"\x36"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I32Store8(I32):
    def __bytes__(self):
        return (
            b"\x3a"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I32Store16(I32):
    def __bytes__(self):
        return (
            b"\x3b"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I32Const(Instruction):

    value: int

    def __bytes__(self):
        return b"\x41" + bytes(Integer(value=self.value))


class I32Eqz(Instruction):
    def __bytes__(self):
        return b"\x45"


class I32Eq(Instruction):
    def __bytes__(self):
        return b"\x46"


class I32Ne(Instruction):
    def __bytes__(self):
        return b"\x47"


class I32LtS(Instruction):
    def __bytes__(self):
        return b"\x48"


class I32LtU(Instruction):
    def __bytes__(self):
        return b"\x49"


class I32GtS(Instruction):
    def __bytes__(self):
        return b"\x4a"


class I32GtU(Instruction):
    def __bytes__(self):
        return b"\x4b"


class I32LeS(Instruction):
    def __bytes__(self):
        return b"\x4c"


class I32LeU(Instruction):
    def __bytes__(self):
        return b"\x4d"


class I32GeS(Instruction):
    def __bytes__(self):
        return b"\x4e"


class I32GeU(Instruction):
    def __bytes__(self):
        return b"\x4f"


class I32Clz(Instruction):
    def __bytes__(self):
        return b"\x67"


class I32Ctz(Instruction):
    def __bytes__(self):
        return b"\x68"


class I32Popcnt(Instruction):
    def __bytes__(self):
        return b"\x69"


class I32Add(Instruction):
    def __bytes__(self):
        return b"\x6a"


class I32Sub(Instruction):
    def __bytes__(self):
        return b"\x6b"


class I32Mul(Instruction):
    def __bytes__(self):
        return b"\x6c"


class I32DivS(Instruction):
    def __bytes__(self):
        return b"\x6d"


class I32DivU(Instruction):
    def __bytes__(self):
        return b"\x6e"


class I32RemS(Instruction):
    def __bytes__(self):
        return b"\x6f"


class I32RemU(Instruction):
    def __bytes__(self):
        return b"\x70"


class I32And(Instruction):
    def __bytes__(self):
        return b"\x71"


class I32Or(Instruction):
    def __bytes__(self):
        return b"\x72"


class I32Xor(Instruction):
    def __bytes__(self):
        return b"\x73"


class I32Shl(Instruction):
    def __bytes__(self):
        return b"\x74"


class I32ShrS(Instruction):
    def __bytes__(self):
        return b"\x75"


class I32ShrU(Instruction):
    def __bytes__(self):
        return b"\x76"


class I32Rotl(Instruction):
    def __bytes__(self):
        return b"\x77"


class I32Rotr(Instruction):
    def __bytes__(self):
        return b"\x78"


class I32WrapI64(Instruction):
    def __bytes__(self):
        return b"\xa7"


class I32TruncF32S(Instruction):
    def __bytes__(self):
        return b"\xa8"


class I32TruncF32U(Instruction):
    def __bytes__(self):
        return b"\xa9"


class I32TruncF64S(Instruction):
    def __bytes__(self):
        return b"\xaa"


class I32TruncF64U(Instruction):
    def __bytes__(self):
        return b"\xab"


class I32ReinterpretF32(Instruction):
    def __bytes__(self):
        return b"\xbc"


class I32Extend8S(Instruction):
    def __bytes__(self):
        return b"\xc0"


class I32Extend16S(Instruction):
    def __bytes__(self):
        return b"\xc1"


class I64(Instruction):

    align: int
    offset: int

    def __bytes__(self):
        raise NotImplementedError


class I64Load(I64):
    def __bytes__(self):
        return (
            b"\x29"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Load8S(I64):
    def __bytes__(self):
        return (
            b"\x30"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Load8U(I64):
    def __bytes__(self):
        return (
            b"\x31"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Load16S(I64):
    def __bytes__(self):
        return (
            b"\x32"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Load16U(I64):
    def __bytes__(self):
        return (
            b"\x33"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Load32S(I64):
    def __bytes__(self):
        return (
            b"\x34"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Load32U(I64):
    def __bytes__(self):
        return (
            b"\x35"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Store(I64):
    def __bytes__(self):
        return (
            b"\x37"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Store8(I64):
    def __bytes__(self):
        return (
            b"\x3c"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Store16(I64):
    def __bytes__(self):
        return (
            b"\x3d"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Store32(I64):
    def __bytes__(self):
        return (
            b"\x3e"
            + bytes(Integer(value=self.align))
            + bytes(Integer(value=self.offset))
        )


class I64Const(Instruction):

    value: int

    def __bytes__(self):
        return b"\x42" + bytes(Integer(value=self.value))


class I64Eqz(Instruction):
    def __bytes__(self):
        return b"\x50"


class I64Eq(Instruction):
    def __bytes__(self):
        return b"\x51"


class I64Ne(Instruction):
    def __bytes__(self):
        return b"\x52"


class I64LtS(Instruction):
    def __bytes__(self):
        return b"\x53"


class I64LtU(Instruction):
    def __bytes__(self):
        return b"\x54"


class I64GtS(Instruction):
    def __bytes__(self):
        return b"\x55"


class I64GtU(Instruction):
    def __bytes__(self):
        return b"\x56"


class I64LeS(Instruction):
    def __bytes__(self):
        return b"\x57"


class I64LeU(Instruction):
    def __bytes__(self):
        return b"\x58"


class I64GeS(Instruction):
    def __bytes__(self):
        return b"\x59"


class I64GeU(Instruction):
    def __bytes__(self):
        return b"\x5a"


class I64Clz(Instruction):
    def __bytes__(self):
        return b"\x79"


class I64Ctz(Instruction):
    def __bytes__(self):
        return b"\x7a"


class I64Popcnt(Instruction):
    def __bytes__(self):
        return b"\x7b"


class I64Add(Instruction):
    def __bytes__(self):
        return b"\x7c"


class I64Sub(Instruction):
    def __bytes__(self):
        return b"\x7d"


class I64Mul(Instruction):
    def __bytes__(self):
        return b"\x7e"


class I64DivS(Instruction):
    def __bytes__(self):
        return b"\x7f"


class I64DivU(Instruction):
    def __bytes__(self):
        return b"\x80"


class I64RemS(Instruction):
    def __bytes__(self):
        return b"\x81"


class I64RemU(Instruction):
    def __bytes__(self):
        return b"\x82"


class I64And(Instruction):
    def __bytes__(self):
        return b"\x83"


class I64Or(Instruction):
    def __bytes__(self):
        return b"\x84"


class I64Xor(Instruction):
    def __bytes__(self):
        return b"\x85"


class I64Shl(Instruction):
    def __bytes__(self):
        return b"\x86"


class I64ShrS(Instruction):
    def __bytes__(self):
        return b"\x87"


class I64ShrU(Instruction):
    def __bytes__(self):
        return b"\x88"


class I64Rotl(Instruction):
    def __bytes__(self):
        return b"\x89"


class I64Rotr(Instruction):
    def __bytes__(self):
        return b"\x8a"


class I64ExtendI32S(Instruction):
    def __bytes__(self):
        return b"\xac"


class I64ExtendI32U(Instruction):
    def __bytes__(self):
        return b"\xad"


class I64TruncF32S(Instruction):
    def __bytes__(self):
        return b"\xae"


class I64TruncF32U(Instruction):
    def __bytes__(self):
        return b"\xaf"


class I64TruncF64S(Instruction):
    def __bytes__(self):
        return b"\xb0"


class I64TruncF64U(Instruction):
    def __bytes__(self):
        return b"\xb1"


class I64ReinterpretF64(Instruction):
    def __bytes__(self):
        return b"\xbd"


class I64Extend8S(Instruction):
    def __bytes__(self):
        return b"\xc0"


class I64Extend16S(Instruction):
    def __bytes__(self):
        return b"\xc1"


class I64Extend32S(Instruction):
    def __bytes__(self):
        return b"\xc2"
