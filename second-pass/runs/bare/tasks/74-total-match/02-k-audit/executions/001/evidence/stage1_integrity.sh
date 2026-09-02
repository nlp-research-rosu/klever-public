#!/usr/bin/env bash
set -uo pipefail

status=0
required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
)

echo "GENERATED_SEMANTICS trusted-mount boundary"
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  echo "FAIL: /reference/reference-semantics exists"
  status=1
else
  echo "PASS: /reference/reference-semantics does not exist"
fi

echo
echo "Required candidate artifact types"
for name in "${required[@]}"; do
  path="/candidate/$name"
  if [[ -L "$path" ]]; then
    echo "SYMLINK: $path"
    status=1
  elif [[ -f "$path" ]]; then
    echo "REGULAR: $path"
  elif [[ -e "$path" ]]; then
    echo "MISTYPED: $path"
    status=1
  else
    echo "MISSING: $path"
    status=1
  fi
done

echo
echo "All candidate symlinks"
find /candidate -type l -print

echo
echo "Candidate inventory"
find /candidate -mindepth 1 -printf '%y\t%P\n' | LC_ALL=C sort

echo
echo "Trusted/candidate identity checks"
for pair in \
  "/reference/prompt.py:/candidate/prompt.py" \
  "/reference/py2mpy.py:/candidate/py2mpy.py"
do
  trusted=${pair%%:*}
  submitted=${pair#*:}
  if cmp -s "$trusted" "$submitted"; then
    echo "IDENTICAL: $trusted $submitted"
  else
    echo "DIFFERENT: $trusted $submitted"
    cmp -l "$trusted" "$submitted" | head -20
    status=1
  fi
done

echo
echo "SHA-256 values"
sha256sum \
  /reference/prompt.py \
  /candidate/prompt.py \
  /reference/py2mpy.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k

echo
echo "Structured trace files and JSON validity"
find /candidate/codex-trace -type f -print | LC_ALL=C sort
python3 - <<'PY'
import json
from pathlib import Path

for path in sorted(Path("/candidate/codex-trace").rglob("*")):
    if not path.is_file():
        continue
    counts = {}
    lines = 0
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            obj = json.loads(line)
            lines += 1
            kind = obj.get("type", "<no-type>")
            counts[kind] = counts.get(kind, 0) + 1
    print(f"{path}: valid JSONL; lines={lines}; top_level_types={counts}")
PY

exit "$status"
