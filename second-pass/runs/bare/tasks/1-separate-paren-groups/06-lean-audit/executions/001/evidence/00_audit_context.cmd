printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
if test -e /candidate; then echo 'candidate=present'; else echo 'candidate=absent'; fi
sha256sum /audit-input.json
PYTHONPATH=/reference python3 -c 'from tools.stage6_resolution_contract import verify_audit_input; import json; from pathlib import Path; r,d=verify_audit_input(json.loads(Path("/audit-input.json").read_text())); print("verified_mode="+r["mode"]); print("resolved_input_sha256="+d)'
