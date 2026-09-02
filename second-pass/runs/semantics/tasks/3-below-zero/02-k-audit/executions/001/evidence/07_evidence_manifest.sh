#!/usr/bin/env bash
set -u

log=/audit-output/evidence/07_evidence_manifest.log
exec > >(tee "$log") 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    exit "$status"
  fi
}

run cmp --silent \
  /audit-output/evidence/audit-concrete.py \
  /tmp/audit-work/rebuild/candidate/audit-concrete.py
run cmp --silent \
  /audit-output/evidence/spec-body-sensitivity.k \
  /tmp/audit-work/rebuild/candidate/spec-body-sensitivity.k
run cmp --silent \
  /audit-output/evidence/spec-context-sensitivity-base.k \
  /tmp/audit-work/rebuild/candidate/spec-context-sensitivity.k
run cmp --silent \
  /audit-output/evidence/spec-context-sensitivity-lemma.k \
  /tmp/audit-work/rebuild/candidate/spec-context-sensitivity-lemma.k
run cmp --silent \
  /audit-output/evidence/spec-vacuity.k \
  /tmp/audit-work/rebuild/candidate/spec-vacuity.k

printf '\n$ find /audit-output/evidence -maxdepth 1 -type f ! -name 07_evidence_manifest.log -print0 | sort -z | xargs -0 sha256sum\n'
find /audit-output/evidence -maxdepth 1 -type f \
  ! -name 07_evidence_manifest.log -print0 | sort -z | xargs -0 sha256sum
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
