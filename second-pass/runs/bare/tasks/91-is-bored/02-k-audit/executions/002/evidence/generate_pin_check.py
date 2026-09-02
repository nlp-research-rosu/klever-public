#!/usr/bin/env python3
"""Generate a K claim from K's parsed trusted-translator reconstruction."""

from pathlib import Path


term = Path(
    "/tmp/audit-work/reconstruction/parsed-regenerated.term"
).read_text().rstrip()
output = Path("/tmp/audit-work/reconstruction/pin-check.k")
output.write_text(
    'requires "verification.k"\n\n'
    "module PIN-CHECK\n"
    "  imports VERIFICATION\n\n"
    "  claim <k> done </k>\n"
    "        <program> solutionModule =>\n"
    + "\n".join("          " + line for line in term.splitlines())
    + " </program>\n"
    '        <input> "" </input>\n'
    "        <result> 0 </result>\n"
    + "\nendmodule\n"
)
