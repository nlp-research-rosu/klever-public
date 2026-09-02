#!/usr/bin/env python3
"""Ground witnesses for the formal preconditions and model boundary."""

from __future__ import annotations

import importlib.util
from typing import Callable


def load(path: str, name: str) -> Callable[[str, list[str]], str]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


def fixed_model(class_name: str, extensions: list[str]) -> str:
    """The verification.k result equations use ASCII isUpperC/isLowerC."""

    def score(extension: str) -> int:
        return sum(
            1
            if 65 <= ord(character) <= 90
            else -1
            if 97 <= ord(character) <= 122
            else 0
            for character in extension
        )

    if not extensions:
        return class_name + "."
    best = extensions[0]
    best_score = score(best)
    for extension in extensions[1:]:
        extension_score = score(extension)
        if extension_score > best_score:
            best = extension
            best_score = extension_score
    return class_name + "." + best


def main() -> int:
    canonical = load("/reference/canonical.py", "canonical_witness")
    candidate = load("/candidate/solution.py", "candidate_witness")
    cases = [
        ("entry-empty", "", []),
        ("entry-nonempty-ascii", "C", ["A", "b"]),
        ("supplied-model-greek-gap", "C", ["A", "ΩΩ"]),
        ("candidate-roman-defect", "C", ["A", "ⅠⅠ"]),
    ]
    observed: dict[str, tuple[str, str, str]] = {}
    for label, class_name, extensions in cases:
        model = fixed_model(class_name, extensions)
        canon = (
            canonical(class_name, extensions)
            if extensions
            else "<canonical raises IndexError>"
        )
        generated = candidate(class_name, extensions)
        observed[label] = (model, canon, generated)
        print(
            f"{label}: inputs=({class_name!r}, {extensions!r}) "
            f"fixed_model={model!r} canonical={canon!r} candidate={generated!r}"
        )

    assert observed["entry-empty"] == (".", "<canonical raises IndexError>", ".")
    assert observed["entry-nonempty-ascii"] == ("C.A", "C.A", "C.A")
    assert observed["supplied-model-greek-gap"] == ("C.A", "C.ΩΩ", "C.ΩΩ")
    assert observed["candidate-roman-defect"] == ("C.A", "C.A", "C.ⅠⅠ")
    print("witness_assertions=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
