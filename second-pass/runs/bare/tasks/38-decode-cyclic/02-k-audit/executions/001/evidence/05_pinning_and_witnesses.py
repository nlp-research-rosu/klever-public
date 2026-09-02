#!/usr/bin/env python3
"""Mechanically check the proof macros against the trusted translation.

Also exhibit concrete satisfying states for both entry claims and show that the
loop state is reached by the actual submitted .mpy execution.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/tmp/audit-work/38-decode-cyclic-audit")
SOURCE = ROOT / "candidate-src/solution.py"
MPY = ROOT / "candidate-src/solution.mpy"
SEMANTIC = ROOT / "candidate-src/semantic.k"
TRANSLATOR = ROOT / "trusted/py2mpy.py"
CONCRETE = ROOT / "build-concrete/semantic-llvm-kompiled"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


def rhs_between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def decode_from(s: str, i: int, acc: str) -> str:
    while i + 2 < len(s):
        acc = acc + s[i + 2] + s[i:i + 2]
        i += 3
    return acc + s[i:]


def main() -> int:
    translator = load(TRANSLATOR, "trusted_translator_for_pinning")
    submitted = load(SOURCE, "submitted_for_pinning")
    canonical = load(Path("/reference/canonical.py"), "canonical_for_pinning")

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text)
    translator.SCOPES.clear()
    translator._walk_symtable(__import__("symtable").symtable(
        source_text, str(SOURCE), "exec"
    ))
    function = tree.body[0]
    assert isinstance(function, ast.FunctionDef)
    while_stmt = function.body[2]
    return_stmt = function.body[3]
    assert isinstance(while_stmt, ast.While)
    assert isinstance(return_stmt, ast.Return)

    expected = {
        "solutionProgram": translator.render(translator.emit_module(tree)),
        "decodeBody": translator.render(translator.emit_stmts(while_stmt.body)),
        "decodeTest": translator.render(translator.emit_expr(while_stmt.test)),
        "decodeReturn": translator.render(translator.emit_stmt(return_stmt)),
    }

    semantic = SEMANTIC.read_text(encoding="utf-8")
    actual = {
        "solutionProgram": rhs_between(
            semantic,
            "rule solutionProgram =>",
            "// Independent accumulator specification:",
        ),
        "decodeBody": rhs_between(
            semantic, "rule decodeBody =>", 'syntax Expr ::= "decodeTest"'
        ),
        "decodeTest": rhs_between(
            semantic, "rule decodeTest =>", 'syntax Stmts ::= "decodeReturn"'
        ),
        "decodeReturn": rhs_between(
            semantic, "rule decodeReturn =>", "endmodule"
        ),
    }

    failures = []
    print("Trusted-translator pinning:")
    for name in expected:
        want = normalize(expected[name])
        got = normalize(actual[name])
        equal = want == got
        print(json.dumps({
            "macro": name,
            "normalized_equal": equal,
            "trusted_expected_sha256": digest(want),
            "semantic_rhs_sha256": digest(got),
        }, sort_keys=True))
        if not equal:
            failures.append({
                "macro": name, "expected": expected[name], "actual": actual[name]
            })

    mpy_equal = MPY.read_text(encoding="utf-8") == expected["solutionProgram"] + "\n"
    print(f"submitted_mpy_equals_trusted_render={mpy_equal}")
    if not mpy_equal:
        failures.append({"artifact": "solution.mpy trusted render mismatch"})

    witness_s = "bcaefdgh"
    witness_i = 3
    witness_acc = "abc"
    loop_post = decode_from(witness_s, witness_i, witness_acc)
    program_post = decode_from(witness_s, 0, "")
    witness_record = {
        "program_entry": {
            "precondition": "true",
            "S": witness_s,
            "formal_decodeFrom": program_post,
            "submitted_python": submitted.decode_cyclic(witness_s),
            "trusted_canonical": canonical.decode_cyclic(witness_s),
        },
        "loop_entry": {
            "precondition": f"0 <= {witness_i} <= len({witness_s!r}) == {len(witness_s)}",
            "S": witness_s,
            "I": witness_i,
            "ACC": witness_acc,
            "formal_decodeFrom": loop_post,
            "submitted_full_program": submitted.decode_cyclic(witness_s),
            "trusted_canonical": canonical.decode_cyclic(witness_s),
        },
    }
    print("satisfying_witnesses=" + json.dumps(witness_record, sort_keys=True))
    if not (
        program_post
        == loop_post
        == submitted.decode_cyclic(witness_s)
        == canonical.decode_cyclic(witness_s)
    ):
        failures.append({"artifact": "ground witness result mismatch"})

    command = [
        "krun",
        str(MPY),
        '-cS="bcaefdgh"',
        "--definition",
        str(CONCRETE),
        "--depth",
        "63",
    ]
    print("$ " + " ".join(json.dumps(piece) for piece in command))
    proc = subprocess.run(command, text=True, capture_output=True, check=False)
    output = proc.stdout + proc.stderr
    print(output.rstrip())
    print(f"[exit {proc.returncode}]")
    reached = (
        proc.returncode == 0
        and "<k>\n    whileLoop" in output
        and '"i" |-> pyInt ( 3 )' in output
        and '"result" |-> pyStr ( "abc" )' in output
        and '"s" |-> pyStr ( "bcaefdgh" )' in output
        and "exec ( Return" in output
        and "noResult" in output
    )
    print(f"actual_mpy_reaches_loop_claim_shape={reached}")
    if not reached:
        failures.append({"artifact": "reachable loop witness not observed"})

    print(f"failures={len(failures)}")
    if failures:
        print(json.dumps(failures, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
