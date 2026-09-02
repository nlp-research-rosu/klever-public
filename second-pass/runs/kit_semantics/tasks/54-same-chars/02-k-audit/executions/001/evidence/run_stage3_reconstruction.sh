#!/usr/bin/env bash
set -euo pipefail
set -o xtrace
export PATH="/home/agent/.nix-profile/bin:$PATH"
scratch=/tmp/audit-work/54-same-chars
cd "$scratch"

command -v kompile
command -v krun
command -v kprove
kompile --version
krun --version
kprove --version

test ! -e audit-runtime-kompiled
test ! -e audit-verification-kompiled
python3 /reference/py2mpy.py /audit-output/evidence/k_concrete_cases.py > audit-concrete-cases.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

set +e
krun audit-concrete-cases.mpy \
  --definition audit-runtime-kompiled 2>&1 | tee audit-concrete.out
concrete_status=${PIPESTATUS[0]}
set -e

rg -F '"case_empty" |-> true' audit-concrete.out
rg -F '"case_empty_left" |-> false' audit-concrete.out
rg -F '"case_duplicate" |-> true' audit-concrete.out
rg -F '"case_reordered" |-> true' audit-concrete.out
rg -F '"case_different_left" |-> false' audit-concrete.out
rg -F '"case_different_right" |-> false' audit-concrete.out
rg -F '<k>' audit-concrete.out
rg -F '.K' audit-concrete.out
rg -F '<exc>' audit-concrete.out
rg -F 'NoExc' audit-concrete.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

set +e
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC 2>&1 | tee audit-positive-proof.out
proof_status=${PIPESTATUS[0]}
set -e

top_count=$(rg -x '#Top' audit-positive-proof.out | wc -l)
printf 'CONCRETE_EXIT_STATUS=%s\n' "$concrete_status"
printf 'POSITIVE_PROOF_EXIT_STATUS=%s\n' "$proof_status"
printf 'POSITIVE_PROOF_TOP_COUNT=%s\n' "$top_count"
if (( concrete_status != 0 || proof_status != 0 || top_count != 1 )); then
  exit 1
fi
printf 'EXIT_STATUS=0\n'
