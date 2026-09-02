#!/usr/bin/env bash
set -uo pipefail

definition=/tmp/audit-work/160-do-algebra/concrete-kompiled
work=/tmp/audit-work/160-do-algebra/candidate

printf -v zeroes '%*s' 4300 ''
zeroes=${zeroes// /0}
large_integer="1${zeroes}"
operators='ops(Op("+", .Ops))'
operands="ints(Num(${large_integer}, Num(0, .Ints)))"

printf 'scope=one plus operator, first operand 10**4300 (4301 decimal digits), second operand 0\n'
printf 'COMMAND: krun solution.mpy --definition %q -cOPS=<operators above> -cOPERANDS=<4301-digit witness above>\n' "$definition"
cd "$work" || exit 125
k_output="$(krun solution.mpy --definition "$definition" -cOPS="$operators" -cOPERANDS="$operands" 2>&1)"
k_status=$?
printf 'K_EXIT: %d\n' "$k_status"
printf 'K_OUTPUT_BYTES: %d\n' "${#k_output}"
if grep -Fq "answer ( ${large_integer} )" <<<"$k_output"; then
  printf 'K_RETURNED_INPUT_PLUS_ZERO: true\n'
else
  printf 'K_RETURNED_INPUT_PLUS_ZERO: false\n'
fi

printf 'COMMAND: python3 inline importer for trusted canonical and candidate on the same witness\n'
python3 - <<'PY'
import importlib.util
import sys

print("python_default_max_str_digits=", sys.int_info.default_max_str_digits)
value = 10 ** 4300
for name, path in (
    ("trusted_canonical", "/tmp/audit-work/160-do-algebra/reference/canonical.py"),
    ("candidate_solution", "/tmp/audit-work/160-do-algebra/candidate/solution.py"),
):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        result = module.do_algebra(["+"], [value, 0])
        print(name, "return", type(result).__name__)
    except Exception as error:
        print(name, "raise", type(error).__name__)
PY
