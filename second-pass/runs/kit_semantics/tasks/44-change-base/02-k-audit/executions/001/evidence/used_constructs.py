#!/usr/bin/env python3
import collections
import json
from pathlib import Path


data = json.loads(
    Path("/tmp/audit-work/44-change-base/solution-parsed.json").read_text()
)
labels = collections.Counter()
tokens = collections.Counter()


def walk(term):
    if isinstance(term, dict):
        if term.get("node") == "KApply":
            labels[term["label"]["name"]] += 1
        elif term.get("node") == "KToken":
            tokens[(term["sort"]["name"], term["token"])] += 1
        for value in term.values():
            walk(value)
    elif isinstance(term, list):
        for value in term:
            walk(value)


walk(data["term"])
print(f"UNIQUE_KLABELS={len(labels)}")
for label, count in sorted(labels.items()):
    print(f"KLABEL count={count} {label}")
print(f"UNIQUE_TOKENS={len(tokens)}")
for (sort, token), count in sorted(tokens.items()):
    print(f"TOKEN count={count} sort={sort} value={token}")
