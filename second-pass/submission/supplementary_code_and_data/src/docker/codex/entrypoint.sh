#!/usr/bin/env bash
# Run one initial or resumed Codex invocation. The model can write only the
# stage workspace. Supervisor state and immutable invocation evidence remain
# outside its workspace-write roots.
set -uo pipefail

HARNESS_ERROR_RC=70
FROZEN_TOOLCHAIN_CHECK="${FROZEN_TOOLCHAIN_CHECK:-/usr/local/bin/assert-frozen-toolchain}"
"$FROZEN_TOOLCHAIN_CHECK" agent || exit "$HARNESS_ERROR_RC"
MODEL="${MODEL:-gpt-5.6-sol}"
EFFORT="${EFFORT:-xhigh}"
TIMEOUT_S="${TIMEOUT_S:-3600}"
TIMEOUT_GRACE_S="${TIMEOUT_GRACE_S:-60}"
KIT="${KIT:-0}"
LEMMA_DISCOVERY="${LEMMA_DISCOVERY:-0}"

WORKSPACE="${WORKSPACE:-/workspace}"
INVOCATION_OUTPUT="${INVOCATION_OUTPUT:-/invocation-output}"
PROMPT_FILE="${PROMPT_FILE:-/invocation-prompt.md}"
CODEX_HOME="${CODEX_HOME:-/codex-home}"
CODEX_AUTH_FILE="${CODEX_AUTH_FILE:-/auth/auth.json}"
CODEX_BWRAP="${CODEX_BWRAP:-/usr/local/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/codex-resources/bwrap}"
KIT_SKILLS_DIR="${KIT_SKILLS_DIR:-/kit-skills}"
SUPERVISOR_PARENT="${SUPERVISOR_PARENT:-/tmp}"
CGROUP_ROOT="${CGROUP_ROOT:-/sys/fs/cgroup}"
INVOCATION_KIND="${INVOCATION_KIND:-initial}"
SESSION_ID="${SESSION_ID:-}"
K_REFERENCE="${K_REFERENCE:-/reference/k-proof}"
RULE_INVENTORY_FILE="${RULE_INVENTORY_FILE:-/reference/rule-inventory.json}"

SUPERVISOR_DIR=""
MODEL_PGID=""
WATCHDOG_PID=""
HARNESS_EXIT_CODE=0

error() {
  printf 'codex harness error: %s\n' "$*" >&2
}

is_real_regular_file() {
  [[ -f "$1" && ! -L "$1" ]]
}

is_real_directory() {
  [[ -d "$1" && ! -L "$1" ]]
}

terminate_model_group() {
  local pgid="$1"
  if [[ "$pgid" =~ ^[0-9]+$ ]] && kill -0 -- "-$pgid" 2>/dev/null; then
    kill -TERM -- "-$pgid" 2>/dev/null || true
    sleep "$TIMEOUT_GRACE_S"
    kill -KILL -- "-$pgid" 2>/dev/null || true
  fi
}

cleanup() {
  if [[ -n "$WATCHDOG_PID" ]]; then
    kill "$WATCHDOG_PID" 2>/dev/null || true
    wait "$WATCHDOG_PID" 2>/dev/null || true
    WATCHDOG_PID=""
  fi
  if [[ -n "$MODEL_PGID" ]]; then
    terminate_model_group "$MODEL_PGID"
    MODEL_PGID=""
  fi
  if [[
    -n "$SUPERVISOR_DIR"
    && "$SUPERVISOR_DIR" == "$SUPERVISOR_PARENT"/.codex-supervisor.*
    && -d "$SUPERVISOR_DIR"
    && ! -L "$SUPERVISOR_DIR"
  ]]; then
    rm -rf -- "$SUPERVISOR_DIR"
  fi
}

trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

setup_error() {
  error "$*"
  exit "$HARNESS_ERROR_RC"
}

mark_harness_error() {
  error "$*"
  HARNESS_EXIT_CODE="$HARNESS_ERROR_RC"
}

validate_positive_number() {
  python3 - "$1" "$2" <<'PY'
import math
import sys
try:
    value = float(sys.argv[1])
except ValueError:
    raise SystemExit(f"{sys.argv[2]} must be numeric")
if not math.isfinite(value) or value <= 0:
    raise SystemExit(f"{sys.argv[2]} must be positive")
PY
}

