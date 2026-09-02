#!/usr/bin/env bash
set -u
set -x

mkdir -p /tmp/audit-work/reconstruction
mkdir_rc=$?

cp \
  /candidate/prompt.py \
  /candidate/prove.sh \
  /candidate/semantic.k \
  /candidate/solution.mpy \
  /candidate/solution.py \
  /candidate/spec.k \
  /candidate/verification.k \
  /tmp/audit-work/reconstruction/
copy_candidate_rc=$?

cp /reference/py2mpy.py /tmp/audit-work/reconstruction/py2mpy.py
copy_translator_rc=$?

python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
regen_rc=$?

cmp -s \
  /tmp/audit-work/reconstruction/solution.regenerated.mpy \
  /tmp/audit-work/reconstruction/solution.mpy
cmp_rc=$?

sha256sum \
  /tmp/audit-work/reconstruction/solution.regenerated.mpy \
  /tmp/audit-work/reconstruction/solution.mpy
sha_rc=$?

python3 /audit-output/evidence/differential_test.py
diff_rc=$?

set +x
printf 'mkdir_exit=%d\n' "$mkdir_rc"
printf 'copy_candidate_exit=%d\n' "$copy_candidate_rc"
printf 'copy_translator_exit=%d\n' "$copy_translator_rc"
printf 'regeneration_exit=%d\n' "$regen_rc"
printf 'byte_identity_cmp_exit=%d\n' "$cmp_rc"
printf 'sha256sum_exit=%d\n' "$sha_rc"
printf 'differential_exit=%d\n' "$diff_rc"
test "$mkdir_rc" -eq 0 \
  && test "$copy_candidate_rc" -eq 0 \
  && test "$copy_translator_rc" -eq 0 \
  && test "$regen_rc" -eq 0 \
  && test "$cmp_rc" -eq 0 \
  && test "$sha_rc" -eq 0 \
  && test "$diff_rc" -eq 0
