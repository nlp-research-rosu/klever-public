import re


def compact(text):
    return re.sub(r"\s+", "", text).replace(".Stmts", "")


with open("solution.mpy", encoding="utf-8") as solution_file:
    translated = compact(solution_file.read())

prefix = 'Module(FuncDef("count_upper",Params("s"),'
if not translated.startswith(prefix) or not translated.endswith("))"):
    raise AssertionError("unexpected solution.mpy wrapper")

# Remove Module(FuncDef(..., and the two closing delimiters for FuncDef/Module.
body = translated[len(prefix):-2]

with open("spec.k", encoding="utf-8") as spec_file:
    specification = compact(spec_file.read())

exact_closure = 'closureVal(("s",.ParamNames),' + body + ",0)"
if specification.count(exact_closure) != 1:
    raise AssertionError("SPEC.count-upper does not contain the exact translated body")

print("SPEC_PROGRAM_IDENTITY=PASS")
