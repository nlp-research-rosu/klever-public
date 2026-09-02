#!/usr/bin/env bash
set -euo pipefail
set -x

task_dir=/tmp/audit-work/75-is-multiply-prime
extractor=/audit-output/evidence/stage4/extract_embedded_module.py

cd "$task_dir"
python3 "$extractor" verification.k > embedded-module.raw.mpy
python3 "$extractor" --external-program-syntax verification.k > embedded-module.mpy

kast \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore \
  --output-file solution-module.kore \
  solution.regenerated.mpy

kast \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore \
  --output-file embedded-module.kore \
  embedded-module.mpy

sha256sum \
  solution.regenerated.mpy \
  embedded-module.raw.mpy \
  embedded-module.mpy \
  solution-module.kore \
  embedded-module.kore

cmp -s solution-module.kore embedded-module.kore
echo "PARSED_CONSTRUCTOR_KORE_BYTE_IDENTITY=$?"
