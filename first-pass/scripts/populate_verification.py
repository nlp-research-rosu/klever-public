#!/usr/bin/env python3
"""Populate verification/humaneval/<n>-<name>/ for every HumanEval task, and emit
a deterministic per-problem AST inventory (for downstream categorization).

Per problem (existing/hand-worked folders are LEFT ALONE — idempotent):
  solution.py   canonical solution, mechanically cleaned: drop `typing` imports,
                the docstring, and type annotations (all runtime no-ops). The
                algorithm is unchanged — per-problem rewrites (e.g. enumerate ->
                range) happen later, when the problem is actually tackled.
  solution.mpy  py2mpy(solution.py); on Unsupported, a `solution.mpy.UNSUPPORTED`
                marker records which node blocked it.
  smoke.py      cleaned solution + asserts from the docstring `>>>` examples
                (only examples that actually pass are kept).
  smoke.mpy     py2mpy(smoke.py), when the solution transliterates.

Inventory (data/humaneval/inventory.json): task_id, entry_point, folder,
py2mpy status, smoke-assert count, and an AST fact sheet (data types, control
flow, builtins/methods, float signals) — deterministic facts the categorization
workflow reasons over.

Usage: python scripts/populate_verification.py
"""
from __future__ import annotations

import ast
import doctest
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATASET = REPO / "data/humaneval/HumanEval.jsonl"
OUTROOT = REPO / "verification/humaneval"
INVENTORY = REPO / "data/humaneval/inventory.json"
PY2MPY = REPO / "scripts/py2mpy.py"

PY_BUILTINS = {
    "len", "range", "abs", "sum", "min", "max", "sorted", "reversed", "enumerate",
    "zip", "map", "filter", "round", "int", "float", "str", "bool", "list", "tuple",
    "set", "dict", "any", "all", "ord", "chr", "isinstance", "type", "pow", "divmod",
    "print", "input", "format", "repr", "hash", "iter", "next", "frozenset",
}


def folder_name(rec: dict) -> str:
    return f"{rec['task_id'].split('/')[-1]}-{rec['entry_point'].replace('_','-')}"


# ---------------------------------------------------------------------------
# Mechanical cleanup (behaviour-preserving: drops only runtime no-ops)
# ---------------------------------------------------------------------------
def clean_source(full_src: str) -> str:
    tree = ast.parse(full_src)
    body = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "typing":
            continue
        if isinstance(node, ast.Import) and all(a.name.split(".")[0] == "typing" for a in node.names):
            continue
        body.append(node)
    tree.body = body

    class Cleaner(ast.NodeTransformer):
        def _strip_func(self, node):
            self.generic_visit(node)
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(getattr(node.body[0], "value", None), ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body = node.body[1:] or [ast.Pass()]
            a = node.args
            for arg in (a.posonlyargs + a.args + a.kwonlyargs):
                arg.annotation = None
            if a.vararg:
                a.vararg.annotation = None
            if a.kwarg:
                a.kwarg.annotation = None
            node.returns = None
            return node

        visit_FunctionDef = _strip_func
        visit_AsyncFunctionDef = _strip_func

    tree = Cleaner().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree) + "\n"


def docstring_of(prompt: str) -> str:
    """Extract the function docstring from a HumanEval prompt (sig + docstring)."""
    try:
        tree = ast.parse(prompt + "\n    pass\n")
    except SyntaxError:
        return ""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            d = ast.get_docstring(node)
            if d:
                return d
    return ""


def smoke_asserts(prompt: str, clean_src: str) -> list[str]:
    """Build `assert <call> == <want>` lines from docstring examples; keep only
    those that actually pass against the cleaned solution."""
    doc = docstring_of(prompt)
    if not doc:
        return []
    try:
        examples = doctest.DocTestParser().get_examples(doc)
    except Exception:
        return []  # malformed doctest formatting — skip smoke for this one
    kept = []
    for ex in examples:
        call, want = ex.source.strip(), ex.want.strip()
        if not call or not want or "\n" in want:
            continue
        stmt = f"assert {call} == {want}"
        ns: dict = {}
        try:
            exec(clean_src, ns)
            exec(stmt, ns)
        except Exception:
            continue
        kept.append(stmt)
    return kept


