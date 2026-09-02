#!/usr/bin/env bash
set +e

printf '$ python3 /audit-output/evidence/01_integrity.py\n'
python3 /audit-output/evidence/01_integrity.py
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ sha256sum /audit-input.json /audit-campaign-lock.json /run.json /task.json /generation-result.json /generation-evidence/invocation.json /generation-evidence/metrics.json /generation-evidence/runtime-metrics.json /generation-evidence/usage.json /generation-evidence/codex-last.txt /generation-evidence/codex-output.log /generation-evidence/prompt.txt\n'
sha256sum /audit-input.json /audit-campaign-lock.json /run.json /task.json /generation-result.json /generation-evidence/invocation.json /generation-evidence/metrics.json /generation-evidence/runtime-metrics.json /generation-evidence/usage.json /generation-evidence/codex-last.txt /generation-evidence/codex-output.log /generation-evidence/prompt.txt
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ diff -r --no-dereference -- /reference/reference-semantics /candidate/reference-semantics\n'
diff -r --no-dereference -- /reference/reference-semantics /candidate/reference-semantics
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ find -P /candidate -type l -o ! -type d ! -type f\n'
find -P /candidate -type l -o ! -type d ! -type f
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

exit 0
