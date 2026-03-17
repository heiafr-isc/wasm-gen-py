# wasm-gen

Python library for generating WebAssembly (WASM) modules.

## Install

```bash
pip install wasm-gen
```

For local development:

```bash
uv sync
```

## Quick Example

```python
from wasm_gen import Export, Function, FunctionType, Module
from wasm_gen import instructions as I

m = Module()
f = Function(type=FunctionType(params=[], results=[]))
f.body.extend([
    I.End(),
])

m.funcs.append(f)
m.exports.append(Export(node=f, name="main"))

wasm_bytes = bytes(m)
with open("module.wasm", "wb") as out:
    out.write(wasm_bytes)
```

## Run Tests

```bash
uv run pytest
```

## Build Documentation

```bash
just make-doc
```

## License

Licensed under MIT.
