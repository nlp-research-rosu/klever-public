#!/usr/bin/env python3
"""Probe the prompt's ambiguous non-ASCII decimal-digit boundary."""

import importlib.util


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.odd_count


canonical = load("/reference/canonical.py", "canonical_unicode_probe")
generated = load("/tmp/audit-work/113-odd-count/solution.py", "generated_unicode_probe")
cases = [["١٢٣"], ["１２３４"], ["१२३४५"]]
for values in cases:
    code_points = [[ord(ch) for ch in value] for value in values]
    all_python_decimal = all(ch.isdecimal() for value in values for ch in value)
    canonical_result = canonical(values)
    generated_result = generated(values)
    formally_ascii = all(48 <= code <= 57 for codes in code_points for code in codes)
    print(
        repr(values),
        f"code_points={code_points}",
        f"python_isdecimal={all_python_decimal}",
        f"digitCodes_guard={formally_ascii}",
        f"implementations_equal={canonical_result == generated_result}",
        f"result={generated_result!r}",
    )
