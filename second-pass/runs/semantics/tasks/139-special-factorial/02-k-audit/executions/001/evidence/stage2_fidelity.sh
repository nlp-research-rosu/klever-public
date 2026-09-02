#!/usr/bin/env bash
set -u

task_dir=/tmp/audit-work/139-special-factorial

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'STAGE 2 PROGRAM FIDELITY AND DIFFERENTIAL TESTING\n'
run mkdir -p "$task_dir"
run cp -a /candidate/reference-semantics "$task_dir/reference-semantics"
for artifact in solution.py solution.mpy run.py run.mpy spec.k verification.k prove.sh; do
  run cp "/candidate/$artifact" "$task_dir/$artifact"
done
run cp /reference/canonical.py "$task_dir/trusted-canonical.py"
run cp /reference/prompt.py "$task_dir/trusted-prompt.py"
run cp /reference/py2mpy.py "$task_dir/trusted-py2mpy.py"

printf '$ python3 /reference/py2mpy.py %q > %q\n' \
  "$task_dir/solution.py" "$task_dir/solution.regenerated.mpy"
python3 /reference/py2mpy.py "$task_dir/solution.py" \
  > "$task_dir/solution.regenerated.mpy"
rc=$?
printf '[exit %d]\n' "$rc"

run cmp "$task_dir/solution.mpy" "$task_dir/solution.regenerated.mpy"
run sha256sum "$task_dir/solution.mpy" "$task_dir/solution.regenerated.mpy"
run python3 /audit-output/evidence/differential_test.py