# ---------------------------------------------------------------------------
# Deterministic AST fact sheet
# ---------------------------------------------------------------------------
def inventory_of(full_src: str, clean_src: str) -> dict:
    tree = ast.parse(clean_src)
    node_types: set[str] = set()
    builtins: set[str] = set()
    methods: set[str] = set()
    float_signal: set[str] = set()
    has_while = has_for = has_comp = has_recursion = has_early_return = False
    nested_loop = False
    funcnames = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

    def loops_under(node):
        return [n for n in ast.walk(node) if isinstance(n, (ast.For, ast.While))]

    for node in ast.walk(tree):
        node_types.add(type(node).__name__)
        if isinstance(node, ast.While):
            has_while = True
        if isinstance(node, ast.For):
            has_for = True
            inner = [n for n in ast.walk(node) if isinstance(n, (ast.For, ast.While)) and n is not node]
            if inner:
                nested_loop = True
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            has_comp = True
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            float_signal.add("float-literal")
        if isinstance(node, ast.Div):
            float_signal.add("true-division")
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                if f.id in PY_BUILTINS:
                    builtins.add(f.id)
                if f.id in funcnames:
                    has_recursion = True
                if f.id in ("float", "round"):
                    float_signal.add(f.id + "()")
            elif isinstance(f, ast.Attribute):
                methods.add(f.attr)
        if isinstance(node, ast.For):
            for r in ast.walk(node):
                if isinstance(r, ast.Return):
                    has_early_return = True

    # py2mpy transliterability + (if any) the blocking node
    p = subprocess.run([sys.executable, str(PY2MPY), "/dev/stdin"],
                       input=clean_src, capture_output=True, text=True)
    if p.returncode == 0:
        py2mpy = {"ok": True, "reason": ""}
    else:
        last = (p.stderr.strip().splitlines() or [""])[-1]
        reason = last.split("Unsupported:", 1)[1].strip() if "Unsupported:" in last else last
        py2mpy = {"ok": False, "reason": reason}

    return {
        "node_types": sorted(node_types),
        "builtins": sorted(builtins),
        "methods": sorted(methods),
        "float_signals": sorted(float_signal),
        "control": {
            "for": has_for, "while": has_while, "nested_loop": nested_loop,
            "comprehension": has_comp, "recursion": has_recursion,
            "early_return_in_loop": has_early_return,
        },
        "py2mpy": py2mpy,
    }


def main() -> None:
    if not DATASET.exists():
        raise SystemExit(f"dataset missing: {DATASET} (run scripts/dissect_humaneval.py)")
    records = [json.loads(l) for l in DATASET.read_text().splitlines() if l.strip()]

    inventory = []
    created = skipped = unsupported = 0
    for rec in records:
        name = folder_name(rec)
        d = OUTROOT / name
        full = rec["prompt"] + rec["canonical_solution"]
        try:
            clean = clean_source(full)
        except SyntaxError as e:
            clean = full  # leave as-is if unparseable; rare
        inv = inventory_of(full, clean)
        smoke = smoke_asserts(rec["prompt"], clean)
        inventory.append({
            "task_id": rec["task_id"], "entry_point": rec["entry_point"],
            "folder": f"verification/humaneval/{name}", "smoke_asserts": len(smoke),
            **inv,
        })
        if not inv["py2mpy"]["ok"]:
            unsupported += 1

        if d.exists():
            skipped += 1
            continue
        d.mkdir(parents=True)
        (d / "solution.py").write_text(clean)
        smoke_src = clean + "\n\n# Smoke checks from the prompt docstring (NOT hidden tests).\n" + "\n".join(smoke) + ("\n" if smoke else "")
        (d / "smoke.py").write_text(smoke_src)
        for src_name, out_name in (("solution.py", "solution.mpy"), ("smoke.py", "smoke.mpy")):
            r = subprocess.run([sys.executable, str(PY2MPY), str(d / src_name)],
                               capture_output=True, text=True)
            if r.returncode == 0:
                (d / out_name).write_text(r.stdout)
            elif out_name == "solution.mpy":
                last = (r.stderr.strip().splitlines() or [""])[-1]
                (d / "solution.mpy.UNSUPPORTED").write_text(last + "\n")
        created += 1

    INVENTORY.write_text(json.dumps(inventory, indent=2) + "\n")
    print(f"created {created}, skipped {skipped} (already present), "
          f"py2mpy-unsupported {unsupported}/{len(records)}")
    print(f"inventory -> {INVENTORY.relative_to(REPO)}")


if __name__ == "__main__":
    main()
