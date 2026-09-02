#!/usr/bin/env bash
set -u

definition=${1:-/tmp/audit-work/candidate-src/concrete-kompiled}
program=/tmp/audit-work/candidate-src/solution.mpy

run_case() {
  name=$1
  karg=$2
  python_hex=$3
  printf 'CASE=%s\n' "$name"
  printf 'python_input_utf8_hex=%s\n' "$python_hex"
  python3 - "$python_hex" <<'PY'
import sys
value = bytes.fromhex(sys.argv[1]).decode("utf-8")
print(f"python_input={value!r}")
print(f"python_output={value.swapcase()!r}")
print(f"python_output_utf8_hex={value.swapcase().encode('utf-8').hex()}")
PY
  printf '$ krun %q --definition %q %q\n' "$program" "$definition" "-cARG=$karg"
  krun "$program" --definition "$definition" "-cARG=$karg"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

run_case empty '""' ''
run_case documented '"Hello"' '48656c6c6f'
run_case ascii-boundaries '"@AZ[\x60az{"' '40415a5b60617a7b'
run_case unicode-example '"Stra\xc3\x9fe \xce\x94elta"' \
  '53747261c39f6520ce94656c7461'
run_case unicode-expansions '"\xc3\x9f\xc4\xb0\xc5\x89\xef\xac\x83"' \
  'c39fc4b0c589efac83'
run_case utf8-width-boundaries \
  '"\xc2\x80\xc2\xb5\xdf\xbf\xe0\xa0\x80\xce\x94\xef\xbf\xbf\xf0\x90\x80\x80\xf0\x90\x90\x80\xf4\x8f\xbf\xbf"' \
  'c280c2b5dfbfe0a080ce94efbfbff0908080f0909080f48fbfbf'
