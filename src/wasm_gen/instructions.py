# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from dataclasses import dataclass

from wasm_gen.core import Node
from wasm_gen.function import BaseFunction
from wasm_gen.globals import BaseGlobal
from wasm_gen.values import SignedInt, UnsignedInt


@dataclass
class Instruction(Node):
    def __bytes__(self) -> bytes:
        raise NotImplementedError


@dataclass
class Unreachable(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x00"


@dataclass
class Nop(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x01"


@dataclass
class BlockInstruction(Instruction):
    block_type: int = 0x40


@dataclass
class Block(BlockInstruction):
    def __bytes__(self) -> bytes:
        return b"\x02" + bytes(UnsignedInt(value=self.block_type))


@dataclass
class Loop(BlockInstruction):
    def __bytes__(self) -> bytes:
        return b"\x03" + bytes(UnsignedInt(value=self.block_type))


@dataclass
class If(BlockInstruction):
    def __bytes__(self) -> bytes:
        return b"\x04" + bytes(UnsignedInt(value=self.block_type))


@dataclass
class Else(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x05"


@dataclass
class End(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x0b"


@dataclass
class Br(Instruction):

    label: int

    def __bytes__(self) -> bytes:
        return b"\x0c" + bytes(UnsignedInt(value=self.label))


@dataclass
class BrIf(Instruction):

    label: int

    def __bytes__(self) -> bytes:
        return b"\x0d" + bytes(UnsignedInt(value=self.label))


@dataclass
class BrTable(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x0e"


class Return(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x0f"


@dataclass
class Call(Instruction):

    function: BaseFunction

    def __bytes__(self) -> bytes:
        return b"\x10" + bytes(UnsignedInt(value=self.function._index))


@dataclass
class CallIndirect(Instruction):

    typeidx: int
    tableidx: int

    def __bytes__(self) -> bytes:
        return (
            b"\x11"
            + bytes(UnsignedInt(value=self.typeidx))
            + bytes(UnsignedInt(value=self.tableidx))
        )


@dataclass
class Drop(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x1a"


@dataclass
class Select(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x1b"


@dataclass
class LocalGet(Instruction):

    localidx: int

    def __bytes__(self) -> bytes:
        return b"\x20" + bytes(UnsignedInt(value=self.localidx))


@dataclass
class LocalSet(Instruction):

    localidx: int

    def __bytes__(self) -> bytes:
        return b"\x21" + bytes(UnsignedInt(value=self.localidx))


@dataclass
class LocalTee(Instruction):

    localidx: int

    def __bytes__(self) -> bytes:
        return b"\x22" + bytes(UnsignedInt(value=self.localidx))


@dataclass
class GlobalGet(Instruction):

    global_: BaseGlobal

    def __bytes__(self) -> bytes:
        return b"\x23" + bytes(UnsignedInt(value=self.global_._index))


@dataclass
class GlobalSet(Instruction):

    global_: BaseGlobal

    def __bytes__(self) -> bytes:
        return b"\x24" + bytes(UnsignedInt(value=self.global_._index))


@dataclass
class TableGet(Instruction):

    tableidx: int

    def __bytes__(self) -> bytes:
        return b"\x25" + bytes(UnsignedInt(value=self.tableidx))


@dataclass
class TableSet(Instruction):

    tableidx: int

    def __bytes__(self) -> bytes:
        return b"\x26" + bytes(UnsignedInt(value=self.tableidx))


@dataclass
class I32(Instruction):

    align: int = 2
    offset: int = 0

    def __bytes__(self) -> bytes:
        raise NotImplementedError


@dataclass
class I32Load(I32):
    def __bytes__(self) -> bytes:
        return (
            b"\x28"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I32Load8S(I32):
    def __bytes__(self) -> bytes:
        return (
            b"\x2c"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I32Load8U(I32):
    def __bytes__(self) -> bytes:
        return (
            b"\x2d"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I32Load16S(I32):
    def __bytes__(self) -> bytes:
        return (
            b"\x2e"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I32Load16U(I32):
    def __bytes__(self) -> bytes:
        return (
            b"\x2f"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I32Store(I32):
    def __bytes__(self) -> bytes:
        return (
            b"\x36"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I32Store8(I32):
    def __bytes__(self) -> bytes:
        return (
            b"\x3a"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I32Store16(I32):
    def __bytes__(self) -> bytes:
        return (
            b"\x3b"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I32Const(Instruction):

    value: int

    def __bytes__(self) -> bytes:
        return b"\x41" + bytes(SignedInt(value=self.value))


@dataclass
class I32Eqz(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x45"


@dataclass
class I32Eq(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x46"


@dataclass
class I32Ne(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x47"


@dataclass
class I32LtS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x48"


@dataclass
class I32LtU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x49"


@dataclass
class I32GtS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x4a"


@dataclass
class I32GtU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x4b"


@dataclass
class I32LeS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x4c"


@dataclass
class I32LeU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x4d"


@dataclass
class I32GeS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x4e"


@dataclass
class I32GeU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x4f"


@dataclass
class I32Clz(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x67"


@dataclass
class I32Ctz(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x68"


@dataclass
class I32Popcnt(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x69"


@dataclass
class I32Add(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x6a"


@dataclass
class I32Sub(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x6b"


@dataclass
class I32Mul(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x6c"


@dataclass
class I32DivS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x6d"


@dataclass
class I32DivU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x6e"


@dataclass
class I32RemS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x6f"


@dataclass
class I32RemU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x70"


@dataclass
class I32And(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x71"


@dataclass
class I32Or(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x72"


@dataclass
class I32Xor(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x73"


@dataclass
class I32Shl(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x74"


@dataclass
class I32ShrS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x75"


@dataclass
class I32ShrU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x76"


@dataclass
class I32Rotl(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x77"


@dataclass
class I32Rotr(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x78"


@dataclass
class I32WrapI64(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xa7"


@dataclass
class I32TruncF32S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xa8"


@dataclass
class I32TruncF32U(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xa9"


@dataclass
class I32TruncF64S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xaa"


@dataclass
class I32TruncF64U(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xab"


@dataclass
class I32ReinterpretF32(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xbc"


@dataclass
class I32Extend8S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xc0"


@dataclass
class I32Extend16S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xc1"


@dataclass
class I64(Instruction):

    align: int
    offset: int

    def __bytes__(self) -> bytes:
        raise NotImplementedError


@dataclass
class I64Load(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x29"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Load8S(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x30"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Load8U(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x31"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Load16S(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x32"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Load16U(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x33"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Load32S(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x34"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Load32U(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x35"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Store(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x37"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Store8(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x3c"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Store16(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x3d"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Store32(I64):
    def __bytes__(self) -> bytes:
        return (
            b"\x3e"
            + bytes(UnsignedInt(value=self.align))
            + bytes(UnsignedInt(value=self.offset))
        )


@dataclass
class I64Const(Instruction):

    value: int

    def __bytes__(self) -> bytes:
        return b"\x42" + bytes(SignedInt(value=self.value))


@dataclass
class I64Eqz(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x50"


@dataclass
class I64Eq(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x51"


@dataclass
class I64Ne(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x52"


@dataclass
class I64LtS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x53"


@dataclass
class I64LtU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x54"


@dataclass
class I64GtS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x55"


@dataclass
class I64GtU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x56"


@dataclass
class I64LeS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x57"


@dataclass
class I64LeU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x58"


@dataclass
class I64GeS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x59"


@dataclass
class I64GeU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x5a"


@dataclass
class I64Clz(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x79"


@dataclass
class I64Ctz(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x7a"


@dataclass
class I64Popcnt(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x7b"


@dataclass
class I64Add(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x7c"


@dataclass
class I64Sub(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x7d"


@dataclass
class I64Mul(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x7e"


@dataclass
class I64DivS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x7f"


@dataclass
class I64DivU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x80"


@dataclass
class I64RemS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x81"


@dataclass
class I64RemU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x82"


@dataclass
class I64And(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x83"


@dataclass
class I64Or(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x84"


@dataclass
class I64Xor(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x85"


@dataclass
class I64Shl(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x86"


@dataclass
class I64ShrS(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x87"


@dataclass
class I64ShrU(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x88"


@dataclass
class I64Rotl(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x89"


@dataclass
class I64Rotr(Instruction):
    def __bytes__(self) -> bytes:
        return b"\x8a"


@dataclass
class I64ExtendI32S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xac"


@dataclass
class I64ExtendI32U(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xad"


@dataclass
class I64TruncF32S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xae"


@dataclass
class I64TruncF32U(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xaf"


@dataclass
class I64TruncF64S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xb0"


@dataclass
class I64TruncF64U(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xb1"


@dataclass
class I64ReinterpretF64(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xbd"


@dataclass
class I64Extend8S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xc0"


@dataclass
class I64Extend16S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xc1"


@dataclass
class I64Extend32S(Instruction):
    def __bytes__(self) -> bytes:
        return b"\xc2"
