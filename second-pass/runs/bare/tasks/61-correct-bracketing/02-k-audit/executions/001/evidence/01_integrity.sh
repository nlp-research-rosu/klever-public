#!/usr/bin/env bash
set -u

candidate_required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
)

echo "MODE_CHECK"
if [ -e /reference/reference-semantics ] || [ -L /reference/reference-semantics ]; then
  stat -c '%F %N' /reference/reference-semantics
  echo "ERROR: generated-semantics mode contradicts trusted mount"
else
  echo "/reference/reference-semantics: absent (required)"
fi

echo "REQUIRED_CANDIDATE_ARTIFACTS"
for artifact_name in "${candidate_required[@]}"; do
  artifact_path="/candidate/${artifact_name}"
  if [ -L "$artifact_path" ]; then
    echo "SYMLINK $artifact_path -> $(readlink "$artifact_path")"
  elif [ -f "$artifact_path" ]; then
    stat -c 'REGULAR %n size=%s mode=%a' "$artifact_path"
  elif [ -e "$artifact_path" ]; then
    stat -c 'MISTYPED %F %N' "$artifact_path"
  else
    echo "MISSING $artifact_path"
  fi
done

echo "STRUCTURED_TRACE"
find /candidate/codex-trace -type l -printf 'SYMLINK %p -> %l\n' 2>/dev/null
find /candidate/codex-trace -type f -printf 'REGULAR %p size=%s\n' 2>/dev/null | sort

echo "TOP_LEVEL_INVENTORY"
find /candidate -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

echo "ALL_CANDIDATE_SYMLINKS"
candidate_symlinks=$(find /candidate -type l -printf '%p -> %l\n')
if [ -n "$candidate_symlinks" ]; then
  printf '%s\n' "$candidate_symlinks"
else
  echo "none"
fi

echo "TRUSTED_REFERENCE_INVENTORY"
find /reference -mindepth 1 -maxdepth 2 -printf '%y %p -> %l\n' | sort

echo "TRUSTED_IDENTITY"
sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py
cmp /candidate/prompt.py /reference/prompt.py
echo "prompt_cmp_status=$?"
cmp /candidate/py2mpy.py /reference/py2mpy.py
echo "translator_cmp_status=$?"

echo "SOURCE_HASHES"
sha256sum \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k \
  /reference/canonical.py

echo "UNTRUSTED_RUN_CLAIMS"
sed -n '1,220p' /candidate/run-input.json
sed -n '1,220p' /candidate/metrics.json
sed -n '1,220p' /candidate/codex-last.txt

trace_file=$(find /candidate/codex-trace -type f -name '*.jsonl' -print -quit)
if [ -n "$trace_file" ]; then
  echo "TRACE_EVENT_COUNTS"
  jq -r '.type' "$trace_file" | sort | uniq -c
  echo "TRACE_FINAL_MESSAGES"
  jq -r 'select(.type == "event_msg" and (.payload.type == "agent_message" or .payload.type == "task_complete")) | (.payload.message // .payload.last_agent_message)' "$trace_file"
fi

echo "GENERATION_LOG_PROOF_CLAIMS"
rg -n 'RESULT:|successfully replayed|printed `#Top`|WarnStuckClaimState|kprove spec.k' \
  /candidate/codex-output.log | tail -n 80
