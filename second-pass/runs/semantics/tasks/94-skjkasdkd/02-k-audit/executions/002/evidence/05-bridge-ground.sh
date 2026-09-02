#!/usr/bin/env bash
set -u

evidence=/audit-output/evidence
overall=0

{
  echo "COMMAND: compile immutable proof theory with entry bridge removed"
  kompile verification-no-entry-bridge.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module VERIFICATION \
    --output-definition bridge-free-kompiled \
    -I .
  rc=$?
  echo "EXIT_STATUS=$rc"
} > "$evidence/05-bridge-free-kompile.log" 2>&1
echo "kompile_exit=$rc"
(( rc == 0 )) || overall=1

for label in one-is-not-prime smallest-prime two-digit-prime; do
  log="$evidence/05-bridge-free-$label.log"
  {
    echo "COMMAND: kprove bridge-free-ground.k label $label"
    kprove bridge-free-ground.k \
      --definition bridge-free-kompiled \
      --spec-module BRIDGE-FREE-GROUND \
      --claims "BRIDGE-FREE-GROUND.$label" \
      --output pretty
    rc=$?
    echo "EXIT_STATUS=$rc"
  } > "$log" 2>&1
  echo "$label exit=$rc"
  if (( rc != 0 )) || ! grep -Fxq '#Top' "$log"; then
    overall=1
  fi
done

echo "FINAL_STATUS=$overall"
exit "$overall"
