#!/usr/bin/env python3
import re
from pathlib import Path


def tokens(text):
    text = re.sub(r"//.*", "", text)
    return re.findall(r'"(?:[^"\\]|\\.)*"|=>|[A-Za-z_#][A-Za-z0-9_#-]*|[(),.]', text)


submitted = Path("/tmp/audit-work/work/solution.mpy").read_text()
verification = Path("/tmp/audit-work/work/verification.k").read_text()

required_fragments = [
    'rule checkDictCaseModule()',
    'Module(',
    'FuncDef("check_dict_case", Params("dict"), checkDictBody())',
    'rule checkDictBody()',
    'Assign(Name("has_key"), Bool(false))',
    'Assign(Name("all_lower"), Bool(true))',
    'Assign(Name("all_upper"), Bool(true))',
    'Assign(Name("key"), NoneVal)',
    'For(Name("key"),',
    'Call(Attribute(Name("dict"), "keys"), .Exprs),',
    'checkDictLoopBody())',
    'Return(checkDictResultExpr())',
    'rule checkDictLoopBody()',
    'Assign(Name("has_key"), Bool(true))',
    'Call(Name("isinstance"), (Name("key"), Name("str"), .Exprs))',
    'Call(Attribute(Name("key"), "islower"), .Exprs)',
    'Call(Attribute(Name("key"), "isupper"), .Exprs)',
    'rule checkDictResultExpr()',
    'BoolOp("and",',
    'Name("has_key")',
    'BoolOp("or", (Name("all_lower"), Name("all_upper"), .Exprs))',
]
missing = [fragment for fragment in required_fragments if fragment not in verification]

# This is the exact constructor term obtained by recursively replacing the four
# zero-argument helper symbols with the right-hand sides of their equations.
expanded_helper = """
Module(
  FuncDef("check_dict_case", Params("dict"),
    Assign(Name("has_key"), Bool(false))
    Assign(Name("all_lower"), Bool(true))
    Assign(Name("all_upper"), Bool(true))
    Assign(Name("key"), NoneVal)
    For(Name("key"), Call(Attribute(Name("dict"), "keys"), ),
      Assign(Name("has_key"), Bool(true))
      If(UnaryOp("not", Call(Name("isinstance"), Name("key"), Name("str"))),
        Assign(Name("all_lower"), Bool(false))
        Assign(Name("all_upper"), Bool(false)),
        If(UnaryOp("not", Call(Attribute(Name("key"), "islower"), )),
          Assign(Name("all_lower"), Bool(false)),
          )
        If(UnaryOp("not", Call(Attribute(Name("key"), "isupper"), )),
          Assign(Name("all_upper"), Bool(false)),
          )))
    Return(
      BoolOp(
        "and",
        Name("has_key"),
        BoolOp("or", Name("all_lower"), Name("all_upper"))))))
"""

submitted_tokens = tokens(submitted)
expanded_tokens = tokens(expanded_helper)
print("HELPER_REQUIRED_FRAGMENTS_MISSING:", missing)
print("SUBMITTED_TOKEN_COUNT:", len(submitted_tokens))
print("EXPANDED_HELPER_TOKEN_COUNT:", len(expanded_tokens))
print("CONSTRUCTOR_TOKEN_IDENTITY:", submitted_tokens == expanded_tokens)
if submitted_tokens != expanded_tokens:
    for index, pair in enumerate(zip(submitted_tokens, expanded_tokens)):
        if pair[0] != pair[1]:
            print("FIRST_DIFFERENCE:", index, pair)
            break
raise SystemExit(1 if missing or submitted_tokens != expanded_tokens else 0)
