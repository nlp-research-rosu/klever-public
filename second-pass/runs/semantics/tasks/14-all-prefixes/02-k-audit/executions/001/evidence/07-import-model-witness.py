#!/usr/bin/env python3
"""Show the CPython state omitted by the supplied ImportFrom trivia rule."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

path = Path("/tmp/audit-work/proof-audit.Dl0nBZ/candidate/solution.py")
spec = importlib.util.spec_from_file_location("candidate_import_state", path)
if spec is None or spec.loader is None:
    raise RuntimeError(path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print(
    json.dumps(
        {
            "List_is_bound": "List" in vars(module),
            "List_repr": repr(vars(module).get("List")),
            "all_prefixes_annotations": {
                name: repr(value)
                for name, value in module.all_prefixes.__annotations__.items()
            },
            "return_for_abc": module.all_prefixes("abc"),
            "result_depends_on_List_binding": False,
        },
        sort_keys=True,
    )
)

