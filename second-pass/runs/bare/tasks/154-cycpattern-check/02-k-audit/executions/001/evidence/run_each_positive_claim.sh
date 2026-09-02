#!/usr/bin/env bash
set -u

workdir=/tmp/audit-work/154-cycpattern-check/reconstructed
definition=verification-fresh-kompiled
spec=spec-labeled.k
module=SPEC-LABELED

labels=(
  example-abcd-abd
  example-hello-ell
  example-whassup-psus
  example-abab-baa
  example-efef-eeff
  example-himenss-simen
  boundary-unrotated
  boundary-one-character
  boundary-empty-ground
  boundary-empty-symbolic
  loop-invariant
  whole-program
)

cd "$workdir"
overall_status=0
for label in "${labels[@]}"; do
  if [[ "$label" == "loop-invariant" ]]; then
    selector='SPEC-LABELED.label(loop-invariant)'
  else
    selector="SPEC-LABELED.label(loop-invariant),SPEC-LABELED.label(${label})"
  fi
  printf 'TARGET_CLAIM: %s\n' "$label"
  printf 'COMMAND: kprove --claims %q %q --definition %q --spec-module %q\n' \
    "$selector" "$spec" "$definition" "$module"
  set +e
  kprove --claims "$selector" "$spec" \
    --definition "$definition" --spec-module "$module"
  command_status=$?
  set -e
  printf 'EXIT_STATUS: %d\n' "$command_status"
  if (( command_status != 0 )); then
    overall_status=$command_status
  fi
done

exit "$overall_status"
