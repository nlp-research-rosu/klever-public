#!/usr/bin/env python3
from pathlib import Path
import sys


PALINDROMES = [
    value
    for value in range(1, 1001)
    if str(value) == str(value)[::-1]
]


def cumulative_counts():
    even = 0
    odd = 0
    counts = []
    for value in PALINDROMES:
        if value % 2 == 0:
            even += 1
        else:
            odd += 1
        counts.append((even, odd))
    return counts


COUNTS = cumulative_counts()


def emit_tree(first, last, indentation):
    prefix = " " * indentation
    if first == last:
        even, odd = COUNTS[first]
        return [f"{prefix}return ({even}, {odd})"]

    middle = (first + last + 1) // 2
    lines = [f"{prefix}if n < {PALINDROMES[middle]}:"]
    lines.extend(emit_tree(first, middle - 1, indentation + 4))
    lines.append(f"{prefix}else:")
    lines.extend(emit_tree(middle, last, indentation + 4))
    return lines


def write_solution():
    lines = ["def even_odd_palindrome(n):"]
    lines.extend(emit_tree(0, len(PALINDROMES) - 1, 4))
    Path("solution.py").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_smoke():
    cases = [
        (1, (0, 1)),
        (3, (1, 2)),
        (9, (4, 5)),
        (10, (4, 5)),
        (11, (4, 6)),
        (12, (4, 6)),
        (99, (8, 10)),
        (100, (8, 10)),
        (101, (8, 11)),
        (202, (9, 20)),
        (999, (48, 60)),
        (1000, (48, 60)),
    ]
    text = Path("solution.py").read_text(encoding="utf-8")
    lines = [text.rstrip(), ""]
    for value, result in cases:
        lines.append(
            f"assert even_odd_palindrome({value}) == {result!r}"
        )
    Path("smoke.py").write_text("\n".join(lines) + "\n", encoding="utf-8")


def closure_body():
    text = Path("solution.mpy").read_text(encoding="utf-8").rstrip()
    prefix = (
        'Module(\n'
        '  FuncDef("even_odd_palindrome", Params("n"),\n'
    )
    if not text.startswith(prefix) or not text.endswith("))"):
        raise SystemExit("solution.mpy has an unexpected outer shape")
    return text[len(prefix):-2]


def indent(text, amount):
    padding = " " * amount
    return "\n".join(padding + line if line else line for line in text.splitlines())


def write_verification():
    body = indent(closure_body(), 8)
    lines = [
        'requires "reference-semantics/semantics.k"',
        "",
        "module VERIFICATION",
        "  imports MPY",
        "  imports INT",
        "  imports BOOL",
        "",
        "  // Exact closure value transliterated from solution.py / solution.mpy.",
        '  syntax Val ::= "solutionClosure" "(" ")" [function, total]',
        "  rule solutionClosure()",
        "    => closureVal(",
        '         ("n", .ParamNames),',
        body + ",",
        "         0)",
    ]
    lines.extend(["endmodule", ""])
    Path("verification.k").write_text("\n".join(lines), encoding="utf-8")


def claim(label, lower, upper, inclusive_upper, even, odd):
    upper_condition = (
        f"N <=Int {upper}" if inclusive_upper else f"N <Int {upper}"
    )
    return f"""  claim [{label}]:
    <k> Call(solutionClosure(), Int(N))
      => tuple(vCons({even}, vCons({odd}, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires {lower} <=Int N andBool {upper_condition}
"""


def write_spec():
    blocks = [
        'requires "verification.k"',
        "",
        "module SPEC",
        "  imports VERIFICATION",
        "",
    ]
    for index, (even, odd) in enumerate(COUNTS):
        lower = PALINDROMES[index]
        if index + 1 < len(PALINDROMES):
            upper = PALINDROMES[index + 1]
            inclusive_upper = False
            label = f"range-{lower}-{upper - 1}"
        else:
            upper = 1000
            inclusive_upper = True
            label = "range-999-1000"
        blocks.append(
            claim(
                label,
                lower,
                upper,
                inclusive_upper,
                even,
                odd,
            )
        )
    blocks.extend(["endmodule", ""])
    Path("spec.k").write_text("\n".join(blocks), encoding="utf-8")


def write_mutation():
    text = Path("verification.k").read_text(encoding="utf-8")
    original = "Return(TupleExpr(Int(0), Int(1)))"
    mutated = "Return(TupleExpr(Int(9), Int(9)))"
    if text.count(original) != 1:
        raise SystemExit("expected exactly one n=1 return in verification.k")
    Path("verification-mutation.k").write_text(
        text.replace(original, mutated),
        encoding="utf-8",
    )


def main():
    modes = {"solution", "smoke", "k", "mutation"}
    if len(sys.argv) != 2 or sys.argv[1] not in modes:
        raise SystemExit(
            "usage: generate_artifacts.py <solution|smoke|k|mutation>"
        )
    if sys.argv[1] == "solution":
        write_solution()
    elif sys.argv[1] == "smoke":
        write_smoke()
    elif sys.argv[1] == "mutation":
        write_mutation()
    else:
        write_verification()
        write_spec()


if __name__ == "__main__":
    main()