validate_uuid() {
  python3 - "$1" <<'PY'
import sys
import uuid
try:
    parsed = uuid.UUID(sys.argv[1])
except ValueError:
    raise SystemExit(1)
if str(parsed) != sys.argv[1]:
    raise SystemExit(1)
PY
}

assert_outside_workspace() {
  local path="$1" label="$2"
  case "$path" in
    "$WORKSPACE"|"$WORKSPACE"/*)
      setup_error "$label must stay outside the model workspace"
      ;;
  esac
}

validate_tree() {
  python3 - "$1" <<'PY'
import os
import stat
import sys

root = os.fsencode(sys.argv[1])
pending = [root]
while pending:
    directory = pending.pop()
    try:
        entries = list(os.scandir(directory))
    except OSError as error:
        raise SystemExit(f"cannot scan tree: {error}")
    for entry in entries:
        try:
            mode = entry.stat(follow_symlinks=False).st_mode
        except OSError as error:
            raise SystemExit(f"cannot inspect tree entry: {error}")
        if stat.S_ISDIR(mode):
            pending.append(entry.path)
        elif not stat.S_ISREG(mode):
            raise SystemExit(
                f"tree contains linked or unsupported entry: "
                f"{os.fsdecode(entry.path)}"
            )
PY
}

compare_trees() {
  python3 - "$1" "$2" <<'PY'
import hashlib
import os
import stat
import sys
from pathlib import Path

def digest(root, *, ignore_codex_system=False):
    root = Path(root)
    pending = [root]
    entries = []
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            if (
                ignore_codex_system
                and directory == root
                and entry.name == ".system"
            ):
                continue
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((rel, "d", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((rel, "f", path))
            else:
                raise SystemExit(f"unsupported tree entry: {path}")
    result = hashlib.sha256()
    for rel, kind, path in sorted(entries):
        result.update(rel.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "f":
            result.update(path.read_bytes())
    return result.hexdigest()

if digest(sys.argv[1]) != digest(
    sys.argv[2], ignore_codex_system=True
):
    raise SystemExit("persisted Kit tree differs from approved Kit source")
PY
}

prepare_destination() {
  local destination="$1" label="$2"
  if [[ -e "$destination" || -L "$destination" ]]; then
    error "$label destination already exists: $destination"
    return 1
  fi
}

publish_regular_file() {
  local source="$1" destination="$2" label="$3"
  local temporary=""
  is_real_regular_file "$source" || {
    error "$label source is missing, linked, or not regular: $source"
    return 1
  }
  prepare_destination "$destination" "$label" || return 1
  temporary="$(mktemp "$INVOCATION_OUTPUT/.${destination##*/}.XXXXXX")" || {
    error "cannot stage $label"
    return 1
  }
  if ! cp -- "$source" "$temporary" || ! mv -T -- "$temporary" "$destination"; then
    error "cannot atomically publish $label"
    rm -f -- "$temporary"
    return 1
  fi
}

publish_trace_tree() {
  local source="$1" destination="$2"
  local temporary=""
  is_real_directory "$source" || {
    error "Codex trace source is missing or linked: $source"
    return 1
  }
  validate_tree "$source" || return 1
  prepare_destination "$destination" "Codex trace" || return 1
  temporary="$(mktemp -d "$INVOCATION_OUTPUT/.codex-trace.XXXXXX")" || return 1
  if ! cp -R -- "$source/." "$temporary/"; then
    rm -rf -- "$temporary"
    return 1
  fi
  if ! validate_tree "$temporary" || ! mv -T -- "$temporary" "$destination"; then
    rm -rf -- "$temporary"
    return 1
  fi
}

read_oom_kill_count() {
  local events="$CGROUP_ROOT/memory.events"
  if [[ -r "$events" ]]; then
    awk '$1 == "oom_kill" && $2 ~ /^[0-9]+$/ {print $2; found=1} END {if (!found) print 0}' "$events"
  else
    printf '0\n'
  fi
}

read_memory_peak() {
  local file value
  for file in \
    "$CGROUP_ROOT/memory.peak" \
    "$CGROUP_ROOT/memory/memory.max_usage_in_bytes"
  do
    if [[ -r "$file" ]]; then
      value="$(<"$file")"
      if [[ "$value" =~ ^[0-9]+$ ]]; then
        printf '%s\n' "$value"
        return
      fi
    fi
  done
  printf 'null\n'
}

validate_positive_number "$TIMEOUT_S" "TIMEOUT_S" \
  || setup_error "TIMEOUT_S must be a positive number"
