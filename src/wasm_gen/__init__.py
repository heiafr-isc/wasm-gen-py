# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from wasm_gen.data import ActiveData, PassiveData
from wasm_gen.exports import Export
from wasm_gen.function import BaseFunction, Function, FunctionType
from wasm_gen.globals import BaseGlobal, Global, GlobalType
from wasm_gen.imports import Import
from wasm_gen.memory import BaseMemory, Memory, MemoryType
from wasm_gen.module import Module

__all__ = [
    "ActiveData",
    "BaseFunction",
    "BaseGlobal",
    "BaseMemory",
    "Export",
    "Function",
    "FunctionType",
    "Global",
    "GlobalType",
    "Import",
    "Memory",
    "MemoryType",
    "Module",
    "PassiveData",
]
