#!/usr/bin/env bash
set -euo pipefail

fresh=/tmp/audit-work/42-incr-list-audit/fresh-build-003
definition="$fresh/audit-verification-kompiled"
evidence=/audit-output/evidence
dry_root=/tmp/audit-work/42-incr-list-audit/stage4-dry-run-002

if [[ -e "$dry_root" ]]; then
  echo "refusing to reuse stage4 dry-run directory: $dry_root" >&2
  exit 2
fi
mkdir -p "$dry_root"

echo '$ kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.incr-list --dry-run --temp-dir stage4-dry-run'
(
  cd "$fresh"
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.incr-list \
    --dry-run \
    --temp-dir "$dry_root"
)
echo "EXIT_STATUS=0"

echo '$ kast solution.mpy --definition audit-verification-kompiled --module MPY-SYNTAX --sort Module --output kore'
kast "$fresh/solution.mpy" \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore \
  > "$fresh/submitted-program.kore"
echo "EXIT_STATUS=0"

spec_kore=$(find "$dry_root" -type f -name spec.kore -print -quit)
test -n "$spec_kore"
echo '$ python3 stage4_extract_kore_loadall.py stage4-dry-run/.../spec.kore > entry-program.kore'
python3 "$evidence/stage4_extract_kore_loadall.py" "$spec_kore" \
  > "$fresh/entry-program.kore"
echo "EXIT_STATUS=0"

echo '$ cmp -s submitted-program.kore entry-program.kore'
cmp -s "$fresh/submitted-program.kore" "$fresh/entry-program.kore"
echo "constructor_level_program_identity_exit=0"
sha256sum "$fresh/submitted-program.kore" "$fresh/entry-program.kore"

echo '$ python3 /audit-output/evidence/stage4_witness.py'
python3 "$evidence/stage4_witness.py"

echo "STAGE4_PINNING_OK"
