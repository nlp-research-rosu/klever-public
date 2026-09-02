#!/usr/bin/env bash
set -euo pipefail

# Stage 6 reuses the hardened independent-audit supervisor while keeping its
# own prompt and host-side dual-mode contract. The supervisor creates a fresh
# ephemeral CODEX_HOME for every execution.
exec /independent-audit-entrypoint.sh
