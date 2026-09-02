#!/usr/bin/env bash
# run_task.sh [--print-config] <config> <problem-id>
#   e.g. run_task.sh --print-config claude-code-opus-xhigh-4-8-bare 0-has-close-elements
#
# Runs ONE benchmark task in the confined container. Model, effort, and prompt
# are inferred from the config name:
#   *opus*      -> MODEL=opus        *fable*    -> MODEL=fable
#   *-xhigh-*   -> EFFORT=xhigh
#   *-bare      -> prompts/bare.md   *-semantics -> prompts/with-semantics.md
# Results (agent artifacts + metrics.json + claude-output.json) land in the
# task folder itself.
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

[[ "$CONFIG" == claude-code-* ]] || {
  echo "Not a claude-code config: $CONFIG" >&2
  exit 2
}

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

KIT=0
case "$CONFIG" in
  *-kit-semantics) CONDITION=kit-semantics; CONFIG_CORE="${CONFIG%-kit-semantics}"; PROMPT_FILE="$REPO/prompts/kit-semantics.md"; KIT=1 ;;
  *-kit)           CONDITION=kit; CONFIG_CORE="${CONFIG%-kit}"; PROMPT_FILE="$REPO/prompts/kit-bare.md"; KIT=1 ;;
  *-bare)          CONDITION=bare; CONFIG_CORE="${CONFIG%-bare}"; PROMPT_FILE="$REPO/prompts/bare.md" ;;
  *-semantics)     CONDITION=semantics; CONFIG_CORE="${CONFIG%-semantics}"; PROMPT_FILE="$REPO/prompts/with-semantics.md" ;;
  *) echo "Cannot infer condition from '$CONFIG'" >&2; exit 2 ;;
esac
if [[ "$CONFIG_CORE" =~ ^claude-code-(opus|fable)-xhigh-(.+)$ ]]; then
  MODEL="${BASH_REMATCH[1]}"
else
  echo "Invalid Claude config grammar: $CONFIG" >&2
  exit 2
fi
EFFORT=xhigh

resolve_task_dir
python3 "$REPO/tools/populate_runs.py" \
  --validate-task "$CONFIG" "$PROB" "$TASK_DIR"
[[ -f "$PROMPT_FILE" ]] || { echo "Missing prompt file: $PROMPT_FILE" >&2; exit 2; }

COMPOSE_FILES=(-f "$HERE/docker-compose.yml")
if [[ "$KIT" == 1 ]]; then
  COMPOSE_FILES+=(-f "$HERE/docker-compose.kit.yml")
fi

if [[ "$PRINT_CONFIG" == 1 ]]; then
  printf 'config=%s\n' "$CONFIG"
  printf 'problem=%s\n' "$PROB"
  printf 'task_dir=%s\n' "$TASK_DIR"
  printf 'model=%s\n' "$MODEL"
  printf 'condition=%s\n' "$CONDITION"
  printf 'prompt=%s\n' "$(basename "$PROMPT_FILE")"
  printf 'kit=%s\n' "$KIT"
  printf 'compose_file=%s\n' "docker-compose.yml"
  [[ "$KIT" == 1 ]] && printf 'compose_file=%s\n' "docker-compose.kit.yml"
  exit 0
fi

echo ">> $CONFIG / $PROB  (model=$MODEL effort=$EFFORT prompt=$(basename "$PROMPT_FILE"))" >&2
TASK_DIR="$TASK_DIR" MODEL="$MODEL" EFFORT="$EFFORT" KIT="$KIT" \
  docker compose "${COMPOSE_FILES[@]}" run --rm -T runner \
  "$(cat "$PROMPT_FILE")"
