#!/usr/bin/env bash
# Run one independent audit container for a completed generation task.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
# The campaign lock validates the resolved image ID below, so an explicit
# frozen tag can be supplied when "latest" has moved past the campaign.
IMAGE="${HUMANEVAL_AUDIT_IMAGE:-humaneval-codex-runner:latest}"
MODEL="gpt-5.6-sol"
EFFORT="xhigh"
MEMORY="8g"
TIMEOUT_S="3600"

PRINT_CONFIG=0
PROBE_ONLY=0
REPLACE_SELECTED=0
while [[ "${1:-}" == --* ]]; do
  case "$1" in
    --print-config)
      PRINT_CONFIG=1
      ;;
    --probe)
      PROBE_ONLY=1
      ;;
    --replace-selected)
      REPLACE_SELECTED=1
      ;;
    *)
      echo "unknown option: $1" >&2
      exit 2
      ;;
  esac
  shift
done
if [[ "$#" -ne 2 ]]; then
  echo "usage: run_task.sh [--print-config] [--probe] [--replace-selected] <generation-config> <problem-id>" >&2
  exit 2
fi
if [[ "$PROBE_ONLY" == 1 && "$REPLACE_SELECTED" == 1 ]]; then
  echo "--probe and --replace-selected cannot be combined" >&2
  exit 2
fi
CONFIG="$1"
PROBLEM="$2"
PIPELINE_MODE=0
if [[ -f "$REPO/runs/$CONFIG/run.json" || -L "$REPO/runs/$CONFIG/run.json" ]]; then
  PIPELINE_MODE=1
fi

RESOLUTION="$(mktemp /tmp/humaneval-audit-resolution.XXXXXXXX.json)"
AUDIT_INPUT=""
PROBE_OUTPUT=""
cleanup() {
  local status=$?
  trap - EXIT
  [[ -n "$RESOLUTION" && -f "$RESOLUTION" ]] && rm -f -- "$RESOLUTION"
  [[ -n "$AUDIT_INPUT" && -f "$AUDIT_INPUT" ]] && rm -f -- "$AUDIT_INPUT"
  if [[
    -n "$PROBE_OUTPUT"
    && "$PROBE_OUTPUT" == /tmp/humaneval-audit-probe-output.*
    && -d "$PROBE_OUTPUT"
    && ! -L "$PROBE_OUTPUT"
  ]]; then
    rm -rf -- "$PROBE_OUTPUT"
  fi
  exit "$status"
}
trap cleanup EXIT

if [[ "$PIPELINE_MODE" == 1 ]]; then
  python3 "$REPO/tools/audit_contract.py" resolve-stage2 \
    --repo "$REPO" --run-id "$CONFIG" --problem "$PROBLEM" > "$RESOLUTION"
else
  python3 "$REPO/tools/audit_contract.py" resolve \
    --repo "$REPO" --config "$CONFIG" --problem "$PROBLEM" > "$RESOLUTION"
fi

mapfile -d '' -t FIELDS < <(
  python3 - "$RESOLUTION" <<'PY'
import json
import sys

document = json.load(open(sys.argv[1], encoding="utf-8"))
for key in (
    "candidate",
    "canonical",
    "trusted_prompt",
    "translator",
    "condition",
    "semantics_mode",
    "reference_semantics",
    "record_layout",
    "generation_root",
    "stage1_result",
    "task_manifest",
    "run_manifest",
):
    value = document.get(key)
    sys.stdout.write(("" if value is None else str(value)) + "\0")
sys.stdout.write(("1" if document["mount_reference_semantics"] else "0") + "\0")
PY
)
if [[ "${#FIELDS[@]}" -ne 13 ]]; then
  echo "audit input error: cannot decode resolved input" >&2
  exit 2
fi
CANDIDATE="${FIELDS[0]}"
CANONICAL="${FIELDS[1]}"
TRUSTED_PROMPT="${FIELDS[2]}"
TRANSLATOR="${FIELDS[3]}"
CONDITION="${FIELDS[4]}"
SEMANTICS_MODE="${FIELDS[5]}"
REFERENCE_SEMANTICS="${FIELDS[6]}"
RECORD_LAYOUT="${FIELDS[7]}"
GENERATION_ROOT="${FIELDS[8]}"
STAGE1_RESULT="${FIELDS[9]}"
TASK_MANIFEST="${FIELDS[10]}"
RUN_MANIFEST="${FIELDS[11]}"
MOUNT_REFERENCE_SEMANTICS="${FIELDS[12]}"
if [[ "$PIPELINE_MODE" == 1 ]]; then
  OUTPUT_BASE="$REPO/runs/$CONFIG/tasks/$PROBLEM/02-k-audit/executions"
else
  OUTPUT_BASE="$REPO/audits/$CONFIG/$PROBLEM"
