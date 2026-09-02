#!/usr/bin/env bash
set -euo pipefail

work_dir=/tmp/audit-work/reconstruction

kompile --backend haskell "$work_dir/verification.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work_dir/verification-kompiled"
