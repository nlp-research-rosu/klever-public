#!/usr/bin/env bash
# Run one fresh Stage 6 audit of classification and any Stage 5 Lean proof.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
IMAGE="humaneval-codex-runner:latest"
MEMORY="8g"
TIMEOUT_S="3600"
AUDIT_STAGE="06-lean-audit"

REPLACE_SELECTED=0
REPLACE_ARGUMENT=()
if [[ "${1:-}" == "--replace-selected" ]]; then
  REPLACE_SELECTED=1
  REPLACE_ARGUMENT=(--replace-selected)
  shift
fi
if [[ "$#" -ne 2 ]]; then
  echo "usage: run_task.sh [--replace-selected] <run-id> <problem-id>" >&2
  exit 2
fi
RUN_ID="$1"
PROBLEM="$2"
CHECKER="$HERE/check_tool_bundle.py"
CHECKER_LOCK="$REPO/data/klean-audit-tools.lock.json"
TOOLCHAIN_LOCK="$REPO/data/klean-toolchain.lock.json"
for path in "$CHECKER" "$CHECKER_LOCK" "$TOOLCHAIN_LOCK"; do
  [[ -f "$path" && ! -L "$path" ]] || {
    echo "Stage 6 required file must be real: $path" >&2
    exit 2
  }
done
python3 "$CHECKER" --root "$REPO" --lock "$CHECKER_LOCK"
IMAGE_ID="$(docker image inspect "$IMAGE" --format '{{.Id}}')"

RESOLUTION="$(mktemp /tmp/humaneval-klean-audit-resolution.XXXXXXXX.json)"
MECHANICAL_TMP="$(
  mktemp /tmp/humaneval-mechanical-check.XXXXXXXX.json
)"
cleanup() {
  local status=$?
  trap - EXIT
  rm -f -- "$RESOLUTION" "$MECHANICAL_TMP"
  exit "$status"
}
trap cleanup EXIT

python3 "$REPO/tools/klean_audit_contract.py" resolve \
  --repo "$REPO" --run-id "$RUN_ID" --problem "$PROBLEM" > "$RESOLUTION"

mapfile -d '' -t FIELDS < <(
  python3 - "$RESOLUTION" <<'PY'
import json
import sys

document = json.load(open(sys.argv[1], encoding="utf-8"))
resolution = document["resolution"]
for key in (
    "k_workspace",
    "k_audit",
    "discovery_manifest",
    "klean_generation",
    "generation_producer_sources",
    "lean_workspace",
    "mode",
    "condition",
    "semantics_mode",
    "resolved_input_sha256",
):
    value = (
        document[key]
        if key == "resolved_input_sha256"
        else resolution[key]
    )
    sys.stdout.write(("" if value is None else str(value)) + "\0")
PY
)
if [[ "${#FIELDS[@]}" -ne 10 ]]; then
  echo "Stage 6 input error: cannot decode resolved inputs" >&2
  exit 2
fi
K_WORKSPACE="${FIELDS[0]}"
K_AUDIT="${FIELDS[1]}"
DISCOVERY_MANIFEST="${FIELDS[2]}"
KLEAN_GENERATION="${FIELDS[3]}"
GENERATION_PRODUCER_SOURCES="${FIELDS[4]}"
LEAN_WORKSPACE="${FIELDS[5]}"
AUDIT_MODE="${FIELDS[6]}"
CONDITION="${FIELDS[7]}"
SEMANTICS_MODE="${FIELDS[8]}"
RESOLVED_INPUT_SHA256="${FIELDS[9]}"

case "$AUDIT_MODE" in
  CLASSIFICATION_AND_PROOF)
    [[ -n "$LEAN_WORKSPACE" ]] || {
      echo "Stage 6 input error: proof mode has no Stage 5 workspace" >&2
      exit 2
    }
    ;;
  CLASSIFICATION_ONLY)
    [[ -z "$LEAN_WORKSPACE" ]] || {
      echo "Stage 6 input error: classification-only mode has a Stage 5 workspace" >&2
      exit 2
    }
    ;;
  *)
    echo "Stage 6 input error: unsupported audit mode: $AUDIT_MODE" >&2
    exit 2
    ;;
esac

docker run --rm --network none --pull=never \
  --mount "type=bind,source=$CHECKER,target=/reference/check-tool-bundle.py,readonly" \
  --mount "type=bind,source=$CHECKER_LOCK,target=/reference/klean-audit-tools.lock.json,readonly" \
  --mount "type=bind,source=$DISCOVERY_MANIFEST,target=/reference/lemma-discovery.json,readonly" \
  --entrypoint bash \
  "$IMAGE_ID" \
  -lc '/usr/local/bin/assert-frozen-toolchain agent && python3 /reference/check-tool-bundle.py --root /opt/humaneval --lock /reference/klean-audit-tools.lock.json --discovery-manifest /reference/lemma-discovery.json'

OUTPUT="$(
  python3 "$REPO/tools/klean_audit_contract.py" prepare \
    --repo "$REPO" --run-id "$RUN_ID" --problem "$PROBLEM" \
    --expected-resolved-input-sha256 "$RESOLVED_INPUT_SHA256" \
    "${REPLACE_ARGUMENT[@]}"
)"

