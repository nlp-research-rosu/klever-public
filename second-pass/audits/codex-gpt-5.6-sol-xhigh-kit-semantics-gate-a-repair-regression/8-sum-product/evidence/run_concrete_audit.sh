#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction
LOG=/audit-output/evidence/logs/concrete_krun.log
FULL="$SCRATCH/concrete_krun.full.log"
export PATH="/home/agent/.nix-profile/bin:$PATH"

cp /audit-output/evidence/k_concrete_audit.py "$SCRATCH/k_concrete_audit.py"
printf '%s\n' '$ python3 py2mpy.py k_concrete_audit.py > k_concrete_audit.mpy' > "$LOG"
(
  cd "$SCRATCH" || exit 1
  python3 py2mpy.py k_concrete_audit.py > k_concrete_audit.mpy
)
status=$?
printf '[exit %d]\n' "$status" >> "$LOG"
if [ "$status" -ne 0 ]; then
  sed -n '1,200p' "$LOG"
  exit "$status"
fi

cp "$SCRATCH/k_concrete_audit.mpy" \
  /audit-output/evidence/inputs/k_concrete_audit.mpy
printf '%s\n' '$ krun k_concrete_audit.mpy --definition audit-runtime-kompiled' >> "$LOG"
(
  cd "$SCRATCH" || exit 1
  krun k_concrete_audit.mpy --definition audit-runtime-kompiled
) > "$FULL" 2>&1
status=$?
lines=$(wc -l < "$FULL")
{
  printf '[exit %d; output lines %d]\n' "$status" "$lines"
  if [ "$lines" -le 200 ]; then
    sed -n '1,200p' "$FULL"
  else
    sed -n '1,100p' "$FULL"
    printf '[... %d middle lines omitted ...]\n' "$((lines - 200))"
    tail -n 100 "$FULL"
  fi
} >> "$LOG"
sed -n '1,220p' "$LOG"
exit "$status"
