#!/usr/bin/env python3
"""Concrete satisfying states and substitutions for both formal claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


def rot4_code(code: int) -> int:
    return ((code - 97 + 4) % 26) + 97


def encrypted_char(code: int) -> int:
    if code < 97:
        return code
    if code <= 122:
        return rot4_code(code)
    return code


def encrypt_result(value: str) -> str:
    # Direct ground interpretation of verification.k's encryptResult /
    # encryptFold / encryptedChar equations.
    return "".join(chr(encrypted_char(ord(char))) for char in value)


def final_loop_char(suffix: str, initial: str) -> str:
    return initial if not suffix else suffix[-1]


def main() -> None:
    work = Path("/tmp/audit-work/reconstruction")
    canonical = load(work / "canonical.py", "witness_canonical")
    candidate = load(work / "solution.py", "witness_candidate")

    witnesses = [
        "",
        "`az{",
        "vwxyz",
        "Hello, World!",
        "éλ中🙂",
        "\ud800\udfff",
    ]
    for value in witnesses:
        formal = encrypt_result(value)
        trusted = canonical(value)
        generated = candidate(value)
        assert formal == trusted == generated
        print(
            f"S={ascii(value)} formal={ascii(formal)} "
            f"canonical={ascii(trusted)} candidate={ascii(generated)}"
        )

    loop_s = "`az{"
    loop_a = "PREFIX:"
    loop_c0 = ""
    loop_post_out = loop_a + encrypt_result(loop_s)
    loop_post_c = final_loop_char(loop_s, loop_c0)
    print(
        "loop_pre_witness="
        f"env=1,s={ascii(loop_s)},out={ascii(loop_a)},c={ascii(loop_c0)},"
        "heap=.Map,stack=.List,ret=noRet,exc=NoExc"
    )
    print(
        f"loop_post_substitution=out={ascii(loop_post_out)},"
        f"c={ascii(loop_post_c)}"
    )
    print(
        "entry_pre_witness=S='',env=0,module_scope=.Map,builtins=-1,"
        "heap=.Map,stack=.List,ret=noRet,exc=NoExc"
    )
    print("SATISFYING_WITNESS_SUBSTITUTION=PASS")


if __name__ == "__main__":
    main()