python3 - \
  "$RESOLUTION" "$OUTPUT/audit-input.json" "$IMAGE_ID" "$OUTPUT" "$REPO" "$CHECKER_LOCK" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[5])
from tools.audit_contract import write_json_atomic

document = json.load(open(sys.argv[1], encoding="utf-8"))
document["audit"] = {
    "image_id": sys.argv[3],
    "model": "gpt-5.6-sol",
    "effort": "xhigh",
    "memory_bytes": 8 * 1024**3,
    "memory_swap_bytes": 8 * 1024**3,
    "timeout_s": 3600,
    "output": sys.argv[4],
    "fresh_session": True,
    "mechanical_checker_lock_sha256": hashlib.sha256(
        Path(sys.argv[6]).read_bytes()
    ).hexdigest(),
}
write_json_atomic(Path(sys.argv[2]), document)
PY
chmod 0444 "$OUTPUT/audit-input.json"

AUTH="$REPO/docker/codex/secrets/codex/auth.json"
PROMPT="$REPO/prompts/klean-audit.md"
KIT_SKILLS="$REPO/data/skills"
WRAPPER="$HERE/entrypoint.sh"
SUPERVISOR="$REPO/docker/audit/entrypoint.sh"
for path in "$AUTH" "$PROMPT" "$WRAPPER" "$SUPERVISOR"; do
  [[ -f "$path" && ! -L "$path" ]] || {
    echo "Stage 6 required file must be real: $path" >&2
    exit 2
  }
done
[[ -f "$DISCOVERY_MANIFEST" && ! -L "$DISCOVERY_MANIFEST" ]] || {
  echo "Stage 6 discovery manifest must be real: $DISCOVERY_MANIFEST" >&2
  exit 2
}
for path in "$KIT_SKILLS" "$REPO/tools" "$GENERATION_PRODUCER_SOURCES"; do
  [[ -d "$path" && ! -L "$path" ]] || {
    echo "Stage 6 required directory must be real: $path" >&2
    exit 2
  }
done

AUDIT_MOUNTS=(
  --mount "type=bind,source=$K_WORKSPACE,target=/reference/k-proof,readonly"
  --mount "type=bind,source=$K_AUDIT,target=/reference/k-audit,readonly"
  --mount "type=bind,source=$DISCOVERY_MANIFEST,target=/reference/lemma-discovery.json,readonly"
  --mount "type=bind,source=$KLEAN_GENERATION,target=/reference/klean-generation,readonly"
  --mount "type=bind,source=$GENERATION_PRODUCER_SOURCES,target=/reference/generation-tools,readonly"
)
if [[ "$AUDIT_MODE" == "CLASSIFICATION_AND_PROOF" ]]; then
  AUDIT_MOUNTS+=(
    --mount "type=bind,source=$LEAN_WORKSPACE,target=/candidate,readonly"
  )
fi

set +e
docker run --rm -i --init --pull=never \
  --security-opt seccomp=unconfined \
  --memory "$MEMORY" --memory-swap "$MEMORY" \
  --env "AUDIT_PROBLEM_ID=$PROBLEM" \
  --env "AUDIT_CONDITION=$CONDITION" \
  --env "AUDIT_SEMANTICS_MODE=$SEMANTICS_MODE" \
  --env "AUDIT_MODE=$AUDIT_MODE" \
  "${AUDIT_MOUNTS[@]}" \
  --mount "type=bind,source=$REPO/tools,target=/reference/tools,readonly" \
  --mount "type=bind,source=$TOOLCHAIN_LOCK,target=/reference/klean-toolchain.lock.json,readonly" \
  --mount "type=bind,source=$KIT_SKILLS,target=/kit-skills,readonly" \
  --mount "type=bind,source=$AUTH,target=/auth/auth.json,readonly" \
  --mount "type=bind,source=$PROMPT,target=/audit-prompt.md,readonly" \
  --mount "type=bind,source=$OUTPUT/audit-input.json,target=/audit-input.json,readonly" \
  --mount "type=bind,source=$WRAPPER,target=/klean-audit-entrypoint.sh,readonly" \
  --mount "type=bind,source=$SUPERVISOR,target=/independent-audit-entrypoint.sh,readonly" \
  --mount "type=bind,source=$OUTPUT,target=/audit-output" \
  --workdir /audit-output \
  --entrypoint /klean-audit-entrypoint.sh \
  "$IMAGE_ID"
DOCKER_RC=$?
set -e

