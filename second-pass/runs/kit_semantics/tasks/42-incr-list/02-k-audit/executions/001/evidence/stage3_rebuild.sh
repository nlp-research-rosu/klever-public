#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/42-incr-list-audit
fresh="$scratch/fresh-build-003"
evidence=/audit-output/evidence

if [[ -e "$fresh" ]]; then
  echo "refusing to reuse existing fresh-build directory: $fresh" >&2
  exit 2
fi

mkdir -p "$fresh"
cp "$scratch/solution.py" "$fresh/solution.py"
cp "$scratch/submitted-solution.mpy" "$fresh/solution.mpy"
cp "$scratch/spec.k" "$fresh/spec.k"
cp "$scratch/verification.k" "$fresh/verification.k"
cp "$scratch/py2mpy.py" "$fresh/py2mpy.py"
cp -R "$scratch/reference-semantics" "$fresh/reference-semantics"
cp /audit-output/evidence/stage3_concrete.py "$fresh/stage3_concrete.py"

run_logged() {
  local log_path=$1
  shift
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@" 2>&1 | tee "$log_path"
  local command_status=${PIPESTATUS[0]}
  set -e
  echo "EXIT_STATUS=$command_status"
  if [[ "$command_status" -ne 0 ]]; then
    return "$command_status"
  fi
}

echo '$ command -v kup; command -v kompile; command -v krun; command -v kprove'
command -v kup || true
command -v kompile
command -v krun
command -v kprove
echo '$ kompile --version; kprove --version'
kompile --version
kprove --version

(
  cd "$fresh"
  run_logged "$evidence/stage3_llvm_kompile.log" \
    kompile reference-semantics/semantics.k \
      --backend llvm \
      --main-module MPY-KRUN \
      --syntax-module MPY-SYNTAX \
      --output-definition audit-runtime-kompiled

  echo '$ python3 py2mpy.py stage3_concrete.py > stage3_concrete.mpy'
  python3 py2mpy.py stage3_concrete.py > stage3_concrete.mpy
  echo "EXIT_STATUS=0"

  run_logged "$evidence/stage3_concrete_krun.log" \
    krun stage3_concrete.mpy --definition audit-runtime-kompiled
  grep -Pzq '<exit-code>\s+0\s+</exit-code>' "$evidence/stage3_concrete_krun.log"
  ! grep -q 'AssertionError' "$evidence/stage3_concrete_krun.log"

  run_logged "$evidence/stage3_haskell_kompile.log" \
    kompile --backend haskell verification.k \
      --main-module VERIFICATION \
      --syntax-module MPY-SYNTAX \
      --output-definition audit-verification-kompiled

  run_logged "$evidence/stage3_loop_kprove.log" \
    kprove spec.k \
      --definition audit-verification-kompiled \
      --spec-module SPEC \
      --claims SPEC.loop-inv
  grep -qx '#Top' "$evidence/stage3_loop_kprove.log"

  run_logged "$evidence/stage3_all_claims_kprove.log" \
    kprove spec.k \
      --definition audit-verification-kompiled \
      --spec-module SPEC
  grep -qx '#Top' "$evidence/stage3_all_claims_kprove.log"
)

echo "STAGE3_RECONSTRUCTION_OK"
