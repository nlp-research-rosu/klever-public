#!/usr/bin/env bash
# Detached stage-6 pump daemon: re-runs s6pump.sh every 4 minutes until the
# queue empties and no audit is running. Log: /tmp/s6daemon.log.
# Kill: pkill -f s6daemon.sh
#
# Path-sanitized copy of the operational script used during the campaign.
HERE="$(cd "$(dirname "$0")" && pwd)"
while :; do
  bash "$HERE/s6pump.sh" >> /tmp/s6daemon.log 2>&1
  # stop condition: nothing left to pump and nothing running
  n=$(tail -5 /tmp/s6daemon.log | grep -o '[0-9]* tasks remaining' | tail -1 | cut -d' ' -f1)
  if [ "${n:-1}" = "0" ] && [ "$(pgrep -fc 'klean-audit/run_task.sh')" -le 1 ]; then
    echo "QUEUE EMPTY — daemon exiting" >> /tmp/s6daemon.log; exit 0
  fi
  sleep 240
done
