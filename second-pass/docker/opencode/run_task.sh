#!/usr/bin/env bash
# run_task.sh [--print-config] <config> <problem-id>
#   e.g. run_task.sh --print-config opencode-kimi-k3-bare 0-has-close-elements
#
# Runs ONE benchmark task in the confined opencode container. Model and prompt
# are inferred from the config name:
#   opencode-kimi-k3-bare       -> openrouter/moonshotai/kimi-k3, prompts/bare.md
#   opencode-kimi-k3-semantics  -> openrouter/moonshotai/kimi-k3, prompts/with-semantics.md
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"

PRINT_CONFIG=0
if [[ "${1:-}" == "--print-config" ]]; then
  PRINT_CONFIG=1
  shift
fi

if [[ $# -ne 2 ]]; then
  echo "usage: run_task.sh [--print-config] <config> <problem-id>" >&2
  exit 2
fi
CONFIG="$1"
PROB="$2"

is_safe_component() {
  local value="$1"
  [[ "$value" =~ ^[A-Za-z0-9._-]+$ && "$value" != "." && "$value" != ".." ]]
}

is_safe_component "$CONFIG" || {
  echo "Config must be a safe path component" >&2
  exit 2
}
is_safe_component "$PROB" || {
  echo "Problem ID must be a safe path component" >&2
  exit 2
}

[[ "$CONFIG" == opencode-* ]] || { echo "Not an opencode config: $CONFIG" >&2; exit 2; }

if [[ "$CONFIG" == *-kit || "$CONFIG" == *-kit-semantics ]]; then
  echo "OpenCode runner does not support Kit conditions: $CONFIG" >&2
  exit 2
fi

resolve_task_dir() {
  local runs_dir config_path task_path
  runs_dir="$(realpath -e -- "$REPO/runs")" || {
    echo "Runs root must be a real directory" >&2
    exit 2
  }
  config_path="$runs_dir/$CONFIG"
  if [[ -L "$config_path" || ! -d "$config_path" ]]; then
    echo "Config directory must be a real directory" >&2
    exit 2
  fi
  CONFIG_DIR="$(realpath -e -- "$config_path")" || {
    echo "Config directory must be a real directory" >&2
    exit 2
  }
  if [[ "${CONFIG_DIR%/*}" != "$runs_dir" || "$CONFIG_DIR" == "$runs_dir/archive" ]]; then
    echo "Config directory must resolve directly below runs, outside archive" >&2
    exit 2
  fi
  task_path="$CONFIG_DIR/$PROB"
  if [[ -L "$task_path" || ! -d "$task_path" ]]; then
    echo "Task directory must be a real directory" >&2
    exit 2
  fi
  TASK_DIR="$(realpath -e -- "$task_path")" || {
    echo "Task directory must be a real directory" >&2
    exit 2
  }
  if [[ "${TASK_DIR%/*}" != "$CONFIG_DIR" ]]; then
    echo "Task directory must resolve directly below its config" >&2
    exit 2
  fi
}

case "$CONFIG" in
  *-bare)      CONDITION=bare; CONFIG_CORE="${CONFIG%-bare}"; PROMPT_FILE="$REPO/prompts/bare.md" ;;
  *-semantics) CONDITION=semantics; CONFIG_CORE="${CONFIG%-semantics}"; PROMPT_FILE="$REPO/prompts/with-semantics.md" ;;
  *) echo "Cannot infer condition (-bare/-semantics) from '$CONFIG'" >&2; exit 2 ;;
esac
if [[ "$CONFIG_CORE" =~ ^opencode-(.+)$ ]]; then
  SHORT="${BASH_REMATCH[1]}"
else
  echo "Invalid OpenCode config grammar: $CONFIG" >&2
  exit 2
fi
case "$SHORT" in
  kimi-k3) MODEL="openrouter/moonshotai/kimi-k3" ;;
  glm-5.2) MODEL="zai-coding-plan/glm-5.2" ;;
  *)       MODEL="${MODEL:-openrouter/$SHORT}" ;;   # fallback: explicit MODEL env wins
esac

resolve_task_dir
python3 "$REPO/tools/populate_runs.py" \
  --validate-task "$CONFIG" "$PROB" "$TASK_DIR"
[[ -f "$PROMPT_FILE" ]] || { echo "Missing prompt file: $PROMPT_FILE" >&2; exit 2; }

KIT=0
COMPOSE_FILES=(-f "$HERE/docker-compose.yml")

if [[ "$PRINT_CONFIG" == 1 ]]; then
  printf 'config=%s\n' "$CONFIG"
  printf 'problem=%s\n' "$PROB"
  printf 'task_dir=%s\n' "$TASK_DIR"
  printf 'model=%s\n' "$MODEL"
  printf 'condition=%s\n' "$CONDITION"
  printf 'prompt=%s\n' "$(basename "$PROMPT_FILE")"
  printf 'kit=%s\n' "$KIT"
  printf 'compose_file=%s\n' "docker-compose.yml"
  exit 0
fi

echo ">> $CONFIG / $PROB  (model=$MODEL prompt=$(basename "$PROMPT_FILE"))" >&2
TASK_DIR="$TASK_DIR" MODEL="$MODEL" \
  docker compose "${COMPOSE_FILES[@]}" run --rm -T runner \
  "$(cat "$PROMPT_FILE")"
