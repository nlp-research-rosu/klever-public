from pathlib import Path


def compact(text):
    return "".join(text.split())


def call_args(text, start, name):
    prefix = name + "("
    if not text.startswith(prefix, start):
        raise ValueError(f"expected {prefix!r} at offset {start}")
    args = []
    arg_start = start + len(prefix)
    depth = 0
    in_string = False
    escaped = False
    index = arg_start
    while index < len(text):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                args.append(text[arg_start:index])
                return args
            depth -= 1
        elif char == "," and depth == 0:
            args.append(text[arg_start:index])
            arg_start = index + 1
        index += 1
    raise ValueError(f"unterminated {name} call")


mpy = compact(Path("solution.mpy").read_text(encoding="utf-8"))
module_args = call_args(mpy, 0, "Module")
function_args = call_args(module_args[0], 0, "FuncDef")
if function_args[:2] != ['"fizz_buzz"', 'Params("n")']:
    raise SystemExit("solution.mpy has an unexpected entry-point signature")

spec = compact(Path("spec.k").read_text(encoding="utf-8"))
closure_start = spec.index('closureVal("n",')
closure_args = call_args(spec, closure_start, "closureVal")
if closure_args[0] != '"n"' or closure_args[2] != "0":
    raise SystemExit("spec.k has an unexpected closure binding")
spec_body = closure_args[1].replace(".Stmts", "")
mpy_body = function_args[2].replace(".Stmts", "")
if spec_body != mpy_body:
    mismatch = next(
        (
            index
            for index, (left, right) in enumerate(
                zip(spec_body, mpy_body)
            )
            if left != right
        ),
        min(len(spec_body), len(mpy_body)),
    )
    raise SystemExit(
        "spec.k closure body differs from solution.mpy near "
        f"{spec_body[mismatch:mismatch + 80]!r} versus "
        f"{mpy_body[mismatch:mismatch + 80]!r}"
    )

print("program-identity: PASS")
