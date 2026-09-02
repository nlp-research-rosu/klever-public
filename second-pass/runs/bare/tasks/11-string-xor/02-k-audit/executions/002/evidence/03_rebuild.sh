#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

source_dir=/tmp/audit-work/11-string-xor/source
build_dir=/tmp/audit-work/11-string-xor/build

echo 'COMMAND: bash /audit-output/evidence/03_rebuild.sh'
echo 'TOOLCHAIN:'
kompile --version
kprove --version

mkdir -p "$build_dir"

echo 'COMMAND: kompile semantic.k --main-module XOR --syntax-module MPY-SYNTAX --backend llvm --output-definition /tmp/audit-work/11-string-xor/build/semantic-kompiled'
kompile "$source_dir/semantic.k" \
  --main-module XOR \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "$build_dir/semantic-kompiled"

echo 'COMMAND: kompile verification.k --main-module XOR-VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/11-string-xor/build/verification-kompiled'
kompile "$source_dir/verification.k" \
  --main-module XOR-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$build_dir/verification-kompiled"

cd "$source_dir"

echo 'COMMAND: kprove spec.k --spec-module XOR-SPEC --definition /tmp/audit-work/11-string-xor/build/verification-kompiled --output pretty'
kprove spec.k \
  --spec-module XOR-SPEC \
  --definition "$build_dir/verification-kompiled" \
  --output pretty

echo 'COMMAND: kprove spec-audit-labeled.k --spec-module XOR-SPEC-AUDIT --claims XOR-SPEC-AUDIT.audit-recursive --definition /tmp/audit-work/11-string-xor/build/verification-kompiled --output pretty'
kprove spec-audit-labeled.k \
  --spec-module XOR-SPEC-AUDIT \
  --claims XOR-SPEC-AUDIT.audit-recursive \
  --definition "$build_dir/verification-kompiled" \
  --output pretty

echo 'COMMAND: kprove spec-audit-labeled.k --spec-module XOR-SPEC-AUDIT --definition /tmp/audit-work/11-string-xor/build/verification-kompiled --output pretty'
kprove spec-audit-labeled.k \
  --spec-module XOR-SPEC-AUDIT \
  --definition "$build_dir/verification-kompiled" \
  --output pretty
