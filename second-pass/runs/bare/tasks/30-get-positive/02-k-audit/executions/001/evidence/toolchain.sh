#!/usr/bin/env bash
set -uo pipefail

for tool in kompile krun kprove; do
  path=$(command -v "$tool")
  printf 'TOOL %s path=%s\n' "$tool" "$path"
  "$path" --version
  printf 'TOOL_VERSION_EXIT_STATUS %s=%d\n' "$tool" "$?"
done
