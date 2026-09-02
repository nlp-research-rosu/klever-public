#!/usr/bin/env bash
set -u

echo "== trusted mount mode check =="
test -d /reference/reference-semantics
echo "trusted_reference_semantics_present=$?"

echo "== required candidate artifacts =="
for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log prompt.py py2mpy.py \
  solution.py solution.mpy spec.k verification.k reference-semantics
do
  if [[ -e "/candidate/$artifact" ]]; then
    stat -c '%F %n' "/candidate/$artifact"
  else
    echo "MISSING /candidate/$artifact"
  fi
done

echo "== symlinks in candidate source/provenance tree =="
find /candidate \
  \( -path /candidate/runtime-kompiled -o -path /candidate/verification-kompiled \
     -o -path /candidate/__pycache__ \) -prune \
  -o -type l -printf '%p -> %l\n' | sort

echo "== prompt identity =="
cmp -s /candidate/prompt.py /reference/prompt.py
echo "prompt_cmp_status=$?"
sha256sum /candidate/prompt.py /reference/prompt.py

echo "== translator identity =="
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
echo "translator_cmp_status=$?"
sha256sum /candidate/py2mpy.py /reference/py2mpy.py

echo "== supplied semantics recursive type/path/content comparison =="
(
  cd /candidate/reference-semantics &&
  find . -printf '%P\t%y\t%s\t%l\n' | LC_ALL=C sort
) > /tmp/audit-work/candidate-semantics-manifest.txt
(
  cd /reference/reference-semantics &&
  find . -printf '%P\t%y\t%s\t%l\n' | LC_ALL=C sort
) > /tmp/audit-work/trusted-semantics-manifest.txt
diff -u /tmp/audit-work/trusted-semantics-manifest.txt \
        /tmp/audit-work/candidate-semantics-manifest.txt
echo "semantics_manifest_diff_status=$?"
diff -r --no-dereference /reference/reference-semantics \
                         /candidate/reference-semantics
echo "semantics_recursive_diff_status=$?"

echo "== candidate source hashes (compiled outputs excluded) =="
find /candidate \
  \( -path /candidate/runtime-kompiled -o -path /candidate/verification-kompiled \
     -o -path /candidate/__pycache__ -o -path /candidate/codex-trace \) -prune \
  -o -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
