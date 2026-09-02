#!/usr/bin/env python3
import json
import re
from pathlib import Path

candidate_path = Path("/candidate/Proof.lean")
candidate = candidate_path.read_text()
target = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)["target"]
inventory = json.loads(Path("/reference/lemma-discovery.json").read_text())
rule_class = {
    rule["source_rule_id"]: rule["classification"]
    for rule in inventory["rules"]
}

records = []
for parameter in target["parameters"]:
    name = parameter["name"]
    pattern = re.compile(
        r"(?m)^(?:noncomputable\s+)?def\s+"
        + re.escape(name)
        + r"(?=\s|\()"
    )
    matches = list(pattern.finditer(candidate))
    definitions = []
    for match in matches:
        next_comment = candidate.find("\n/- KORE symbol:", match.end())
        next_theorem = candidate.find("\n@[simp]", match.end())
        ends = [end for end in (next_comment, next_theorem) if end >= 0]
        end = min(ends) if ends else len(candidate)
        definitions.append(
            {
                "start_line": candidate.count("\n", 0, match.start()) + 1,
                "text": candidate[match.start() : end].rstrip(),
            }
        )
    records.append(
        {
            **parameter,
            "candidate_definition_count": len(matches),
            "candidate_definitions": definitions,
            "source_classifications": [
                rule_class[source_rule_id]
                for source_rule_id in parameter["source_rule_ids"]
            ],
        }
    )

print(
    json.dumps(
        {
            "candidate": str(candidate_path),
            "parameter_count": len(target["parameters"]),
            "all_parameters_have_exactly_one_candidate_definition": all(
                record["candidate_definition_count"] == 1
                for record in records
            ),
            "parameters": records,
        },
        indent=2,
        sort_keys=True,
    )
)
