requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  syntax Stmts ::= "loopBody" [function, total]
  rule loopBody =>
    If(Compare(Name("bracket"), CmpOp("==", Str("[")), .CmpOps),
      If(Compare(Name("state"), CmpOp("<", Int(2)), .CmpOps),
        Assign(Name("state"), BinOp("+", Name("state"), Int(1))),
        .Stmts),
      If(Compare(Name("state"), CmpOp("==", Int(2)), .CmpOps),
        Assign(Name("state"), Int(3)),
        If(Compare(Name("state"), CmpOp("==", Int(3)), .CmpOps),
          Return(Bool(true)),
          .Stmts)))

  syntax Stmts ::= "solutionBody" [function, total]
  rule solutionBody =>
    Assign(Name("state"), Int(0))
    For(Name("bracket"), Name("string"), loopBody)
    Return(Bool(false))

  syntax Module ::= "theSolution" [function, total]
  rule theSolution =>
    Module(FuncDef("is_nested", Params("string"), solutionBody))

  // Audit experiment: same equations, but no totality declaration on scan.
  syntax Bool ::= scan(Int, BString) [function]
  rule scan(_, .BString) => false
  rule scan(0, lbr BS) => scan(1, BS)
  rule scan(0, rbr BS) => scan(0, BS)
  rule scan(1, lbr BS) => scan(2, BS)
  rule scan(1, rbr BS) => scan(1, BS)
  rule scan(2, lbr BS) => scan(2, BS)
  rule scan(2, rbr BS) => scan(3, BS)
  rule scan(3, lbr BS) => scan(3, BS)
  rule scan(3, rbr _)  => true
endmodule