fi

print_config() {
  printf 'generation_config=%s\n' "$CONFIG"
  printf 'problem=%s\n' "$PROBLEM"
  printf 'model=%s\n' "$MODEL"
  printf 'effort=%s\n' "$EFFORT"
  printf 'memory=%s\n' "$MEMORY"
  printf 'memory_swap=%s\n' "$MEMORY"
  printf 'timeout_s=%s\n' "$TIMEOUT_S"
  printf 'condition=%s\n' "$CONDITION"
  printf 'semantics_mode=%s\n' "$SEMANTICS_MODE"
  printf 'mount_reference_semantics=%s\n' "$MOUNT_REFERENCE_SEMANTICS"
  printf 'candidate=%s\n' "$CANDIDATE"
  printf 'canonical=%s\n' "$CANONICAL"
  printf 'trusted_prompt=%s\n' "$TRUSTED_PROMPT"
  printf 'translator=%s\n' "$TRANSLATOR"
  printf 'record_layout=%s\n' "$RECORD_LAYOUT"
  printf 'generation_root=%s\n' "$GENERATION_ROOT"
  if [[ "$RECORD_LAYOUT" == "pipeline-v3" ]]; then
    printf 'stage1_result=%s\n' "$STAGE1_RESULT"
    printf 'task_manifest=%s\n' "$TASK_MANIFEST"
    printf 'run_manifest=%s\n' "$RUN_MANIFEST"
  fi
  if [[ "$MOUNT_REFERENCE_SEMANTICS" == 1 ]]; then
    printf 'reference_semantics=%s\n' "$REFERENCE_SEMANTICS"
  fi
  printf 'kit_skills=%s\n' "$REPO/data/audit-skills"
  printf 'campaign_lock=%s\n' "$REPO/data/audit-campaign.lock.json"
  printf 'output_base=%s\n' "$OUTPUT_BASE"
}

if [[ "$PRINT_CONFIG" == 1 ]]; then
  print_config
  exit 0
fi

AUTH="$REPO/docker/codex/secrets/codex/auth.json"
AUDIT_PROMPT="$REPO/prompts/audit.md"
CAMPAIGN_LOCK="$REPO/data/audit-campaign.lock.json"
ENTRYPOINT="$HERE/entrypoint.sh"
# The auditor mounts the campaign-frozen Kit bundle, not the moving
# generation bundle in data/skills.
KIT_SKILLS="$REPO/data/audit-skills"
AUDIT_KIT_LOCK="$REPO/data/audit-kit-skills.lock.json"

[[ -f "$AUTH" && ! -L "$AUTH" ]] || {
  echo "Missing real Codex auth file: $AUTH" >&2
  exit 2
}
for required_file in "$AUDIT_PROMPT" "$CAMPAIGN_LOCK" "$ENTRYPOINT"; do
  [[ -f "$required_file" && ! -L "$required_file" ]] || {
    echo "Missing real audit file: $required_file" >&2
    exit 2
  }
done
[[ -d "$KIT_SKILLS" && ! -L "$KIT_SKILLS" ]] || {
  echo "Missing real Kit skills directory: $KIT_SKILLS" >&2
  exit 2
}
# The campaign lock (checked below) already pins the audit Kit lock hash,
# commit, and tree; here we only verify the bundle bytes match that lock.
python3 "$REPO/tools/check_kit_bundle.py" \
  --bundle "$KIT_SKILLS" --lock "$AUDIT_KIT_LOCK" >/dev/null
IMAGE_ID="$(docker image inspect "$IMAGE" --format '{{.Id}}')"
python3 "$REPO/tools/check_audit_campaign.py" \
  --image-id "$IMAGE_ID" >/dev/null

ensure_directory() {
  local directory="$1" label="$2"
  if [[ -L "$directory" || ( -e "$directory" && ! -d "$directory" ) ]]; then
    echo "$label must be a real directory: $directory" >&2
    return 1
  fi
  if [[ ! -d "$directory" ]]; then
    mkdir -- "$directory"
  fi
}

if [[ "$PROBE_ONLY" == 1 ]]; then
  PROBE_OUTPUT="$(mktemp -d /tmp/humaneval-audit-probe-output.XXXXXXXX)"
  OUTPUT="$PROBE_OUTPUT"
elif [[ "$PIPELINE_MODE" == 1 ]]; then
  PREPARE_ARGS=(
    prepare-stage2
    --repo "$REPO"
    --run-id "$CONFIG"
    --problem "$PROBLEM"
  )
  if [[ "$REPLACE_SELECTED" == 1 ]]; then
    PREPARE_ARGS+=(--replace-selected)
  fi
  OUTPUT="$(
    python3 "$REPO/tools/audit_contract.py" "${PREPARE_ARGS[@]}"
  )"
