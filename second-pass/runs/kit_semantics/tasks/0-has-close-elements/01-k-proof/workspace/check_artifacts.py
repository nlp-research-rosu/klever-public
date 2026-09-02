import ast
import subprocess


def normalized(text):
    return "".join(text.split())


def target_function(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef)
                 and node.name == "has_close_elements"]
    assert len(functions) == 1
    return functions[0]


def main():
    generated = subprocess.check_output(
        ["python3", "py2mpy.py", "solution.py"], text=True)
    recorded = open("solution.mpy", encoding="utf-8").read()
    spec = open("spec.k", encoding="utf-8").read()

    assert generated == recorded, "solution.mpy is stale"
    claim_spelling = normalized(generated).replace(
        ",),)", ",.Stmts),.Stmts)")
    assert claim_spelling.rstrip() in normalized(spec), (
        "spec.k does not contain the exact translated program module")

    prompt_function = target_function("prompt.py")
    solution_function = target_function("solution.py")
    smoke_function = target_function("smoke.py")

    assert [arg.arg for arg in prompt_function.args.args] == [
        arg.arg for arg in solution_function.args.args
    ], "entry-point parameters changed"
    assert ast.dump(solution_function) == ast.dump(smoke_function), (
        "smoke.py implementation drifted from solution.py")
    print("artifact identity checks: passed")


if __name__ == "__main__":
    main()
