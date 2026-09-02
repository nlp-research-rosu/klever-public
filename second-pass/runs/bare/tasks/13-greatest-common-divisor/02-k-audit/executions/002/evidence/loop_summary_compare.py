#!/usr/bin/env python3
"""Compare the proved loop claim with the manually installed summary rule."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Iterator

work = Path("/tmp/audit-work/reconstruction")
emitted_path = work / "loop-spec-emitted-for-comparison.json"
command = [
    "kprove",
    "loop-spec.k",
    "--definition",
    "loop-haskell-audit",
    "--spec-module",
    "LOOP-SPEC",
    "--dry-run",
    "--emit-json-spec",
    str(emitted_path),
    "--output",
    "none",
]
print("COMMAND:", " ".join(command))
completed = subprocess.run(
    command,
    cwd=work,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)
print(f"EXIT_STATUS: {completed.returncode}")
print(completed.stdout.rstrip())
if completed.returncode != 0:
    raise SystemExit("could not emit loop claim")

claim_json = json.loads(emitted_path.read_text())
claim_module = next(
    module
    for module in claim_json["term"]["term"]
    if module["name"] == "LOOP-SPEC"
)
claim = next(
    sentence
    for sentence in claim_module["localSentences"]
    if sentence["node"] == "KClaim"
)

rule_json = json.loads(
    (work / "verification-json-audit" / "parsed.json").read_text()
)
rule_module = next(
    module
    for module in rule_json["term"]["modules"]
    if module["name"] == "VERIFICATION"
)
summary = next(
    sentence
    for sentence in rule_module["localSentences"]
    if sentence["node"] == "KRule"
)


def children(node: Any) -> Iterator[dict[str, Any]]:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "att":
                continue
            if isinstance(value, dict):
                yield value
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        yield item


def walk(node: dict[str, Any]) -> Iterator[dict[str, Any]]:
    yield node
    for child in children(node):
        yield from walk(child)


def label(node: dict[str, Any]) -> str | None:
    value = node.get("label")
    return value.get("name") if isinstance(value, dict) else None


def find_label(node: dict[str, Any], name: str) -> dict[str, Any]:
    return next(candidate for candidate in walk(node) if label(candidate) == name)


def find_rewrite(node: dict[str, Any]) -> dict[str, Any]:
    return next(candidate for candidate in walk(node) if candidate.get("node") == "KRewrite")


def erase_casts(node: Any) -> Any:
    if isinstance(node, list):
        return [erase_casts(item) for item in node]
    if not isinstance(node, dict):
        return node
    if label(node) in {
        "#SemanticCastToInt",
        "#SemanticCastToK",
        "#SemanticCastToMap",
    }:
        return erase_casts(node["args"][0])
    if node.get("node") == "KVariable":
        return {
            key: erase_casts(value)
            for key, value in node.items()
            if key not in {"att", "sort"}
        }
    return {
        key: erase_casts(value)
        for key, value in node.items()
        if key != "att"
    }


claim_k = find_label(claim["body"], "<k>")
rule_k = find_label(summary["body"], "<k>")
claim_env = find_label(claim["body"], "<env>")
rule_env = find_label(summary["body"], "<env>")
claim_loop = find_label(claim_k, "execStmt(_)_MPY_KItem_Stmt")
rule_loop = find_label(rule_k, "execStmt(_)_MPY_KItem_Stmt")
claim_env_rewrite = find_rewrite(claim_env)
rule_env_rewrite = find_rewrite(rule_env)

loop_equal = erase_casts(claim_loop) == erase_casts(rule_loop)
env_equal = erase_casts(claim_env_rewrite) == erase_casts(rule_env_rewrite)
requires_equal = erase_casts(claim["requires"]) == erase_casts(summary["requires"])
rule_priority = summary["att"]["att"].get("priority")

print(f"loop_constructor_equal={loop_equal}")
print(f"environment_rewrite_equal={env_equal}")
print(f"requires_equal={requires_equal}")
print(f"summary_priority={rule_priority}")
print("proved_claim_k_context=exact empty continuation")
print("installed_rule_k_context=framed continuation via source ellipsis")

if not (loop_equal and env_equal and requires_equal and rule_priority == "40"):
    raise SystemExit("installed loop summary differs materially from the proved claim")
