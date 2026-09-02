#!/usr/bin/env python3
"""Append reviewer assertions to the exact submitted source in scratch."""

from pathlib import Path


scratch = Path("/tmp/audit-work/38-decode-cyclic")
solution = (scratch / "solution.py").read_text(encoding="utf-8")
assertions = r'''

assert decode_cyclic("") == ""
assert decode_cyclic("a") == "a"
assert decode_cyclic("ab") == "ab"
assert decode_cyclic("abc") == "cab"
assert decode_cyclic("abcd") == "cabd"
assert decode_cyclic("abcde") == "cabde"
assert decode_cyclic("abcdef") == "cabfde"
assert decode_cyclic("abcdefg") == "cabfdeg"
assert decode_cyclic("abcdefgh") == "cabfdegh"
assert decode_cyclic("abcdefghi") == "cabfdeigh"
assert decode_cyclic("bca") == "abc"
assert decode_cyclic("bcaefd") == "abcdef"
assert decode_cyclic("bcaefdg") == "abcdefg"
assert decode_cyclic("elho lorwld") == "hello world"
assert decode_cyclic("\n\t ") == " \n\t"
assert decode_cyclic(encode_cyclic("0123456789")) == "0123456789"
'''
(scratch / "review_concrete_tests.py").write_text(
    solution.rstrip() + assertions,
    encoding="utf-8",
)
