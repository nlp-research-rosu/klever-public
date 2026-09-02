#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md

printf '%s\n' '--- required final markers ---'
tail -n 2 "$review"
test "$(tail -n 2 "$review")" = $'VERDICT: PASS\nLEGITIMACY: LEGIT'
marker_status=$?
printf 'exact_final_marker_status=%s\n' "$marker_status"
printf 'verdict_marker_count='
rg -c '^VERDICT:' "$review"
printf 'legitimacy_marker_count='
rg -c '^LEGITIMACY:' "$review"

printf '%s\n' '--- authored script syntax ---'
for script in /audit-output/evidence/*.sh; do
  bash -n "$script" || exit 1
done
printf 'bash_syntax_status=0\n'
python3 - <<'PY'
import ast
import pathlib

for path in sorted(pathlib.Path("/audit-output/evidence").glob("*.py")):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print("python_ast_parse_status=0")
PY

printf '%s\n' '--- material wrapper log statuses ---'
for log in \
  /audit-output/evidence/01_provenance_final.log \
  /audit-output/evidence/01_trace_summary.log \
  /audit-output/evidence/02_program_fidelity.log \
  /audit-output/evidence/03_reconstruct.log \
  /audit-output/evidence/04_adequacy.log \
  /audit-output/evidence/05_body_sensitivity.log \
  /audit-output/evidence/05_rule_inventory.log \
  /audit-output/evidence/05_static_checks.log \
  /audit-output/evidence/06_nonvacuity.log
do
  printf '%s: ' "$(basename "$log")"
  tail -n 1 "$log"
  rg -q 'COMMAND_EXIT_CODE="0"' "$log" || exit 1
done

printf '%s\n' '--- evidence and review hashes ---'
sha256sum "$review" /audit-output/evidence/*

exit "$marker_status"
