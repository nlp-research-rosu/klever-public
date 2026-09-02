#!/usr/bin/env bash
set -u

failures=0

cmp /candidate/prompt.py /reference/prompt.py
status=$?
echo "PROMPT_CMP_EXIT=$status"
(( failures += status != 0 ))

cmp /candidate/py2mpy.py /reference/py2mpy.py
status=$?
echo "TRANSLATOR_CMP_EXIT=$status"
(( failures += status != 0 ))

diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
status=$?
echo "SEMANTICS_TREE_DIFF_EXIT=$status"
(( failures += status != 0 ))

candidate_manifest=$(mktemp)
trusted_manifest=$(mktemp)
find /candidate/reference-semantics -mindepth 1 -printf '%P\t%y\t%l\n' \
  | LC_ALL=C sort > "$candidate_manifest"
find /reference/reference-semantics -mindepth 1 -printf '%P\t%y\t%l\n' \
  | LC_ALL=C sort > "$trusted_manifest"
diff -u "$trusted_manifest" "$candidate_manifest"
status=$?
echo "SEMANTICS_TYPE_MANIFEST_DIFF_EXIT=$status"
(( failures += status != 0 ))

sha256sum /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py

echo "INTEGRITY_FAILURE_COUNT=$failures"
exit "$failures"
