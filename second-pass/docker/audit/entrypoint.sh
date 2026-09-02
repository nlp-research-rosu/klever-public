#!/usr/bin/env bash
# Run one independent Codex audit session. The supervisor profile and spool
# stay outside the workspace-write roots passed to Codex, so model-generated
# commands cannot write those supervisor paths. The reviewer still controls the
# semantic content it emits to its own outputs.
set -uo pipefail

MODEL="gpt-5.6-sol"
EFFORT="xhigh"
TIMEOUT_S="3600"
HARNESS_ERROR_RC=70
FROZEN_TOOLCHAIN_CHECK="${FROZEN_TOOLCHAIN_CHECK:-/usr/local/bin/assert-frozen-toolchain}"
"$FROZEN_TOOLCHAIN_CHECK" agent || exit "$HARNESS_ERROR_RC"

AUTH_FILE="${AUDIT_AUTH_FILE:-/auth/auth.json}"
KIT_SKILLS_DIR="${AUDIT_KIT_SKILLS_DIR:-/kit-skills}"
PROMPT_FILE="${AUDIT_PROMPT_FILE:-/audit-prompt.md}"
OUTPUT_DIR="${AUDIT_OUTPUT_DIR:-/audit-output}"
WORK_DIR="${AUDIT_WORK_DIR:-/tmp/audit-work}"
SUPERVISOR_PARENT="${AUDIT_SUPERVISOR_PARENT:-$HOME}"
CGROUP_ROOT="${AUDIT_CGROUP_ROOT:-/sys/fs/cgroup}"

SUPERVISOR_DIR=""
MODEL_PGID=""
HARNESS_EXIT_CODE=0

error() {
  printf 'audit harness error: %s\n' "$*" >&2
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
    kill -KILL -- "-$pgid" 2>/dev/null || true
  fi
}

