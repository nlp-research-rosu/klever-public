#!/usr/bin/env python3
"""Lexical inventory of every candidate-local K declaration and rule."""

from __future__ import annotations

from pathlib import Path
import re
import sys


SEMANTIC = Path("/tmp/audit-work/53-add-audit-002/semantic.k")
VERIFICATION = Path("/tmp/audit-work/53-add-audit-002/verification.k")
SPEC = Path("/tmp/audit-work/53-add-audit-002/spec.k")


def numbered_block(lines: list[str], start: int) -> tuple[str, int]:
    end = start + 1
    while end < len(lines) and lines[end].strip() and not re.match(
        r"^\s{2}(?:rule|syntax|configuration|imports|endmodule)\b", lines[end]
    ):
        end += 1
    rendered = "\n".join(f"{index + 1}: {lines[index]}" for index in range(start, end))
    return rendered, end


def main() -> int:
    semantic = SEMANTIC.read_text()
    verification = VERIFICATION.read_text()
    spec = SPEC.read_text()
    lines = semantic.splitlines()

    candidate_k_files = sorted(
        path.name for path in Path("/candidate").glob("*.k") if path.is_file()
    )
    print(f"candidate_k_files={candidate_k_files}")
    assert candidate_k_files == ["semantic.k", "spec.k", "verification.k"]

    syntax_starts = [
        index for index, line in enumerate(lines) if re.match(r"^\s{2}syntax\b", line)
    ]
    rule_starts = [
        index for index, line in enumerate(lines) if re.match(r"^\s{2}rule\b", line)
    ]
    configurations = [
        index for index, line in enumerate(lines)
        if re.match(r"^\s{2}configuration\b", line)
    ]
    assert len(syntax_starts) == 7
    assert len(rule_starts) == 11
    assert len(configurations) == 1

    print("LOCAL_SYNTAX_DECLARATIONS")
    for number, start in enumerate(syntax_starts, 1):
        block, _ = numbered_block(lines, start)
        print(f"syntax-{number}\n{block}")

    print("CONFIGURATION")
    start = configurations[0]
    end = next(index for index in rule_starts if index > start)
    print("\n".join(f"{index + 1}: {lines[index]}" for index in range(start, end)))

    print("ORDINARY_OPERATIONAL_RULES")
    for number, start in enumerate(rule_starts, 1):
        block, _ = numbered_block(lines, start)
        print(f"rule-{number}\n{block}")

    local_attribute_counts = {
        "function": len(re.findall(r"\[\s*function\b", semantic)),
        "total": len(re.findall(r"\[\s*total\b", semantic)),
        "functional": len(re.findall(r"\[\s*functional\b", semantic)),
        "simplification": len(re.findall(r"\[\s*simplification\b", semantic)),
        "priority": len(re.findall(r"\bpriority\b", semantic)),
        "opaque": len(re.findall(r"\bopaque\b", semantic)),
    }
    print(f"local_special_declarations={local_attribute_counts}")
    assert all(count == 0 for count in local_attribute_counts.values())

    verification_rules = len(re.findall(r"(?m)^\s*rule\b", verification))
    verification_claims = len(re.findall(r"(?m)^\s*claim\b", verification))
    spec_claims = len(re.findall(r"(?m)^\s*claim\b", spec))
    print(f"verification_rules={verification_rules}")
    print(f"verification_claims={verification_claims}")
    print(f"spec_claims={spec_claims}")
    assert verification_rules == 0
    assert verification_claims == 0
    assert spec_claims == 1

    used_program_constructors = ["Module", "FuncDef", "Params", "Return", "BinOp", "Name"]
    for constructor in used_program_constructors:
        assert re.search(rf'"{re.escape(constructor)}"', semantic)
    print(f"used_program_constructors={used_program_constructors}")
    print("unused_declared_source_constructor=Int")
    print("STATIC_INVENTORY_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