validate_positive_number "$TIMEOUT_GRACE_S" "TIMEOUT_GRACE_S" \
  || setup_error "TIMEOUT_GRACE_S must be a positive number"
[[ "$KIT" == "0" || "$KIT" == "1" ]] \
  || setup_error "KIT must be 0 or 1"
[[ "$LEMMA_DISCOVERY" == "0" || "$LEMMA_DISCOVERY" == "1" ]] \
  || setup_error "LEMMA_DISCOVERY must be 0 or 1"
case "$INVOCATION_KIND" in
  initial)
    [[ -z "$SESSION_ID" ]] \
      || setup_error "initial invocation must not receive SESSION_ID"
    ;;
  timeout-resume|stage-resume|infrastructure-retry)
    validate_uuid "$SESSION_ID" \
      || setup_error "resume invocation requires a canonical session UUID"
    ;;
  *)
    setup_error "unsupported INVOCATION_KIND: $INVOCATION_KIND"
    ;;
esac

is_real_directory "$WORKSPACE" \
  || setup_error "workspace is missing, linked, or not a directory: $WORKSPACE"
is_real_directory "$INVOCATION_OUTPUT" \
  || setup_error "invocation output is missing, linked, or not a directory"
is_real_directory "$CODEX_HOME" \
  || setup_error "persistent CODEX_HOME is missing, linked, or not a directory"
is_real_directory "$SUPERVISOR_PARENT" \
  || setup_error "supervisor parent is missing, linked, or not a directory"
is_real_regular_file "$PROMPT_FILE" \
  || setup_error "prompt is missing, linked, or not a regular file"
is_real_regular_file "$CODEX_AUTH_FILE" \
  || setup_error "auth source is missing, linked, or not a regular file"

WORKSPACE="$(realpath -e -- "$WORKSPACE")" \
  || setup_error "cannot resolve workspace"
INVOCATION_OUTPUT="$(realpath -e -- "$INVOCATION_OUTPUT")" \
  || setup_error "cannot resolve invocation output"
CODEX_HOME="$(realpath -e -- "$CODEX_HOME")" \
  || setup_error "cannot resolve persistent CODEX_HOME"
SUPERVISOR_PARENT="$(realpath -e -- "$SUPERVISOR_PARENT")" \
  || setup_error "cannot resolve supervisor parent"
PROMPT_FILE="$(realpath -e -- "$PROMPT_FILE")" \
  || setup_error "cannot resolve prompt"
CODEX_AUTH_FILE="$(realpath -e -- "$CODEX_AUTH_FILE")" \
  || setup_error "cannot resolve auth source"

