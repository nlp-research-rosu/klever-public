requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Closed constructor terms used by the specification.  The body is exactly
  // the tree in solution.mpy; the named abbreviation keeps proof states small
  // and does not shortcut execution to a result.
  syntax Stmts ::= "multiplyBody" [symbol(multiplyBody)]
  rule multiplyBody =>
    If(Compare(Name("a"), CmpOp("<", Int(0))),
       Assign(Name("a"), UnaryOp("-", Name("a"))), .Stmts)
    If(Compare(Name("b"), CmpOp("<", Int(0))),
       Assign(Name("b"), UnaryOp("-", Name("b"))), .Stmts)
    Return(BinOp("*",
                 BinOp("%", Name("a"), Int(10)),
                 BinOp("%", Name("b"), Int(10))))

  syntax Program ::= "multiplyProgram" [symbol(multiplyProgram)]
  rule multiplyProgram =>
    Module(FuncDef("multiply", Params("a", "b"), multiplyBody))

  // Mathematical definition of an integer's decimal unit digit.
  syntax Int ::= "unitDigit" "(" Int ")" [function, total,
                                             symbol(unitDigit)]
  rule unitDigit(I) => absInt(I) %Int 10
endmodule
