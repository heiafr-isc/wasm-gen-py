.. SPDX-FileCopyrightText: 2026 Jacques Supcik <jacques.supcik@hefr.ch>
   SPDX-License-Identifier: MIT

WASI Example
============

This example builds a small WebAssembly module that writes `Hello, World!`
through the WASI `fd_write` import.

.. literalinclude:: ../examples/example_wasi.py
   :language: python
   :caption: examples/example_wasi.py
