#!/usr/bin/env bash
set -euo pipefail

definition=/tmp/audit-work/131-digits/build/semantic-kompiled
solution=/tmp/audit-work/131-digits/candidate-src/solution.mpy
scratch=$(mktemp -d /tmp/audit-work/131-digits/concrete.XXXXXX)
trap 'rm -rf "$scratch"' EXIT

cases=(
  0
  1
  4
  10
  11
  235
  2468
  10203
  999999999999999999999999999999999999999999999999999999999999
)

for n in "${cases[@]}"; do
  program="$scratch/invoke-$n.mpy"
  sed "1s/^/Invoke(/; \$s/\$/, \"digits\", $n)/" "$solution" > "$program"
  printf 'COMMAND: krun %s --definition %s --output pretty\n' \
    "$program" "$definition"
  output=$(krun "$program" --definition "$definition" --output pretty)
  answer=$(
    printf '%s\n' "$output" |
      awk '/<answer>/{getline; gsub(/[[:space:]]/,""); sub(/~>.K/,""); print}'
  )
  python_values=$(
    python3 - "$n" <<'PY'
import importlib.util
import sys
from pathlib import Path

n = int(sys.argv[1])
root = Path("/tmp/audit-work/131-digits")

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digits

canonical = load(root / "trusted" / "canonical.py", "concrete_canonical")
generated = load(root / "candidate-src" / "solution.py", "concrete_generated")
print(canonical(n), generated(n))
PY
  )
  read -r canonical_answer python_answer <<< "$python_values"
  printf 'n=%s k=%s canonical_python=%s generated_python=%s\n' \
    "$n" "$answer" "$canonical_answer" "$python_answer"
  test "$answer" = "$canonical_answer"
  test "$answer" = "$python_answer"
done

printf 'cases=%s mismatches=0\n' "${#cases[@]}"