cleanup() {
  if [[ -n "$MODEL_PGID" ]]; then
    terminate_model_group "$MODEL_PGID"
    MODEL_PGID=""
  fi
  if [[
    -n "$SUPERVISOR_DIR"
    && "$SUPERVISOR_DIR" == "$SUPERVISOR_PARENT"/.audit-supervisor.*
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

prepare_destination() {
  local destination="$1" label="$2"
  if [[ -L "$destination" || -f "$destination" ]]; then
    if ! rm -f -- "$destination"; then
      error "cannot remove existing $label destination: $destination"
      return 1
    fi
  elif [[ -e "$destination" ]]; then
    error "$label destination is a directory or unsupported node: $destination"
    return 1
  fi
}

publish_regular_file() {
  local source="$1" destination="$2" label="$3"
  local temporary=""
  if ! is_real_regular_file "$source"; then
    error "$label source is missing, linked, or not a regular file: $source"
    return 1
  fi
  if ! temporary="$(mktemp "$OUTPUT_DIR/.${destination##*/}.XXXXXX")"; then
    error "cannot stage $label in $OUTPUT_DIR"
    return 1
  fi
  if ! cp -- "$source" "$temporary"; then
    error "cannot copy $label into its publication stage"
    rm -f -- "$temporary"
    return 1
  fi
  if ! is_real_regular_file "$temporary"; then
    error "$label publication stage is not a real regular file"
    rm -f -- "$temporary"
    return 1
  fi
  if ! prepare_destination "$destination" "$label"; then
    rm -f -- "$temporary"
    return 1
  fi
  if ! mv -fT -- "$temporary" "$destination"; then
    error "cannot atomically publish $label to $destination"
    rm -f -- "$temporary"
    return 1
  fi
}

validate_trace_tree() {
  local source="$1"
  if ! is_real_directory "$source"; then
    error "Codex trace source is missing, linked, or not a directory: $source"
    return 1
  fi
  python3 - "$source" <<'PY'
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
        print(f"cannot scan Codex trace tree: {error}", file=sys.stderr)
        raise SystemExit(1)
    for entry in entries:
        try:
            mode = entry.stat(follow_symlinks=False).st_mode
        except OSError as error:
            print(f"cannot stat Codex trace entry: {error}", file=sys.stderr)
            raise SystemExit(1)
        if stat.S_ISDIR(mode):
            pending.append(entry.path)
        elif not stat.S_ISREG(mode):
            print(
                f"Codex trace contains a linked or unsupported entry: "
                f"{os.fsdecode(entry.path)}",
                file=sys.stderr,
            )
            raise SystemExit(1)
PY
}

publish_trace_tree() {
  local source="$1" destination="$2"
  local temporary=""
  if ! validate_trace_tree "$source"; then
    return 1
  fi
  if ! temporary="$(mktemp -d "$OUTPUT_DIR/.codex-trace.XXXXXX")"; then
    error "cannot stage Codex trace in $OUTPUT_DIR"
    return 1
  fi
  if ! cp -R -- "$source/." "$temporary/"; then
    error "cannot copy Codex trace into its publication stage"
    rm -rf -- "$temporary"
    return 1
  fi
  if ! validate_trace_tree "$temporary"; then
    error "staged Codex trace failed regular-file validation"
    rm -rf -- "$temporary"
    return 1
  fi
  if ! prepare_destination "$destination" "Codex trace"; then
    rm -rf -- "$temporary"
    return 1
  fi
  if ! mv -fT -- "$temporary" "$destination"; then
    error "cannot atomically publish Codex trace to $destination"
    rm -rf -- "$temporary"
    return 1
  fi
}

: "${AUDIT_PROBLEM_ID:?AUDIT_PROBLEM_ID is required}"
: "${AUDIT_CONDITION:?AUDIT_CONDITION is required}"
: "${AUDIT_SEMANTICS_MODE:?AUDIT_SEMANTICS_MODE is required}"

is_real_regular_file "$AUTH_FILE" \
  || setup_error "auth source is missing, linked, or not a regular file: $AUTH_FILE"
is_real_regular_file "$PROMPT_FILE" \
  || setup_error "prompt source is missing, linked, or not a regular file: $PROMPT_FILE"
is_real_directory "$KIT_SKILLS_DIR" \
  || setup_error "Kit source is missing, linked, or not a directory: $KIT_SKILLS_DIR"
is_real_directory "$OUTPUT_DIR" \
  || setup_error "audit output is missing, linked, or not a directory: $OUTPUT_DIR"
[[ -w "$OUTPUT_DIR" && -x "$OUTPUT_DIR" ]] \
  || setup_error "audit output is not writable: $OUTPUT_DIR"
is_real_directory "$SUPERVISOR_PARENT" \
  || setup_error "supervisor parent is missing, linked, or not a directory: $SUPERVISOR_PARENT"

if [[ "${AUDIT_PROBE_ONLY:-0}" == 1 ]]; then
  python3 - <<'PY'
import json
from importlib.metadata import version
from pathlib import Path
import subprocess

audit_input = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
layout = audit_input["record_layout"]

print("OBSERVED AUDIT TOOLCHAIN")
for command in ("codex", "kompile", "kprove", "krun"):
    result = subprocess.run(
        [command, "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    print(f"{command}: {result.stdout.strip()}")
print(f"K source: {Path('/opt/runtimeverification-k/.source-commit').read_text().strip()}")
print(f"pyk/Klean: {version('kframework')}")
result = subprocess.run(
    ["lean", "--version"],
    check=True,
    capture_output=True,
    text=True,
)
print(f"Lean: {result.stdout.strip()}")

required_files = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/audit-prompt.md",
    "/audit-entrypoint.sh",
    "/auth/auth.json",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/prompt.txt",
    "/run.json",
    "/task.json",
    "/generation-result.json",
]
if layout == "pipeline-v3":
    required_files.extend(
        (
            "/generation-evidence/runtime-metrics.json",
            "/generation-evidence/usage.json",
        )
    )

required_directories = [
    "/candidate",
    "/generation-evidence",
    "/generation-evidence/codex-trace",
    "/kit-skills",
]
if audit_input["mount_reference_semantics"]:
    required_directories.append("/reference/reference-semantics")

print(f"REQUIRED AUDIT INPUTS ({layout})")
for value in required_files:
    path = Path(value)
    if not path.is_file() or path.is_symlink():
        raise SystemExit(f"MISSING file {value}")
    print(f"OK file {value}")
for value in required_directories:
    path = Path(value)
    if not path.is_dir() or path.is_symlink():
        raise SystemExit(f"MISSING directory {value}")
    print(f"OK directory {value}")

print("READ-ONLY MOUNTS")
mounts = [
    "/candidate",
    "/generation-evidence",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
    "/kit-skills",
    "/audit-prompt.md",
    "/audit-entrypoint.sh",
    "/auth/auth.json",
]
if audit_input["mount_reference_semantics"]:
    mounts.append("/reference/reference-semantics")
for value in mounts:
    result = subprocess.run(
        ["findmnt", "-T", value, "-n", "-o", "OPTIONS"],
        check=True,
        capture_output=True,
        text=True,
    )
    options = result.stdout.strip()
    if "ro" not in options.split(","):
        raise SystemExit(f"WRITABLE mount {value}: {options}")
    print(f"OK readonly {value} options={options}")

campaign = json.loads(
    Path("/audit-campaign-lock.json").read_text(encoding="utf-8")
)
print("AUDIT CAMPAIGN LOCK")
for key in (
    "campaign_id",
    "audit_image_id",
    "codex_cli_version",
    "k_version",
    "pyk_version",
    "lean_toolchain",
    "kit_commit",
    "kit_skills_tree",
    "audit_prompt_sha256",
):
    print(f"{key}: {campaign[key]}")
print("NO MODEL CALL: probe complete")
PY
  exit 0
fi

if [[ ! -e "$WORK_DIR" && ! -L "$WORK_DIR" ]]; then
  WORK_PARENT="$(dirname -- "$WORK_DIR")" \
    || setup_error "cannot resolve scratch parent for $WORK_DIR"
  is_real_directory "$WORK_PARENT" \
    || setup_error "scratch parent is missing, linked, or not a directory: $WORK_PARENT"
  mkdir -- "$WORK_DIR" || setup_error "cannot create scratch directory: $WORK_DIR"
fi
is_real_directory "$WORK_DIR" \
  || setup_error "scratch path is linked or not a directory: $WORK_DIR"

SUPERVISOR_DIR="$(mktemp -d "$SUPERVISOR_PARENT/.audit-supervisor.XXXXXX")" \
  || setup_error "cannot create supervisor directory below $SUPERVISOR_PARENT"
chmod 700 "$SUPERVISOR_DIR" \
  || setup_error "cannot protect supervisor directory: $SUPERVISOR_DIR"
CODEX_HOME="$SUPERVISOR_DIR/codex-home"
SPOOL_DIR="$SUPERVISOR_DIR/spool"
mkdir -m 700 "$CODEX_HOME" "$SPOOL_DIR" \
  || setup_error "cannot create protected supervisor profile and spool"
mkdir -m 700 "$CODEX_HOME/skills" \
  || setup_error "cannot create Codex skills directory"
install -m 600 -- "$AUTH_FILE" "$CODEX_HOME/auth.json" \
  || setup_error "cannot install isolated Codex auth"
cp -R -- "$KIT_SKILLS_DIR/." "$CODEX_HOME/skills/" \
  || setup_error "cannot install approved Kit skills"
export CODEX_HOME

PROMPT_BUFFER="$SPOOL_DIR/rendered-audit-prompt.txt"
LOG_BUFFER="$SPOOL_DIR/codex-output.log"
LAST_BUFFER="$SPOOL_DIR/codex-last.txt"
METRICS_BUFFER="$SPOOL_DIR/metrics.json"

# Byte-oriented replacement preserves every non-placeholder byte from the
# launcher-owned prompt.
if ! python3 - \
  "$PROMPT_FILE" \
  "$AUDIT_PROBLEM_ID" \
  "$AUDIT_CONDITION" \
  "$AUDIT_SEMANTICS_MODE" \
  > "$PROMPT_BUFFER" <<'PY'
from pathlib import Path
import sys

prompt = Path(sys.argv[1]).read_bytes()
replacements = (
    (b"__PROBLEM_ID__", sys.argv[2].encode()),
    (b"__CONDITION__", sys.argv[3].encode()),
    (b"__SEMANTICS_MODE__", sys.argv[4].encode()),
)
for placeholder, value in replacements:
    if prompt.count(placeholder) != 1:
        raise SystemExit(
            f"audit prompt must contain exactly one {placeholder.decode()} placeholder"
        )
    prompt = prompt.replace(placeholder, value)
sys.stdout.buffer.write(prompt)
PY
then
  setup_error "cannot render audit prompt"
fi
is_real_regular_file "$PROMPT_BUFFER" \
  || setup_error "rendered audit prompt is not a real regular file"

START_EPOCH="$(date +%s)" || setup_error "cannot record audit start time"
setsid timeout --signal=TERM --kill-after=60 "$TIMEOUT_S" \
  codex -a never exec \
    --sandbox workspace-write \
    --add-dir "$WORK_DIR" \
    --ignore-user-config \
    --skip-git-repo-check \
    -C "$OUTPUT_DIR" \
    -m "$MODEL" \
    -c model_reasoning_effort="$EFFORT" \
    --output-last-message "$LAST_BUFFER" \
    - < "$PROMPT_BUFFER" \
    > "$LOG_BUFFER" 2>&1 &
MODEL_PGID=$!
wait "$MODEL_PGID"
MODEL_EXIT_CODE=$?
terminate_model_group "$MODEL_PGID"
MODEL_PGID=""
END_EPOCH="$(date +%s)" || mark_harness_error "cannot record audit end time"

publish_regular_file \
  "$PROMPT_BUFFER" "$OUTPUT_DIR/prompt.txt" "rendered audit prompt" \
  || mark_harness_error "rendered audit prompt publication failed"
publish_regular_file \
  "$LOG_BUFFER" "$OUTPUT_DIR/codex-output.log" "Codex output log" \
  || mark_harness_error "Codex output log publication failed"
publish_regular_file \
  "$LAST_BUFFER" "$OUTPUT_DIR/codex-last.txt" "Codex last message" \
  || mark_harness_error "Codex last-message publication failed"
publish_trace_tree "$CODEX_HOME/sessions" "$OUTPUT_DIR/codex-trace" \
  || mark_harness_error "Codex trace publication failed"

MEM_PEAK=null
for file in \
  "$CGROUP_ROOT/memory.peak" \
  "$CGROUP_ROOT/memory/memory.max_usage_in_bytes"
do
  if [[ -r "$file" ]]; then
    value="$(<"$file")"
    if [[ "$value" =~ ^[0-9]+$ ]]; then
      MEM_PEAK="$value"
      break
    fi
  fi
done

TIMED_OUT=false
if [[ "$MODEL_EXIT_CODE" -eq 124 || "$MODEL_EXIT_CODE" -eq 137 ]]; then
  TIMED_OUT=true
fi

FINAL_EXIT_CODE="$MODEL_EXIT_CODE"
if [[ "$HARNESS_EXIT_CODE" -ne 0 ]]; then
  FINAL_EXIT_CODE="$HARNESS_EXIT_CODE"
fi

if ! cat > "$METRICS_BUFFER" <<EOF
{
  "agent": "codex",
  "model": "$MODEL",
  "effort": "$EFFORT",
  "timeout_s": $TIMEOUT_S,
  "start_epoch": $START_EPOCH,
  "end_epoch": $END_EPOCH,
  "duration_s": $((END_EPOCH - START_EPOCH)),
  "exit_code": $FINAL_EXIT_CODE,
  "model_exit_code": $MODEL_EXIT_CODE,
  "harness_exit_code": $HARNESS_EXIT_CODE,
  "timed_out": $TIMED_OUT,
  "mem_peak_bytes": $MEM_PEAK
}
EOF
then
  mark_harness_error "cannot create metrics publication source"
fi

if is_real_regular_file "$METRICS_BUFFER"; then
  publish_regular_file "$METRICS_BUFFER" "$OUTPUT_DIR/metrics.json" "audit metrics" \
    || mark_harness_error "metrics publication failed"
fi

FINAL_EXIT_CODE="$MODEL_EXIT_CODE"
if [[ "$HARNESS_EXIT_CODE" -ne 0 ]]; then
  FINAL_EXIT_CODE="$HARNESS_EXIT_CODE"
fi
echo "audit metrics: model_exit=$MODEL_EXIT_CODE harness_exit=$HARNESS_EXIT_CODE timed_out=$TIMED_OUT mem_peak=$MEM_PEAK" >&2
exit "$FINAL_EXIT_CODE"
