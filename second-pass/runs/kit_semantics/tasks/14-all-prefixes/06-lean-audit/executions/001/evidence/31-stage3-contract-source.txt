#!/usr/bin/env python3
"""Validate Stage 3 classifications against the canonical K rule inventory."""

from __future__ import annotations

import json
import stat
from pathlib import Path
from typing import Any

from tools.k_rule_inventory import KRuleInventoryError, inventory_verification


_MANIFEST_KEYS = {"schema_version", "inventory_sha256", "rules"}
_RULE_KEYS = {"source_rule_id", "classification", "rationale"}
_CLASSIFICATIONS = {
    "DEFINITION",
    "OPERATIONAL_RULE",
    "PROVED_DERIVED_LEMMA",
    "DOMAIN_LEMMA",
}


class LemmaDiscoveryContractError(RuntimeError):
    """Raised when a Stage 3 manifest crosses its trust boundary."""


def _regular_json(path: Path) -> dict[str, Any]:
    path = Path(path)
    try:
        mode = path.stat(follow_symlinks=False).st_mode
    except OSError as error:
        raise LemmaDiscoveryContractError(
            f"lemma discovery manifest must be a regular file: {path}"
        ) from error
    if not stat.S_ISREG(mode):
        raise LemmaDiscoveryContractError(
            f"lemma discovery manifest must be a regular file: {path}"
        )
    try:
        document = json.loads(path.read_bytes())
    except (OSError, UnicodeError, ValueError) as error:
        raise LemmaDiscoveryContractError(
            f"lemma discovery manifest is malformed: {path}"
        ) from error
    if not isinstance(document, dict):
        raise LemmaDiscoveryContractError(
            "lemma discovery manifest must be a JSON object"
        )
    return document


def _exact_keys(
    document: dict[str, Any], expected: set[str], label: str
) -> None:
    unexpected = sorted(set(document) - expected)
    if unexpected:
        raise LemmaDiscoveryContractError(
            f"{label} has unexpected key: {unexpected[0]}"
        )
    missing = sorted(expected - set(document))
    if missing:
        raise LemmaDiscoveryContractError(
            f"{label} is missing key: {missing[0]}"
        )


def validate_trust_boundary(
    workspace: Path, manifest: Path
) -> dict[str, Any]:
    try:
        inventory = inventory_verification(Path(workspace))
    except KRuleInventoryError as error:
        raise LemmaDiscoveryContractError(str(error)) from error
    document = _regular_json(Path(manifest))
    _exact_keys(document, _MANIFEST_KEYS, "lemma discovery manifest")
    schema_version = document["schema_version"]
    if (
        not isinstance(schema_version, int)
        or isinstance(schema_version, bool)
        or schema_version != 2
    ):
        raise LemmaDiscoveryContractError(
            "lemma discovery schema_version must be 2"
        )
    if document["inventory_sha256"] != inventory["inventory_sha256"]:
        raise LemmaDiscoveryContractError(
            "lemma discovery inventory_sha256 does not match canonical inventory"
        )
    entries = document["rules"]
    if not isinstance(entries, list):
        raise LemmaDiscoveryContractError(
            "lemma discovery rules must be a JSON list"
        )
    canonical_rules = inventory["rules"]
    canonical_by_id = {
        rule["source_rule_id"]: rule for rule in canonical_rules
    }
    classified_by_id: dict[str, dict[str, str]] = {}
    for index, entry in enumerate(entries):
        label = f"lemma discovery rule {index}"
        if not isinstance(entry, dict):
            raise LemmaDiscoveryContractError(f"{label} must be an object")
        _exact_keys(entry, _RULE_KEYS, label)
        source_rule_id = entry["source_rule_id"]
        if not isinstance(source_rule_id, str) or not source_rule_id:
            raise LemmaDiscoveryContractError(
                f"{label} source_rule_id must be a nonempty string"
            )
        if source_rule_id in classified_by_id:
            raise LemmaDiscoveryContractError(
                f"duplicate lemma discovery source_rule_id: {source_rule_id}"
            )
        if source_rule_id not in canonical_by_id:
            raise LemmaDiscoveryContractError(
                f"unknown lemma discovery source_rule_id: {source_rule_id}"
            )
        classification = entry["classification"]
        if (
            not isinstance(classification, str)
            or classification not in _CLASSIFICATIONS
        ):
            raise LemmaDiscoveryContractError(
                f"{label} classification must be DEFINITION, "
                "OPERATIONAL_RULE, PROVED_DERIVED_LEMMA, or DOMAIN_LEMMA"
            )
        canonical_rule = canonical_by_id[source_rule_id]
        if (
            "simplification" in canonical_rule["attributes"]
            and classification
            in {"OPERATIONAL_RULE", "PROVED_DERIVED_LEMMA"}
        ):
            raise LemmaDiscoveryContractError(
                f"{label} simplification rule must be classified as "
                "DEFINITION or DOMAIN_LEMMA"
            )
        rationale = entry["rationale"]
        if not isinstance(rationale, str) or not rationale.strip():
            raise LemmaDiscoveryContractError(
                f"{label} rationale must be a nonempty string"
            )
        classified_by_id[source_rule_id] = {
            "classification": classification,
            "rationale": rationale,
        }
    missing = [
        rule["source_rule_id"]
        for rule in canonical_rules
        if rule["source_rule_id"] not in classified_by_id
    ]
    if missing:
        raise LemmaDiscoveryContractError(
            f"lemma discovery manifest is missing source_rule_id: {missing[0]}"
        )
    definitions: list[dict[str, Any]] = []
    operational_rules: list[dict[str, Any]] = []
    proved_derived_lemmas: list[dict[str, Any]] = []
    domain_lemmas: list[dict[str, Any]] = []
    for rule in canonical_rules:
        classification = classified_by_id[rule["source_rule_id"]]
        classified_rule = {**rule, **classification}
        role = classification["classification"]
        if role == "DEFINITION":
            definitions.append(classified_rule)
        elif role == "OPERATIONAL_RULE":
            operational_rules.append(classified_rule)
        elif role == "PROVED_DERIVED_LEMMA":
            proved_derived_lemmas.append(classified_rule)
        else:
            domain_lemmas.append(classified_rule)
    return {
        **inventory,
        "definitions": definitions,
        "operational_rules": operational_rules,
        "proved_derived_lemmas": proved_derived_lemmas,
        "domain_lemmas": domain_lemmas,
    }
