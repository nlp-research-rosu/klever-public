#!/usr/bin/env bash
set -uo pipefail

export PATH="$HOME/.nix-profile/bin:$PATH"
printf '%s\n' '$ command -v kompile kprove krun python3'
command -v kompile kprove krun python3
printf 'command_lookup_exit=%s\n' "$?"
printf '%s\n' '$ kompile --version'
kompile --version
printf 'kompile_version_exit=%s\n' "$?"
printf '%s\n' '$ kprove --version'
kprove --version
printf 'kprove_version_exit=%s\n' "$?"
printf '%s\n' '$ krun --version'
krun --version
printf 'krun_version_exit=%s\n' "$?"
printf '%s\n' '$ python3 --version'
python3 --version
printf 'python_version_exit=%s\n' "$?"
