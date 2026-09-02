#!/usr/bin/env bash
# babysit.sh — keep the claude matrix running across 5-hour subscription
# windows until every claude-code-* task is done.
#
# Loop: reset session-limit-failed task folders, check the OAuth usage endpoint,
# sleep until the window resets if needed, re-seed the token, then start one
# Claude matrix in the background and supervise that exact PID. If a task hits
# the session limit, stop only that matrix's xargs spawner so unrelated Codex or
# OpenCode matrices cannot be mistaken for this one.
# Exits when all claude tasks have metrics (or a weekly limit is exhausted).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
JOBS="${JOBS:-4}"
BABYSIT_POLL_SECONDS="${BABYSIT_POLL_SECONDS:-5}"
LIMIT_STOP_RC=75
# Restrict which claude configs to drive, e.g. CONFIG_GLOB="claude-code-opus-*"
CONFIG_GLOB="${CONFIG_GLOB:-claude-code-*}"

log() { echo "[$(date '+%m-%d %H:%M:%S')] $*"; }

# Prints one line: GO | WAIT <seconds> | STOP <reason...>
usage_decision() {
  python3 - <<'PY'
import json, subprocess, sys, datetime
try:
    tok = json.load(open('/home/yuqing/.claude/.credentials.json'))['claudeAiOauth']['accessToken']
    out = subprocess.run(['curl','-s','-m','20','https://api.anthropic.com/api/oauth/usage',
                          '-H',f'Authorization: Bearer {tok}',
                          '-H','anthropic-beta: oauth-2025-04-20'],
                         capture_output=True, text=True, timeout=30).stdout
    d = json.loads(out)
except Exception as e:
    print('WAIT 600'); sys.exit()          # endpoint unreachable -> retry later
if 'five_hour' not in d:
    # 401/error body -> the token is dead; firing would churn auth failures.
    print('STOP host auth is dead (usage endpoint rejected the token) — run `claude auth login`, then restart babysit.sh')
    sys.exit()
now = datetime.datetime.now(datetime.timezone.utc)
def until(iso):
    t = datetime.datetime.fromisoformat(iso)
    return max(60, int((t - now).total_seconds()) + 180)
# NOTE: is_active on weekly_scoped means "this limit applies", not "blocked"
# (observed True at 41% with severity normal) — so gate on percent only.
for lim in d.get('limits', []):
    if lim.get('group') == 'weekly' and lim.get('percent', 0) >= 100:
        print('STOP weekly limit exhausted:', lim.get('kind'), f"{lim.get('percent')}%",
              'resets', lim.get('resets_at')); sys.exit()
fh = d.get('five_hour', {})
sess_active = any(l.get('kind')=='session' and l.get('is_active') for l in d.get('limits', []))
if sess_active or (fh.get('utilization') or 0) >= 97:
    print('WAIT', until(fh['resets_at'])); sys.exit()
print('GO')
PY
}

