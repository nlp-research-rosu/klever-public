#!/usr/bin/env python3
"""Mechanically isolate and prove each submitted positive claim unchanged."""

from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path


def main() -> int:
    root = Path("/tmp/audit-work/fresh")
    text = (root / "spec.k").read_text(encoding="utf-8")
    module_match = re.search(r"(?m)^module SPEC\s*$", text)
    end_match = re.search(r"(?m)^endmodule\s*$", text)
    if module_match is None or end_match is None:
        raise RuntimeError("cannot locate submitted SPEC module")
    body = text[module_match.end() : end_match.start()]
    starts = [match.start() for match in re.finditer(r"(?m)^[ \t]*claim[ \t]*$", body)]
    if len(starts) != 7:
        raise RuntimeError(f"expected 7 claims, found {len(starts)}")

    failures = 0
    for index, start in enumerate(starts, 1):
        end = starts[index] if index < len(starts) else len(body)
        claim = body[start:end]
        # Comments immediately preceding the next sentence were captured after
        # the previous claim. They do not alter K, but remove them so each file
        # contains only one submitted claim sentence.
        claim = re.sub(r"(?:\n[ \t]*//[^\n]*)+\s*\Z", "\n", claim).rstrip() + "\n"
        module = f"SPEC-CLAIM-{index:02d}"
        path = root / f"spec-claim-{index:02d}.k"
        isolated = (
            'requires "verification.k"\n\n'
            f"module {module}\n"
            "  imports VERIFICATION\n\n"
            f"{claim}"
            "endmodule\n"
        )
        path.write_text(isolated, encoding="utf-8")
        command = [
            "kprove",
            path.name,
            "--definition",
            "verification-kompiled",
            "--spec-module",
            module,
        ]
        print(f"CLAIM {index} FILE: {path}")
        print(f"COMMAND: {shlex.join(command)}")
        completed = subprocess.run(
            command,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"EXIT: {completed.returncode}")
        print(completed.stdout.rstrip())
        success = completed.returncode == 0 and "#Top" in completed.stdout
        print(f"SUCCESS: {success}")
        if not success:
            failures += 1
    print(f"positive_claims=7")
    print(f"positive_claim_failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
