#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
EVIDENCE=/audit-output/evidence
overall=0

run_bounded() {
  local label="$1"
  local command_text="$2"
  local temporary
  temporary="$(mktemp /tmp/audit-work/${label}.XXXXXX)"
  printf '$ %s\n' "$command_text" > "$EVIDENCE/${label}.log"
  bash -o pipefail -c "$command_text" > "$temporary" 2>&1
  local status=$?
  local lines
  lines="$(wc -l < "$temporary")"
  local bytes
  bytes="$(wc -c < "$temporary")"
  printf '[captured output: %s lines, %s bytes]\n' "$lines" "$bytes" >> "$EVIDENCE/${label}.log"
  if [ "$lines" -le 500 ]; then
    sed -n '1,500p' "$temporary" >> "$EVIDENCE/${label}.log"
  else
    sed -n '1,80p' "$temporary" >> "$EVIDENCE/${label}.log"
    printf '[... bounded omission of middle output ...]\n' >> "$EVIDENCE/${label}.log"
    tail -n 420 "$temporary" >> "$EVIDENCE/${label}.log"
  fi
  printf '[exit %d]\n' "$status" >> "$EVIDENCE/${label}.log"
  rm -f "$temporary"
  printf '%s exit=%d\n' "$label" "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

run_bounded stage4_pinning \
  "python3 '$EVIDENCE/pinning_check.py'"

run_bounded stage4_make_harness \
  "python3 '$EVIDENCE/make_concrete_harness.py'"

run_bounded stage4_translate_harness \
  "cd '$SCRATCH' && python3 py2mpy.py audit-concrete-harness.py > audit-concrete-harness.mpy"

run_bounded stage4_krun_harness \
  "cd '$SCRATCH' && krun audit-concrete-harness.mpy --definition audit-runtime-kompiled"

run_bounded stage4_copy_witness_spec \
  "cp '$EVIDENCE/spec-witnesses.k' '$SCRATCH/spec-witnesses.k'"

run_bounded stage4_witness_claims \
  "cd '$SCRATCH' && kprove spec-witnesses.k --definition audit-verification-kompiled --spec-module SPEC-WITNESSES"

run_bounded stage4_python_witnesses \
  "python3 -c 'import importlib.util; load=lambda n,p:(lambda s:(s.loader.exec_module(m:=importlib.util.module_from_spec(s)),m)[1])(importlib.util.spec_from_file_location(n,p)); c=load(\"canonical\",\"/reference/canonical.py\").separate_paren_groups; g=load(\"candidate\",\"/candidate/solution.py\").separate_paren_groups; cases=[\"\", \"()\", \"( ) (( )) (( )( ))\"]; print([(x,c(x),g(x)) for x in cases]); assert all(c(x)==g(x) for x in cases)'"

exit "$overall"
