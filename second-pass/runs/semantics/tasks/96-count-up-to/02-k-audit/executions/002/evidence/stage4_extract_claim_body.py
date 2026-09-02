#!/usr/bin/env python3
"""Mechanically extract the entry claim's executed body as an MPY module."""

from pathlib import Path


spec = Path("/candidate/spec.k").read_text(encoding="utf-8")
module_start = spec.index("module COUNT-UP-TO-ENTRY-SPEC")
module_end = spec.index("endmodule", module_start)
entry_module = spec[module_start:module_end]
k_open = entry_module.index("    <k>\n") + len("    <k>\n")
k_end = entry_module.index("\n      ~> #endcall", k_open)
body = entry_module[k_open:k_end]

# Rule syntax writes collection units explicitly; MPY program syntax writes the
# same empty list productions by omission.
body = body.replace(".Exprs", "").replace(".Stmts", "")
lines = body.splitlines()
minimum_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
body = "\n".join("    " + line[minimum_indent:] for line in lines)

rendered = (
    'Module(\n'
    '  FuncDef("count_up_to", Params("n"),\n'
    f"{body}))\n"
)
output = Path("/tmp/audit-work/audit96/build/extracted-claim-program.mpy")
output.write_text(rendered, encoding="utf-8")
print(f"extracted_source=/candidate/spec.k:COUNT-UP-TO-ENTRY-SPEC")
print(f"output={output}")
print(rendered)
