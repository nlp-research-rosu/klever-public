#!/usr/bin/env python3
"""Extract and normalize the actual #loadAll Module term from SPEC.find-max."""

import re
from pathlib import Path


source_path = Path("/tmp/audit-work/reconstruct-001/spec.k")
raw_output = Path("/audit-output/evidence/claim_program_extracted_raw.k")
normalized_output = Path(
    "/audit-output/evidence/claim_program_extracted_normalized.mpy"
)

source = source_path.read_text(encoding="utf-8")
entry_start = source.index("claim [find-max]:")
module_start = source.index("Module(", entry_start)

depth = 0
in_string = False
escaped = False
module_end = None
for index in range(module_start, len(source)):
    character = source[index]
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
            module_end = index + 1
            break

if module_end is None:
    raise SystemExit("unbalanced Module term")

raw = source[module_start:module_end]
normalized = re.sub(r",\s*\.Exprs\b", "", raw)
normalized = re.sub(r"\s*\.Stmts\b", "", normalized)

raw_output.write_text(raw + "\n", encoding="utf-8")
normalized_output.write_text(normalized + "\n", encoding="utf-8")

print(f"source={source_path}")
print(f"entry_offset={entry_start}")
print(f"module_offset={module_start}")
print(f"raw={raw_output}")
print(f"normalized={normalized_output}")
print(f"removed_exprs={raw.count('.Exprs')}")
print(f"removed_stmts={raw.count('.Stmts')}")
