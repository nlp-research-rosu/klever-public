#!/usr/bin/env python3
import collections
import json
from pathlib import Path


ast = json.loads(Path("/tmp/audit-work/review/solution.ast.json").read_text())["term"]
labels = collections.Counter()
tokens = collections.Counter()


def visit(node):
    if isinstance(node, dict):
        if node.get("node") == "KApply":
            labels[node["label"]["name"]] += 1
        elif node.get("node") == "KToken":
            tokens[(node["sort"]["name"], node["token"])] += 1
        for value in node.values():
            visit(value)
    elif isinstance(node, list):
        for value in node:
            visit(value)


visit(ast)
print("PROGRAM_KLABELS")
for label, count in sorted(labels.items()):
    print(f"{count}\t{label}")
print("PROGRAM_TOKENS")
for (sort, token), count in sorted(tokens.items()):
    print(f"{count}\t{sort}\t{token}")
print(f"SUMMARY unique_labels={len(labels)} unique_tokens={len(tokens)}")
