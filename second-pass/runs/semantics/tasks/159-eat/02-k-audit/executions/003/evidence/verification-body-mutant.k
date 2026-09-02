requires "reference-semantics/semantics.k"

module EAT-VERIFICATION
  imports MPY

  // This is the closure denoted by the FuncDef in solution.mpy.  Keeping the
  // translated statement tree here lets spec.k call the implementation with
  // symbolic arguments while using the supplied function-call semantics.
  syntax Val ::= "eatClosure" [function]

  rule eatClosure
    => closureVal(
         ("number", "need", "remaining"),
         If(
           Compare(Name("need"), CmpOp("<=", Name("remaining"))),
           Return(
             ListExpr(
               BinOp("-", Name("number"), Name("need")),
               BinOp("-", Name("remaining"), Name("need"))))
           .Stmts,
           .Stmts)
         Return(
           ListExpr(
             BinOp("+", Name("number"), Name("remaining")),
             Int(0)))
         .Stmts,
         0)
endmodule
