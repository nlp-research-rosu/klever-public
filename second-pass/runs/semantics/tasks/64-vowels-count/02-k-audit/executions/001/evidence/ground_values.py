#!/usr/bin/env python3
from differential_test import CANONICAL, GENERATED, outcome

inputs = ["", "a", "y", "by", "abcde", "ACEDY", "yellowy"]
for value in inputs:
    print(
        f"{value!r}: canonical={outcome(CANONICAL, value)!r} "
        f"generated={outcome(GENERATED, value)!r}"
    )
