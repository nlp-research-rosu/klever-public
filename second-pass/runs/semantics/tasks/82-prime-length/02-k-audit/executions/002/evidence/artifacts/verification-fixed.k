requires "reference-semantics/semantics.k"

module VERIFICATION-FIXED
  imports MPY

  syntax Stmts ::= "primeLoopBodyFixed" [function]
  rule primeLoopBodyFixed
    => If(
         Compare(
           BinOp("%", Name("n"), Name("divisor")),
           CmpOp("==", Int(0))),
         Return(Bool(false)) .Stmts,
         .Stmts)
       AugAssign(Name("divisor"), "+", Int(1))
       .Stmts

  syntax Stmts ::= "primeBodyFixed" [function]
  rule primeBodyFixed
    => Assign(Name("n"), Call(Name("len"), (Name("string"), .Exprs)))
       If(
         Compare(Name("n"), CmpOp("<", Int(2))),
         Return(Bool(false)) .Stmts,
         .Stmts)
       Assign(Name("divisor"), Int(2))
       While(
         Compare(Name("divisor"), CmpOp("<", Name("n"))),
         primeLoopBodyFixed)
       Return(Bool(true))
       .Stmts

  syntax Val ::= "primeLengthClosureFixed" [function]
  rule primeLengthClosureFixed
    => closureVal(("string", .ParamNames), primeBodyFixed, 0)

  // Syntax only: the fixed semantics has no rewrite to this proof marker.
  syntax KItem ::= #primeLoopEntryFixed(Int, Int)
endmodule
