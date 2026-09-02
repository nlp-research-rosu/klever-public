#!/usr/bin/env bash
set -euo pipefail

printf '$ verify stage status markers\n'
rg -n 'FINAL_STATUS=0|stage[23456]_[a-z_]*exit=0|stage[23456]_script_exit=0' \
  /audit-output/evidence/provenance_check.log \
  /audit-output/evidence/stage2_program_fidelity.log \
  /audit-output/evidence/stage3_reconstruction.log \
  /audit-output/evidence/stage4_adequacy.log \
  /audit-output/evidence/stage5_inventory.log \
  /audit-output/evidence/stage6_nonvacuity.log
printf '[exit 0]\n'

printf '$ verify four independent positive target logs contain exact #Top\n'
for label in residue-0 residue-1 residue-2 get-max-triples-correct; do
  grep -Fx '#Top' "/audit-output/evidence/kprove-$label.log"
done
printf '[exit 0]\n'

printf '$ verify concrete witness #Top and expected negative probes\n'
grep -Fx '#Top' /audit-output/evidence/kprove-entry-n5.log
rg -n 'WarnStuckClaimState|\\[Error\\] Prover' \
  /audit-output/evidence/kprove-body-mutant.log \
  /audit-output/evidence/kprove-vacuity.log
printf '[exit 0]\n'

printf '$ count indexed K attributes\n'
printf 'function_syntax='
rg '^\s*syntax .*\[.*function' \
  /tmp/audit-work/147-get-max-triples-clean/reference-semantics/semantics/*.k \
  /tmp/audit-work/147-get-max-triples-clean/verification.k | wc -l
printf 'total_syntax='
rg '^\s*syntax .*\[.*total' \
  /tmp/audit-work/147-get-max-triples-clean/reference-semantics/semantics/*.k \
  /tmp/audit-work/147-get-max-triples-clean/verification.k | wc -l
printf 'opaque_no_evaluators='
rg '^\s*syntax .*no-evaluators' \
  /tmp/audit-work/147-get-max-triples-clean/reference-semantics/semantics/*.k \
  /tmp/audit-work/147-get-max-triples-clean/verification.k | wc -l
printf 'priority_attributes='
rg '^\s*\[priority|\[priority\(' \
  /tmp/audit-work/147-get-max-triples-clean/reference-semantics/semantics/*.k \
  /tmp/audit-work/147-get-max-triples-clean/verification.k | wc -l
printf 'owise_attributes='
rg '\[owise\]' \
  /tmp/audit-work/147-get-max-triples-clean/reference-semantics/semantics/*.k \
  /tmp/audit-work/147-get-max-triples-clean/verification.k | wc -l
printf 'concrete_attributes='
rg '\[concrete\]' \
  /tmp/audit-work/147-get-max-triples-clean/reference-semantics/semantics/*.k \
  /tmp/audit-work/147-get-max-triples-clean/verification.k | wc -l
printf 'simplification_attributes='
rg '\[.*simplification' \
  /tmp/audit-work/147-get-max-triples-clean/reference-semantics/semantics/*.k \
  /tmp/audit-work/147-get-max-triples-clean/verification.k | wc -l || true
printf 'functional_attributes='
rg '\[.*functional' \
  /tmp/audit-work/147-get-max-triples-clean/reference-semantics/semantics/*.k \
  /tmp/audit-work/147-get-max-triples-clean/verification.k | wc -l || true
printf '[exit 0]\n'

printf '$ list bounded evidence artifacts\n'
find /audit-output/evidence -maxdepth 1 -type f -printf '%f\t%s bytes\n' | sort
printf '[exit 0]\n'
