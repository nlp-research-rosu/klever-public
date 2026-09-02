#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/review-31
candidate="$scratch/candidate"
concrete_def="$scratch/semantic-concrete-kompiled"
proof_def="$scratch/verification-proof-kompiled"
overall=0

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  if [[ "$rc" -ne 0 ]]; then
    overall=1
  fi
  return "$rc"
}

cd "$candidate" || exit 2

run kompile \
  --backend llvm \
  semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$concrete_def"

for n in -5 0 1 2 3 4 9 101 13441 1000003; do
  printf 'COMMAND: krun solution.mpy --definition %q -cN=%q\n' \
    "$concrete_def" "$n"
  krun solution.mpy --definition "$concrete_def" -cN="$n" \
    | sed -n '/<result>/,/<\/result>/p'
  rc=${PIPESTATUS[0]}
  printf 'EXIT: %d\n' "$rc"
  if [[ "$rc" -ne 0 ]]; then
    overall=1
  fi
done

printf 'COMMAND: PYTHONDONTWRITEBYTECODE=1 python3 - [fixed input table]\n'
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime

def outcome(fn, n):
    try:
        return ("return", fn(n))
    except BaseException as error:
        return ("raise", type(error).__name__, str(error))

canonical = load("canonical", "/tmp/audit-work/review-31/reference/canonical.py")
generated = load("generated", "/tmp/audit-work/review-31/candidate/solution.py")
for value in (-5, 0, 1, 2, 3, 4, 9, 101, 13441, 1000003):
    print(
        f"PYTHON n={value} canonical={outcome(canonical, value)!r} "
        f"generated={outcome(generated, value)!r}"
    )
PY
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then overall=1; fi

run kompile \
  --backend haskell \
  verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_def"

prove_one() {
  local label="$1"
  printf 'COMMAND: kprove spec.k --definition %q --spec-module SPEC --claims %q\n' \
    "$proof_def" "$label"
  local output
  output="$(kprove spec.k \
    --definition "$proof_def" \
    --spec-module SPEC \
    --claims "$label" 2>&1)"
  local rc=$?
  printf '%s\n' "$output"
  printf 'EXIT: %d\n' "$rc"
  if [[ "$rc" -ne 0 || "$output" != "#Top" ]]; then
    overall=1
  fi
}

prove_one helper-correct
prove_one is-prime-correct

printf 'STAGE3_OVERALL=%d\n' "$overall"
exit "$overall"
