#!/usr/bin/env bash
set +e

cd /tmp/audit-work/task134 || exit 90

printf '%s\n' \
  'COMMAND_TEMPLATE: krun solution.mpy --definition semantic-audit-kompiled -cTXT="\"${text}\""'

cases=(
  ''
  'A'
  '7'
  'ab'
  ' a'
  'a b'
  'apple pie'
  'apple pi e'
  'apple pi e '
  'é'
  ' é'
  'λ'
  ' 界'
)

for text in "${cases[@]}"; do
  printf 'CASE_PY_REPR='
  TEXT="$text" python3 -c 'import os; print(repr(os.environ["TEXT"]))'
  krun solution.mpy \
    --definition semantic-audit-kompiled \
    -cTXT="\"${text}\""
  status=$?
  printf 'KRUN_EXIT_STATUS=%s\n' "$status"
  TEXT="$text" python3 - <<'PY'
import importlib.util
import os

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter

text = os.environ["TEXT"]
canonical = load("/reference/canonical.py", "canonical_concrete")
submitted = load("/tmp/audit-work/task134/solution.py", "submitted_concrete")
print(f"PYTHON_CANONICAL={canonical(text)!r}")
print(f"PYTHON_SUBMITTED={submitted(text)!r}")
PY
  printf '%s\n' '---'
done
