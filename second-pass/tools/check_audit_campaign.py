#!/usr/bin/env python3
"""Refuse to launch an audit when its frozen campaign inputs differ."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CAMPAIGN_LOCK = REPO / "data/audit-campaign.lock.json"
# The auditor's Kit is frozen for the whole campaign in its own bundle,
# independent of the moving generation Kit in data/skills.
KIT_LOCK = REPO / "data/audit-kit-skills.lock.json"
TOOLCHAIN_LOCK = REPO / "data/klean-toolchain.lock.json"
AUDIT_PROMPT = REPO / "prompts/audit.md"


class CampaignError(ValueError):
    pass


def regular_bytes(path: Path, label: str) -> bytes:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise CampaignError(f"{label} is missing: {path}") from error
    if not stat.S_ISREG(metadata.st_mode):
        raise CampaignError(f"{label} must be a real regular file: {path}")
    try:
        return path.read_bytes()
    except OSError as error:
        raise CampaignError(f"cannot read {label}: {path}") from error


def json_file(path: Path, label: str) -> tuple[dict[str, object], bytes]:
    raw = regular_bytes(path, label)
    try:
        document = json.loads(raw)
    except (UnicodeError, ValueError) as error:
        raise CampaignError(f"{label} is malformed: {path}") from error
    if not isinstance(document, dict):
        raise CampaignError(f"{label} must contain one JSON object: {path}")
    return document, raw


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check(image_id: str) -> dict[str, object]:
    campaign, _campaign_raw = json_file(CAMPAIGN_LOCK, "audit campaign lock")
    kit, kit_raw = json_file(KIT_LOCK, "Kit lock")
    toolchain, toolchain_raw = json_file(TOOLCHAIN_LOCK, "toolchain lock")
    prompt_raw = regular_bytes(AUDIT_PROMPT, "audit prompt")

    expected = {
        "schema_version": 1,
        "campaign_id": "bare-semantics-audit-20260726+kitsem-v3-20260730",
        "audit_image": "humaneval-codex-runner",
        "audit_image_id": image_id,
        "codex_cli_version": toolchain.get("codex_cli_version"),
        "k_version": toolchain.get("k_version"),
        "pyk_version": toolchain.get("pyk_version"),
        "lean_toolchain": toolchain.get("lean_toolchain"),
        "toolchain_lock_sha256": digest(toolchain_raw),
        "kit_commit": kit.get("commit"),
        "kit_skills_tree": kit.get("skills_tree"),
        "kit_plugin_version": kit.get("plugin_version"),
        "kit_lock_sha256": digest(kit_raw),
        "audit_prompt_sha256": digest(prompt_raw),
        "amendment": campaign.get("amendment"),
    }
    if campaign != expected:
        differing = sorted(
            key
            for key in set(campaign) | set(expected)
            if campaign.get(key) != expected.get(key)
        )
        raise CampaignError(
            "audit campaign inputs differ from the frozen lock: "
            + ", ".join(differing)
        )
    return campaign


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-id", required=True)
    arguments = parser.parse_args()
    try:
        campaign = check(arguments.image_id)
    except CampaignError as error:
        print(f"audit campaign error: {error}", file=sys.stderr)
        return 2
    print(
        "audit campaign OK: "
        f"{campaign['campaign_id']}, "
        f"Codex {campaign['codex_cli_version']}, "
        f"K {campaign['k_version']}, "
        f"Kit {campaign['kit_commit']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
