#!/usr/bin/env python3
"""Mechanically extract and compare the program terms duplicated in spec.k."""

import argparse
import hashlib
import re
import sys
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/reconstruction/solution.mpy")
SPEC = Path("/tmp/audit-work/reconstruction/spec.k")


def matching_close(text: str, opening: int) -> int:
    depth = 0
    quote = False
    escaped = False
    for i in range(opening, len(text)):
        ch = text[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quote = False
            continue
        if ch == '"':
            quote = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("unbalanced constructor")


def split_top_args(body: str):
    args = []
    start = 0
    depth = 0
    quote = False
    escaped = False
    for i, ch in enumerate(body):
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quote = False
            continue
        if ch == '"':
            quote = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            args.append(body[start:i].strip())
            start = i + 1
    args.append(body[start:].strip())
    return args


def extract_calls(text: str, name: str):
    pattern = re.compile(re.escape(name) + r"\s*\(")
    calls = []
    for match in pattern.finditer(text):
        opening = text.find("(", match.start())
        close = matching_close(text, opening)
        calls.append((text[match.start():close + 1], split_top_args(text[opening + 1:close])))
    return calls


solution_text = SOLUTION.read_text()
spec_text = SPEC.read_text()
func_calls = extract_calls(solution_text, "FuncDef")
closure_calls = extract_calls(spec_text, "closureVal")
solution_whiles = extract_calls(solution_text, "While")
spec_whiles = extract_calls(spec_text, "#while")

if len(func_calls) != 1:
    raise SystemExit(f"expected one FuncDef, found {len(func_calls)}")
if len(closure_calls) != 3:
    raise SystemExit(f"expected three closureVal terms, found {len(closure_calls)}")
if len(solution_whiles) != 1:
    raise SystemExit(f"expected one solution While, found {len(solution_whiles)}")
if len(spec_whiles) != 1:
    raise SystemExit(f"expected one helper #while, found {len(spec_whiles)}")

func_args = func_calls[0][1]
if func_args[:2] != ['"f"', 'Params("n")']:
    raise SystemExit(f"unexpected function binding: {func_args[:2]}")
for _, args in closure_calls:
    if args[0] != '"n"' or args[1] != ".ParamNames" or args[3] != "0":
        raise SystemExit(f"unexpected closure header/tail: {args[:2]} {args[3:]}")

closure_bodies = [args[2] for _, args in closure_calls]
if len(set(closure_bodies)) != 1:
    raise SystemExit("entry claims contain different closure bodies")

parser = argparse.ArgumentParser()
parser.add_argument(
    "mode",
    choices=["report", "solution-module", "spec-closure-module", "solution-while", "spec-while"],
)
args = parser.parse_args()

if args.mode == "solution-module":
    print(solution_text, end="")
elif args.mode == "spec-closure-module":
    # Empty K collection tokens are available in rule syntax; concrete MPY
    # program syntax spells the same collection by omitting its elements.
    concrete_body = closure_bodies[0].replace(".Exprs", "")
    print(f'Module(FuncDef("f", Params("n"), {concrete_body}))')
elif args.mode == "solution-while":
    print(solution_whiles[0][0])
elif args.mode == "spec-while":
    print("While" + spec_whiles[0][0][len("#while"):])
else:
    compact = lambda s: re.sub(r"\s+", "", s)
    print("solution_function_name:", func_args[0])
    print("solution_params:", func_args[1])
    print("entry_closure_count:", len(closure_calls))
    print("entry_closure_headers:", [(a[0], a[1], a[3]) for _, a in closure_calls])
    print("entry_closure_bodies_textually_identical:", len(set(closure_bodies)) == 1)
    print(
        "solution_body_compact_sha256:",
        hashlib.sha256(compact(func_args[2]).encode()).hexdigest(),
    )
    print(
        "spec_body_compact_sha256:",
        hashlib.sha256(compact(closure_bodies[0]).encode()).hexdigest(),
    )
    print("helper_while_count:", len(spec_whiles))
    print(
        "solution_while_compact_sha256:",
        hashlib.sha256(compact(solution_whiles[0][0]).encode()).hexdigest(),
    )
    normalized_helper = "While" + spec_whiles[0][0][len("#while"):]
    print(
        "helper_as_while_compact_sha256:",
        hashlib.sha256(compact(normalized_helper).encode()).hexdigest(),
    )
