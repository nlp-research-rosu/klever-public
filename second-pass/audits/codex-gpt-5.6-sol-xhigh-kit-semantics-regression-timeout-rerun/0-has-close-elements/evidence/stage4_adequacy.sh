#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/0-has-close-elements
evidence=/audit-output/evidence
failures=0

run_bounded() {
  local label=$1
  shift
  local raw="$scratch/${label}.raw.log"
  local log="$evidence/${label}.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  "$@" > "$raw" 2>&1
  local status=$?
  local lines bytes
  lines=$(wc -l < "$raw")
  bytes=$(wc -c < "$raw")
  {
    printf 'exit_status=%s\n' "$status"
    printf 'raw_output_lines=%s raw_output_bytes=%s\n' "$lines" "$bytes"
    if (( lines <= 320 )); then
      cat "$raw"
    else
      head -n 140 "$raw"
      printf '%s\n' '--- middle omitted from bounded reviewer log ---'
      tail -n 160 "$raw"
    fi
  } >> "$log"
  rm -f "$raw"
  printf '%s exit=%s lines=%s bytes=%s\n' "$label" "$status" "$lines" "$bytes"
  return "$status"
}

cd "$scratch" || exit 1
export PATH="$HOME/.nix-profile/bin:$PATH"

run_bounded stage4-module-poststate \
  krun solution.mpy --definition audit-runtime-kompiled ||
  failures=$((failures + 1))

printf '%s\n' '$ python3 /reference/py2mpy.py evidence/concrete_audit.py > scratch/concrete-audit.mpy'
python3 /reference/py2mpy.py "$evidence/concrete_audit.py" \
  > "$scratch/concrete-audit.mpy"
translate_status=$?
printf 'concrete_translate_exit=%s\n' "$translate_status"
if (( translate_status != 0 )); then
  failures=$((failures + 1))
fi

run_bounded stage4-krun-concrete-witnesses \
  krun concrete-audit.mpy --definition audit-runtime-kompiled ||
  failures=$((failures + 1))

run_bounded stage4-python-witnesses \
  python3 "$evidence/stage4_witness.py" ||
  failures=$((failures + 1))

printf 'adequacy_dynamic_failures=%s\n' "$failures"
if (( failures != 0 )); then
  printf '%s\n' 'stage4_script_exit=1'
  exit 1
fi
printf '%s\n' 'stage4_script_exit=0'
