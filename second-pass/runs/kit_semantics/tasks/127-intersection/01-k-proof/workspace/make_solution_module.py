import argparse
from pathlib import Path
import re


parser = argparse.ArgumentParser()
parser.add_argument("term_file", nargs="?", default="solution.mpy")
parser.add_argument("--constant", default="solutionModule")
parser.add_argument("--prefix", default="SOLUTION-MODULE")
args = parser.parse_args()

term = Path(args.term_file).read_text(encoding="utf-8").strip()
# The standalone .mpy parser accepts a trailing empty Stmts argument as blank
# text. Inside a K rule, spell that same list value explicitly.
term = re.sub(r",\n(?P<indent> *)\)", r",\n\g<indent>.Stmts)", term)

print('requires "reference-semantics/semantics/syntax.k"')
print()
print(f"module {args.prefix}-SYNTAX")
print("  imports MPY-SYNTAX")
print(f'  syntax Module ::= "{args.constant}" [function, total]')
print("endmodule")
print()
print(f"module {args.prefix}")
print(f"  imports {args.prefix}-SYNTAX")
print(f"  rule {args.constant}")
print("    => " + term.replace("\n", "\n       "))
print("endmodule")
