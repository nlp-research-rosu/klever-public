#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration/rule inventory as TSV."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
EXTRA = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(
    r"^(?P<indent>\s*)(?P<kind>module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)
TOP_REQUIRE = re.compile(r'^requires\s+"')
ATTR = re.compile(
    r"\b(function|total|functional|simplification|concrete|priority|owise|"
    r"anywhere|symbol|no-evaluators|macro|strict|seqstrict|bracket|token)\b"
)

# Source rules and contexts reached by the target program. Line numbers are
# declaration starts in the immutable trusted supplied-semantics tree.
ACTIVE: dict[tuple[str, int], str] = {
    ("semantics/syntax.k", 9): "PROGRAM_AST_GRAMMAR",
    ("semantics/syntax.k", 32): "PROGRAM_AST_GRAMMAR",
    ("semantics/syntax.k", 38): "PROGRAM_AST_GRAMMAR",
    ("semantics/syntax.k", 39): "PROGRAM_AST_GRAMMAR",
    ("semantics/syntax.k", 41): "PROGRAM_AST_GRAMMAR",
    ("semantics/syntax.k", 56): "PROGRAM_AST_GRAMMAR",
    ("semantics/syntax.k", 57): "PROGRAM_AST_GRAMMAR",
    ("semantics/syntax.k", 60): "PROGRAM_AST_GRAMMAR",
    ("semantics/syntax.k", 61): "PROGRAM_AST_GRAMMAR",
    ("semantics/core.k", 13): "STRING_SEQUENCE_MODEL",
    ("semantics/core.k", 15): "STRING_SEQUENCE_MODEL",
    ("semantics/core.k", 25): "VALUE_MODEL",
    ("semantics/core.k", 36): "CALL_STATE_MODEL",
    ("semantics/core.k", 37): "CALL_STATE_MODEL",
    ("semantics/core.k", 38): "EVALUATION_RESULTS",
    ("semantics/core.k", 39): "EVALUATION_RESULTS",
    ("semantics/core.k", 40): "ARGUMENT_SEQUENCE",
    ("semantics/core.k", 41): "FINAL_STATE_MODEL",
    ("semantics/core.k", 42): "CALL_STATE_MODEL",
    ("semantics/core.k", 49): "INITIAL_CONFIGURATION",
    ("semantics/core.k", 124): "MODULE_LOAD",
    ("semantics/core.k", 125): "MODULE_LOAD",
    ("semantics/core.k", 126): "STATEMENT_SEQUENCE",
    ("semantics/core.k", 127): "STATEMENT_SEQUENCE",
    ("semantics/core.k", 130): "NAME_LOOKUP",
    ("semantics/core.k", 131): "NAME_LOOKUP",
    ("semantics/core.k", 132): "NAME_LOOKUP",
    ("semantics/core.k", 185): "CALL_ARGUMENT_EVALUATION",
    ("semantics/core.k", 186): "CALL_ARGUMENT_EVALUATION",
    ("semantics/core.k", 189): "CALL_ARGUMENT_EVALUATION",
    ("semantics/core.k", 190): "CALL_ARGUMENT_EVALUATION",
    ("semantics/core.k", 191): "CALL_ARGUMENT_EVALUATION",
    ("semantics/core.k", 194): "INTEGER_LITERAL",
    ("semantics/core.k", 208): "OPERATOR_DISPATCH",
    ("semantics/core.k", 210): "OPERATOR_DISPATCH",
    ("semantics/core.k", 213): "ARGUMENT_APPEND",
    ("semantics/core.k", 214): "ARGUMENT_APPEND",
    ("semantics/core.k", 215): "ARGUMENT_APPEND",
    ("semantics/core.k", 227): "SEQUENCE_LENGTH",
    ("semantics/core.k", 228): "SEQUENCE_LENGTH",
    ("semantics/core.k", 229): "SEQUENCE_LENGTH",
    ("semantics/functions.k", 8): "CALL_FRAME_MODEL",
    ("semantics/functions.k", 14): "FUNCTION_BINDING",
    ("semantics/functions.k", 63): "PARAMETER_BINDING",
    ("semantics/functions.k", 64): "PARAMETER_BINDING",
    ("semantics/functions.k", 78): "RETURN_CONTROL",
    ("semantics/functions.k", 85): "RETURN_CONTROL",
    ("semantics/call.k", 19): "CALL_ROUTING",
    ("semantics/call.k", 20): "CALL_ROUTING",
    ("semantics/call.k", 21): "CALL_ROUTING",
    ("semantics/call.k", 69): "CALL_FRAME_ENTRY",
    ("semantics/controls.k", 9): "RESULT_ASSIGNMENT",
    ("semantics/operators.k", 10): "UNARY_NEGATION_DISPATCH",
    ("semantics/operators.k", 15): "COMPARE_EVALUATION_ORDER",
    ("semantics/operators.k", 16): "COMPARE_EVALUATION_ORDER",
    ("semantics/operators.k", 17): "COMPARE_DISPATCH",
    ("semantics/int.k", 7): "NEGATIVE_SLICE_STEP",
    ("semantics/subscript.k", 16): "REVERSE_ELEMENT_ACCESS",
    ("semantics/subscript.k", 17): "REVERSE_ELEMENT_ACCESS",
    ("semantics/subscript.k", 18): "REVERSE_ELEMENT_ACCESS",
    ("semantics/subscript.k", 27): "SUBSCRIPT_EVALUATION_ORDER",
    ("semantics/subscript.k", 28): "SUBSCRIPT_EVALUATION_ORDER",
    ("semantics/subscript.k", 44): "SLICE_BOUND_EVALUATION",
    ("semantics/subscript.k", 49): "SLICE_BOUND_MODEL",
    ("semantics/subscript.k", 50): "SLICE_BOUND_EVALUATION",
    ("semantics/subscript.k", 51): "SLICE_BOUND_EVALUATION",
    ("semantics/subscript.k", 52): "SLICE_BOUND_EVALUATION",
    ("semantics/subscript.k", 54): "SLICE_BOUND_EVALUATION",
    ("semantics/subscript.k", 55): "SLICE_BOUND_EVALUATION",
    ("semantics/subscript.k", 56): "SLICE_BOUND_EVALUATION",
    ("semantics/subscript.k", 61): "STRING_SLICE_DISPATCH",
    ("semantics/subscript.k", 63): "STRING_SLICE",
    ("semantics/subscript.k", 68): "STRING_SLICE",
    ("semantics/subscript.k", 72): "SLICE_STEP",
    ("semantics/subscript.k", 74): "SLICE_STEP",
    ("semantics/subscript.k", 76): "REVERSE_SLICE_START",
    ("semantics/subscript.k", 79): "REVERSE_SLICE_START",
    ("semantics/subscript.k", 83): "REVERSE_SLICE_STOP",
    ("semantics/subscript.k", 86): "REVERSE_SLICE_STOP",
    ("semantics/subscript.k", 116): "REVERSE_SEQUENCE_BUILD",
    ("semantics/subscript.k", 117): "REVERSE_SEQUENCE_BUILD",
    ("semantics/subscript.k", 120): "REVERSE_SEQUENCE_BUILD",
    ("semantics/str.k", 25): "STRING_EQUALITY",
}


def normalized(text: str) -> str:
    return " ".join(part for part in text.split())


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("kind")))
        elif TOP_REQUIRE.match(line):
            starts.append((index, "requires-file"))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        while end > start + 1 and not lines[end - 1].strip():
            end -= 1
        yield start + 1, end, kind, "\n".join(lines[start:end])


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return f"candidate/{path.name}"


