#!/usr/bin/env python3
"""Extract the first target FuncDef from spec.k by balanced delimiters.

The output wraps exactly that constructor subtree in Module(...), allowing K's
own parser to normalize and compare it with trusted-regenerated solution.mpy.
"""

from pathlib import Path


spec_path = Path("/tmp/audit-work/case95/candidate-src/spec.k")
output_path = Path("/tmp/audit-work/case95/target-function.mpy")
text = spec_path.read_text()

target_offset = text.index("claim [target]:")
start = text.index('FuncDef("check_dict_case"', target_offset)
open_paren = text.index("(", start)
depth = 0
in_string = False
escaped = False
end = None
for index in range(open_paren, len(text)):
    char = text[index]
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
            end = index + 1
            break

if end is None:
    raise RuntimeError("unbalanced FuncDef constructor")

func_def = text[start:end]
# In claim/rule syntax K spells empty user lists as their generated terminator
# (".Exprs"); the program parser spells the same list as an empty position.
terminator_count = func_def.count(".Exprs")
program_form = func_def.replace(".Exprs", "")
output_path.write_text("Module(\n" + program_form + ")\n")
print(
    f"extracted_chars={len(func_def)} normalized_empty_exprs={terminator_count} "
    f"output={output_path}"
)
