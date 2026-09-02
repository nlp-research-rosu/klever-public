#!/usr/bin/env python3
"""Extract every #loadAll(Module(...)) argument from the submitted entry spec."""

from pathlib import Path


text = Path("/candidate/spec.k").read_text()
needle = "#loadAll("
offset = 0
modules: list[str] = []

while True:
    found = text.find(needle, offset)
    if found < 0:
        break
    start = found + len(needle)
    depth = 1
    index = start
    quoted = False
    escaped = False
    while index < len(text) and depth:
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        else:
            if char == '"':
                quoted = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
        index += 1
    if depth:
        raise RuntimeError(f"unbalanced #loadAll beginning at byte {found}")
    modules.append(text[start : index - 1].strip() + "\n")
    offset = index

if len(modules) != 4:
    raise RuntimeError(f"expected four entry modules, found {len(modules)}")

output_dir = Path("/tmp/audit-work/reconstruction/extracted-claim-modules")
output_dir.mkdir(exist_ok=True)
for number, module in enumerate(modules, 1):
    (output_dir / f"claim-module-{number}.mpy").write_text(module)
    # Rule syntax admits the explicit list unit `.Stmts`; the standalone MPY
    # parser spells the same empty List{Stmt,""} production as an omitted item.
    # This is the sole normalization used for constructor-level comparison.
    normalized = module.replace(", .Stmts)", ",\n)")
    (output_dir / f"claim-module-{number}.program.mpy").write_text(normalized)
print(f"extracted_modules={len(modules)}")
print(f"textually_identical={len(set(modules)) == 1}")
print("normalization=replace explicit empty .Stmts with standalone empty-list spelling")