assert_outside_workspace "$INVOCATION_OUTPUT" "invocation output"
assert_outside_workspace "$CODEX_HOME" "persistent CODEX_HOME"
assert_outside_workspace "$SUPERVISOR_PARENT" "supervisor parent"
[[ "$INVOCATION_OUTPUT" != "$CODEX_HOME" && "$INVOCATION_OUTPUT" != "$CODEX_HOME"/* ]] \
  || setup_error "invocation output must stay outside persistent CODEX_HOME"
if [[ "$LEMMA_DISCOVERY" == "1" ]]; then
  is_real_directory "$K_REFERENCE" \
    || setup_error "Stage 1 reference is missing, linked, or not a directory"
  is_real_regular_file "$RULE_INVENTORY_FILE" \
    || setup_error "rule inventory is missing, linked, or not a regular file"
  K_REFERENCE="$(realpath -e -- "$K_REFERENCE")" \
    || setup_error "cannot resolve Stage 1 reference"
  RULE_INVENTORY_FILE="$(realpath -e -- "$RULE_INVENTORY_FILE")" \
    || setup_error "cannot resolve rule inventory"
  assert_outside_workspace "$K_REFERENCE" "Stage 1 reference"
  assert_outside_workspace "$RULE_INVENTORY_FILE" "rule inventory"
fi
chmod 700 "$CODEX_HOME" \
  || setup_error "cannot protect persistent CODEX_HOME"

if [[ ! -e "$CODEX_HOME/auth.json" && ! -L "$CODEX_HOME/auth.json" ]]; then
  install -m 600 -- "$CODEX_AUTH_FILE" "$CODEX_HOME/auth.json" \
    || setup_error "cannot seed approved Codex auth"
elif ! is_real_regular_file "$CODEX_HOME/auth.json"; then
  setup_error "persisted Codex auth is linked or not a regular file"
fi

is_real_regular_file "$CODEX_BWRAP" && [[ -x "$CODEX_BWRAP" ]] \
  || setup_error "bundled bubblewrap is missing, linked, or not executable"
"$CODEX_BWRAP" \
  --unshare-user \
  --unshare-pid \
  --unshare-net \
  --die-with-parent \
  --ro-bind / / \
  -- /bin/true \
  >/dev/null 2>&1 \
  || setup_error "Codex workspace sandbox preflight failed"

if [[ "$KIT" == "1" ]]; then
  is_real_directory "$KIT_SKILLS_DIR" \
    || setup_error "approved Kit source is missing, linked, or not a directory"
  KIT_SKILLS_DIR="$(realpath -e -- "$KIT_SKILLS_DIR")" \
    || setup_error "cannot resolve approved Kit source"
  validate_tree "$KIT_SKILLS_DIR" \
    || setup_error "approved Kit source contains unsupported entries"
  if [[ ! -e "$CODEX_HOME/skills" && ! -L "$CODEX_HOME/skills" ]]; then
    mkdir -m 700 "$CODEX_HOME/.skills-staging" \
      || setup_error "cannot create Kit staging directory"
    cp -R -- "$KIT_SKILLS_DIR/." "$CODEX_HOME/.skills-staging/" \
      || setup_error "cannot seed approved Kit"
    mv -T -- "$CODEX_HOME/.skills-staging" "$CODEX_HOME/skills" \
      || setup_error "cannot publish approved Kit"
  fi
  is_real_directory "$CODEX_HOME/skills" \
    || setup_error "persisted Kit skills are linked or not a directory"
  compare_trees "$KIT_SKILLS_DIR" "$CODEX_HOME/skills" \
    || setup_error "persisted Kit skills differ from approved Kit"
fi

for reserved in \
  prompt.txt codex-output.log codex-last.txt codex-trace metrics.json
do
  [[ ! -e "$INVOCATION_OUTPUT/$reserved" && ! -L "$INVOCATION_OUTPUT/$reserved" ]] \
    || setup_error "invocation output already contains reserved evidence: $reserved"
done

SUPERVISOR_DIR="$(mktemp -d "$SUPERVISOR_PARENT/.codex-supervisor.XXXXXX")" \
  || setup_error "cannot create protected supervisor directory"
chmod 700 "$SUPERVISOR_DIR" \
  || setup_error "cannot protect supervisor directory"
SPOOL_DIR="$SUPERVISOR_DIR/spool"
mkdir -m 700 "$SPOOL_DIR" \
  || setup_error "cannot create protected supervisor spool"
PROMPT_BUFFER="$SPOOL_DIR/prompt.txt"
LOG_BUFFER="$SPOOL_DIR/codex-output.log"
LAST_BUFFER="$SPOOL_DIR/codex-last.txt"
METRICS_BUFFER="$SPOOL_DIR/metrics.json"
TIMEOUT_MARKER="$SPOOL_DIR/wrapper-timeout"
cp -- "$PROMPT_FILE" "$PROMPT_BUFFER" \
  || setup_error "cannot copy invocation prompt into protected spool"

export CODEX_HOME
COMMON_ARGS=(
  -a never
  exec
  --sandbox workspace-write
  --ignore-user-config
  --ignore-rules
  --skip-git-repo-check
  -C "$WORKSPACE"
)
if [[ "$INVOCATION_KIND" == "initial" ]]; then
  CODEX_ARGS=(
    "${COMMON_ARGS[@]}"
    -m "$MODEL"
    -c "model_reasoning_effort=\"$EFFORT\""
    --output-last-message "$LAST_BUFFER"
    -
  )
else
  CODEX_ARGS=(
    "${COMMON_ARGS[@]}"
    resume
    "$SESSION_ID"
    -m "$MODEL"
    -c "model_reasoning_effort=\"$EFFORT\""
    --output-last-message "$LAST_BUFFER"
    -
  )
fi

START_EPOCH="$(date +%s)"
OOM_BEFORE="$(read_oom_kill_count)"
setsid codex "${CODEX_ARGS[@]}" \
  < "$PROMPT_BUFFER" > "$LOG_BUFFER" 2>&1 &
MODEL_PGID=$!
(
  sleep "$TIMEOUT_S"
  if kill -0 "$MODEL_PGID" 2>/dev/null; then
    : > "$TIMEOUT_MARKER"
    kill -TERM -- "-$MODEL_PGID" 2>/dev/null || true
    sleep "$TIMEOUT_GRACE_S"
    kill -KILL -- "-$MODEL_PGID" 2>/dev/null || true
  fi
) </dev/null >/dev/null 2>&1 &
WATCHDOG_PID=$!

wait "$MODEL_PGID"
MODEL_EXIT_CODE=$?
MODEL_PGID=""
kill "$WATCHDOG_PID" 2>/dev/null || true
wait "$WATCHDOG_PID" 2>/dev/null || true
WATCHDOG_PID=""
END_EPOCH="$(date +%s)"
OOM_AFTER="$(read_oom_kill_count)"
MEM_PEAK="$(read_memory_peak)"

TIMEOUT_MARKED=false
[[ -f "$TIMEOUT_MARKER" && ! -L "$TIMEOUT_MARKER" ]] && TIMEOUT_MARKED=true
OOM_KILLED=false
if [[ "$OOM_BEFORE" =~ ^[0-9]+$ && "$OOM_AFTER" =~ ^[0-9]+$ ]] \
  && (( OOM_AFTER > OOM_BEFORE )); then
  OOM_KILLED=true
fi

publish_regular_file \
  "$PROMPT_BUFFER" "$INVOCATION_OUTPUT/prompt.txt" "invocation prompt" \
  || mark_harness_error "prompt publication failed"
publish_regular_file \
  "$LOG_BUFFER" "$INVOCATION_OUTPUT/codex-output.log" "Codex output log" \
  || mark_harness_error "Codex output publication failed"
publish_regular_file \
  "$LAST_BUFFER" "$INVOCATION_OUTPUT/codex-last.txt" "Codex final message" \
  || mark_harness_error "Codex final-message publication failed"
publish_trace_tree "$CODEX_HOME/sessions" "$INVOCATION_OUTPUT/codex-trace" \
  || mark_harness_error "Codex trace publication failed"

FINAL_EXIT_CODE="$MODEL_EXIT_CODE"
if [[ "$HARNESS_EXIT_CODE" -ne 0 ]]; then
  FINAL_EXIT_CODE="$HARNESS_EXIT_CODE"
fi

python3 - \
  "$METRICS_BUFFER" \
  "$MODEL" "$EFFORT" "$TIMEOUT_S" \
  "$START_EPOCH" "$END_EPOCH" "$MODEL_EXIT_CODE" \
  "$HARNESS_EXIT_CODE" "$FINAL_EXIT_CODE" \
  "$TIMEOUT_MARKED" "$OOM_KILLED" "$MEM_PEAK" <<'PY' \
  || mark_harness_error "cannot create metrics publication source"
import json
import sys
from pathlib import Path

(
    destination, model, effort, timeout_s, start, end, exit_code,
    harness_exit_code, final_exit_code, timeout_marked, oom_killed, mem_peak,
) = sys.argv[1:]
document = {
    "agent": "codex",
    "model": model,
    "effort": effort,
    "timeout_s": float(timeout_s),
    "start_epoch": int(start),
    "end_epoch": int(end),
    "duration_s": int(end) - int(start),
    "model_exit_code": int(exit_code),
    "harness_exit_code": int(harness_exit_code),
    "final_exit_code": int(final_exit_code),
    "timeout_marker": timeout_marked == "true",
    "oom_killed": oom_killed == "true",
    "mem_peak_bytes": None if mem_peak == "null" else int(mem_peak),
}
Path(destination).write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
PY

if is_real_regular_file "$METRICS_BUFFER"; then
  publish_regular_file \
    "$METRICS_BUFFER" "$INVOCATION_OUTPUT/metrics.json" "invocation metrics" \
    || mark_harness_error "metrics publication failed"
fi

# Metrics publication is itself part of the harness. If it failed after the
# document was formed, the container's final status remains authoritative and
# the host finalizes the invocation as a non-resumable harness failure.
if [[ "$HARNESS_EXIT_CODE" -ne 0 ]]; then
  FINAL_EXIT_CODE="$HARNESS_EXIT_CODE"
fi
printf \
  'codex metrics: model_exit=%s harness_exit=%s timeout_marker=%s oom=%s peak=%s\n' \
  "$MODEL_EXIT_CODE" "$HARNESS_EXIT_CODE" "$TIMEOUT_MARKED" "$OOM_KILLED" "$MEM_PEAK" \
  >&2
exit "$FINAL_EXIT_CODE"
