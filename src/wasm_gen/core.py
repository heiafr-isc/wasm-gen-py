# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

from dataclasses import dataclass


@dataclass
class Node:
    def __bytes__(self) -> bytes:
        raise NotImplementedError
