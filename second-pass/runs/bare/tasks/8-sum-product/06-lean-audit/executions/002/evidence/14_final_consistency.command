set -euo pipefail
printf 'REVIEW final pair\n'
tail -n 2 /audit-output/REVIEW.md
test "$(tail -n 2 /audit-output/REVIEW.md)" = \
  $'VERDICT: PASS\nLEGITIMACY: LEGIT'
printf '\nCritical check maps\n'
python3 - <<'PY'
import json
from pathlib import Path

for name in (
    "03_inventory_audit.result",
    "07_hash_ledger.result",
    "13_independent_stage3_stage4_judgment.result",
):
    document = json.loads((Path("/audit-output/evidence") / name).read_text())
    failed = [key for key, value in document["checks"].items() if value is not True]
    print(f"{name}: checks={len(document['checks'])} failed={failed}")
    if failed:
        raise SystemExit(1)

preflight = json.loads(
    Path(
        "/audit-output/evidence/11_preflight_rerun_with_pid_shim.result"
    ).read_text()
)
returned = preflight["returned_evidence"]
print(
    "preflight:",
    returned["status"],
    "obligations=",
    returned["obligation_count"],
    "target=",
    returned["target"],
)
assert returned["status"] == "KLEAN_NO_OBLIGATIONS"
assert returned["obligation_count"] == 0
assert returned["target"] is None
assert all(item["exit_code"] == 0 for item in preflight["command_evidence"])
PY
printf '\nEvidence files\n'
rg --files /audit-output/evidence | sort