limit_failure_present() {
  for m in "$REPO"/runs/$CONFIG_GLOB/*/metrics.json; do
    [[ -f "$m" ]] || continue
    python3 -c "
import json, os
d = json.load(open('$m'))
if d.get('exit_code', 0) == 0: raise SystemExit(1)
co = os.path.join(os.path.dirname('$m'), 'claude-output.json')
txt = ''
try: txt = json.load(open(co)).get('result') or ''
except Exception: pass
bad = ('session limit' in txt) or ('Failed to authenticate' in txt) or ('Not logged in' in txt)
raise SystemExit(0 if bad else 1)" 2>/dev/null && return 0
  done
  return 1
}

refresh_credentials() {
  cp ~/.claude/.credentials.json "$HERE/secrets/claude/.credentials.json" 2>/dev/null \
    && chmod 600 "$HERE/secrets/claude/.credentials.json"
}

# Stop only the xargs process directly owned by the matrix we started. The
# matrix then finishes its summary and returns nonzero; no process-name search
# can match an unrelated harness.
stop_matrix_spawner() {
  local matrix_pid="$1" child command found=1
  while read -r child; do
    [[ -n "$child" ]] || continue
    command="$(ps -o comm= -p "$child" 2>/dev/null || true)"
    if [[ "$command" == "xargs" ]]; then
      if kill "$child" 2>/dev/null; then
        log "session limit detected — stopped matrix $matrix_pid spawner $child"
        found=0
      fi
    fi
  done < <(pgrep -P "$matrix_pid" 2>/dev/null || true)
  return "$found"
}

# Run a matrix concurrently with this monitor and return its exact status. A
# deliberate session-limit stop uses LIMIT_STOP_RC so main can wait for the
# subscription window and retry; all other failures propagate to the caller.
supervise_matrix() {
  local matrix_pid matrix_rc=0 limit_stopped=0
  "$@" &
  matrix_pid=$!
  while kill -0 "$matrix_pid" 2>/dev/null; do
    if [[ $limit_stopped -eq 0 ]] && limit_failure_present; then
      if stop_matrix_spawner "$matrix_pid"; then
        limit_stopped=1
      fi
    fi
    sleep "$BABYSIT_POLL_SECONDS"
  done
  wait "$matrix_pid" || matrix_rc=$?
  if [[ $limit_stopped -eq 1 ]] || limit_failure_present; then
    return "$LIMIT_STOP_RC"
  fi
  return "$matrix_rc"
}

reset_limit_failures() {
  local n=0
  for m in "$REPO"/runs/$CONFIG_GLOB/*/metrics.json; do
    [[ -f "$m" ]] || continue
    if python3 -c "
import json, os
d = json.load(open('$m'))
if d.get('exit_code', 0) == 0: raise SystemExit(1)
co = os.path.join(os.path.dirname('$m'), 'claude-output.json')
txt = ''
try: txt = json.load(open(co)).get('result') or ''
except Exception: pass
bad = ('session limit' in txt) or ('Failed to authenticate' in txt) or ('Not logged in' in txt)
raise SystemExit(0 if bad else 1)" 2>/dev/null; then
      d="$(dirname "$m")"
      find "$d" -mindepth 1 -maxdepth 1 ! -name prompt.py ! -name py2mpy.py \
           ! -name run-input.json ! -name reference-semantics -exec rm -rf {} +
      n=$((n+1))
    fi
  done
  log "reset $n session-limit-failed task folder(s)"
}

remaining_tasks() {
  local n=0
  for d in "$REPO"/runs/$CONFIG_GLOB/*/; do
    [[ -f "$d/metrics.json" ]] || n=$((n+1))
  done
  echo "$n"
}

main() {
  local REM DECISION SECS cd_ matrix_rc
  local -a CFG_ARGS=()
  log "babysitter started (jobs=$JOBS)"
  while true; do
    reset_limit_failures
    REM=$(remaining_tasks)
    if [[ "$REM" -eq 0 ]]; then
      log "ALL CLAUDE TASKS COMPLETE"
      return 0
    fi

    DECISION=$(usage_decision)
    case "$DECISION" in
      GO)
        log "$REM task(s) remaining, window open — firing run_matrix --jobs $JOBS"
        if ! refresh_credentials; then
          log "could not refresh Claude credentials; refusing to launch"
          return 2
        fi
        CFG_ARGS=()
        for cd_ in "$REPO"/runs/$CONFIG_GLOB/; do
          [[ -d "$cd_" && ! -L "$cd_" ]] \
            && CFG_ARGS+=(--config "$(basename "$cd_")")
        done
        if [[ ${#CFG_ARGS[@]} -eq 0 ]]; then
          log "no real Claude config directories matched $CONFIG_GLOB"
          return 2
        fi
        matrix_rc=0
        supervise_matrix "$HERE/run_matrix.sh" --jobs "$JOBS" "${CFG_ARGS[@]}" \
          >> "$REPO/_setup/babysit-matrix.log" 2>&1 || matrix_rc=$?
        if [[ $matrix_rc -eq $LIMIT_STOP_RC ]]; then
          log "matrix stopped after a session-limit failure; rechecking the window"
          continue
        fi
        if [[ $matrix_rc -ne 0 ]]; then
          log "run_matrix failed with status $matrix_rc"
          return "$matrix_rc"
        fi
        log "run_matrix exited successfully"
        ;;
      WAIT*)
        SECS="${DECISION#WAIT }"
        log "window exhausted — sleeping ${SECS}s until reset (+3 min buffer), $REM task(s) remaining"
        sleep "$SECS"
        ;;
      STOP*)
        log "$DECISION — babysitter exiting; resume manually after the weekly reset"
        return 0
        ;;
      *)
        log "invalid usage decision: $DECISION"
        return 2
        ;;
    esac
  done
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
