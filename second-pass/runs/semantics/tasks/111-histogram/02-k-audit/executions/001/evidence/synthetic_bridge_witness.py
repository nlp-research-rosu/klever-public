#!/usr/bin/env python3
"""Concrete counterexample to interpreting tokenText as real string text."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load_histogram(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    args = parser.parse_args()
    canonical = load_histogram("canonical_bridge_witness", args.canonical)
    generated = load_histogram("generated_bridge_witness", args.generated)
    concrete_text = "a b"
    synthetic_claim_expected = {"a b": 1}
    canonical_value = canonical(concrete_text)
    generated_value = generated(concrete_text)
    print(
        json.dumps(
            {
                "A_codepoints": [97, 32, 98],
                "concrete_text": concrete_text,
                "synthetic_c06_expected": synthetic_claim_expected,
                "canonical_on_concrete_text": canonical_value,
                "generated_on_concrete_text": generated_value,
                "synthetic_expected_equals_real": (
                    synthetic_claim_expected == generated_value
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if synthetic_claim_expected != generated_value else 1


if __name__ == "__main__":
    raise SystemExit(main())
