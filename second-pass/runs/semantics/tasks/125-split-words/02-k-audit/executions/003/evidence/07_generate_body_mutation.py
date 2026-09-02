#!/usr/bin/env python3
"""Mutate the K term actually executed by the entry claim."""

from pathlib import Path


WORK = Path("/tmp/audit-work/125-split-words")
verification = (WORK / "verification.k").read_text(encoding="utf-8")
needle = 'Call(Attribute(Name("txt"), "count"), Str("z"))'
replacement = 'Call(Attribute(Name("txt"), "count"), Str("a"))'
if verification.count(needle) != 1:
    raise SystemExit("expected exactly one executable final z-count")
mutated = verification.replace(needle, replacement, 1)
mutated = mutated.replace(
    "module SPLIT-WORDS-VERIFICATION",
    "module SPLIT-WORDS-BODY-MUTATION",
    1,
)
(WORK / "verification-body-mutation.k").write_text(mutated, encoding="utf-8")

spec = (WORK / "spec.k").read_text(encoding="utf-8")
spec = spec.replace('requires "verification.k"', 'requires "verification-body-mutation.k"', 1)
spec = spec.replace("module SPEC", "module SPEC-BODY-MUTATION", 1)
spec = spec.replace(
    "imports SPLIT-WORDS-VERIFICATION",
    "imports SPLIT-WORDS-BODY-MUTATION",
    1,
)
(WORK / "spec-body-mutation.k").write_text(spec, encoding="utf-8")
print("mutation=executable final txt.count('z') changed to txt.count('a')")
print("mutation_count=1")
