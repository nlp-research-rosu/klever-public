#!/usr/bin/env python3
"""Exhibit a satisfiable entry state and ground-substitute its formal result."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
from collections.abc import Callable


WORK = pathlib.Path("/tmp/audit-work/reconstruction")


def load(path: pathlib.Path, name: str) -> Callable[[str, str], tuple[str, bool]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def delete_acc(source: list[int], deleted: list[int], accumulator: list[int]) -> list[int]:
    result = list(accumulator)
    for code in source:
        if [code] not in [deleted[index : index + 1] for index in range(len(deleted))]:
            result.append(code)
    return result


def reverse_delete_acc(
    source: list[int], deleted: list[int], accumulator: list[int]
) -> list[int]:
    result = list(accumulator)
    for code in source:
        if [code] not in [deleted[index : index + 1] for index in range(len(deleted))]:
            result.insert(0, code)
    return result


def intseq(codes: list[int]) -> str:
    result = ".IntSeq"
    for code in reversed(codes):
        result = f"iCons({code}, {result})"
    return result


def main() -> int:
    s = "abcde"
    c = "ae"
    source_codes = [ord(char) for char in s]
    deleted_codes = [ord(char) for char in c]
    forward = delete_acc(source_codes, deleted_codes, [])
    reverse = reverse_delete_acc(source_codes, deleted_codes, [])
    formal_result = ("".join(map(chr, forward)), forward == reverse)
    canonical = load(WORK / "canonical.py", "witness_canonical")
    candidate = load(WORK / "solution.py", "witness_candidate")

    print("SATISFYING ENTRY STATE")
    print("<k>")
    print(
        '  Call(Name("reverse_delete"), '
        f"(str({intseq(source_codes)}), str({intseq(deleted_codes)}), .Exprs))"
    )
    print("</k>")
    print("<env> 0 </env>")
    print(
        '<scopes> 0 |-> scope("reverse_delete" |-> '
        'closureVal(("s", "c", .ParamNames), PINNED_BODY, 0), parent(-1)) '
        "-1 |-> builtinsScope </scopes>"
    )
    print("<scopeLoc> 1 </scopeLoc> <heap> .Map </heap> <heapLoc> 0 </heapLoc>")
    print("<stack> .List </stack> <ret> noRet </ret> <exc> NoExc </exc> <exit-code> 0 </exit-code>")
    print(f"S_codes={source_codes}")
    print(f"C_codes={deleted_codes}")
    print(f"deleteAcc_ground={intseq(forward)}")
    print(f"reverseDeleteAcc_ground={intseq(reverse)}")
    print(f"formal_ground_result={formal_result!r}")
    print(f"canonical_ground_result={canonical(s, c)!r}")
    print(f"candidate_ground_result={candidate(s, c)!r}")
    ok = formal_result == canonical(s, c) == candidate(s, c) == ("bcd", False)
    print(f"all_ground_results_equal={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
