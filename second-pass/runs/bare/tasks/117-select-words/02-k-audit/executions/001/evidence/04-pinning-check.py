#!/usr/bin/env python3
"""Compare the submitted module with the universal claim's executed K term."""

from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
from pathlib import Path


def balanced_module(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise RuntimeError("unterminated Module term")


def kast_json(root: Path, path: Path) -> tuple[dict, list[str], str]:
    command = [
        "kast",
        "--definition",
        "semantic-kompiled",
        "--sort",
        "Module",
        "--output",
        "json",
        str(path),
    ]
    completed = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    print(f"COMMAND: {shlex.join(command)}")
    print(f"EXIT: {completed.returncode}")
    if completed.stderr:
        print(f"STDERR: {completed.stderr.rstrip()}")
    if completed.returncode != 0:
        raise RuntimeError(f"kast failed for {path}")
    return json.loads(completed.stdout), command, completed.stdout


def digest(document: dict) -> str:
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    root = Path("/tmp/audit-work/fresh")
    spec_text = (root / "spec.k").read_text(encoding="utf-8")
    claim = spec_text.index("claim")
    module_start = spec_text.index("Module(", claim)
    entry_term = balanced_module(spec_text, module_start)
    # K's claim parser pretty-syntax permits explicit collection units, while
    # the standalone MPY program scanner spells those same empty lists by
    # omission. Normalize only those syntax-level unit spellings before asking
    # kast for the constructor tree.
    entry_term = entry_term.replace(".Strings", "").replace(".Exprs", "")
    extracted = root / "spec-entry-program.mpy"
    extracted.write_text(entry_term + "\n", encoding="utf-8")

    submitted_json, _, _ = kast_json(root, root / "solution.mpy")
    claim_json, _, _ = kast_json(root, extracted)
    equal = submitted_json == claim_json
    print(f"submitted_kast_sha256={digest(submitted_json)}")
    print(f"claim_entry_kast_sha256={digest(claim_json)}")
    print(f"constructor_level_equal={equal}")
    print(f"extracted_claim_term={extracted}")
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
