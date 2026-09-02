#!/usr/bin/env bash
set -u

echo '== Candidate inventory (physical walk; symlinks shown) =='
find -P /candidate -printf '%y %m %p -> %l\n' | sort

echo '== Trusted input inventory (physical walk; symlinks shown) =='
find -P /reference -printf '%y %m %p -> %l\n' | sort

echo '== Required generation-accounting artifacts =='
for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "/candidate/$artifact" || -L "/candidate/$artifact" ]]; then
    stat --printf='%F %s bytes %n\n' "/candidate/$artifact"
  else
    echo "MISSING /candidate/$artifact"
  fi
done

trace_count=$(find -P /candidate -maxdepth 2 -type f \
  \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*trace*.log' \) \
  -print | sort | tee /dev/stderr | wc -l)
echo "STRUCTURED_TRACE_CANDIDATE_COUNT=$trace_count"

echo '== Candidate required source object types =='
for artifact in prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k reference-semantics; do
  if [[ -e "/candidate/$artifact" || -L "/candidate/$artifact" ]]; then
    stat --printf='%F %s bytes %n\n' "/candidate/$artifact"
  else
    echo "MISSING /candidate/$artifact"
  fi
done

echo '== Byte comparisons =='
cmp -s /reference/prompt.py /candidate/prompt.py
echo "PROMPT_CMP_STATUS=$?"
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
echo "TRANSLATOR_CMP_STATUS=$?"
diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics
echo "SEMANTICS_DIFF_STATUS=$?"

echo '== SHA-256 checksums of trusted and candidate source inputs =='
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k

echo '== K toolchain =='
command -v kompile
command -v kprove
command -v krun
kompile --version
kprove --version
krun --version
