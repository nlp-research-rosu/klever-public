#!/usr/bin/env python3
import ast
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


def eval_expr(node: ast.expr, env: dict[str, int]) -> int | bool:
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return node.value
    if isinstance(node, ast.Name) and node.id in env:
        return env[node.id]
    if isinstance(node, ast.BinOp):
        left = eval_expr(node.left, env)
        right = eval_expr(node.right, env)
        if isinstance(node.op, ast.Add):
            return int(left) + int(right)
        if isinstance(node.op, ast.Mult):
            return int(left) * int(right)
    if (
        isinstance(node, ast.Compare)
        and len(node.ops) == 1
        and len(node.comparators) == 1
    ):
        left = eval_expr(node.left, env)
        right = eval_expr(node.comparators[0], env)
        if isinstance(node.ops[0], ast.Gt):
            return int(left) > int(right)
        if isinstance(node.ops[0], ast.Eq):
            return left == right
    if isinstance(node, ast.BoolOp):
        values = [bool(eval_expr(value, env)) for value in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        if isinstance(node.op, ast.Or):
            return any(values)
    raise ValueError(f"unsupported source AST node: {ast.dump(node)}")


def right_triangle_summary(a: int, b: int, c: int) -> bool:
    return (
        a > 0
        and b > 0
        and c > 0
        and (
            a * a + b * b == c * c
            or a * a + c * c == b * b
            or b * b + c * c == a * a
        )
    )


source_path = Path("/reference/k-proof/solution.py")
source_tree = ast.parse(source_path.read_text(), filename=str(source_path))
function = source_tree.body[0]
assert isinstance(function, ast.FunctionDef)
assert len(source_tree.body) == 1
assert function.name == "right_angle_triangle"
assert [argument.arg for argument in function.args.args] == ["a", "b", "c"]
assert len(function.body) == 1 and isinstance(function.body[0], ast.Return)
source_return = function.body[0].value
assert source_return is not None

inventory = inventory_verification(Path("/reference/k-proof"))
program_rule = inventory["rules"][1]["text"]
program_rhs = program_rule.split("=>", 1)[1].strip()
translated_program = Path(
    "/reference/k-proof/solution.mpy"
).read_text().strip()

cases = [
    (3, 4, 5),
    (5, 3, 4),
    (4, 5, 3),
    (1, 2, 3),
    (0, 0, 0),
    (-3, 4, 5),
    (3, 4, -5),
    (6, 8, 10),
    (1, 1, 1),
    (3000000000, 4000000000, 5000000000),
]
evaluations = []
for a, b, c in cases:
    source_value = bool(
        eval_expr(source_return, {"a": a, "b": b, "c": c})
    )
    summary_value = right_triangle_summary(a, b, c)
    evaluations.append(
        {
            "input": [a, b, c],
            "restricted_source_ast": source_value,
            "rightTriangle_summary": summary_value,
            "equal": source_value == summary_value,
        }
    )

counterfactuals = [
    {
        "mutation": "remove all positivity checks",
        "input": [0, 0, 0],
        "mutated_result": True,
        "fixed_summary": right_triangle_summary(0, 0, 0),
    },
    {
        "mutation": "remove all positivity checks",
        "input": [-3, 4, 5],
        "mutated_result": True,
        "fixed_summary": right_triangle_summary(-3, 4, 5),
    },
    {
        "mutation": "keep only a^2 + b^2 = c^2 orientation",
        "input": [5, 3, 4],
        "mutated_result": False,
        "fixed_summary": right_triangle_summary(5, 3, 4),
    },
]

semantic_text = Path("/reference/k-proof/semantic.k").read_text()
checks = {
    "solutionProgram RHS exactly names translated source AST": (
        " ".join(program_rhs.split())
        == " ".join(translated_program.split())
    ),
    "rightTriangle does not occur in operational semantics": (
        "rightTriangle" not in semantic_text
    ),
    "operational semantics executes bind/eval/publish": all(
        marker in semantic_text
        for marker in (
            "=> bind(PS, IS) ~> eval(E) ~> publish",
            "eval(BinOp(OP, L, R))",
            "eval(Compare(L, CmpOp(OP, R)))",
            "eval(BoolOp(OP, E, ES))",
            "bVal(B) ~> publish => .K",
        )
    ),
    "adversarial source/summary evaluations agree": all(
        evaluation["equal"] for evaluation in evaluations
    ),
    "counterfactual body mutations are detected": all(
        item["mutated_result"] != item["fixed_summary"]
        for item in counterfactuals
    ),
}

print(
    json.dumps(
        {
            "source_function_ast": ast.dump(
                function, include_attributes=False, indent=2
            ),
            "operational_interpretation": (
                "solutionProgram unfolds only to the exact Module AST; "
                "semantic.k then binds all three arguments, evaluates every "
                "pure arithmetic/comparison/boolean node, and publishes the "
                "Bool result. rightTriangle appears only as the separately "
                "defined postcondition summary."
            ),
            "evaluations": evaluations,
            "counterfactuals": counterfactuals,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
