#!/usr/bin/env python3
"""Create a material body mutation that the unpinned outer bridge ignores."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/tmp/audit-work/86-anti-shuffle")
EVIDENCE = Path("/audit-output/evidence")


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one occurrence of {old!r}, found {count}")
    return text.replace(old, new, 1)


def balanced_term(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(text.index("(", start), len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise RuntimeError("unbalanced Module term")


def main() -> int:
    source_py = (ROOT / "solution.py").read_text()
    mutated_py = replace_once(source_py, "    return result + word\n", '    return "x"\n')
    py_path = ROOT / "solution-final-return-mutated.py"
    py_path.write_text(mutated_py)

    source_spec = (ROOT / "spec.k").read_text()
    entry = source_spec[source_spec.index("module SPEC-ENTRY") :]
    old = 'Return(BinOp("+", Name("result"), Name("word")))'
    new = 'Return(Str("x"))'
    mutated_spec = 'requires "verification.k"\n\n' + entry
    mutated_spec = replace_once(mutated_spec, "module SPEC-ENTRY", "module AUDIT-FINAL-RETURN-MUTATION")
    mutated_spec = replace_once(mutated_spec, old, new)
    scratch_spec = ROOT / "spec-final-return-body-mutation.k"
    evidence_spec = EVIDENCE / "spec-final-return-body-mutation.k"
    scratch_spec.write_text(mutated_spec)
    evidence_spec.write_text(mutated_spec)
    module_start = mutated_spec.index("Module(")
    embedded_module = balanced_term(mutated_spec, module_start).replace(".Stmts", "")
    (ROOT / "final-return-mutated-entry.mpy").write_text(embedded_module + "\n")

    concrete_py = mutated_py + '\n\nassert anti_shuffle("") == "x"\n'
    concrete_path = ROOT / "final-return-mutation-concrete.py"
    concrete_path.write_text(concrete_py)
    print(f"mutated_python={py_path}")
    print(f"mutated_spec={scratch_spec}")
    print(f"evidence_spec={evidence_spec}")
    print(f"concrete_python={concrete_path}")
    print("mutation=anti_shuffle final statement changed from return result+word to return 'x'")
    print("false_witness=input empty; formal target empty; mutated program returns 'x'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
