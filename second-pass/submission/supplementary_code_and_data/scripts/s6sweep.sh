#!/usr/bin/env bash
# Idempotent replace-selected sweep: tops up to 3 re-audits of remediated
# tasks (fresh stage-5 SUCCEEDED, old stage-6 selection stale). One launch
# per task ever, tracked in a local state directory.
#
# Path-sanitized copy of the operational script used during the campaign.
# Set LIST to the space-separated task ids to re-audit.
set -u
REPO="${REPO:-$(cd "$(dirname "$0")/../src" && pwd)}"
RUN="${RUN:-codex-gpt-5.6-sol-xhigh-kit-semantics-frozen-20260724}"
STATE="${STATE:-$(cd "$(dirname "$0")" && pwd)/s6sweep-launched}"
LIST="${LIST:-}"
mkdir -p "$STATE"
active=$(pgrep -fc 'run_task.sh --replace-selected' 2>/dev/null); active=${active:-0}
for t in $LIST; do
  [ "$active" -ge 3 ] && break
  [ -e "$STATE/$t" ] && continue
  status=$(python3 -c "import json;print(json.load(open('$REPO/runs/$RUN/tasks/$t/05-lean-proof/result.json')).get('status'))" 2>/dev/null)
  [ "$status" = "SUCCEEDED" ] || continue
  touch "$STATE/$t"
  setsid bash "$REPO/docker/klean-audit/run_task.sh" --replace-selected "$RUN" "$t" >> "$STATE/$t.log" 2>&1 < /dev/null &
  echo "sweep launched: $t"
  active=$((active+1))
done
echo "sweep pass: active=$active"
