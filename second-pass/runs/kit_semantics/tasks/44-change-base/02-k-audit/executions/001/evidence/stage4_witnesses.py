#!/usr/bin/env python3
import importlib.util
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


def base_acc(n: int, base: int, accumulator: list[int]) -> list[int]:
    while n > 0:
        accumulator.insert(0, 48 + (n % base))
        n //= base
    return accumulator


def change_base_codes(n: int, base: int) -> list[int]:
    if n == 0:
        return [48]
    if n > 0:
        return base_acc(n, base, [])
    return [45] + base_acc(-n, base, [])


def decode(codes: list[int]) -> str:
    return "".join(chr(code) for code in codes)


canonical = load("trusted_canonical_witness", Path("/reference/canonical.py"))
generated = load(
    "generated_solution_witness",
    Path("/tmp/audit-work/44-change-base/solution.py"),
)

loop_x, loop_base, loop_accumulator = 8, 3, []
print(
    "loop_witness "
    f"x={loop_x} base={loop_base} sign_codes=[] accumulator={loop_accumulator} "
    f"satisfies_loop_precondition={loop_x >= 0 and 2 <= loop_base < 10} "
    f"expected_final_accumulator={base_acc(loop_x, loop_base, loop_accumulator.copy())}"
)

for x, base in [(8, 3), (0, 2), (-8, 3), (9, 9)]:
    satisfies = 2 <= base < 10
    codes = change_base_codes(x, base)
    claimed = decode(codes)
    generated_result = generated(x, base)
    canonical_result = canonical(x, base)
    print(
        f"x={x} base={base} satisfies_entry_precondition={satisfies} "
        f"changeBaseCodes={codes} claimed={claimed!r} "
        f"generated={generated_result!r} canonical={canonical_result!r} "
        f"claim_matches_generated={claimed == generated_result} "
        f"claim_matches_canonical={claimed == canonical_result}"
    )
