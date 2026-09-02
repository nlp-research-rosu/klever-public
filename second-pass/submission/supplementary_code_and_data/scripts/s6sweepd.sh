#!/usr/bin/env bash
# Detached sweep daemon: run the replace-selected sweep every 4 minutes until
# every listed task has been launched and none is active.
# Log: /tmp/s6sweepd.log
#
# Path-sanitized copy of the operational script used during the campaign.
# LIST_COUNT must match the number of tasks in s6sweep.sh's LIST.
HERE="$(cd "$(dirname "$0")" && pwd)"
LIST_COUNT="${LIST_COUNT:-0}"
while :; do
  bash "$HERE/s6sweep.sh" >> /tmp/s6sweepd.log 2>&1
  launched=$(ls "$HERE/s6sweep-launched" 2>/dev/null | grep -vc '\.log$')
  active=$(pgrep -fc 'run_task.sh --replace-selected'); active=${active:-0}
  if [ "$launched" -ge "$LIST_COUNT" ] && [ "$active" -eq 0 ]; then
    echo "SWEEP COMPLETE — daemon exiting" >> /tmp/s6sweepd.log; exit 0
  fi
  sleep 240
done
