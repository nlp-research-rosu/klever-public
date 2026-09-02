#!/usr/bin/env bash
set -u

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return 0
}

run bash -n \
  /audit-output/evidence/01_integrity.sh \
  /audit-output/evidence/02_program_fidelity.sh \
  /audit-output/evidence/03_reconstruct.sh \
  /audit-output/evidence/04_static_inventory.sh \
  /audit-output/evidence/04a_program_term_identity.sh \
  /audit-output/evidence/05_bridge_witness.sh \
  /audit-output/evidence/05a_bridge_connection.sh \
  /audit-output/evidence/06_nonvacuity.sh \
  /audit-output/evidence/07_final_checks.sh

run python3 -c 'import ast, pathlib; [ast.parse(pathlib.Path(p).read_text(), p) for p in ["/audit-output/evidence/differential.py", "/audit-output/evidence/k_inventory.py", "/audit-output/evidence/concrete-audit.py"]]'

run tail -n 2 /audit-output/REVIEW.md
run sh -c 'test "$(grep -c "^VERDICT:" /audit-output/REVIEW.md)" -eq 1 && test "$(grep -c "^LEGITIMACY:" /audit-output/REVIEW.md)" -eq 1'

printf '\nCOMMAND: find /audit-output/evidence -type f ! -name 07_final_checks.log -print0 | sort -z | xargs -0 sha256sum; sha256sum /audit-output/REVIEW.md\n'
find /audit-output/evidence -type f ! -name 07_final_checks.log -print0 \
  | sort -z | xargs -0 sha256sum
sha256sum /audit-output/REVIEW.md
printf 'EXIT_STATUS: %d\n' "$?"
