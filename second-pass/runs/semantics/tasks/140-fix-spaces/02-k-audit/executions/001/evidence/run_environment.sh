#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run command -v kup
run command -v kompile
run command -v kprove
run command -v krun
run kompile --version
run kprove --version
run krun --version
run python3 --version
