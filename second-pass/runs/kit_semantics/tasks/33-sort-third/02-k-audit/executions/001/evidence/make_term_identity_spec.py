#!/usr/bin/env python3
"""Create a K claim comparing translated and entry-claim program constructors."""

from __future__ import annotations

import pathlib


SCRATCH = pathlib.Path("/tmp/audit-work/33-sort-third")
translated = (SCRATCH / "solution.mpy").read_text(encoding="utf-8").strip()
claimed = (SCRATCH / "claimed-program.mpy").read_text(encoding="utf-8").strip()
specification = f"""requires "verification.k"

module TERM-IDENTITY
  imports VERIFICATION

  claim
    {translated}
    =>
    {claimed}
endmodule
"""
(SCRATCH / "term-identity.k").write_text(specification, encoding="utf-8")
print(f"translated_characters={len(translated)}")
print(f"claimed_characters={len(claimed)}")
print(f"output={SCRATCH / 'term-identity.k'}")