def disposition(rel: str, line: int, kind: str, text: str) -> tuple[str, str]:
    active = ACTIVE.get((rel, line))
    if active:
        return (
            active,
            "ACCEPT_TARGET_PATH: fixed supplied rule/declaration; manually checked "
            "against the submitted constructor path and Python str behavior",
        )
    if rel == "candidate/verification.k":
        return (
            "PROOF_MODULE",
            "ACCEPT_NO_EXTENSION: module only imports fixed MPY; no local rule, "
            "function, lemma, priority, simplification, or opaque symbol",
        )
    if rel == "candidate/spec.k" and kind == "claim":
        return (
            "TARGET_CLAIM",
            "AUDIT_SEPARATELY: positive theorem, not a rule imported into the "
            "verification definition",
        )
    if kind == "rule" and "[concrete]" in text:
        return (
            "FIXED_CONCRETE_ONLY_NOT_REACHED",
            "NOT_RELIED_UPON: supplied LLVM-only equation is absent from the "
            "Haskell proof definition; no target-domain false witness identified",
        )
    return (
        "FIXED_BASELINE_NOT_REACHED",
        "NOT_RELIED_UPON: outside the target execution slice; retained only as "
        "part of the supplied fixed semantics; no target-domain false witness identified",
    )


def main() -> None:
    paths = sorted((ROOT / "semantics").glob("*.k"))
    paths.insert(0, ROOT / "semantics.k")
    paths.extend(EXTRA)
    print(
        "id\tfile\tstart\tend\tkind\tattributes\ttarget_relevance\t"
        "disposition\tsource"
    )
    counter = 0
    for path in paths:
        rel = relative(path)
        for start, end, kind, text in blocks(path):
            counter += 1
            no_comments = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
            brackets = " ".join(re.findall(r"\[[^\]]*\]", no_comments, flags=re.S))
            attrs = ",".join(sorted(set(ATTR.findall(brackets)))) or "-"
            relevance, decision = disposition(rel, start, kind, text)
            source = normalized(text).replace("\t", " ")
            print(
                f"K{counter:04d}\t{rel}\t{start}\t{end}\t{kind}\t{attrs}\t"
                f"{relevance}\t{decision}\t{source}"
            )


if __name__ == "__main__":
    main()
