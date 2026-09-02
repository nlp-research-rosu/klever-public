#!/usr/bin/env python3
import importlib.util
import re
from pathlib import Path

SCRATCH = Path("/tmp/audit-work/53-add")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


solution_mpy = (SCRATCH / "solution.mpy").read_text()
spec_k = (SCRATCH / "spec.k").read_text()
verification_k = (SCRATCH / "verification.k").read_text()
semantic_k = (SCRATCH / "semantic.k").read_text()

program_term = compact(solution_mpy)
claim_text = compact(spec_k)
program_is_embedded = f"load({program_term})" in claim_text
actual_invocation = 'invoke("add",pyInt(X),pyInt(Y))' in claim_text
result_is_constrained = "<result>0=>X+IntY</result>" in claim_text
empty_initial_env = "<env>.Map=>" in claim_text
empty_initial_functions = "<functions>.Map=>" in claim_text
verification_has_no_rules = re.search(r"\brule\b", verification_k) is None
verification_has_no_functions = "[function" not in verification_k
semantic_has_no_proof_shortcut = not any(
    marker in semantic_k
    for marker in ("[simplification", "[priority", "claim", "oracle", "summary")
)

x, y = 2, 3
canonical = load_module("trusted_canonical_witness", SCRATCH / "trusted-canonical.py")
generated = load_module("generated_solution_witness", SCRATCH / "solution.py")
claimed_result = x + y
canonical_result = canonical.add(x, y)
generated_result = generated.add(x, y)

print(f"NORMALIZED_SUBMITTED_PROGRAM: {program_term}")
print(f"PROGRAM_TERM_EMBEDDED_UNDER_LOAD: {program_is_embedded}")
print(f"ACTUAL_ADD_INVOCATION_PRESENT: {actual_invocation}")
print(f"RESULT_EXACTLY_X_PLUS_Y: {result_is_constrained}")
print(f"INITIAL_ENV_IS_EMPTY: {empty_initial_env}")
print(f"INITIAL_FUNCTIONS_IS_EMPTY: {empty_initial_functions}")
print(f"VERIFICATION_HAS_NO_RULES: {verification_has_no_rules}")
print(f"VERIFICATION_HAS_NO_FUNCTIONS: {verification_has_no_functions}")
print(f"SEMANTIC_HAS_NO_PROOF_SHORTCUT_MARKERS: {semantic_has_no_proof_shortcut}")
print("FORMAL_PRECONDITION: X and Y are arbitrary K Int values; no requires clause")
print(
    "SATISFYING_WITNESS: X=2, Y=3, <env>=.Map, "
    "<functions>=.Map, <result>=0, <k>=load(submitted program) ~> invoke(add,2,3)"
)
print(f"CLAIMED_WITNESS_RESULT: {claimed_result}")
print(f"CANONICAL_PYTHON_WITNESS_RESULT: {canonical_result}")
print(f"GENERATED_PYTHON_WITNESS_RESULT: {generated_result}")

checks = [
    program_is_embedded,
    actual_invocation,
    result_is_constrained,
    empty_initial_env,
    empty_initial_functions,
    verification_has_no_rules,
    verification_has_no_functions,
    semantic_has_no_proof_shortcut,
    claimed_result == canonical_result == generated_result == 5,
]
print(f"FAILED_CHECK_COUNT: {checks.count(False)}")
raise SystemExit(1 if not all(checks) else 0)
