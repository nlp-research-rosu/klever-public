#!/usr/bin/env python3
import ast
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent

EXPECTED_SOURCE = """\
def reverse_delete(s, c):
    result = ""
    reversed_result = ""
    ch = ""
    for ch in s:
        if ch not in c:
            result += ch
            reversed_result = ch + reversed_result
    return (result, result == reversed_result)
"""

EXPECTED_CLOSURE = """\
closureVal(
  ("s", "c", .ParamNames),
  Assign(Name("result"), Str(""))
  Assign(Name("reversed_result"), Str(""))
  Assign(Name("ch"), Str(""))
  For(
    Name("ch"),
    Name("s"),
    If(
      Compare(Name("ch"), CmpOp("not in", Name("c"))),
      AugAssign(Name("result"), "+", Name("ch"))
      Assign(
        Name("reversed_result"),
        BinOp("+", Name("ch"), Name("reversed_result"))),
      .Stmts))
  Return(
    TupleExpr(
      Name("result"),
      Compare(
        Name("result"),
        CmpOp("==", Name("reversed_result")))))
  .Stmts,
  0)
"""


def compact(text):
    return "".join(text.split())


def function(tree):
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef))


def main():
    prompt_tree = ast.parse((ROOT / "prompt.py").read_text(encoding="utf-8"))
    solution_text = (ROOT / "solution.py").read_text(encoding="utf-8")
    solution_tree = ast.parse(solution_text)
    expected_tree = ast.parse(EXPECTED_SOURCE)

    prompt_function = function(prompt_tree)
    solution_function = function(solution_tree)
    assert prompt_function.name == solution_function.name == "reverse_delete"
    assert [arg.arg for arg in prompt_function.args.args] == ["s", "c"]
    assert [arg.arg for arg in solution_function.args.args] == ["s", "c"]
    assert ast.dump(solution_tree) == ast.dump(expected_tree)

    translated = subprocess.run(
        ["python3", str(ROOT / "py2mpy.py"), str(ROOT / "solution.py")],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout
    assert translated == (ROOT / "solution.mpy").read_text(encoding="utf-8")

    spec_text = (ROOT / "spec.k").read_text(encoding="utf-8")
    assert compact(EXPECTED_CLOSURE) in compact(spec_text)
    print("Program identity: prompt signature, solution.mpy, and spec body match")


if __name__ == "__main__":
    main()
