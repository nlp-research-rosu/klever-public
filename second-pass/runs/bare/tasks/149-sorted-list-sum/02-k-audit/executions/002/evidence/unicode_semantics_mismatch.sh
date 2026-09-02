#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/reconstruction

python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum

canonical = load("unicode_canonical", "/reference/canonical.py")
candidate = load("unicode_candidate", "/tmp/audit-work/reconstruction/solution.py")
parity_value = ["😀"]
ordering_value = ["😀😀", "aaaa"]
print(f"PYTHON_CODEPOINT_LENGTH_SINGLE={len(parity_value[0])}")
print(f"PARITY_CANONICAL_RESULT={canonical(list(parity_value))!r}")
print(f"PARITY_CANDIDATE_RESULT={candidate(list(parity_value))!r}")
print(
    "PYTHON_CODEPOINT_LENGTHS_ORDERING="
    f"{[len(word) for word in ordering_value]!r}"
)
print(f"ORDERING_CANONICAL_RESULT={canonical(list(ordering_value))!r}")
print(f"ORDERING_CANDIDATE_RESULT={candidate(list(ordering_value))!r}")
PY

(
  cd "$scratch"
  python3 make_run.py 'Call(Name("sorted_list_sum"), ListExpr(Str("😀")))'
) > "$scratch/reviewer-unicode-parity.run"
krun "$scratch/reviewer-unicode-parity.run" \
  --definition "$scratch/concrete-kompiled" \
  --output pretty > "$scratch/reviewer-unicode-parity.out"
printf 'K_LLVM_PARITY_RESULT\n'
sed -n '1,20p' "$scratch/reviewer-unicode-parity.out"
grep -Fq 'VList ( "\xf0\x9f\x98\x80" , .Words )' \
  "$scratch/reviewer-unicode-parity.out"
krun "$scratch/reviewer-unicode-parity.run" \
  --definition "$scratch/proof-kompiled" \
  --output pretty > "$scratch/reviewer-unicode-parity-haskell.out"
printf 'K_HASKELL_PARITY_RESULT\n'
sed -n '1,20p' "$scratch/reviewer-unicode-parity-haskell.out"
grep -Fq 'VList ( "\xf0\x9f\x98\x80" , .Words )' \
  "$scratch/reviewer-unicode-parity-haskell.out"

(
  cd "$scratch"
  python3 make_run.py \
    'Call(Name("sorted_list_sum"), ListExpr(Str("😀😀"), Str("aaaa")))'
) > "$scratch/reviewer-unicode-ordering.run"
krun "$scratch/reviewer-unicode-ordering.run" \
  --definition "$scratch/concrete-kompiled" \
  --output pretty > "$scratch/reviewer-unicode-ordering.out"
printf 'K_LLVM_ORDERING_RESULT\n'
sed -n '1,20p' "$scratch/reviewer-unicode-ordering.out"
grep -Fq 'VList ( "aaaa" , "\xf0\x9f\x98\x80\xf0\x9f\x98\x80" , .Words )' \
  "$scratch/reviewer-unicode-ordering.out"
krun "$scratch/reviewer-unicode-ordering.run" \
  --definition "$scratch/proof-kompiled" \
  --output pretty > "$scratch/reviewer-unicode-ordering-haskell.out"
printf 'K_HASKELL_ORDERING_RESULT\n'
sed -n '1,20p' "$scratch/reviewer-unicode-ordering-haskell.out"
grep -Fq 'VList ( "aaaa" , "\xf0\x9f\x98\x80\xf0\x9f\x98\x80" , .Words )' \
  "$scratch/reviewer-unicode-ordering-haskell.out"

printf 'EXPECTED_PARITY_AND_ORDERING_MISMATCHES_CONFIRMED=true\n'
