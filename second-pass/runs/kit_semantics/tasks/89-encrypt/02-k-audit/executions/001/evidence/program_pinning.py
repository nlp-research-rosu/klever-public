#!/usr/bin/env python3
"""String-token- and constructor-boundary-aware real-program pinning checks."""

from __future__ import annotations

import hashlib
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")


def compact_k(text: str) -> str:
    """Drop whitespace outside K String tokens while preserving token contents."""
    result = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    if in_string:
        raise AssertionError("unterminated String token")
    return "".join(result)


def balanced_constructor(text: str, start: int) -> tuple[str, int]:
    open_paren = text.find("(", start)
    if open_paren < 0:
        raise AssertionError("constructor has no opening parenthesis")
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1], index + 1
    raise AssertionError("unbalanced constructor")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    submitted = compact_k((WORK / "solution.mpy").read_text(encoding="utf-8"))
    regenerated = compact_k(
        (WORK / "solution.regenerated.mpy").read_text(encoding="utf-8")
    )
    specification = compact_k((WORK / "spec.k").read_text(encoding="utf-8"))
    assert submitted == regenerated

    module_term, module_end = balanced_constructor(submitted, 0)
    assert module_end == len(submitted)
    assert module_term.startswith("Module(")
    solution_inner = module_term[len("Module(") : -1]
    function_term, function_end = balanced_constructor(solution_inner, 0)
    assert function_end == len(solution_inner)
    assert function_term.startswith("FuncDef(")

    entry_start = specification.index("claim[encrypt-entry]:")
    load_start = specification.index("#loadAll(Module(", entry_start)
    loaded_module_start = load_start + len("#loadAll(")
    loaded_module, loaded_module_end = balanced_constructor(
        specification, loaded_module_start
    )
    assert loaded_module.startswith("Module(")
    loaded_inner = loaded_module[len("Module(") : -1]
    loaded_function, loaded_function_end = balanced_constructor(loaded_inner, 0)
    assert loaded_function == function_term

    audit_call = loaded_inner[loaded_function_end:]
    expected_audit_call = (
        'Assign(Name("result"),Call(Name("encrypt"),str(S:IntSeq)))'
    )
    assert audit_call == expected_audit_call, audit_call

    func_prefix = 'FuncDef("encrypt",Params("s"),'
    assert function_term.startswith(func_prefix)
    body = function_term[len(func_prefix) : -1]
    expected_closure = f'closureVal("s",{body},0)'
    entry_text = specification[entry_start:]
    assert entry_text.count(expected_closure) == 1
    assert entry_text.count('"result"|->str(encryptResult(S))') == 1
    assert "requires" not in entry_text

    # The only constructor-level normalization is deletion of whitespace outside
    # String tokens. The submitted body occurs as the exact first constructor in
    # the loaded audit module; the sole extra constructor invokes that binding.
    print(f"submitted_module_sha256={digest(module_term)}")
    print(f"submitted_function_sha256={digest(function_term)}")
    print(f"loaded_function_sha256={digest(loaded_function)}")
    print(f"submitted_function_constructor_bytes={len(function_term)}")
    print(f"entry_wrapper_constructor={audit_call}")
    print(f"post_closure_exact_occurrences={entry_text.count(expected_closure)}")
    print("entry_requires_clause=false")
    print("constructor_level_function_identity=true")
    print("entry_executes_exact_binding_then_call=true")
    print("PROGRAM_PINNING=PASS")


if __name__ == "__main__":
    main()
