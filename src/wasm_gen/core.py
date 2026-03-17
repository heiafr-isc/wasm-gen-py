# SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass


@dataclass
class Node:
    def __bytes__(self) -> bytes:
        raise NotImplementedError
