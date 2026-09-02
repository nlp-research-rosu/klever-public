#!/usr/bin/env bash
set -euo pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

wc -l -c /generation-evidence/codex-output.log
sed -n '1,30p' /generation-evidence/codex-output.log
rg -n '#Top|WarnStuckClaimState|KPROVE_PASSED|VALIDATED|kprove spec|kompile --backend|mismatches:' \
  /generation-evidence/codex-output.log | tail -120
tail -40 /generation-evidence/codex-output.log
