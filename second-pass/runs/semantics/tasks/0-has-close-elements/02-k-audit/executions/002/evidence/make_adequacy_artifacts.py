#!/usr/bin/env python3
"""Generate exact-term pinning and a body-sensitive false-program mutation."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

case = Path("/tmp/audit-work/case")
evidence = Path("/audit-output/evidence")


def pinning_spec(term_path: Path, verification_name: str, module_name: str) -> str:
    term = term_path.read_text(encoding="utf-8").rstrip()
    return (
        f'requires "{verification_name}"\n\n'
        f"module {module_name}\n"
        "  imports VERIFICATION-BASE\n\n"
        f"  claim <k> solutionModule() => {term} </k>\n"
        "endmodule\n"
    )


def normalize_mpy(mpy_path: Path, normalized_path: Path) -> None:
    result = subprocess.run(
        [
            "kast",
            str(mpy_path),
            "--definition",
            "/tmp/audit-work/build/base-kompiled",
            "--module",
            "MPY-SYNTAX",
            "--output",
            "pretty",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    normalized_path.write_text(result.stdout, encoding="utf-8")


normalize_mpy(case / "solution.mpy", case / "solution.normalized.kterm")
shutil.copyfile(
    case / "solution.normalized.kterm",
    evidence / "solution.normalized.kterm",
)
original_pinning = pinning_spec(
    case / "solution.normalized.kterm", "verification.k", "PINNING-ORIGINAL"
)
(case / "pinning-original.k").write_text(original_pinning, encoding="utf-8")
(evidence / "pinning-original.k").write_text(original_pinning, encoding="utf-8")

original_source = (case / "solution.py").read_text(encoding="utf-8")
old_entry = """def has_close_elements(numbers: List[float], threshold: float) -> bool:
    found = False
    start = 1
    number = threshold
    for number in numbers:
        if is_close_to_any(number, numbers, threshold, start):
            found = True
            break
        start += 1
    start = 1
    number = threshold
    return found
"""
new_entry = """def has_close_elements(numbers: List[float], threshold: float) -> bool:
    return False
"""
if original_source.count(old_entry) != 1:
    raise RuntimeError("expected exactly one source entry body")
mutated_source = original_source.replace(old_entry, new_entry)
(case / "solution-body-mutated.py").write_text(mutated_source, encoding="utf-8")
(evidence / "solution-body-mutated.py").write_text(mutated_source, encoding="utf-8")

original_verification = (case / "verification.k").read_text(encoding="utf-8")
old_entry_rule = """  rule entryBody() =>
    Assign(Name("found"), Bool(false))
    Assign(Name("start"), Int(1))
    Assign(Name("number"), Name("threshold"))
    For(Name("number"), Name("numbers"), outerLoopBody())
    Assign(Name("start"), Int(1))
    Assign(Name("number"), Name("threshold"))
    Return(Name("found"))
    .Stmts
"""
new_entry_rule = """  rule entryBody() =>
    Return(Bool(false))
    .Stmts
"""
if original_verification.count(old_entry_rule) != 1:
    raise RuntimeError("expected exactly one K entryBody rule")
mutated_verification = original_verification.replace(old_entry_rule, new_entry_rule)
(case / "verification-body-mutated.k").write_text(
    mutated_verification, encoding="utf-8"
)
(evidence / "verification-body-mutated.k").write_text(
    mutated_verification, encoding="utf-8"
)

body_spec = """requires "verification-body-mutated.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION-WITH-ENTRY

  claim <k> #loadAll(solutionModule())
              ~> Call(Name("has_close_elements"),
                      list(ALL:FloatSeq), T:Float, .Exprs)
         => hasPairs(ALL, ALL, T, 1) ... </k>
        <env> 0 </env>
        <scopes>
          0  |-> (scope(.Map, parent(-1)) => solutionScope())
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule
"""
(case / "body-mutation-spec.k").write_text(body_spec, encoding="utf-8")
(evidence / "body-mutation-spec.k").write_text(body_spec, encoding="utf-8")

shutil.copyfile(evidence / "bridge-witnesses.k", case / "bridge-witnesses.k")
shutil.copyfile(evidence / "ground-summary.k", case / "ground-summary.k")


def finish_mutated_pinning() -> None:
    shutil.copyfile(
        case / "solution-body-mutated.mpy",
        evidence / "solution-body-mutated.mpy",
    )
    normalize_mpy(
        case / "solution-body-mutated.mpy",
        case / "solution-body-mutated.normalized.kterm",
    )
    shutil.copyfile(
        case / "solution-body-mutated.normalized.kterm",
        evidence / "solution-body-mutated.normalized.kterm",
    )
    mutated_pinning = pinning_spec(
        case / "solution-body-mutated.normalized.kterm",
        "verification-body-mutated.k",
        "PINNING-BODY-MUTATED",
    )
    (case / "pinning-body-mutated.k").write_text(mutated_pinning, encoding="utf-8")
    (evidence / "pinning-body-mutated.k").write_text(
        mutated_pinning, encoding="utf-8"
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2 and sys.argv[1] == "--finish":
        finish_mutated_pinning()
    elif len(sys.argv) == 1:
        pass
    else:
        raise SystemExit("usage: make_adequacy_artifacts.py [--finish]")
