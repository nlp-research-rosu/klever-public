import json
from pathlib import Path

from tools.klean_final_gate import evaluate_proof_candidate


result = evaluate_proof_candidate(
    Path("/reference/klean-generation"),
    Path("/candidate"),
)
print(json.dumps(result, indent=2, sort_keys=True))