else
  ensure_directory "$REPO/audits" "audits root"
  ensure_directory "$REPO/audits/$CONFIG" "audit config directory"

  if [[ ! -e "$OUTPUT_BASE" && ! -L "$OUTPUT_BASE" ]]; then
    mkdir -- "$OUTPUT_BASE"
    OUTPUT="$OUTPUT_BASE"
  else
    [[ -d "$OUTPUT_BASE" && ! -L "$OUTPUT_BASE" ]] || {
      echo "Audit problem path must be a real directory: $OUTPUT_BASE" >&2
      exit 2
    }
    if [[ -f "$OUTPUT_BASE/verdict.json" && ! -L "$OUTPUT_BASE/verdict.json" ]] \
      && python3 - "$OUTPUT_BASE/verdict.json" <<'PY'
import json
import sys

raise SystemExit(0 if json.load(open(sys.argv[1], encoding="utf-8")).get("audit_status") == "COMPLETE" else 1)
PY
    then
      echo "Completed audit already exists: $OUTPUT_BASE" >&2
      exit 2
    fi
    ensure_directory "$OUTPUT_BASE/attempts" "audit attempts directory"
    ATTEMPT="attempt-$(date -u +%Y%m%dT%H%M%SZ)-$$"
    OUTPUT="$OUTPUT_BASE/attempts/$ATTEMPT"
    mkdir -- "$OUTPUT"
  fi
fi
mkdir -p -- "$OUTPUT/evidence"

AUDIT_INPUT="$(mktemp /tmp/humaneval-audit-input.XXXXXXXX.json)"
python3 - \
  "$RESOLUTION" \
  "$AUDIT_INPUT" \
  "$IMAGE_ID" \
  "$OUTPUT" \
  "$RECORD_LAYOUT" \
  "$CAMPAIGN_LOCK" <<'PY'
import hashlib
import json
import os
import sys

with open(sys.argv[1], encoding="utf-8") as source:
    document = json.load(source)
record_layout = sys.argv[5]
container_paths = {
    "candidate": "/candidate",
    "canonical": "/reference/canonical.py",
    "trusted_prompt": "/reference/prompt.py",
    "translator": "/reference/py2mpy.py",
    "generation_root": "/generation-evidence",
    "generation_manifest": (
        "/generation-evidence/invocation.json"
        if record_layout in {"pipeline-v3", "legacy-selected-stage1"}
        else "/generation-evidence/run-input.json"
    ),
    "generation_metrics": "/generation-evidence/metrics.json",
    "generation_output": "/generation-evidence/codex-output.log",
    "generation_last": "/generation-evidence/codex-last.txt",
    "generation_trace": "/generation-evidence/codex-trace",
    "run_manifest": (
        "/run.json"
        if record_layout in {"pipeline-v3", "legacy-selected-stage1"}
        else None
    ),
    "task_manifest": (
        "/task.json"
        if record_layout in {"pipeline-v3", "legacy-selected-stage1"}
        else None
    ),
    "stage1_result": (
        "/generation-result.json"
        if record_layout in {"pipeline-v3", "legacy-selected-stage1"}
        else None
    ),
    "audit_campaign_lock": "/audit-campaign-lock.json",
}
document["record_layout"] = record_layout
document["container_paths"] = container_paths
with open(sys.argv[6], "rb") as source:
    campaign_bytes = source.read()
document["audit_campaign"] = json.loads(campaign_bytes)
document["hashes"]["audit_campaign_lock_sha256"] = hashlib.sha256(
    campaign_bytes
).hexdigest()
document["audit"] = {
    "image_id": sys.argv[3],
    "model": "gpt-5.6-sol",
    "effort": "xhigh",
    "memory_bytes": 8 * 1024**3,
    "memory_swap_bytes": 8 * 1024**3,
    "timeout_s": 3600,
    "output": sys.argv[4],
}
temporary = sys.argv[2] + ".tmp"
with open(temporary, "w", encoding="utf-8") as destination:
    json.dump(document, destination, indent=2, sort_keys=True)
    destination.write("\n")
    destination.flush()
    os.fsync(destination.fileno())
os.replace(temporary, sys.argv[2])
PY
chmod 0444 "$AUDIT_INPUT"

