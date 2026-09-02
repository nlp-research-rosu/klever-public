#!/usr/bin/env python3
import hashlib
import importlib.util
import math
import re
from pathlib import Path


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.closest_integer


def balanced_term(text: str, constructor: str, start_at: int = 0):
    marker = constructor + "("
    start = text.index(marker, start_at)
    open_pos = start + len(constructor)
    depth = 0
    quote = None
    escaped = False
    for pos in range(open_pos, len(text)):
        ch = text[pos]
        if quote is not None:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in {'"', "'"}:
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return start, pos + 1, text[start : pos + 1]
    raise ValueError(f"unterminated {constructor} at {start}")


def constructor_args(term: str, constructor: str):
    assert term.startswith(constructor + "(") and term.endswith(")")
    inner = term[len(constructor) + 1 : -1]
    args = []
    depth = 0
    quote = None
    escaped = False
    last = 0
    for pos, ch in enumerate(inner):
        if quote is not None:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in {'"', "'"}:
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            args.append(inner[last:pos])
            last = pos + 1
    args.append(inner[last:])
    return args


def normalize_body(body: str):
    # The translator prints empty Stmts list arguments as blank positions,
    # while the spec spells the same syntax-list unit explicitly.
    body = body.replace(".Stmts", "")
    return re.sub(r"\s+", "", body)


solution_mpy = Path("/candidate/solution.mpy").read_text()
spec_k = Path("/candidate/spec.k").read_text()

_, _, func_term = balanced_term(solution_mpy, "FuncDef")
func_args = constructor_args(func_term, "FuncDef")
assert len(func_args) == 3
assert normalize_body(func_args[0]) == '"closest_integer"'
assert normalize_body(func_args[1]) == 'Params("value")'
translated_body = normalize_body(func_args[2])

closure_bodies = []
cursor = 0
while True:
    try:
        start, end, closure_term = balanced_term(spec_k, "closureVal", cursor)
    except ValueError:
        break
    args = constructor_args(closure_term, "closureVal")
    assert len(args) == 3
    assert normalize_body(args[0]) == '"value"'
    assert normalize_body(args[2]) == "0"
    closure_bodies.append(normalize_body(args[1]))
    cursor = end

print(f"closure_count={len(closure_bodies)}")
print(
    "translated_body_sha256="
    + hashlib.sha256(translated_body.encode()).hexdigest()
)
for idx, body in enumerate(closure_bodies, 1):
    digest = hashlib.sha256(body.encode()).hexdigest()
    print(
        f"closure_{idx}_body_sha256={digest} "
        f"matches_translated={body == translated_body}"
    )
assert len(closure_bodies) == 4
assert all(body == translated_body for body in closure_bodies)

normalized_spec = re.sub(r"\s+", "", spec_k)
call = 'Call(Name("closest_integer"),str(CS:IntSeq))'
print(f"entry_call_count={normalized_spec.count(call)}")
assert normalized_spec.count(call) == 4

for pinned in (
    "<env>0</env>",
    "<scopeLoc>1</scopeLoc>",
    "<heap>.Map</heap>",
    "<heapLoc>0</heapLoc>",
    "<stack>.List</stack>",
    "<ret>noRet</ret>",
    "<exc>NoExc</exc>",
    "<exit-code>0</exit-code>",
):
    count = normalized_spec.count(pinned)
    print(f"pinned_cell={pinned} count={count}")
    assert count == 4

candidate = load_function("candidate_pin", "/candidate/solution.py")
canonical = load_function("canonical_pin", "/reference/canonical.py")

witnesses = [
    ("closest-positive-lower", "15.3", "positive-lower"),
    ("closest-positive-upper", "14.5", "positive-upper"),
    ("closest-nonpositive-upper", "-14.3", "nonpositive-upper"),
    ("closest-nonpositive-lower", "-14.5", "nonpositive-lower"),
]

print("satisfying_witnesses")
for label, text, expected_branch in witnesses:
    f = float(text)
    lower = math.floor(f)
    upper = math.ceil(f)
    positive = 0 < f
    dl_lt = f - float(lower) < 0.5
    du_lt = float(upper) - f < 0.5
    if positive:
        branch = "positive-lower" if dl_lt else "positive-upper"
        post = lower if dl_lt else upper
    else:
        branch = "nonpositive-upper" if du_lt else "nonpositive-lower"
        post = upper if du_lt else lower
    cand = candidate(text)
    canon = canonical(text)
    print(
        f"  label={label} input={text!r} F={f!r} lower={lower} upper={upper} "
        f"positive={positive} dl_lt_half={dl_lt} du_lt_half={du_lt} "
        f"branch={branch} substituted_post={post} candidate={cand} canonical={canon}"
    )
    assert branch == expected_branch
    assert cand == post
    assert canon == post