MECHANICAL_MOUNTS=(
  --mount "type=bind,source=$K_WORKSPACE,target=/reference/k-proof,readonly"
  --mount "type=bind,source=$DISCOVERY_MANIFEST,target=/reference/lemma-discovery.json,readonly"
  --mount "type=bind,source=$KLEAN_GENERATION,target=/reference/klean-generation,readonly"
  --mount "type=bind,source=$TOOLCHAIN_LOCK,target=/reference/klean-toolchain.lock.json,readonly"
  --mount "type=bind,source=$OUTPUT/audit-input.json,target=/audit-input.json,readonly"
)
MECHANICAL_ARGUMENTS=(
  --frozen-k /reference/k-proof
  --discovery-manifest /reference/lemma-discovery.json
  --generation /reference/klean-generation
  --toolchain-lock /reference/klean-toolchain.lock.json
  --audit-input /audit-input.json
)
if [[ "$AUDIT_MODE" == "CLASSIFICATION_AND_PROOF" ]]; then
  MECHANICAL_MOUNTS+=(
    --mount "type=bind,source=$LEAN_WORKSPACE,target=/candidate,readonly"
  )
  MECHANICAL_ARGUMENTS+=(--candidate /candidate)
fi

set +e
docker run --rm --network none --pull=never \
  --memory "$MEMORY" --memory-swap "$MEMORY" \
  "${MECHANICAL_MOUNTS[@]}" \
  --entrypoint python3 \
  "$IMAGE_ID" \
  /opt/humaneval/tools/klean_final_gate.py \
  "${MECHANICAL_ARGUMENTS[@]}" \
  >"$MECHANICAL_TMP"
MECHANICAL_RC=$?
set -e

set +e
python3 - "$MECHANICAL_TMP" "$OUTPUT/mechanical-check.json" <<'PY'
import json
import os
import sys
from pathlib import Path

source = Path(sys.argv[1])
destination = Path(sys.argv[2])
document = json.loads(source.read_text())
if document.get("status") not in {"PASS", "FAIL", "AUDIT_ERROR"}:
    raise SystemExit("invalid mechanical gate status")
temporary = destination.with_name(f".{destination.name}.tmp")
temporary.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
os.replace(temporary, destination)
PY
MECHANICAL_PUBLISH_RC=$?
set -e

set +e
python3 "$REPO/tools/audit_contract.py" verdict \
  --review "$OUTPUT/REVIEW.md" \
  --metrics "$OUTPUT/metrics.json" \
  --output "$OUTPUT/verdict.json"
VERDICT_RC=$?
set -e

set +e
python3 "$REPO/tools/klean_audit_contract.py" reconcile \
  --verdict "$OUTPUT/verdict.json" \
  --mechanical-check "$OUTPUT/mechanical-check.json" \
  --audit-input "$OUTPUT/audit-input.json"
RECONCILE_RC=$?
set -e

FINAL_AUDIT_COMPLETE=0
if [[ "$RECONCILE_RC" -eq 0 ]] && python3 - "$OUTPUT/verdict.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    verdict = json.load(stream)
raise SystemExit(0 if verdict.get("audit_status") == "COMPLETE" else 1)
PY
then
  FINAL_AUDIT_COMPLETE=1
fi

MODEL_TRACE_AVAILABLE=0
if [[ -d "$OUTPUT/codex-trace" && ! -L "$OUTPUT/codex-trace" ]]; then
  MODEL_TRACE_AVAILABLE=1
fi

USAGE_RC=0
if [[
  "$FINAL_AUDIT_COMPLETE" -eq 1
  || "$MODEL_TRACE_AVAILABLE" -eq 1
]]; then
  set +e
  python3 "$REPO/tools/usage_accounting.py" write --trace "$OUTPUT/codex-trace" --output "$OUTPUT/usage.json"
  USAGE_RC=$?
  set -e
fi

EXPECTED_CANDIDATE_SHA256="$(
  python3 - "$REPO" "$OUTPUT" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tools.pipeline_contract import sha256_tree

print(sha256_tree(Path(sys.argv[2])))
PY
)"

set +e
python3 "$REPO/tools/klean_audit_contract.py" publish \
  --repo "$REPO" \
  --run-id "$RUN_ID" \
  --problem "$PROBLEM" \
  --candidate "$(basename "$OUTPUT")" \
  --expected-resolved-input-sha256 "$RESOLVED_INPUT_SHA256" \
  --expected-candidate-sha256 "$EXPECTED_CANDIDATE_SHA256" \
  "${REPLACE_ARGUMENT[@]}"
SELECTION_RC=$?
set -e

SUMMARY_RC=0
if [[ "$SELECTION_RC" -eq 0 ]]; then
  set +e
  flock "$REPO/runs/$RUN_ID/.usage-summary.lock" python3 "$REPO/tools/usage_accounting.py" summarize --run "$REPO/runs/$RUN_ID"
  SUMMARY_RC=$?
  set -e
fi

printf 'audit_stage=%s audit_output=%s\n' "$AUDIT_STAGE" "$OUTPUT"
if [[
  "$DOCKER_RC" -ne 0
  || "$MECHANICAL_RC" -ne 0
  || "$MECHANICAL_PUBLISH_RC" -ne 0
  || "$VERDICT_RC" -ne 0
  || "$RECONCILE_RC" -ne 0
  || "$USAGE_RC" -ne 0
  || "$SELECTION_RC" -ne 0
  || "$SUMMARY_RC" -ne 0
]]; then
  exit 1
fi
