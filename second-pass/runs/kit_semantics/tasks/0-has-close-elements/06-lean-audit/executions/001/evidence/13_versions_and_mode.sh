#!/usr/bin/env bash
set -eu

env | rg '^AUDIT_MODE='
kompile --version
kprove --version
krun --version
LD_PRELOAD=/tmp/audit-work/liblean_proc_exe_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/liblean_proc_exe_shim.so lake --version
sha256sum /reference/generation-tools/klean_export.py
sha256sum /reference/generation-tools/klean.py
