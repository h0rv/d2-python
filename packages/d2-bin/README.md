# d2-bin

The official [D2](https://d2lang.com) command line tool, packaged as a Python wheel so you can install it with pip or uv. D2 turns text into diagrams.

The wheels contain the unmodified binaries from the [D2 v0.9.0 release](https://github.com/terrastruct/d2/releases/tag/v0.9.0). Nothing is rebuilt or patched. The build script checks every download against the release checksums.

Run it without installing:

```bash
uvx d2-bin --version
```

Install it once and use `d2` everywhere:

```bash
uv tool install d2-bin
d2 --version
```

Or add it to a project, which puts `d2` on the project's PATH:

```bash
uv add d2-bin
```

`d2-bin` and `python -m d2_bin` run the same binary, and `d2_bin.find_d2_bin()` returns its path.

This package is built from [h0rv/d2-python](https://github.com/h0rv/d2-python). It pairs with `d2-python`, which can render diagrams through this binary: `pip install 'd2-python[bin]'`.

## License

D2 is licensed under the [MPL-2.0](https://github.com/terrastruct/d2/blob/master/LICENSE.txt) and includes the TALA layout engine since v0.9.0. The D2 license and third party notices are included in the wheel.
