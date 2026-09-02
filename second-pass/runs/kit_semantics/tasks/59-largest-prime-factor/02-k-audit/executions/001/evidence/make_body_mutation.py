#!/usr/bin/env python3
"""Create a fresh body-sensitive mutation of the program term in the claims."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/h59/spec.k")
OUTPUT = Path("/audit-output/evidence/spec-body-mutation.k")


def main() -> int:
    text = SOURCE.read_text()
    if text.count("module SPEC\n") != 1:
        raise RuntimeError("unexpected module declaration")
    text = text.replace("module SPEC\n", "module SPEC-BODY-MUTATION\n", 1)

    original = 'Assign(Name("factor"), Int(2))'
    count = text.count(original)
    if count != 4:
        raise RuntimeError(f"expected four embedded body occurrences, got {count}")
    text = text.replace(original, 'Assign(Name("factor"), Int(3))')

    precondition = "requires N0 >=Int 2"
    if text.count(precondition) != 1:
        raise RuntimeError("unexpected entry precondition count")
    text = text.replace(precondition, "requires N0 ==Int 4", 1)
    OUTPUT.write_text(text)
    print("mutation=embedded function initialization factor 2 changed to factor 3")
    print(f"changed_embedded_program_occurrences={count}")
    print("satisfying_witness=N0=4")
    print("mutated_program_result=4")
    print("original_required_result=2")
    print(f"output={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
