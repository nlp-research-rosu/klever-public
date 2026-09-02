#!/usr/bin/env python3
"""Extract and compare the program embedded by #runIsMultiplyPrime."""

from __future__ import annotations

import hashlib
import shlex
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/75-prime")
CANDIDATE = SCRATCH / "candidate"


def extract_balanced_argument(source: str, marker: str) -> str:
    marker_index = source.index(marker)
    open_index = marker_index + len(marker) - 1
    depth = 1
    in_string = False
    escaped = False
    for index in range(open_index + 1, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return source[open_index + 1 : index].strip() + "\n"
    raise ValueError(f"unterminated argument following {marker!r}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> None:
    print(f"command: {shlex.join(command)}")
    result = subprocess.run(command, text=True, capture_output=True)
    print(f"exit_status: {result.returncode}")
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    verification_source = (CANDIDATE / "verification.k").read_text()
    extracted = extract_balanced_argument(verification_source, "#loadAll(")
    extracted_path = SCRATCH / "extracted-verification-program.mpy"
    extracted_path.write_text(extracted)
    # `.Stmts` is K's internal empty-list spelling accepted in rule terms but
    # not by the external MPY program parser.  Replace that one explicit empty
    # list with the external empty-list spelling before parsing both programs.
    empty_list_occurrences = extracted.count(".Stmts")
    normalized_extracted = extracted.replace(".Stmts", "")
    normalized_extracted_path = (
        SCRATCH / "extracted-verification-program-normalized.mpy"
    )
    normalized_extracted_path.write_text(normalized_extracted)

    submitted = CANDIDATE / "solution.mpy"
    proof_definition = CANDIDATE / "verification-kompiled"
    submitted_kore = SCRATCH / "submitted-program.kore"
    extracted_kore = SCRATCH / "extracted-program.kore"

    common = [
        "--definition",
        str(proof_definition),
        "--module",
        "VERIFICATION",
        "--sort",
        "Module",
        "--output",
        "kore",
    ]
    run(["kast", str(submitted), *common, "--output-file", str(submitted_kore)])
    run(
        [
            "kast",
            str(normalized_extracted_path),
            *common,
            "--output-file",
            str(extracted_kore),
        ]
    )

    print(f"submitted_source_sha256={sha256(submitted)}")
    print(f"extracted_source_sha256={sha256(extracted_path)}")
    print(f"empty_stmts_normalizations={empty_list_occurrences}")
    print(
        "normalized_extracted_source_sha256="
        f"{sha256(normalized_extracted_path)}"
    )
    print(f"submitted_kore_sha256={sha256(submitted_kore)}")
    print(f"extracted_kore_sha256={sha256(extracted_kore)}")
    identical = submitted_kore.read_bytes() == extracted_kore.read_bytes()
    print(f"normalized_program_terms_identical={str(identical).lower()}")
    return 0 if identical and empty_list_occurrences == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
