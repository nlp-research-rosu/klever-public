#!/usr/bin/env bash
set -uo pipefail

run_checked() {
  echo "+ $*"
  "$@"
  local status=$?
  echo "EXIT: $status"
  if [[ $status -ne 0 ]]; then
    exit "$status"
  fi
}

cd /tmp/audit-work/reconstruction

run_checked command -v kompile
run_checked command -v krun
run_checked command -v kprove
run_checked kompile --version
run_checked kprove --version

run_checked kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition auditor-runtime-kompiled

run_checked kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition auditor-verification-base-kompiled

run_checked kprove connection-spec.k \
  --definition auditor-verification-base-kompiled \
  --spec-module CONNECTION-SPEC

run_checked kprove projection-positive.k \
  --definition auditor-verification-base-kompiled \
  --spec-module PROJECTION-POSITIVE

run_checked kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition auditor-verification-kompiled

run_checked kprove spec.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC
