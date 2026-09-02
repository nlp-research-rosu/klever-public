#!/usr/bin/env bash
set -euo pipefail
set -x

kast \
  /tmp/audit-work/solution.trusted-regenerated.mpy \
  --definition /tmp/audit-work/verification-fresh-kompiled \
  --module MPY-SYNTAX \
  --sort Program \
  --expand-macros \
  --output kore \
  --output-file /tmp/audit-work/submitted-expanded.kore
kast \
  /audit-output/evidence/solutionProgram.term \
  --definition /tmp/audit-work/verification-fresh-kompiled \
  --module SOLUTION \
  --sort Program \
  --expand-macros \
  --output kore \
  --output-file /tmp/audit-work/macro-expanded.kore
cmp --silent \
  /tmp/audit-work/submitted-expanded.kore \
  /tmp/audit-work/macro-expanded.kore
sha256sum \
  /tmp/audit-work/submitted-expanded.kore \
  /tmp/audit-work/macro-expanded.kore

cp /audit-output/evidence/spec-ground.k \
  /tmp/audit-work/candidate-src/spec-ground.k
timeout 300s kprove \
  /tmp/audit-work/candidate-src/spec-ground.k \
  --definition /tmp/audit-work/verification-fresh-kompiled \
  --spec-module SPEC-GROUND \
  --output pretty
