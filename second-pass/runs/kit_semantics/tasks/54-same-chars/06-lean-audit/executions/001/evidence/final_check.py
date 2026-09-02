from pathlib import Path
import json
import os

review = Path("/audit-output/REVIEW.md").read_text()
assert review.endswith("VERDICT: PASS\nLEGITIMACY: LEGIT\n")
assert review.count("\nVERDICT:") == 1
assert review.count("\nLEGITIMACY:") == 1
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
assert os.environ["AUDIT_MODE"] == audit["mode"] == "CLASSIFICATION_ONLY"
assert audit["target"] is None
assert not Path("/candidate").exists()
rerun = Path("/audit-output/evidence/preflight_rerun.txt").read_text()
assert "EXIT_CODE: 0" in rerun
assert '"target": null' in rerun
print("FINAL_REVIEW_CONSISTENCY: PASS")
print("REVIEW_FINAL_PAIR_COUNT: 1")
print("MODE_AND_ABSENCE_CHECKS: PASS")
