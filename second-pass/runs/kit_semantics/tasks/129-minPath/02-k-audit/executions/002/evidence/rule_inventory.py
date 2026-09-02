#!/usr/bin/env python3
"""Location-complete inventory of all local supplied and proof K constructs."""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

work = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/audit-work/minpath-129")
paths = [work / "reference-semantics" / "semantics.k"]
paths += sorted((work / "reference-semantics" / "semantics").glob("*.k"))
paths += [work / "verification.k", work / "spec.k"]

starter = re.compile(r"^\s*(requires|module|imports|syntax|configuration|context|rule|claim|endmodule)\b")
attribute_names = (
    "function", "functional", "total", "symbol", "no-evaluators", "priority",
    "simplification", "concrete", "trusted", "owise", "macro", "macro-rec",
    "strict", "seqstrict", "anywhere",
)
records = []
by_file = collections.Counter()
by_kind = collections.Counter()
by_attr = collections.Counter()

for path in paths:
    lines = path.read_text().splitlines()
    starts = []
    for idx, line in enumerate(lines):
        match = starter.match(line)
        if match:
            starts.append((idx, match.group(1)))
    for pos, (idx, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        statement = " ".join(part.strip() for part in lines[idx:end] if part.strip() and not part.lstrip().startswith("//"))
        attrs = [name for name in attribute_names if re.search(r"\b" + re.escape(name) + r"(?:\b|\()", statement)]
        rel = path.relative_to(work).as_posix()
        record = {
            "source": rel,
            "line": idx + 1,
            "kind": kind,
            "attributes": attrs,
            "sha256": hashlib.sha256(statement.encode()).hexdigest(),
            "statement": statement,
        }
        records.append(record)
        by_file[rel] += 1
        by_kind[kind] += 1
        by_attr.update(attrs)

print("SUMMARY=" + json.dumps({
    "source_files": len(paths),
    "records": len(records),
    "by_kind": dict(sorted(by_kind.items())),
    "by_attribute": dict(sorted(by_attr.items())),
    "by_file": dict(sorted(by_file.items())),
}, sort_keys=True))
for number, record in enumerate(records, 1):
    print("RECORD=" + json.dumps({"number": number, **record}, sort_keys=True))
