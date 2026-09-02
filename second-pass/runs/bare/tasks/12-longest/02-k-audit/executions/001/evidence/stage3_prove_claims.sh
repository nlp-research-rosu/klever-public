#!/usr/bin/env bash
set -euo pipefail
cd /tmp/audit-work/12-longest-audit

export PATH="/home/agent/.nix-profile/bin:$PATH"
definition=verification-fresh-kompiled

prove() {
  local target="$1"
  local labels="$2"
  local log="/audit-output/evidence/proof-${target}.log"
  local output
  local status

  echo "TARGET=$target"
  echo "$ kprove spec.k --definition $definition --spec-module SPEC --claims $labels --output pretty --warnings none --haskell-backend-command 'kore-exec --log-level error'"
  set +e
  output="$(
    kprove spec.k \
      --definition "$definition" \
      --spec-module SPEC \
      --claims "$labels" \
      --output pretty \
      --warnings none \
      --haskell-backend-command 'kore-exec --log-level error' \
      2>&1
  )"
  status=$?
  set -e
  {
    echo "TARGET=$target"
    echo "SELECTED_CLAIMS=$labels"
    printf '%s\n' "$output"
    echo "KPROVE_EXIT_STATUS=$status"
  } | tee "$log"
  if [[ $status -ne 0 || "$output" != "#Top" ]]; then
    return 1
  fi
}

prove longest-loop 'SPEC.longest-loop'
prove longest-empty 'SPEC.longest-empty'
# The entry theorem consumes the separately checked loop circularity.
prove longest-nonempty 'SPEC.longest-loop,SPEC.longest-nonempty'
prove concrete-empty 'SPEC.concrete-empty'
prove concrete-first-tie 'SPEC.concrete-first-tie'
prove concrete-increasing 'SPEC.concrete-increasing'
prove concrete-late-tie 'SPEC.concrete-late-tie'

echo 'SCRIPT_EXIT_STATUS=0'
