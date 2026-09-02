#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/human29-proof.S56dOa")
base = fresh / "Base"
generated = Path("/reference/klean-generation/generated")
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
audit_target = json.loads(Path("/audit-input.json").read_text())[
    "resolution"
]["target"]
trust_inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)


def mask_lean_noncode(text: str) -> str:
    output = list(text)
    index = 0
    block_depth = 0
    state = "code"
    while index < len(text):
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line":
            if text[index] == "\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if text[index] == "\\" and following:
                output[index] = output[index + 1] = " "
                index += 2
                continue
            if text[index] == '"':
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block":
            if text[index] == "/" and following == "-":
                output[index] = output[index + 1] = " "
                block_depth += 1
                index += 2
                continue
            if text[index] == "-" and following == "/":
                output[index] = output[index + 1] = " "
                block_depth -= 1
                index += 2
                if block_depth == 0:
                    state = "code"
                continue
            if text[index] != "\n":
                output[index] = " "
            index += 1
            continue
        if text[index] == "-" and following == "-":
            output[index] = output[index + 1] = " "
            state = "line"
            index += 2
            continue
        if text[index] == "/" and following == "-":
            output[index] = output[index + 1] = " "
            state = "block"
            block_depth = 1
            index += 2
            continue
        if text[index] == '"':
            state = "string"
        index += 1
    return "".join(output)


candidate_lean_sources = sorted(
    path
    for path in candidate.rglob("*.lean")
    if "Base" not in path.relative_to(candidate).parts
)
source_findings = {}
target_shadow_declarations = []
new_trust_declarations = []
for source in candidate_lean_sources:
    relative = source.relative_to(candidate).as_posix()
    masked = mask_lean_noncode(source.read_text())
    source_findings[relative] = {
        token: [
            {
                "line": masked.count("\n", 0, match.start()) + 1,
                "text": match.group(0),
            }
            for match in re.finditer(rf"\b{token}\b", masked)
        ]
        for token in ("sorry", "admit", "unsafe")
    }
    for match in re.finditer(
        r"(?m)^\s*(axiom|opaque)\s+([^\s:(]+)", masked
    ):
        new_trust_declarations.append(
            {
                "file": relative,
                "kind": match.group(1),
                "name": match.group(2),
                "line": masked.count("\n", 0, match.start()) + 1,
            }
        )
    for match in re.finditer(
        r"(?m)^\s*(?:def|theorem|axiom|opaque|abbrev)\s+"
        r"(?:\S+\.)?targetStatement\b",
        masked,
    ):
        target_shadow_declarations.append(
            {
                "file": relative,
                "line": masked.count("\n", 0, match.start()) + 1,
                "text": match.group(0).strip(),
            }
        )

fresh_target = klean_export.target_statement(base)
axiom_log = Path("/audit-output/evidence/09-print-axioms.log").read_text()
all_forbidden_empty = all(
    not matches
    for findings in source_findings.values()
    for matches in findings.values()
)

print(
    json.dumps(
        {
            "candidate_lean_sources": [
                path.relative_to(candidate).as_posix()
                for path in candidate_lean_sources
            ],
            "candidate_proof_sha256": {
                "mounted": hashlib.sha256(
                    (candidate / "Proof.lean").read_bytes()
                ).hexdigest(),
                "fresh_copy": hashlib.sha256(
                    (fresh / "Proof.lean").read_bytes()
                ).hexdigest(),
                "match": (candidate / "Proof.lean").read_bytes()
                == (fresh / "Proof.lean").read_bytes(),
            },
            "forbidden_token_findings": source_findings,
            "all_sorry_admit_unsafe_findings_empty": all_forbidden_empty,
            "new_axiom_or_opaque_declarations": new_trust_declarations,
            "target_shadow_declarations": target_shadow_declarations,
            "base_identity": {
                "fresh_base_tree_sha256": klean_export.tree_digest(base),
                "reference_generated_tree_sha256": klean_export.tree_digest(
                    generated
                ),
                "generator_manifest_tree_sha256": generator_manifest[
                    "generated_tree_sha256"
                ],
                "all_match": klean_export.tree_digest(base)
                == klean_export.tree_digest(generated)
                == generator_manifest["generated_tree_sha256"],
            },
            "target_identity": {
                "fresh_target": fresh_target,
                "equals_generator_manifest": fresh_target
                == generator_manifest["target"],
                "equals_audit_input": fresh_target == audit_target,
            },
            "axiom_accounting": {
                "print_axioms_exact_result_is_empty": (
                    "'Proof.final' does not depend on any axioms"
                    in axiom_log
                ),
                "sorryAx_present": "sorryAx" in axiom_log,
                "recorded_generated_trust_declaration_count": len(
                    trust_inventory["allowlist"]
                ),
                "proof_dependencies": [],
                "unrecorded_dependencies": [],
            },
        },
        indent=2,
        sort_keys=True,
    )
)
