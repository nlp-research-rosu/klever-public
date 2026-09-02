#!/usr/bin/env bash
set -uo pipefail
set -x

work=/tmp/audit-work/rebuild
status=0
cd "$work" || exit 1

kompile --version
rc=$?
printf 'kompile_version_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kprove --version
rc=$?
printf 'kprove_version_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

cmp -s reference-semantics/semantics.k /reference/reference-semantics/semantics.k
rc=$?
printf 'scratch_semantics_top_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

diff -qr --no-dereference reference-semantics /reference/reference-semantics
rc=$?
printf 'scratch_semantics_tree_diff_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

python3 /reference/py2mpy.py solution.py > solution.fresh.mpy
rc=$?
printf 'scratch_trusted_translation_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

cmp -s solution.fresh.mpy solution.mpy
rc=$?
printf 'scratch_solution_mpy_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

python3 /reference/py2mpy.py k-concrete-tests.py > k-concrete-tests.mpy
rc=$?
printf 'concrete_test_translation_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
rc=$?
printf 'fresh_llvm_kompile_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

krun k-concrete-tests.mpy --definition audit-runtime-kompiled
rc=$?
printf 'fresh_concrete_krun_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kompile verification.k \
  --backend haskell \
  --main-module GET-ROW-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
rc=$?
printf 'fresh_haskell_kompile_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kprove spec-empty.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-EMPTY-SPEC
rc=$?
printf 'positive_empty_claim_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kprove spec-shape.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SHAPE-SPEC
rc=$?
printf 'positive_shape_claim_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module GET-ROW-SPEC
rc=$?
printf 'positive_combined_candidate_spec_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf 'stage3_rebuild_exit=%d\n' "$status"
exit "$status"
