#!/usr/bin/env python3
"""Generate a constructor-identity claim from the trusted-regenerated .mpy term."""

from pathlib import Path


scratch = Path("/tmp/audit-work/11-string-xor")
term_path = scratch / "regenerated-solution.mpy"
output_path = scratch / "candidate" / "audit-pinning-spec.k"
term = term_path.read_text(encoding="utf-8").rstrip()
indented = "\n".join(f"      {line}" for line in term.splitlines())
output = f"""requires "verification.k"

module AUDIT-PINNING-SPEC
  imports STRING-XOR-VERIFICATION

  claim
    <k>
      stringXorModule
      =>
{indented}
    </k>
endmodule
"""
output_path.write_text(output, encoding="utf-8")
print(f"source={term_path}")
print(f"output={output_path}")
print("PINNING_SPEC_GENERATED")
