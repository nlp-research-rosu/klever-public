#!/usr/bin/env python3
"""Print trusted Python results for the exact concrete K smoke-test inputs."""

import importlib.util
import json
import sys


spec = importlib.util.spec_from_file_location("trusted_canonical_concrete", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

cases = [
    [],
    [0],
    [-2, 0, 5],
    [1, 2, 3],
    [10**50, -(10**50)],
]
for values in cases:
    print(json.dumps({"input": values, "trusted_python_result": module.incr_list(values)}))
