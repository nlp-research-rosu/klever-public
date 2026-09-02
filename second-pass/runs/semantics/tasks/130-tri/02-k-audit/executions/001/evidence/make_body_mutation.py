#!/usr/bin/env python3
"""Generate one controlled proof-body mutation from the untrusted candidate source."""

from pathlib import Path
import sys


source = Path("/candidate/verification.k").read_text(encoding="utf-8")
old = 'Expr(Call(Attribute(Name("result"), "append"),\n                 Name("value"), .Exprs))'
new = 'Expr(Call(Attribute(Name("result"), "append"),\n                 Int(999), .Exprs))'
count = source.count(old)
if count != 1:
    raise SystemExit(f"expected exactly one append fragment, found {count}")
sys.stdout.write(source.replace(old, new))
