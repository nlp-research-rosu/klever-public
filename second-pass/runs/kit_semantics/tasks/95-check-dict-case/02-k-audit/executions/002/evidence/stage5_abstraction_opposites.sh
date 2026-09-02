#!/usr/bin/env bash
set -u

audit_src=/tmp/audit-work/case95/candidate-src
export PATH="$HOME/.nix-profile/bin:$PATH"

cases=(
  "stage5_abstraction_opposite_lower_string.k:AUDIT-ABSTRACTION-OPPOSITE-LOWER-STRING"
  "stage5_abstraction_opposite_nonstring.k:AUDIT-ABSTRACTION-OPPOSITE-NONSTRING"
  "stage5_abstraction_opposite_codes.k:AUDIT-ABSTRACTION-OPPOSITE-CODES"
)

unexpected=0
for item in "${cases[@]}"; do
  filename=${item%%:*}
  module=${item#*:}
  cp "/audit-output/evidence/$filename" "$audit_src/$filename"
  set +e
  kprove \
    "$filename" \
    --definition audit-verification-kompiled \
    --spec-module "$module"
  proof_exit=$?
  set -e
  printf 'OPPOSITE_INTERPRETATION file=%s exit=%s\n' "$filename" "$proof_exit"
  if [[ "$proof_exit" -eq 0 ]]; then
    unexpected=1
  fi
done

exit "$unexpected"
