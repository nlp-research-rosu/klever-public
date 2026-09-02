#!/usr/bin/env bash
set -u

work=/tmp/audit-work/recon
raw_dir="$work/raw-logs"
mkdir -p "$raw_dir"
failed=0

run_bounded() {
  local label=$1
  shift
  local raw="$raw_dir/$label.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$raw" 2>&1
  local status=$?
  local lines
  lines=$(wc -l <"$raw")
  printf '[captured %d lines in %s]\n' "$lines" "$raw"
  sed -n '1,200p' "$raw"
  if (( lines > 280 )); then
    printf '[... middle omitted from bounded evidence log ...]\n'
    tail -n 80 "$raw"
  fi
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    failed=1
  fi
}

printf 'Fresh-definition check before builds:\n'
for definition in runtime-kompiled verification-base-kompiled verification-kompiled
do
  if [[ -e "$work/$definition" ]]; then
    printf 'unexpected pre-existing path: %s\n' "$work/$definition"
    failed=1
  else
    printf 'absent as required: %s\n' "$work/$definition"
  fi
done

run_bounded tool_versions kompile --version
run_bounded runtime_kompile \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

printf '\n$ python3 /reference/py2mpy.py audit_concrete.py > audit_concrete.mpy\n'
python3 /reference/py2mpy.py audit_concrete.py > audit_concrete.mpy
translate_status=$?
printf '[exit %d]\n' "$translate_status"
if (( translate_status != 0 )); then failed=1; fi

run_bounded runtime_krun \
  krun audit_concrete.mpy --definition runtime-kompiled

run_bounded base_kompile \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
run_bounded loop_kprove \
  kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-invariant

run_bounded verification_kompile \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
run_bounded function_kprove \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.function-correct

exit "$failed"
