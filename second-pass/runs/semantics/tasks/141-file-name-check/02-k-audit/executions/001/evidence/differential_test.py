#!/usr/bin/env python3
"""Independent differential test for HumanEval 141.

The candidate implementation is imported from the clean scratch copy.  The
oracle implementation is imported from the trusted /reference mount.  The
small contract_oracle below is an independent rendering of prompt.py and is
used only to diagnose which side of a differential mismatch matches the
natural-language contract.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")
CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/141-file-name-check/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


def contract_oracle(file_name: str) -> str:
    """Literal prompt contract: ASCII letters/digits and exactly one dot."""
    valid = (
        file_name.count(".") == 1
        and bool(file_name.split(".", 1)[0])
        and ("A" <= file_name[0] <= "Z" or "a" <= file_name[0] <= "z")
        and file_name.rsplit(".", 1)[1] in {"txt", "exe", "dll"}
        and sum("0" <= ch <= "9" for ch in file_name) <= 3
    )
    return "Yes" if valid else "No"


documented_and_boundaries = [
    "example.txt",
    "1example.dll",
    "",
    ".",
    ".txt",
    "a.txt",
    "A.txt",
    "Z9.dll",
    "a123.txt",
    "a1234.txt",
    "a0.txt",
    "a012.txt",
    "a0123.txt",
    "a0000.txt",
    "a9z8y7.txt",
    "a9z8y7x6.dll",
    "a.tx",
    "a.txtx",
    "a.pdf",
    "a..txt",
    "atxt",
    "a.",
    "....",
    "@.txt",
    "A.exe",
    "Z.dll",
    "[.txt",
    "`.txt",
    "z.txt",
    "{.txt",
    "é.txt",
    "Ω.exe",
    "a١٢٣.txt",
    "a١٢٣٤.txt",
    "é١٢٣٤.dll",
]

generated = []
alphabet = "aZ0._é١"
suffixes = ("", ".txt", ".exe", ".dll", ".pdf", "txt", "..txt")
for length in range(0, 4):
    for chars in itertools.product(alphabet, repeat=length):
        base = "".join(chars)
        generated.extend(base + suffix for suffix in suffixes)

rng = random.Random(141)
random_alphabet = "abAZ09._-éΩ١"
for _ in range(750):
    length = rng.randrange(0, 13)
    generated.append("".join(rng.choice(random_alphabet) for _ in range(length)))

inputs = list(dict.fromkeys(documented_and_boundaries + generated))
canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
candidate = load_entry(GENERATED_PATH, "scratch_candidate")

rows = []
for text in inputs:
    expected = contract_oracle(text)
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    rows.append(
        {
            "input": text,
            "contract": expected,
            "canonical": canonical_result,
            "candidate": candidate_result,
        }
    )

payload = json.dumps(inputs, ensure_ascii=False, indent=2) + "\n"
(EVIDENCE / "differential_inputs.json").write_text(payload, encoding="utf-8")
(EVIDENCE / "differential_results.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

candidate_vs_canonical = [
    row for row in rows if row["candidate"] != row["canonical"]
]
candidate_vs_contract = [row for row in rows if row["candidate"] != row["contract"]]
canonical_vs_contract = [row for row in rows if row["canonical"] != row["contract"]]

print(f"input_count={len(inputs)}")
print(f"input_json_sha256={hashlib.sha256(payload.encode()).hexdigest()}")
print(f"candidate_vs_canonical_mismatches={len(candidate_vs_canonical)}")
print(f"candidate_vs_contract_mismatches={len(candidate_vs_contract)}")
print(f"canonical_vs_contract_mismatches={len(canonical_vs_contract)}")
print("candidate_vs_canonical_examples=")
print(json.dumps(candidate_vs_canonical[:40], ensure_ascii=False, indent=2))

if candidate_vs_contract:
    raise SystemExit("candidate diverges from the literal prompt contract")
