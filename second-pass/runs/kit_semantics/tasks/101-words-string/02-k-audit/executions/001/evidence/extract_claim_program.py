#!/usr/bin/env python3
"""Mechanically extract the Module argument executed by #loadAll in spec.k."""

from pathlib import Path


text = Path("/candidate/spec.k").read_text()
marker = "#loadAll("
start = text.index(marker) + len(marker)
depth = 0
end = None
for index in range(start, len(text)):
    character = text[index]
    if character == "(":
        depth += 1
    elif character == ")":
        if depth == 0:
            end = index
            break
        depth -= 1

if end is None:
    raise SystemExit("could not find end of #loadAll argument")

module_term = text[start:end].strip()
if not module_term.startswith("Module("):
    raise SystemExit("the #loadAll argument is not a Module constructor")

# The K rule parser spells an empty Exprs production `.Exprs`; the program
# parser spells the same empty production as the empty text between the final
# comma and closing parenthesis. This is the only syntax-level normalization.
module_term = module_term.replace(".Exprs", "")
print(module_term)
