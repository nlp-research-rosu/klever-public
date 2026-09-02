#!/usr/bin/env bash
# Idempotent stage-6 pump: single pass — top up to 6 detached audit launchers
# from the obligation-first todo list, then exit. Safe to re-run anytime.
#
# Path-sanitized copy of the operational script used during the campaign.
# REPO must point at the runnable tree root (src/ in this package, or a
# checkout laid out the same way); RUN is the run id under $REPO/runs/.
# The original consulted a local model-provider quota helper before each
# pass; that helper is omitted here because it requires provider account
# state. Stage-6 audits require a Codex CLI auth.json (see README.md).
set -u
REPO="${REPO:-$(cd "$(dirname "$0")/../src" && pwd)}"
RUN="${RUN:-codex-gpt-5.6-sol-xhigh-kit-semantics-frozen-20260724}"
S="${S:-$(cd "$(dirname "$0")" && pwd)}"
todo=$(REPO="$REPO" RUN="$RUN" python3 - <<'PYEOF'
import json, os
root=os.path.join(os.environ['REPO'],'runs',os.environ['RUN'],'tasks')
ob=[]; mech=[]
for td in sorted(os.listdir(root), key=lambda s:int(s.split('-')[0])):
    s4=os.path.join(root,td,'04-klean-generation','selected.json')
    if not os.path.exists(s4): continue
    st4=json.load(open(s4)).get('status')
    if st4 not in ('PASS','KLEAN_NO_OBLIGATIONS'): continue
    s6=os.path.join(root,td,'06-lean-audit','selected.json')
    if os.path.exists(s6) and json.load(open(s6)).get('status') in ('PASS','FAIL','CONCERNS'): continue
    (ob if st4=='PASS' else mech).append(td)
for t in ob+mech: print(t)
PYEOF
)
n=$(echo "$todo" | grep -c . || true)
echo "pump: $n tasks remaining"
launched=0
for t in $todo; do
  grep -qx "$t" "$S/s6-skip.list" 2>/dev/null && continue
  [ "$(pgrep -fc "klean-audit/run_task.sh")" -ge 12 ] && break
  pgrep -f "klean-audit/run_task.sh.*$RUN $t" >/dev/null && continue
  setsid bash "$REPO/docker/klean-audit/run_task.sh" "$RUN" "$t" > "$S/s6-$t.log" 2>&1 &
  launched=$((launched+1)); echo "pumped: $t"
  sleep 3
done
echo "pump done: launched $launched, active $(pgrep -fc 'klean-audit/run_task.sh')"
