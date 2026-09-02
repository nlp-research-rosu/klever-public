#!/usr/bin/env bash
set -uo pipefail
set -x

candidate=/candidate
reference=/reference

for path in \
  "$candidate/run-input.json" \
  "$candidate/metrics.json" \
  "$candidate/codex-last.txt" \
  "$candidate/codex-output.log" \
  "$candidate/prompt.py" \
  "$candidate/py2mpy.py" \
  "$candidate/solution.py" \
  "$candidate/solution.mpy" \
  "$candidate/spec.k" \
  "$candidate/verification.k"; do
  test -f "$path"
  printf 'required_file status=%s path=%s\n' "$?" "$path"
done

test -d "$reference/reference-semantics"
printf 'trusted_semantics_present status=%s\n' "$?"

find "$candidate/reference-semantics" -type l -print
printf 'candidate_semantics_symlink_count='
find "$candidate/reference-semantics" -type l -print | wc -l

diff -qr --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
printf 'semantics_recursive_diff_status=%s\n' "$?"

cmp -s "$reference/prompt.py" "$candidate/prompt.py"
printf 'prompt_byte_identity_status=%s\n' "$?"
cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"
printf 'translator_byte_identity_status=%s\n' "$?"

printf '%s\n' 'TRUSTED SEMANTICS MANIFEST'
find "$reference/reference-semantics" -printf '%y %P\n' | LC_ALL=C sort
find "$reference/reference-semantics" -type f -print0 |
  LC_ALL=C sort -z |
  xargs -0 sha256sum

printf '%s\n' 'CANDIDATE SEMANTICS MANIFEST'
find "$candidate/reference-semantics" -printf '%y %P\n' | LC_ALL=C sort
find "$candidate/reference-semantics" -type f -print0 |
  LC_ALL=C sort -z |
  xargs -0 sha256sum

python3 - <<'PY'
import json
from pathlib import Path

for path in (Path("/candidate/run-input.json"), Path("/candidate/metrics.json")):
    try:
        value = json.loads(path.read_text())
    except Exception as error:
        print(f"json_parse path={path} ok=False error={error!r}")
    else:
        print(f"json_parse path={path} ok=True type={type(value).__name__}")

trace_paths = sorted(Path("/candidate/codex-trace").rglob("*"))
files = [path for path in trace_paths if path.is_file()]
print(f"structured_trace_file_count={len(files)}")
for path in files:
    ok = True
    line_count = 0
    errors = []
    with path.open() as stream:
        for line_count, line in enumerate(stream, 1):
            try:
                json.loads(line)
            except Exception as error:
                ok = False
                errors.append((line_count, repr(error)))
                if len(errors) == 3:
                    break
    print(f"trace_parse path={path} ok={ok} lines_checked={line_count} errors={errors}")
PY
