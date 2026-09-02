#!/usr/bin/env bash
set -u

pinned_lean_root=/opt/elan/toolchains/leanprover--lean4---v4.22.0
printf '%s\n' 'COMMAND: test explicit Lean sysroot and application path'
printf '\n[LEAN_SYSROOT direct lean]\n'
LEAN_SYSROOT="$pinned_lean_root" "$pinned_lean_root/bin/lean" --version 2>&1
printf 'EXIT_CODE=%s\n' "$?"
printf '\n[LEAN_SYSROOT direct lake]\n'
LEAN_SYSROOT="$pinned_lean_root" "$pinned_lean_root/bin/lake" --version 2>&1
printf 'EXIT_CODE=%s\n' "$?"
printf '\n[explicit argv0 lean]\n'
bash -c "exec -a lean $pinned_lean_root/bin/lean --version" 2>&1
printf 'EXIT_CODE=%s\n' "$?"
printf '\n[environment libraries]\n'
env | sort | rg 'LD_|LEAN|LAKE|ELAN'
