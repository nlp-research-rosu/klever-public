#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"

SMOKE_ROOT=""
cleanup() {
  local status=$?
  trap - EXIT
  if [[ "$SMOKE_ROOT" =~ ^/tmp/humaneval-container-smoke\.[A-Za-z0-9]{8}$ \
        && -d "$SMOKE_ROOT" && ! -L "$SMOKE_ROOT" ]]; then
    rm -rf -- "$SMOKE_ROOT"
  else
    echo "Refusing to clean unexpected smoke path: $SMOKE_ROOT" >&2
    [[ "$status" -ne 0 ]] || status=1
  fi
  exit "$status"
}
SMOKE_ROOT="$(mktemp -d /tmp/humaneval-container-smoke.XXXXXXXX)"
SMOKE_ID="${SMOKE_ROOT##*.}"
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
chmod 0755 "$SMOKE_ROOT"

SIX_STAGE_CONTRACT_TEST=(
  tests.test_klean_audit.KleanAuditTests.test_resolves_proof_bearing_and_no_obligation_modes
)
# This no-model fixture covers a one-DOMAIN_LEMMA proof route through
# 06-lean-audit as CLASSIFICATION_AND_PROOF and a SUMMARY_DEFINITION-only
# KLEAN_NO_OBLIGATIONS route through 06-lean-audit as CLASSIFICATION_ONLY.
python3 -m unittest "${SIX_STAGE_CONTRACT_TEST[@]}" -v

RUNS_ROOT="$SMOKE_ROOT/runs"
python3 - "$REPO" "$RUNS_ROOT" "$SMOKE_ROOT/problem-id" <<'PY'
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
runs_root = Path(sys.argv[2])
problem_marker = Path(sys.argv[3])
sys.path.insert(0, str(repo / "tools"))

from populate_runs import populate, validate_task_seed

configs = (
    "codex-smoke-xhigh-bare",
    "codex-smoke-xhigh-kit",
)
problem_id = json.loads((repo / "data/selection.json").read_text())["selected"][0][
    "id"
]
for config in configs:
    populate(config, repo=repo, runs_root=runs_root)
    validate_task_seed(repo, config, problem_id, runs_root / config / problem_id)
problem_marker.write_text(problem_id + "\n")
PY

PROBLEM_ID="$(<"$SMOKE_ROOT/problem-id")"
BASE_TASK="$RUNS_ROOT/codex-smoke-xhigh-bare/$PROBLEM_ID"
KIT_TASK="$RUNS_ROOT/codex-smoke-xhigh-kit/$PROBLEM_ID"

read -r -d '' COMMON_CHECKS <<'CHECKS' || true
set -euo pipefail
test "$PWD" = /work
test "$(id -u)" = 1000
test "$(id -g)" = 1000
test "$(id -un)" = agent
test "$HOME" = /home/agent
test -r prompt.py
test -r py2mpy.py
test -r run-input.json
test ! -e canonical.py
test ! -L canonical.py
command -v python3 >/dev/null
command -v kompile >/dev/null
command -v krun >/dev/null
command -v kprove >/dev/null
command -v "$1" >/dev/null
CHECKS

read -r -d '' BASE_ONLY_CHECKS <<'CHECKS' || true
test ! -e /kit-skills
test ! -L /kit-skills
CHECKS

read -r -d '' KIT_ONLY_CHECKS <<'CHECKS' || true
grep -Fxq 'name: using-kit' /kit-skills/using-kit/SKILL.md
grep -Fxq '# Proof-extension soundness contract' \
  /kit-skills/shared/proof-extension-soundness.md
awk '$2 == "/kit-skills" && $4 ~ /(^|,)ro(,|$)/ { ok=1 }
     END { exit !ok }' /proc/mounts
CHECKS

read -r -d '' CODEX_PIPELINE_CHECKS <<'CHECKS' || true
/usr/local/bin/assert-frozen-toolchain agent
command -v lean >/dev/null
command -v lake >/dev/null
python3 -c 'import pyk.klean'
python3 /opt/humaneval/tools/klean_final_gate.py --help >/dev/null
CHECKS

BASE_CHECKS="${COMMON_CHECKS}"$'\n'"${BASE_ONLY_CHECKS}"
KIT_CHECKS="${COMMON_CHECKS}"$'\n'"${KIT_ONLY_CHECKS}"

run_container() {
  local mode="$1"
  local image="$2"
  local expected_cli="$3"
  local task_dir="$4"
  local container_name
  local checks
  local -a kit_mount=()

  container_name="humaneval-container-smoke-${SMOKE_ID}-${mode}-${expected_cli}"
  if docker container inspect "$container_name" >/dev/null 2>&1; then
    echo "Refusing colliding smoke container name: $container_name" >&2
    return 1
  fi

  case "$mode" in
    base)
      checks="$BASE_CHECKS"
      ;;
    kit)
      checks="$KIT_CHECKS"
      kit_mount+=(
        --mount "type=bind,source=$REPO/data/skills,target=/kit-skills,readonly"
      )
      ;;
    *)
      echo "Unknown smoke mode: $mode" >&2
      return 2
      ;;
  esac
  if [[ "$expected_cli" == "codex" ]]; then
    checks="${checks}"$'\n'"${CODEX_PIPELINE_CHECKS}"
  fi

  printf 'Required local image: %s\n' "$image" >&2
  docker run --rm --name "$container_name" \
    --pull=never --network none --read-only \
    --entrypoint /bin/bash \
    --mount "type=bind,source=$task_dir,target=/work,readonly" \
    "${kit_mount[@]}" \
    "$image" -c "$checks" smoke "$expected_cli"
}

run_container base "humaneval-codex-runner:latest" codex "$BASE_TASK"
run_container base "humaneval-claude-runner:latest" claude "$BASE_TASK"
run_container base "humaneval-opencode-runner:latest" opencode "$BASE_TASK"
run_container kit "humaneval-codex-runner:latest" codex "$KIT_TASK"
run_container kit "humaneval-claude-runner:latest" claude "$KIT_TASK"
