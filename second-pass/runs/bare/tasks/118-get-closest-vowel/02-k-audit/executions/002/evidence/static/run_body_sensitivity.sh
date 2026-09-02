#!/usr/bin/env bash
set -uo pipefail

original=/tmp/audit-work/118-get-closest-vowel/candidate-src
mutated=/tmp/audit-work/118-get-closest-vowel/body-mutation
definition=/tmp/audit-work/118-get-closest-vowel/build/body-mutated-kompiled

printf 'ORIGINAL_PROGRAM_TERM_SHA256\n'
sha256sum "$original/program.k"
printf 'MUTATED_PROGRAM_TERM_SHA256\n'
sha256sum "$mutated/program.k"

printf 'COMMAND=python3 %q %q > %q\n' \
  /tmp/audit-work/118-get-closest-vowel/reference/py2mpy.py \
  "$mutated/solution.py" "$mutated/solution.mpy"
python3 /tmp/audit-work/118-get-closest-vowel/reference/py2mpy.py \
  "$mutated/solution.py" > "$mutated/solution.mpy"
status=$?
printf 'TRANSLATE_EXIT_STATUS=%s\n' "$status"
if (( status != 0 )); then exit "$status"; fi

printf 'COMMAND=python3 %q %q %q\n' \
  "$mutated/check_program_module.py" "$mutated/solution.mpy" "$mutated/program.k"
python3 "$mutated/check_program_module.py" \
  "$mutated/solution.mpy" "$mutated/program.k"
status=$?
printf 'MUTATED_TERM_CONSTRUCTOR_CHECK_EXIT_STATUS=%s\n' "$status"
if (( status != 0 )); then exit "$status"; fi

printf 'COMMAND=python3 -c <import mutated solution; print(get_closest_vowel(\"bab\"))>\n'
MUTATED="$mutated" python3 - <<'PY'
import importlib.util
import os
from pathlib import Path
path = Path(os.environ["MUTATED"]) / "solution.py"
spec = importlib.util.spec_from_file_location("mutated_solution", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(f"MUTATED_PYTHON_bab={module.get_closest_vowel('bab')!r}")
PY
status=$?
printf 'MUTATED_PYTHON_EXIT_STATUS=%s\n' "$status"
if (( status != 0 )); then exit "$status"; fi

printf 'COMMAND=kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition %q --warnings none\n' \
  "$definition"
(
  cd "$mutated" &&
  kompile semantic.k \
    --backend haskell \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition "$definition" \
    --warnings none
)
status=$?
printf 'KOMPILE_EXIT_STATUS=%s\n' "$status"
if (( status != 0 )); then exit "$status"; fi

printf 'COMMAND=krun solution.mpy -cARG=word(\"bab\") --definition %q --output pretty\n' \
  "$definition"
k_output="$(
  cd "$mutated" &&
  krun solution.mpy -cARG='word("bab")' \
    --definition "$definition" --output pretty
)"
status=$?
printf '%s\n' "$k_output" | sed -n '1,6p'
printf 'KRUN_EXIT_STATUS=%s\n' "$status"
if (( status != 0 )); then exit "$status"; fi
if ! printf '%s\n' "$k_output" |
  rg -q 'pyStr \( snoc \( \.Chars , vow \( v_a \) \) \)'; then
  printf 'EXPECTED_MUTATED_K_RESULT_NOT_FOUND\n'
  exit 97
fi

printf 'COMMAND=kprove spec.k --definition %q --spec-module SPEC --warnings none\n' \
  "$definition"
(
  cd "$mutated" &&
  kprove spec.k --definition "$definition" --spec-module SPEC --warnings none
)
status=$?
printf 'KPROVE_EXIT_STATUS=%s\n' "$status"
exit "$status"
