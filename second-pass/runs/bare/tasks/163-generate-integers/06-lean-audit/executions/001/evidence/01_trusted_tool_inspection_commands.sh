#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nEXIT_CODE=%s\n" "$rc"' EXIT

sha256sum /reference/tools/k_rule_inventory.py /reference/tools/klean_preflight.py
sed -n '1,360p' /reference/tools/k_rule_inventory.py
sed -n '1,420p' /reference/tools/klean_preflight.py
sed -n '1,340p' /reference/tools/lemma_discovery_contract.py
