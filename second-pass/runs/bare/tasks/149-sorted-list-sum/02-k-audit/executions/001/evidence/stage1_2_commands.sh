#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

audit_work=/tmp/audit-work/audit149
mkdir -p "$audit_work"

test ! -e /reference/reference-semantics
test -d /candidate
test -z "$(find /candidate -type l -print -quit)"

required_candidate_files=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  solution-program.k
  verification.k
  spec.k
)
for artifact in "${required_candidate_files[@]}"; do
  test -f "/candidate/$artifact"
  test ! -L "/candidate/$artifact"
done

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-40-15-019f89d7-4b4f-7063-88a7-a0437ab8a11e.jsonl
test -f "$trace"
test ! -L "$trace"

cmp /candidate/prompt.py /reference/prompt.py
cmp /candidate/py2mpy.py /reference/py2mpy.py
sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  "$trace" \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/solution-program.k \
  /candidate/verification.k \
  /candidate/spec.k

cp /candidate/solution.py "$audit_work/solution.py"
cp /candidate/solution.mpy "$audit_work/submitted-solution.mpy"
cp /candidate/semantic.k "$audit_work/semantic.k"
cp /candidate/solution-program.k "$audit_work/solution-program.k"
cp /candidate/verification.k "$audit_work/verification.k"
cp /candidate/spec.k "$audit_work/spec.k"
cp /candidate/make_solution_k.py "$audit_work/make_solution_k.py"
cp /candidate/make_run.py "$audit_work/make_run.py"
cp /reference/canonical.py "$audit_work/trusted-canonical.py"
cp /reference/prompt.py "$audit_work/trusted-prompt.py"
cp /reference/py2mpy.py "$audit_work/trusted-py2mpy.py"

python3 "$audit_work/trusted-py2mpy.py" "$audit_work/solution.py" \
  > "$audit_work/regenerated-solution.mpy"
cmp "$audit_work/regenerated-solution.mpy" "$audit_work/submitted-solution.mpy"
sha256sum "$audit_work/regenerated-solution.mpy" "$audit_work/submitted-solution.mpy"

cp "$audit_work/regenerated-solution.mpy" "$audit_work/solution.mpy"
(
  cd "$audit_work"
  python3 make_solution_k.py > regenerated-solution-program.k
)
cmp "$audit_work/regenerated-solution-program.k" "$audit_work/solution-program.k"
sha256sum \
  "$audit_work/regenerated-solution-program.k" \
  "$audit_work/solution-program.k"

PYTHONDONTWRITEBYTECODE=1 python3 /audit-output/evidence/differential_test.py \
  "$audit_work/trusted-canonical.py" \
  "$audit_work/solution.py"
