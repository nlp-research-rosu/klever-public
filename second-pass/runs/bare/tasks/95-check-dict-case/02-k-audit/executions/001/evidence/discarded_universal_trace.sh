#!/usr/bin/env bash
set -u

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-13-56-019f8988-436f-7ea3-adee-6619f939ad16.jsonl

echo "UNTRUSTED structured trace excerpts: symbolic claim, result, deletion"
sed -n '148p;150p;151p;152p;157p' "$trace"
