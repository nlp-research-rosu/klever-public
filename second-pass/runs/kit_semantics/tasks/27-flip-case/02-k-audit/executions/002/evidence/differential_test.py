#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for flip_case."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/rebuild")
RESULT_PATH = Path("/audit-output/evidence/differential-results.json")
SEED = 2700729


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


def ascii_oracle(text: str) -> str:
    result = []
    for character in text:
        code = ord(character)
        if 65 <= code <= 90:
            result.append(chr(code + 32))
        elif 97 <= code <= 122:
            result.append(chr(code - 32))
        else:
            result.append(character)
    return "".join(result)


candidate = load_function(SCRATCH / "solution.py", "audited_candidate")
canonical = load_function(SCRATCH / "canonical.py", "trusted_canonical")

named_cases = {
    "documented_example": "Hello",
    "empty": "",
    "lower_boundary_below": "@",
    "upper_A": "A",
    "upper_Z": "Z",
    "upper_boundary_above": "[",
    "lower_boundary_below_2": "`",
    "lower_a": "a",
    "lower_z": "z",
    "lower_boundary_above": "{",
    "mixed": "aZ 123!?",
    "all_ascii": "".join(chr(code) for code in range(128)),
    "embedded_nul": "\x00AaZz\x00",
    "unicode_latin": "éÉ",
    "unicode_expansion": "ß",
    "unicode_greek": "Σσς",
    "unicode_turkish": "İı",
    "unicode_ligature": "ﬀ",
    "emoji_and_marks": "🙂e\u0301",
}

alphabet = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789 !?@[]`{}"
    "éÉßΣσςİıﬀ🙂\u0301"
)
rng = random.Random(SEED)
generated_cases = []
for length in (0, 1, 2, 3, 7, 31):
    for _ in range(40):
        generated_cases.append("".join(rng.choice(alphabet) for _ in range(length)))

all_cases = list(named_cases.items()) + [
    (f"generated_{index:03d}", value) for index, value in enumerate(generated_cases)
]

mismatches = []
ascii_oracle_mismatches = []
records = []
for name, value in all_cases:
    candidate_result = candidate(value)
    canonical_result = canonical(value)
    record = {
        "name": name,
        "input": value,
        "input_codepoints": [ord(character) for character in value],
        "candidate": candidate_result,
        "candidate_codepoints": [ord(character) for character in candidate_result],
        "canonical": canonical_result,
        "canonical_codepoints": [ord(character) for character in canonical_result],
    }
    records.append(record)
    if candidate_result != canonical_result:
        mismatches.append(record)
    if value.isascii() and candidate_result != ascii_oracle(value):
        ascii_oracle_mismatches.append(record)

serialized_inputs = json.dumps(
    [(name, value) for name, value in all_cases],
    ensure_ascii=False,
    separators=(",", ":"),
).encode()
result = {
    "oracle": str(SCRATCH / "canonical.py"),
    "candidate": str(SCRATCH / "solution.py"),
    "seed": SEED,
    "named_case_count": len(named_cases),
    "generated_case_count": len(generated_cases),
    "total_case_count": len(all_cases),
    "input_manifest_sha256": hashlib.sha256(serialized_inputs).hexdigest(),
    "candidate_canonical_mismatch_count": len(mismatches),
    "ascii_oracle_mismatch_count": len(ascii_oracle_mismatches),
    "mismatches": mismatches,
    "ascii_oracle_mismatches": ascii_oracle_mismatches,
    "records": records,
}
RESULT_PATH.write_text(
    json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
    encoding="utf-8",
)

print(f"seed={SEED}")
print(f"named_cases={len(named_cases)}")
print(f"generated_cases={len(generated_cases)}")
print(f"total_cases={len(all_cases)}")
print(f"input_manifest_sha256={result['input_manifest_sha256']}")
print(f"candidate_canonical_mismatches={len(mismatches)}")
print(f"ascii_oracle_mismatches={len(ascii_oracle_mismatches)}")
print(
    "unicode_boundary_witness="
    + json.dumps(
        {
            "input": "éß",
            "input_codepoints": [ord(character) for character in "éß"],
            "canonical_output": canonical("éß"),
            "canonical_output_codepoints": [
                ord(character) for character in canonical("éß")
            ],
        },
        ensure_ascii=False,
        sort_keys=True,
    )
)
if mismatches or ascii_oracle_mismatches:
    raise SystemExit(1)
print("DIFFERENTIAL_STATUS=PASS")
