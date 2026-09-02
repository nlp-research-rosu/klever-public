#!/usr/bin/env bash
set -u

cd /tmp/audit-work/run-118 || exit 70
overall=0
counter=50

run_bounded() {
  counter=$((counter + 1))
  out="/tmp/audit-work/run-118/.audit-command-${counter}.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$out" 2>&1
  rc=$?
  lines=$(wc -l <"$out")
  printf '[output lines %d]\n' "$lines"
  if (( lines <= 200 )); then
    sed -n '1,200p' "$out"
  else
    sed -n '1,130p' "$out"
    printf '[... %d lines omitted ...]\n' "$((lines - 200))"
    tail -n 70 "$out"
  fi
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

echo '== Bridge-free proof diagnostic =='
printf '$ sed 83,93d verification.k > verification-no-recursive-bridge.k\n'
sed '83,93d' verification.k > verification-no-recursive-bridge.k
printf '[exit %d]\n' "$?"
cp verification-no-recursive-bridge.k /audit-output/evidence/verification-no-recursive-bridge.k
sed '1s/verification.k/verification-no-recursive-bridge.k/' \
  independent-positive-claims.k > no-bridge-positive-claims.k
cp no-bridge-positive-claims.k /audit-output/evidence/no-bridge-positive-claims.k
run_bounded kompile verification-no-recursive-bridge.k \
  --backend haskell \
  --main-module HUMAN-EVAL-118-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-no-bridge-v2-kompiled
rc=$?
if (( rc == 0 )); then
  run_bounded kprove no-bridge-positive-claims.k \
    --definition audit-no-bridge-v2-kompiled \
    --spec-module AUDIT-CLAIM-THREE-PLUS \
    --depth 200
  no_bridge_rc=$?
  if (( no_bridge_rc == 0 )); then
    echo 'UNEXPECTED: bridge-free depth-bounded proof closed'
    overall=1
  else
    echo 'EXPECTED: bridge-free symbolic proof did not close'
  fi
else
  overall=1
fi

echo '== Operational body-sensitivity witness =='
printf '$ sed first base return in verification.k to Return(Str(\"a\")) > verification-mutated-base.k\n'
sed '0,/Return(Str(""))/s/Return(Str(""))/Return(Str("a"))/' \
  verification.k > verification-mutated-base.k
printf '[exit %d]\n' "$?"
cp verification-mutated-base.k /audit-output/evidence/verification-mutated-base.k
sed '1s/verification.k/verification-mutated-base.k/' \
  /audit-output/evidence/bridge-body-sensitivity.k > bridge-body-sensitivity-mutated.k
cp bridge-body-sensitivity-mutated.k /audit-output/evidence/bridge-body-sensitivity-mutated.k
cp /audit-output/evidence/mutated-body-witness.py ./mutated-body-witness.py

run_bounded python3 mutated-body-witness.py
run_bounded python3 trusted-py2mpy.py mutated-body-witness.py
# The previous command prints the MPY; generate the concrete artifact separately.
printf '\n$ python3 trusted-py2mpy.py mutated-body-witness.py > mutated-body-witness.mpy\n'
python3 trusted-py2mpy.py mutated-body-witness.py > mutated-body-witness.mpy
rc=$?
printf '[exit %d]\n' "$rc"
(( rc == 0 )) || overall=1
cp mutated-body-witness.mpy /audit-output/evidence/mutated-body-witness.mpy
run_bounded krun mutated-body-witness.mpy --definition audit-runtime-kompiled
(( $? == 0 )) || overall=1

run_bounded kompile verification-mutated-base.k \
  --backend haskell \
  --main-module HUMAN-EVAL-118-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-mutated-base-v2-kompiled
rc=$?
if (( rc == 0 )); then
  run_bounded kprove bridge-body-sensitivity-mutated.k \
    --definition audit-mutated-base-v2-kompiled \
    --spec-module AUDIT-BODY-SENSITIVITY
  sensitivity_rc=$?
  if (( sensitivity_rc != 0 )); then
    echo 'UNEXPECTED: bridge-enabled false body-mutation claim was rejected'
    overall=1
  else
    echo 'WITNESS: bridge-enabled theory proved #Top for the false mutated-body claim'
  fi
else
  overall=1
fi

exit "$overall"
