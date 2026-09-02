#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/prime31
evidence=/audit-output/evidence
overall=0

run_recorded() {
  name=$1
  shift
  log="$evidence/$name.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$log" 2>&1
  status=$?
  printf 'EXIT: %s\n' "$status"
  printf 'LOG: %s\n' "$log"
  if [[ $status -ne 0 ]]; then
    overall=1
  fi
}

cd "$scratch" || exit 2

echo '$ cp -a /audit-output/evidence/03_concrete_driver.py /tmp/audit-work/prime31/concrete-driver.py'
cp -a "$evidence/03_concrete_driver.py" "$scratch/concrete-driver.py"
echo "EXIT: $?"

run_recorded 03_kompile_llvm \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled

run_recorded 03_translate_concrete \
  python3 py2mpy.py concrete-driver.py
cp "$evidence/03_translate_concrete.log" concrete-driver.mpy
echo '$ cp /audit-output/evidence/03_translate_concrete.log concrete-driver.mpy'
echo "EXIT: $?"

echo '$ python3 -c <runpy concrete-driver.py and print results>'
python3 -c 'import runpy; print(runpy.run_path("concrete-driver.py")["results"])' \
  > "$evidence/03_python_concrete.log" 2>&1
status=$?
echo "EXIT: $status"
echo "LOG: $evidence/03_python_concrete.log"
if [[ $status -ne 0 ]]; then overall=1; fi

run_recorded 03_krun_concrete \
  krun concrete-driver.mpy \
  --definition reviewer-runtime-kompiled

run_recorded 03_kompile_haskell \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled

run_recorded 03_kprove_all \
  kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC

run_recorded 03_kprove_prime_loop \
  kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.prime-loop

# This diagnostic asks whether the entry proof closes even after its auxiliary
# loop circularity is filtered out. It is not a substitute for the all-claims
# target run above.
run_recorded 03_kprove_entry_without_helper \
  kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.is-prime

echo "OVERALL_NONZERO_SEEN: $overall"
exit 0
