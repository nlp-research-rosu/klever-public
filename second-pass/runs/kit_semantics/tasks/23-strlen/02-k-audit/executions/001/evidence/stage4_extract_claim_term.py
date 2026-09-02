#!/usr/bin/env python3
"""Extract the exact Module term executed by #loadAll in the target claim."""

from __future__ import annotations

import argparse
from pathlib import Path


def matching_paren(text: str, open_index: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced parentheses")


parser = argparse.ArgumentParser()
parser.add_argument("spec")
parser.add_argument("output")
parser.add_argument("--rule-output")
args = parser.parse_args()

text = Path(args.spec).read_text(encoding="utf-8")
needle = "#loadAll("
positions = []
start = 0
while True:
    position = text.find(needle, start)
    if position < 0:
        break
    positions.append(position)
    start = position + len(needle)
if len(positions) != 1:
    raise SystemExit(f"expected one #loadAll occurrence, found {len(positions)}")

open_index = positions[0] + len("#loadAll")
close_index = matching_paren(text, open_index)
module_term = text[open_index + 1 : close_index].strip()
if not module_term.startswith("Module("):
    raise SystemExit("#loadAll argument is not a Module term")

continuation = text[close_index + 1 :]
required_fragments = [
    '~> Call(Name("strlen"), (str(CS:IntSeq), .Exprs))',
    "=> isLen(CS)",
    "<env> 0 </env>",
    '"strlen" |-> closureVal(',
    '"string" , .ParamNames,',
    'Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts,',
    "<scopeLoc> 1 </scopeLoc>",
    "<heap> .Map </heap>",
    "<heapLoc> 0 </heapLoc>",
    "<stack> .List </stack>",
    "<ret> noRet </ret>",
    "<exc> NoExc </exc>",
    "<exit-code> 0 </exit-code>",
]
missing = [fragment for fragment in required_fragments if fragment not in continuation]
if missing:
    raise SystemExit(f"claim pinning fragments missing: {missing}")

Path(args.output).write_text(module_term + "\n", encoding="utf-8")
if args.rule_output:
    Path(args.rule_output).write_text(
        f"#loadAll({module_term}) => #loadAll({module_term})\n",
        encoding="utf-8",
    )
print(f"spec={args.spec}")
print(f"loadAll_occurrences={len(positions)}")
print(f"extracted_module={args.output}")
if args.rule_output:
    print(f"rule_wrapper={args.rule_output}")
print("invocation=Call(Name(\"strlen\"), (str(CS:IntSeq), .Exprs))")
print("destination=isLen(CS)")
print("configuration_pins=env,scopes,scopeLoc,heap,heapLoc,stack,ret,exc,exit-code")
print("CLAIM_TERM_EXTRACTION_OK")
