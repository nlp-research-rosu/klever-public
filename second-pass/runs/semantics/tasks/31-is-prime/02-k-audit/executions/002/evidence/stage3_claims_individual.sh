#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/31-is-prime-audit
cd "${work}" || exit 125
failures=0

run_claim() {
  description=$1
  definition=$2
  module=$3
  label=$4
  echo "COMMAND (${description}): kprove spec.k --definition ${definition} --spec-module ${module} --claims ${label}"
  timeout 900 kprove spec.k \
    --definition "${definition}" \
    --spec-module "${module}" \
    --claims "${label}"
  status=$?
  echo "EXIT_STATUS (${description}): ${status}"
  if [[ ${status} -ne 0 ]]; then
    failures=$((failures + 1))
  fi
}

# These files use trailing [label(...)] attributes, whose CLI spelling is the
# bare label rather than MODULE.label.
run_claim loop-correct proof-base-kompiled LOOP-SPEC loop-correct
run_claim entry-small proof-kompiled SPEC entry-small
run_claim entry-large-prefix proof-kompiled SPEC entry-large-prefix

echo "FAILURE_COUNT: ${failures}"
if [[ ${failures} -ne 0 ]]; then
  exit 1
fi
exit 0
