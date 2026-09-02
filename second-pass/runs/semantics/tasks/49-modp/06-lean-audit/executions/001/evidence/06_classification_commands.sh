#!/usr/bin/env bash
set -eu

printf '%s\n' '$ source solution, translated program, verification definitions, and reachability claim'
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k

printf '%s\n' '$ relevant supplied operational semantics'
nl -ba /reference/k-proof/reference-semantics/semantics/syntax.k \
  | sed -n '9,62p'
nl -ba /reference/k-proof/reference-semantics/semantics/core.k \
  | sed -n '123,195p'
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k \
  | sed -n '10,18p'
nl -ba /reference/k-proof/reference-semantics/semantics/int.k \
  | sed -n '7,27p'
nl -ba /reference/k-proof/reference-semantics/semantics/call.k \
  | sed -n '18,25p;69,75p'
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k \
  | sed -n '13,20p;62,90p'

printf '%s\n' '$ verified generation-time producer selection and no-target logic'
nl -ba /reference/generation-tools/klean_export.py \
  | sed -n '770,918p;1038,1060p;1210,1260p'

printf '%s\n' '$ python3 - (exact source/AST/summary correspondence and independent classification record)'
python3 - <<'PY'
import json
from pathlib import Path

solution = Path("/reference/k-proof/solution.py").read_text()
translated = Path("/reference/k-proof/solution.mpy").read_text()
verification = Path("/reference/k-proof/verification.k").read_text()
semantics_int = Path(
    "/reference/k-proof/reference-semantics/semantics/int.k"
).read_text()

normalize = lambda text: "".join(text.split())
expected_translation = """
Module(
  FuncDef("modp", Params("n", "p"),
    Expr(Str("Return 2^n modulo p."))
    Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))))
"""
checks = {
    "source_body_exact": "return (2 ** n) % p" in solution,
    "translation_exact": normalize(translated)
    == normalize(expected_translation),
    "named_body_exact": normalize(
        """Expr(Str("Return 2^n modulo p."))
           Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))"""
    )
    in normalize(verification),
    "named_program_exact": normalize(
        'Module(FuncDef("modp", Params("n", "p"), modpBody))'
    )
    in normalize(verification),
    "operational_power_exact": normalize(
        'rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 '
        'requires I2 >=Int 0'
    )
    in normalize(semantics_int),
    "operational_mod_exact": normalize(
        'rule applyBin("%", I1:Int, I2:Int) => pyMod(I1, I2)'
    )
    in normalize(semantics_int),
    "summary_exact": normalize(
        "rule specModp(N:Int, P:Int) => pyMod(2 ^Int N, P) "
        "requires N >=Int 0 andBool P >Int 0"
    )
    in normalize(verification),
}
classification = [
    {
        "source_rule_id": (
            "rule-71d349ffafcb30fd76f8fe497ddc3bd83"
            "e9c8f32d2e73927d650e4dc1e713860"
        ),
        "classification": "DEFINITION",
        "judgment": (
            "Exact macro-like name for the translated statement sequence; "
            "it has no configuration cells and does not bypass execution."
        ),
    },
    {
        "source_rule_id": (
            "rule-642fa0e1d269068ee1ff23a4190cc20e8"
            "dd97d36c91e0e7fdd0f6fc2160ca730"
        ),
        "classification": "DEFINITION",
        "judgment": (
            "Exact macro-like name for the Module/FuncDef term; fixed call, "
            "binding, frame, body, return, and state rules still execute."
        ),
    },
    {
        "source_rule_id": (
            "rule-979f0d2fa1ec906f8e5bf589b74d8f25c"
            "d25fe0ce31c6c16227b18246e343ea5"
        ),
        "classification": "DEFINITION",
        "judgment": (
            "Conditional named postcondition summary. Its RHS is exactly the "
            "fixed operational power followed by Python remainder on the "
            "same N>=0, P>0 domain; it asserts no independent arithmetic fact."
        ),
    },
]
print(json.dumps({"checks": checks, "classification": classification}, indent=2))
if not all(checks.values()):
    raise SystemExit(1)
PY
