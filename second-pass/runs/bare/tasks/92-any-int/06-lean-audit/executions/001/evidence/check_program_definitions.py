#!/usr/bin/env python3
import ast
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
inventory = inventory_verification(workspace)
rules = inventory["rules"]
solution_mpy = " ".join(
    (workspace / "solution.mpy").read_text().split()
)
program_rhs = " ".join(
    rules[0]["text"].split("=>", 1)[1].split()
)
solution_mpy_tokens = "".join(solution_mpy.split())
program_rhs_tokens = "".join(program_rhs.split())
run_any_int_rule = " ".join(rules[1]["text"].split())
verification_text = (workspace / "verification.k").read_text()

module = ast.parse((workspace / "solution.py").read_text())
function = module.body[0]
returned = function.body[0].value


def name(expression: ast.expr) -> str | None:
    return expression.id if isinstance(expression, ast.Name) else None


def exact_type_check(expression: ast.expr, variable: str) -> bool:
    return (
        isinstance(expression, ast.Compare)
        and len(expression.ops) == 1
        and isinstance(expression.ops[0], ast.Eq)
        and len(expression.comparators) == 1
        and name(expression.comparators[0]) == "int"
        and isinstance(expression.left, ast.Call)
        and name(expression.left.func) == "type"
        and len(expression.left.args) == 1
        and name(expression.left.args[0]) == variable
    )


def sum_equality(
    expression: ast.expr, left: str, right: str, result: str
) -> bool:
    return (
        isinstance(expression, ast.Compare)
        and len(expression.ops) == 1
        and isinstance(expression.ops[0], ast.Eq)
        and len(expression.comparators) == 1
        and name(expression.comparators[0]) == result
        and isinstance(expression.left, ast.BinOp)
        and isinstance(expression.left.op, ast.Add)
        and name(expression.left.left) == left
        and name(expression.left.right) == right
    )


checks = {
    "solution_has_one_function": (
        len(module.body) == 1
        and isinstance(function, ast.FunctionDef)
        and function.name == "any_int"
    ),
    "function_parameters_are_exact": (
        [argument.arg for argument in function.args.args]
        == ["x", "y", "z"]
        and not function.args.vararg
        and not function.args.kwarg
        and not function.args.defaults
    ),
    "function_has_one_return": (
        len(function.body) == 1
        and isinstance(function.body[0], ast.Return)
    ),
    "outer_expression_is_four_way_and": (
        isinstance(returned, ast.BoolOp)
        and isinstance(returned.op, ast.And)
        and len(returned.values) == 4
    ),
    "three_exact_type_checks": (
        exact_type_check(returned.values[0], "x")
        and exact_type_check(returned.values[1], "y")
        and exact_type_check(returned.values[2], "z")
    ),
    "inner_expression_is_three_way_or": (
        isinstance(returned.values[3], ast.BoolOp)
        and isinstance(returned.values[3].op, ast.Or)
        and len(returned.values[3].values) == 3
    ),
    "three_sum_equalities_are_exact": (
        sum_equality(returned.values[3].values[0], "x", "y", "z")
        and sum_equality(returned.values[3].values[1], "x", "z", "y")
        and sum_equality(returned.values[3].values[2], "y", "z", "x")
    ),
    "solution_program_rhs_is_exact_solution_mpy": (
        program_rhs_tokens == solution_mpy_tokens
    ),
    "solution_program_is_declared_macro": (
        'syntax Program ::= "solutionProgram" [macro]'
        in verification_text
    ),
    "run_any_int_is_declared_macro": (
        'syntax KItem ::= "RunAnyInt" "(" Val "," Val "," Val ")" [macro]'
        in verification_text
    ),
    "run_any_int_is_exact_invocation_alias": (
        run_any_int_rule
        == "rule RunAnyInt(X, Y, Z) => Invoke(solutionProgram, X, Y, Z)"
    ),
    "rules_have_no_guards_cells_or_attributes": all(
        not rule["attributes"]
        and "requires" not in rule["text"]
        and "ensures" not in rule["text"]
        and "<k>" not in rule["text"]
        and "<env>" not in rule["text"]
        for rule in rules
    ),
}

print(
    json.dumps(
        {
            "ast": ast.dump(module, include_attributes=False),
            "normalized_solution_mpy": solution_mpy,
            "normalized_solution_program_rhs": program_rhs,
            "normalized_run_any_int_rule": run_any_int_rule,
            "classification": {
                rules[0]["source_rule_id"]: "DEFINITION",
                rules[1]["source_rule_id"]: "DEFINITION",
            },
            "classification_basis": {
                rules[0]["source_rule_id"]: (
                    "macro naming the exact source-program constructor tree"
                ),
                rules[1]["source_rule_id"]: (
                    "macro naming the exact operational invocation term"
                ),
            },
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
