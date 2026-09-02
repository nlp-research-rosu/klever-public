#!/usr/bin/env bash
set -u
set -x

cd /tmp/audit-work/reconstruction || exit 90

cp \
  /audit-output/evidence/pinning-spec.k \
  /audit-output/evidence/body-mutation.k \
  /audit-output/evidence/body-mutation-spec.k \
  /audit-output/evidence/adequacy-probe.k \
  .
copy_rc=$?

kprove pinning-spec.k \
  --definition verification-kompiled \
  --spec-module PINNING-SPEC
pinning_rc=$?

kompile body-mutation.k \
  --backend haskell \
  --main-module BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutation-kompiled
mutation_build_rc=$?

kprove body-mutation-spec.k \
  --definition body-mutation-kompiled \
  --spec-module BODY-MUTATION-SPEC
body_mutation_proof_rc=$?

kprove adequacy-probe.k \
  --definition verification-kompiled \
  --spec-module ADEQUACY-PROBE
adequacy_probe_rc=$?

python3 -c 'import solution; witnesses=[[],[0],[1,0],[1,11,-1,-11,-12],[12,21,-12,3]]; [print(f"witness={x!r} output={solution.order_by_points(x)!r}") for x in witnesses]; print("insert_le_witness N=0 M=0 scores=0<=0"); print("insert_gt_witness N=1 M=0 scores=1>0")'
witness_rc=$?

set +x
printf 'copy_exit=%d\n' "$copy_rc"
printf 'pinning_exit=%d\n' "$pinning_rc"
printf 'body_mutation_build_exit=%d\n' "$mutation_build_rc"
printf 'body_mutation_proof_exit=%d expected_nonzero=1\n' "$body_mutation_proof_rc"
printf 'adequacy_probe_exit=%d expected_nonzero=1\n' "$adequacy_probe_rc"
printf 'witness_exit=%d\n' "$witness_rc"

test "$copy_rc" -eq 0 \
  && test "$pinning_rc" -eq 0 \
  && test "$mutation_build_rc" -eq 0 \
  && test "$body_mutation_proof_rc" -ne 0 \
  && test "$adequacy_probe_rc" -ne 0 \
  && test "$witness_rc" -eq 0
