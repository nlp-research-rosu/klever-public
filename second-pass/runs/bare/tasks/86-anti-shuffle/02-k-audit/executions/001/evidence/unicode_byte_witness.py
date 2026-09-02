#!/usr/bin/env python3
"""Compare the K representation of identity and anti_shuffle on U+03A9."""

import ast
import importlib.util
import re
import sys
from pathlib import Path


def result_bytes(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<result>\s*(\"(?:[^\"\\]|\\.)*\")\s*</result>", text)
    if match is None:
        raise RuntimeError(f"missing result in {path}")
    escaped = ast.literal_eval(match.group(1))
    return escaped.encode("latin-1")


def load_entry(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def main():
    identity = result_bytes(
        Path("/audit-output/evidence/krun-unicode-identity.log")
    )
    modeled = result_bytes(
        Path("/audit-output/evidence/krun-unicode-single-correct-quoting.log")
    )
    canonical = load_entry("canonical", Path("/reference/canonical.py"))("Ω")
    generated = load_entry(
        "generated", Path("/tmp/audit-work/reconstruction/solution.py")
    )("Ω")
    expected_utf8 = canonical.encode("utf-8")
    print(f"input='Ω' utf8={expected_utf8.hex()}")
    print(f"K_identity_bytes={identity.hex()}")
    print(f"K_anti_shuffle_bytes={modeled.hex()}")
    print(f"canonical={canonical!r} generated={generated!r}")
    print(f"identity_preserves_input={identity == expected_utf8}")
    print(f"modeled_matches_identity={modeled == identity}")
    print(f"python_implementations_match={canonical == generated == 'Ω'}")
    return 0 if identity == expected_utf8 and modeled != identity else 1


if __name__ == "__main__":
    sys.exit(main())
