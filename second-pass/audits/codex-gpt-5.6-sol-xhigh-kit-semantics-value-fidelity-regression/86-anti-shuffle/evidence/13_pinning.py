#!/usr/bin/env python3
"""Structurally compare the entry/loop claims with the submitted MPY AST."""

from pathlib import Path

ROOT = Path("/tmp/audit-work/anti-shuffle-audit")
solution = (ROOT / "solution.submitted.mpy").read_text(encoding="utf-8")
spec = (ROOT / "spec.k").read_text(encoding="utf-8")
verification = (ROOT / "verification.k").read_text(encoding="utf-8")


def extract_call(text: str, marker: str, start: int = 0) -> tuple[str, int]:
    offset = text.index(marker, start)
    open_paren = offset + len(marker) - 1
    if text[open_paren] != "(":
        raise AssertionError(marker)
    depth = 0
    quoted = False
    escaped = False
    for pos in range(open_paren, len(text)):
        char = text[pos]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[offset : pos + 1], pos + 1
    raise AssertionError(f"unclosed {marker}")


def strip_layout(text: str) -> str:
    out: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    # `.Stmts` is the explicit unit of the statement-list production. The
    # translator omits it where layout permits; specs often spell it out.
    return "".join(out).replace(".Stmts", "")


def args(call: str) -> list[str]:
    open_paren = call.index("(")
    body = call[open_paren + 1 : -1]
    result: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for pos, char in enumerate(body):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(body[start:pos].strip())
            start = pos + 1
    result.append(body[start:].strip())
    return result


submitted_module, _ = extract_call(solution, "Module(")
entry_section = spec[spec.index("claim [anti-shuffle]:") :]
loaded_wrapper, _ = extract_call(entry_section, "#loadAll(")
loaded_module = args(loaded_wrapper)[0]

submitted_func, _ = extract_call(submitted_module, "FuncDef(")
func_args = args(submitted_func)
outer_for, outer_end = extract_call(func_args[2], "For(")
outer_args = args(outer_for)
inner_for, _ = extract_call(outer_args[2], "For(")
inner_args = args(inner_for)

insertion_section = spec[
    spec.index("claim [insertion-loop]:") : spec.index("claim [character-loop]:")
]
character_section = spec[
    spec.index("claim [character-loop]:") : spec.index("claim [anti-shuffle]:")
]
insertion_loop, _ = extract_call(insertion_section, "#loop(")
character_loop, _ = extract_call(character_section, "#loop(")
insertion_args = args(insertion_loop)
character_args = args(character_loop)

closure_call, _ = extract_call(verification, "closureVal(")
closure_args = args(closure_call)

checks = {
    "entry_loaded_module_equals_submitted_module": strip_layout(loaded_module)
    == strip_layout(submitted_module),
    "entry_function_name": strip_layout(func_args[0]) == '"anti_shuffle"',
    "entry_params": strip_layout(func_args[1]) == 'Params("s")',
    "outer_loop_target_exact": strip_layout(character_args[1])
    == strip_layout(outer_args[0]),
    "outer_loop_body_exact": strip_layout(character_args[2])
    == strip_layout(outer_args[2]),
    "inner_loop_target_exact": strip_layout(insertion_args[1])
    == strip_layout(inner_args[0]),
    "inner_loop_body_exact": strip_layout(insertion_args[2])
    == strip_layout(inner_args[2]),
    "closure_param_exact": strip_layout(closure_args[0]) == '"s"',
    "closure_remaining_params_empty": strip_layout(closure_args[1])
    == ".ParamNames",
    "closure_body_exact": strip_layout(closure_args[2])
    == strip_layout(func_args[2]),
    "closure_defining_scope_zero": strip_layout(closure_args[3]) == "0",
    "entry_result_constrained": "=> str(antiShuffle(S))" in entry_section,
    "entry_input_symbol_on_lhs": "str(S:IntSeq)" in entry_section,
}

for key, value in checks.items():
    print(f"{key}={value}")
if not all(checks.values()):
    raise SystemExit(1)
