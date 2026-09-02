#!/usr/bin/env bash
set -uo pipefail

mutated=/tmp/audit-work/body-mutation

if [[ -e "$mutated" ]]; then
  echo "ERROR: mutation directory already exists: $mutated"
  exit 1
fi

echo 'COMMAND: cp -a /tmp/audit-work/candidate /tmp/audit-work/body-mutation'
cp -a /tmp/audit-work/candidate "$mutated"
copy_status=$?
echo "EXIT_STATUS: $copy_status"
if (( copy_status != 0 )); then
  exit "$copy_status"
fi

echo 'COMMAND: patch -p0 < /audit-output/evidence/body-sensitivity.patch'
cd "$mutated" || exit 1
patch -p0 < /audit-output/evidence/body-sensitivity.patch
patch_status=$?
echo "EXIT_STATUS: $patch_status"
if (( patch_status != 0 )); then
  exit "$patch_status"
fi

echo 'COMMAND: diff -u /tmp/audit-work/candidate/verification.k /tmp/audit-work/body-mutation/verification.k'
diff -u /tmp/audit-work/candidate/verification.k "$mutated/verification.k"
diff_status=$?
echo "EXIT_STATUS: $diff_status (1 means the intended mutation is present)"
if (( diff_status != 1 )); then
  exit 1
fi

echo 'COMMAND: kompile verification.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutated-kompiled
build_status=$?
echo "EXIT_STATUS: $build_status"
if (( build_status != 0 )); then
  exit "$build_status"
fi

echo 'COMMAND: kprove spec.k --definition body-mutated-kompiled --spec-module SPLIT-WORDS-SPEC'
kprove spec.k \
  --definition body-mutated-kompiled \
  --spec-module SPLIT-WORDS-SPEC
proof_status=$?
echo "EXIT_STATUS: $proof_status (nonzero expected)"
if (( proof_status == 0 )); then
  exit 1
fi
exit 0
