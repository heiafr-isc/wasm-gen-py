# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

import pickle

from pydantic import Field, PositiveInt

from wasm_gen.core import Node
from wasm_gen.exports import Export
from wasm_gen.function import BaseFunction, Function
from wasm_gen.globals import BaseGlobal, Global
from wasm_gen.imports import Import
from wasm_gen.memory import BaseMemory, Memory
from wasm_gen.values import UnsignedInt, Vector


class Section(Node):

    section_id: int
    body: bytes

    def __bytes__(self) -> bytes:
        return (
            bytes(bytes([self.section_id]))
            + bytes(UnsignedInt(value=len(self.body)))
            + self.body
        )


class Module(Node):

    version: PositiveInt = 1

    imports: list[Import] = Field(default_factory=list)
    exports: list[Export] = Field(default_factory=list)
    funcs: list[Function] = Field(default_factory=list)
    memories: list[Memory] = Field(default_factory=list)
    globals_: list[Global] = Field(default_factory=list)
    data: list = Field(default_factory=list)

    _types: list

    def compute_indexes(self):
        types = {}
        type_index = 0
        function_index = 0
        memory_index = 0
        global_index = 0
        self._types = []

        for i in self.imports:
            if isinstance(i.node, BaseFunction):
                f = i.node
                t = f.type
                type_sig = pickle.dumps((t.params, t.results))
                if type_sig not in types:
                    self._types.append(t)
                    types[type_sig] = type_index
                    type_index += 1
                t._index = types[type_sig]
                f._index = function_index
                function_index += 1
            elif isinstance(i.node, BaseMemory):
                m = i.node
                m._index = memory_index
                memory_index += 1
            elif isinstance(i.node, BaseGlobal):
                g = i.node
                g._index = global_index
                global_index += 1

        for f in self.funcs:
            t = f.type
            type_sig = pickle.dumps((t.params, t.results))
            if type_sig not in types:
                self._types.append(t)
                types[type_sig] = type_index
                type_index += 1
            t._index = types[type_sig]
            f._index = function_index
            function_index += 1

        for m in self.memories:
            m._index = memory_index
            memory_index += 1

        for g in self.globals_:
            g._index = global_index
            global_index += 1

    def type_section(self) -> Section:
        return Section(
            section_id=1,
            body=bytes(
                Vector(
                    values=[bytes(t) for t in self._types],
                )
            ),
        )

    def import_section(self) -> Section:
        return Section(
            section_id=2,
            body=bytes(
                Vector(
                    values=[bytes(i) for i in self.imports],
                )
            ),
        )

    def function_section(self) -> Section:
        return Section(
            section_id=3,
            body=bytes(
                Vector(
                    values=[
                        bytes(UnsignedInt(value=f.type._index)) for f in self.funcs
                    ],
                )
            ),
        )

    def memory_section(self) -> Section:
        if len(self.memories) == 0:
            return b""
        mv = bytes(Vector(values=[bytes(i) for i in self.memories]))
        return Section(section_id=5, body=mv)

    def global_section(self) -> Section:
        if len(self.globals_) == 0:
            return b""
        gv = bytes(Vector(values=[bytes(i) for i in self.globals_]))
        return Section(section_id=6, body=gv)

    def export_section(self) -> Section:
        return Section(
            section_id=7,
            body=bytes(
                Vector(
                    values=[bytes(e) for e in self.exports],
                )
            ),
        )

    def code_section(self) -> Section:
        return Section(
            section_id=10, body=bytes(Vector(values=[bytes(f) for f in self.funcs]))
        )

    def data_section(self) -> Section:

        if len(self.data) == 0:
            return b""

        dv = bytes(Vector(values=[bytes(i) for i in self.data]))
        return Section(section_id=11, body=dv)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def magic(self) -> bytes:
        return b"\0asm"

    def write_version(self) -> bytes:
        return self.version.to_bytes(4, "little")

    def add_import(self, import_: Import):
        self.imports.append(import_)

    def add_export(self, export: Node):
        self.exports.append(export)

    def add_function(self, function: Function):
        self.funcs.append(function)

    def add_memory(self, memory):
        self.memories.append(memory)

    def add_data(self, data):
        self.data.append(data)

    def __bytes__(self) -> bytes:
        self.compute_indexes()
        return (
            self.magic()
            + self.write_version()
            + bytes(self.type_section())  # 1
            + bytes(self.import_section())  # 2
            + bytes(self.function_section())  # 3
            + bytes(self.memory_section())  # 5
            + bytes(self.global_section())  # 6
            + bytes(self.export_section())  # 7
            + bytes(self.code_section())  # 10
            + bytes(self.data_section())  # 11
        )
