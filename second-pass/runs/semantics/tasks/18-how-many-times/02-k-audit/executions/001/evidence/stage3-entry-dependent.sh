#!/usr/bin/env bash
set -u
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
work=/tmp/audit-work/fresh

# The helper was independently proved in stage3-reconstruct.log.  Here it is
# available as a trusted lemma solely to isolate the dependent entry target.
timeout 180 kprove /audit-output/evidence/spec-labeled.k \
  --definition "$work/verification-kompiled" \
  --spec-module HOW-MANY-TIMES-SPEC-AUDIT \
  --claims HOW-MANY-TIMES-SPEC-AUDIT.overlap-acc,HOW-MANY-TIMES-SPEC-AUDIT.entry \
  --trusted HOW-MANY-TIMES-SPEC-AUDIT.overlap-acc
entry_rc=$?
echo "ENTRY_WITH_PROVED_HELPER_EXIT=$entry_rc"
exit "$entry_rc"
