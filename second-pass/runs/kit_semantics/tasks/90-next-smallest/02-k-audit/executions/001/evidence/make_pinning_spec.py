#!/usr/bin/env python3
"""Generate a K identity claim from the trusted translator's exact MPY output."""

import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("mpy", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()

term = args.mpy.read_text(encoding="utf-8").strip()
spec = f'''requires "pinning-definition.k"

module PINNING-SPEC
  imports PINNING

  // RHS is inserted verbatim from trusted py2mpy.py output.
  claim <k> pinModule(solutionProgram) => pinModule({term}) ... </k>
endmodule
'''
args.output.write_text(spec, encoding="utf-8")
print(f"source={args.mpy}")
print(f"output={args.output}")
print(f"inserted_bytes={len(term.encode('utf-8'))}")
