#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

run_log() {
  name="$1"
  shift
  log="$evidence/$name.log"
  {
    printf 'WORKDIR: %s\n' "$work"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    (
      cd "$work"
      "$@"
    )
    status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
    return "$status"
  } >"$log" 2>&1
}

{
  printf 'COMMAND: find %q -maxdepth 1 -type d -name %q -print\n' \
    "$work" '*-kompiled'
  find "$work" -maxdepth 1 -type d -name '*-kompiled' -print
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
} > "$evidence/stage3_prebuild_cleanliness.log" 2>&1

{
  printf 'COMMAND: cp %q %q\n' \
    "$evidence/concrete_harness.py" "$work/audit_concrete.py"
  cp "$evidence/concrete_harness.py" "$work/audit_concrete.py"
  copy_status=$?
  printf 'COPY_EXIT_STATUS: %d\n' "$copy_status"
  printf 'COMMAND: python3 %q %q > %q\n' \
    "$work/py2mpy.py" "$work/audit_concrete.py" "$work/audit_concrete.mpy"
  python3 "$work/py2mpy.py" "$work/audit_concrete.py" \
    > "$work/audit_concrete.mpy"
  translate_status=$?
  printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"
} > "$evidence/stage3_concrete_translate.log" 2>&1

run_log stage3_kompile_llvm \
  timeout 300s kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

run_log stage3_krun_concrete \
  timeout 300s krun audit_concrete.mpy \
  --definition audit-runtime-kompiled \
  --output pretty

run_log stage3_kompile_haskell \
  timeout 300s kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

run_log stage3_kprove_mutual_loops \
  timeout 300s kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-zero,SPEC.loop-positive \
  --output pretty

run_log stage3_kprove_all \
  timeout 300s kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-zero,SPEC.loop-positive,SPEC.correct-bracketing \
  --output pretty
