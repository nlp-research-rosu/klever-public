#!/usr/bin/env bash
set -u

status=0

echo '$ test ! -e /reference/reference-semantics'
test ! -e /reference/reference-semantics
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ cmp -s /candidate/prompt.py /reference/prompt.py'
cmp -s /candidate/prompt.py /reference/prompt.py
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ cmp -s /candidate/py2mpy.py /reference/py2mpy.py'
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ sha256sum prompt and translator copies'
sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ required candidate source/provenance artifacts are regular non-symlink files'
required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k
  spec.k prove.sh verification-input.mpy
)
for name in "${required[@]}"; do
  path="/candidate/$name"
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'OK regular %s\n' "$path"
  else
    printf 'FAIL missing/mistyped/symlinked %s\n' "$path"
    status=1
  fi
done

echo '$ structured trace inventory and symlink/type check'
trace_count=0
while IFS= read -r -d '' path; do
  trace_count=$((trace_count + 1))
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'OK regular %s\n' "$path"
  else
    printf 'FAIL mistyped/symlinked %s\n' "$path"
    status=1
  fi
done < <(find /candidate/codex-trace -type f -name '*.jsonl' -print0)
echo "structured_trace_files=$trace_count"
(( trace_count > 0 )) || status=1

echo '$ python3 validates JSON provenance and every structured trace record'
python3 - <<'PY'
import glob
import json

for path in ["/candidate/run-input.json", "/candidate/metrics.json"]:
    with open(path, encoding="utf-8") as stream:
        json.load(stream)
    print("valid_json", path)

records = 0
for path in glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True):
    with open(path, encoding="utf-8") as stream:
        for lineno, line in enumerate(stream, 1):
            json.loads(line)
            records += 1
    print("valid_jsonl", path)
print("trace_records", records)
PY
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ find source/provenance tree entries (candidate-built caches are listed but excluded from reuse)'
find /candidate -maxdepth 2 -printf '%y %p -> %l\n' | sort
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo "stage1_exit=$status"
exit "$status"
