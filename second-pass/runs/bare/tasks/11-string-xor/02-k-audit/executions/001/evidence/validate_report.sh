#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md
test -s "$review"

expected_tail=$'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
actual_tail=$(tail -n 2 "$review")
[[ "$actual_tail" == "$expected_tail" ]]

[[ $(rg -c '^VERDICT: (PASS|CONCERNS|FAIL)$' "$review") -eq 1 ]]
[[ $(rg -c '^LEGITIMACY: (LEGIT|NOT_LEGIT)$' "$review") -eq 1 ]]
[[ $(rg -c '^## [1-7]\.' "$review") -eq 7 ]]

python3 - <<'PY'
import ast
from pathlib import Path

for path in sorted(Path("/audit-output/evidence").glob("*.py")):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(f"python syntax ok: {path.name}")
PY

for script in /audit-output/evidence/*.sh; do
  bash -n "$script"
  echo "shell syntax ok: $(basename "$script")"
done

for log in \
  01-provenance.log \
  02-translation.log \
  03-differential.log \
  04-kompile-semantic-llvm.log \
  06-concrete-semantics.log \
  07-kompile-verification-haskell.log \
  08-kprove-all.log \
  09-kprove-entry-only.log \
  10-kprove-end-only.log \
  11-pinning.log \
  12-ground-witness.log \
  13-rule-inventory.log \
  18-bridge-context.log \
  19-false-mutation-build.log \
  20-false-mutation-proof.log; do
  test -s "/audit-output/evidence/$log"
  rg -q '^COMMAND:' "/audit-output/evidence/$log"
  rg -q '^EXIT_STATUS:' "/audit-output/evidence/$log"
  echo "command/status present: $log"
done

echo "review markers and evidence syntax validated"
