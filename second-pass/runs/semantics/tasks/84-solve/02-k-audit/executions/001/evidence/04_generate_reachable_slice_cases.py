#!/usr/bin/env python3
"""Generate bridge-free K claims for every reachable digit-sum bin payload."""

from __future__ import annotations


def int_seq(text: str) -> str:
    result = ".IntSeq"
    for code in reversed([ord(char) for char in text]):
        result = f"iCons({code}, {result})"
    return result


print('requires "/tmp/audit-work/candidate-src/reference-semantics/semantics.k"')
print()
print("module SLICE-REACHABLE")
print("  imports MPY")
for value in range(37):  # max sum for N <= 10000 is 9+9+9+9 = 36
    digits = bin(value)[2:]
    payload = int_seq(digits)
    prefixed = f"iCons(48, iCons(98, {payload}))"
    print()
    print(f"  // digit_sum={value}, bin payload={digits}")
    print("  claim")
    print("    <k>")
    print(
        "      Subscript("
        f"str({prefixed}), Slice(Int(2), NoBound, NoBound)) ~> CONT:K"
    )
    print("      =>")
    print(f"      str({payload}) ~> CONT")
    print("    </k>")
print("endmodule")
