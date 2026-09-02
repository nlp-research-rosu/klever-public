#!/usr/bin/env bash
set -u

echo 'COMMAND: bash /audit-output/evidence/audit_stage1.sh'
echo 'CHECK: trusted-mode mount'
if [[ -d /reference/reference-semantics ]]; then
  echo 'REFERENCE_SEMANTICS_PRESENT=yes'
else
  echo 'REFERENCE_SEMANTICS_PRESENT=no'
fi

echo 'CHECK: required candidate artifact types'
required=(
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  spec.k
  verification.k
)
for name in "${required[@]}"; do
  path="/candidate/$name"
  if [[ -f "$path" && ! -L "$path" ]]; then
    echo "$name=regular-file"
  elif [[ -L "$path" ]]; then
    echo "$name=symlink"
  elif [[ -e "$path" ]]; then
    echo "$name=wrong-type"
  else
    echo "$name=missing"
  fi
done

echo 'CHECK: named generation records (untrusted when present)'
records=(run-input.json metrics.json codex-last.txt codex-output.log)
for name in "${records[@]}"; do
  path="/candidate/$name"
  if [[ -f "$path" && ! -L "$path" ]]; then
    echo "$name=regular-file"
    sha256sum "$path"
  elif [[ -L "$path" ]]; then
    echo "$name=symlink"
  elif [[ -e "$path" ]]; then
    echo "$name=wrong-type"
  else
    echo "$name=missing"
  fi
done

echo 'CHECK: possible structured generation traces'
find /candidate -maxdepth 1 \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*generation*.json' -o -iname '*generation*.jsonl' \) \
  -printf '%y %p -> %l\n' | sort

echo 'CHECK: all candidate symlinks'
symlink_count="$(find /candidate -type l -print | wc -l)"
echo "CANDIDATE_SYMLINK_COUNT=$symlink_count"
find /candidate -type l -printf '%p -> %l\n' | sort

echo 'CHECK: prompt byte identity'
cmp -s /reference/prompt.py /candidate/prompt.py
prompt_status=$?
echo "PROMPT_CMP_EXIT=$prompt_status"

echo 'CHECK: translator byte identity'
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
echo "TRANSLATOR_CMP_EXIT=$translator_status"

echo 'CHECK: supplied semantics recursive identity'
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
semantics_status=$?
echo "SEMANTICS_DIFF_EXIT=$semantics_status"

echo 'CHECK: submitted and trusted hashes'
sha256sum \
  /reference/prompt.py \
  /candidate/prompt.py \
  /reference/py2mpy.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k

if (( prompt_status != 0 || translator_status != 0 || semantics_status != 0 )); then
  echo 'EXIT_STATUS=1'
  exit 1
fi
echo 'EXIT_STATUS=0'
