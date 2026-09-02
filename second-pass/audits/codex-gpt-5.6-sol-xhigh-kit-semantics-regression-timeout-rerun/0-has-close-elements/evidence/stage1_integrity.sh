#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

printf '%s\n' '$ stat -c "%F %a %s %n" <trusted and required candidate artifacts>'
stat -c '%F %a %s %n' \
  "$reference/canonical.py" \
  "$reference/prompt.py" \
  "$reference/py2mpy.py" \
  "$reference/reference-semantics" \
  "$candidate/run-input.json" \
  "$candidate/metrics.json" \
  "$candidate/codex-last.txt" \
  "$candidate/codex-output.log" \
  "$candidate/prompt.py" \
  "$candidate/py2mpy.py" \
  "$candidate/solution.py" \
  "$candidate/solution.mpy" \
  "$candidate/verification.k" \
  "$candidate/spec.k" \
  "$candidate/prove.sh" \
  "$candidate/PROOF.md"
printf 'stat_exit=%s\n' "$?"

printf '%s\n' '$ find -P /candidate -type l -printf ...'
find -P "$candidate" -type l -printf '%p -> %l\n'
printf 'candidate_symlink_find_exit=%s\n' "$?"

printf '%s\n' '$ find -P <semantics trees> ! -type d ! -type f -printf ...'
find -P "$candidate/reference-semantics" ! -type d ! -type f \
  -printf 'candidate-special: %y %p -> %l\n'
candidate_special_status=$?
find -P "$reference/reference-semantics" ! -type d ! -type f \
  -printf 'reference-special: %y %p -> %l\n'
reference_special_status=$?
printf 'candidate_special_find_exit=%s reference_special_find_exit=%s\n' \
  "$candidate_special_status" "$reference_special_status"

printf '%s\n' '$ diff --no-dereference -rqs /reference/reference-semantics /candidate/reference-semantics'
diff --no-dereference -rqs \
  "$reference/reference-semantics" "$candidate/reference-semantics"
printf 'semantics_diff_exit=%s\n' "$?"

printf '%s\n' '$ cmp -s trusted candidate prompt/translator'
cmp -s "$reference/prompt.py" "$candidate/prompt.py"
printf 'prompt_cmp_exit=%s\n' "$?"
cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"
printf 'translator_cmp_exit=%s\n' "$?"
sha256sum \
  "$reference/prompt.py" "$candidate/prompt.py" \
  "$reference/py2mpy.py" "$candidate/py2mpy.py"

printf '%s\n' '$ python3 - <parse run-input, metrics, and trace JSON>'
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path

for name in ("run-input.json", "metrics.json"):
    path = Path("/candidate") / name
    with path.open(encoding="utf-8") as stream:
        data = json.load(stream)
    print(f"{name}: {json.dumps(data, sort_keys=True)}")

trace_paths = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
print("trace_paths:", [str(path) for path in trace_paths])
for path in trace_paths:
    counts = Counter()
    first = None
    last = None
    rows = 0
    parse_errors = 0
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            rows += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                parse_errors += 1
                continue
            if first is None:
                first = obj
            last = obj
            counts[obj.get("type", "<missing>")] += 1
    print("trace_summary:", path, "rows=", rows, "parse_errors=", parse_errors)
    print("trace_types:", dict(sorted(counts.items())))
    print("trace_first_type:", None if first is None else first.get("type"))
    print("trace_last_type:", None if last is None else last.get("type"))
PY
printf 'json_parse_exit=%s\n' "$?"

printf '%s\n' '$ wc -lc and sha256sum generation logs'
mapfile -t trace_logs < <(
  find -P "$candidate/codex-trace" -type f -name '*.jsonl' -print | sort
)
wc -lc "$candidate/codex-output.log" "${trace_logs[@]}"
printf 'wc_exit=%s\n' "$?"
sha256sum "$candidate/codex-output.log"
sha256sum "${trace_logs[@]}"
printf 'log_hash_exit=%s\n' "$?"

printf '%s\n' '$ grep bounded generation claims from codex-output.log'
grep -nE '^(RESULT:|VALIDATED$|#Top$|differential cases:|mismatches:|EXPECTED FAILURE:)|Four positive claims|KPROVE_PASSED' \
  "$candidate/codex-output.log" | tail -n 80
printf 'bounded_claim_grep_exit=%s\n' "$?"

printf '%s\n' 'stage1_script_exit=0'