DOCKER_ARGS=(
  run --rm -i --init --pull=never
  --security-opt seccomp=unconfined
  --memory "$MEMORY" --memory-swap "$MEMORY"
  --env "AUDIT_PROBLEM_ID=$PROBLEM"
  --env "AUDIT_CONDITION=$CONDITION"
  --env "AUDIT_SEMANTICS_MODE=$SEMANTICS_MODE"
  --mount "type=bind,source=$CANDIDATE,target=/candidate,readonly"
  --mount "type=bind,source=$GENERATION_ROOT,target=/generation-evidence,readonly"
  --mount "type=bind,source=$CANONICAL,target=/reference/canonical.py,readonly"
  --mount "type=bind,source=$TRUSTED_PROMPT,target=/reference/prompt.py,readonly"
  --mount "type=bind,source=$TRANSLATOR,target=/reference/py2mpy.py,readonly"
  --mount "type=bind,source=$KIT_SKILLS,target=/kit-skills,readonly"
  --mount "type=bind,source=$AUTH,target=/auth/auth.json,readonly"
  --mount "type=bind,source=$AUDIT_PROMPT,target=/audit-prompt.md,readonly"
  --mount "type=bind,source=$AUDIT_INPUT,target=/audit-input.json,readonly"
  --mount "type=bind,source=$CAMPAIGN_LOCK,target=/audit-campaign-lock.json,readonly"
  --mount "type=bind,source=$ENTRYPOINT,target=/audit-entrypoint.sh,readonly"
  --mount "type=bind,source=$OUTPUT,target=/audit-output"
  --workdir /audit-output
  --entrypoint /audit-entrypoint.sh
)
if [[ "$PROBE_ONLY" == 1 ]]; then
  DOCKER_ARGS+=(--env "AUDIT_PROBE_ONLY=1")
fi
if [[
  "$RECORD_LAYOUT" == "pipeline-v3"
  || "$RECORD_LAYOUT" == "legacy-selected-stage1"
]]; then
  DOCKER_ARGS+=(
    --mount "type=bind,source=$RUN_MANIFEST,target=/run.json,readonly"
    --mount "type=bind,source=$TASK_MANIFEST,target=/task.json,readonly"
    --mount "type=bind,source=$STAGE1_RESULT,target=/generation-result.json,readonly"
  )
fi
if [[ "$MOUNT_REFERENCE_SEMANTICS" == 1 ]]; then
  DOCKER_ARGS+=(
    --mount "type=bind,source=$REFERENCE_SEMANTICS,target=/reference/reference-semantics,readonly"
  )
fi

set +e
docker "${DOCKER_ARGS[@]}" "$IMAGE"
DOCKER_RC=$?
set -e

if [[ "$PROBE_ONLY" == 1 ]]; then
  exit "$DOCKER_RC"
fi

python3 - "$AUDIT_INPUT" "$OUTPUT/audit-input.json" "$REPO" <<'PY'
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[3])
from tools.audit_contract import write_json_atomic

with open(sys.argv[1], encoding="utf-8") as source:
    write_json_atomic(Path(sys.argv[2]), json.load(source))
PY

set +e
python3 "$REPO/tools/audit_contract.py" verdict \
  --review "$OUTPUT/REVIEW.md" \
  --metrics "$OUTPUT/metrics.json" \
  --output "$OUTPUT/verdict.json"
VERDICT_RC=$?
set -e

MODEL_TRACE_AVAILABLE=0
if [[ -d "$OUTPUT/codex-trace" && ! -L "$OUTPUT/codex-trace" ]]; then
  MODEL_TRACE_AVAILABLE=1
fi

USAGE_RC=0
if [[
  "$PIPELINE_MODE" == 1
  && ( "$VERDICT_RC" -eq 0 || "$MODEL_TRACE_AVAILABLE" -eq 1 )
]]; then
  set +e
  python3 "$REPO/tools/usage_accounting.py" write --trace "$OUTPUT/codex-trace" --output "$OUTPUT/usage.json"
  USAGE_RC=$?
  set -e
fi

SELECTION_RC=0
if [[ "$PIPELINE_MODE" == 1 ]]; then
  set +e
  python3 - \
    "$REPO" \
    "$CONFIG" \
    "$PROBLEM" \
    "$(basename "$OUTPUT")" \
    "$REPLACE_SELECTED" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tools.pipeline_contract import select_stage_output

select_stage_output(
    Path(sys.argv[1]),
    sys.argv[2],
    sys.argv[3],
    "02-k-audit",
    sys.argv[4],
    replace_selected=sys.argv[5] == "1",
)
PY
  SELECTION_RC=$?
  set -e
fi

SUMMARY_RC=0
if [[ "$PIPELINE_MODE" == 1 && "$SELECTION_RC" -eq 0 ]]; then
  set +e
  flock "$REPO/runs/$CONFIG/.usage-summary.lock" python3 "$REPO/tools/usage_accounting.py" summarize --run "$REPO/runs/$CONFIG"
  SUMMARY_RC=$?
  set -e
fi

printf 'audit_output=%s\n' "$OUTPUT"
if [[
  "$DOCKER_RC" -ne 0
  || "$VERDICT_RC" -ne 0
  || "$USAGE_RC" -ne 0
  || "$SELECTION_RC" -ne 0
  || "$SUMMARY_RC" -ne 0
]]; then
  exit 1
fi
