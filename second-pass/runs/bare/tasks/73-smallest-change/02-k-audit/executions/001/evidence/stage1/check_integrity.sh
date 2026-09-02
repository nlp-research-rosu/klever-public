#!/usr/bin/env bash
set -u

audit_fail=0

check_regular() {
  audit_path=$1
  if [[ -L "$audit_path" ]]; then
    printf 'FAIL symlink: %s -> %s\n' "$audit_path" "$(readlink "$audit_path")"
    audit_fail=1
  elif [[ ! -e "$audit_path" ]]; then
    printf 'FAIL missing: %s\n' "$audit_path"
    audit_fail=1
  elif [[ ! -f "$audit_path" ]]; then
    printf 'FAIL not-regular: %s\n' "$audit_path"
    audit_fail=1
  else
    printf 'OK regular: %s\n' "$audit_path"
  fi
}

printf 'Rendered mode: GENERATED_SEMANTICS\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'FAIL infrastructure contradiction: /reference/reference-semantics exists\n'
  audit_fail=1
else
  printf 'OK mode boundary: /reference/reference-semantics absent\n'
fi

for audit_path in \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
do
  check_regular "$audit_path"
done

audit_trace_count=$(find /candidate/codex-trace -type f -name '*.jsonl' | wc -l)
audit_trace_nonregular=$(find /candidate/codex-trace \( -type l -o \( ! -type d ! -type f \) \) -print)
printf 'Structured JSONL trace count: %s\n' "$audit_trace_count"
if [[ "$audit_trace_count" -eq 0 ]]; then
  printf 'FAIL missing structured generation trace\n'
  audit_fail=1
fi
if [[ -n "$audit_trace_nonregular" ]]; then
  printf 'FAIL non-regular trace entries:\n%s\n' "$audit_trace_nonregular"
  audit_fail=1
else
  printf 'OK trace entries are regular files/directories\n'
fi

sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py

if cmp -s /reference/prompt.py /candidate/prompt.py; then
  printf 'OK candidate prompt byte-identical to trusted prompt\n'
else
  printf 'FAIL candidate prompt differs from trusted prompt\n'
  audit_fail=1
fi

if cmp -s /reference/py2mpy.py /candidate/py2mpy.py; then
  printf 'OK candidate translator byte-identical to trusted translator\n'
else
  printf 'FAIL candidate translator differs from trusted translator\n'
  audit_fail=1
fi

printf 'Candidate top-level entry types:\n'
find /candidate -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n' | sort

printf 'Integrity failure count indicator: %d\n' "$audit_fail"
exit "$audit_fail"
