#!/usr/bin/env python3
"""Ground witnesses for all three entry preconditions and postconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/125-split-words")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.split_words


candidate = load("candidate_witness", WORK / "solution.py")
canonical = load("canonical_witness", WORK / "canonical.py")


def whitespace_count(text: str) -> int:
    return sum(text.count(char) for char in (" ", "\t", "\n", "\r"))


def comma_count(text: str) -> int:
    return text.count(",")


def odd_alphabet_count(text: str) -> int:
    return sum(text.count(char) for char in "bdfhjlnprtvxz")


witnesses = [
    ("whitespace", "Hello world!"),
    ("comma", ","),
    ("odd-lowercase-count", ""),
]

for label, text in witnesses:
    wc = whitespace_count(text)
    cc = comma_count(text)
    oc = odd_alphabet_count(text)
    if label == "whitespace":
        precondition = wc > 0
    elif label == "comma":
        precondition = wc <= 0 and cc > 0
    else:
        precondition = wc <= 0 and cc <= 0
    print(
        f"{label}: text={text!r}; codes={[ord(c) for c in text]}; "
        f"whitespaceCount={wc}; commaCount={cc}; oddAlphabetCount={oc}; "
        f"precondition={precondition}; candidate={candidate(text)!r}; "
        f"canonical={canonical(text)!r}"
    )

nbsp_text = "a b\u00a0c"
print(
    f"unicode_whitespace_boundary: text={nbsp_text!r}; "
    f"codes={[ord(c) for c in nbsp_text]}; "
    f"candidate={candidate(nbsp_text)!r}; canonical={canonical(nbsp_text)!r}"
)
