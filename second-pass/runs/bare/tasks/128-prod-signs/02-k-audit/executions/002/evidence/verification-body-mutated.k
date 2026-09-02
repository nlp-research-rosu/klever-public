requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Mathematical contract, independent of the program's control flow.
  syntax Int ::= "magnitude" "(" Int ")" [function, total]
               | "integerSign" "(" Int ")" [function, total]
               | "sumMagnitudes" "(" Ints ")" [function, total]
               | "productSigns" "(" Ints ")" [function, total]
  syntax Value ::= "contract" "(" Ints ")" [function, total]

  rule magnitude(I) => 0 -Int I requires I <Int 0
  rule magnitude(I) => I        requires I >=Int 0

  rule integerSign(I) => -1 requires I <Int 0
  rule integerSign(0) => 0
  rule integerSign(I) => 1  requires I >Int 0

  rule sumMagnitudes(.Ints) => 0
  rule sumMagnitudes(I, IS) => magnitude(I) +Int sumMagnitudes(IS)

  rule productSigns(.Ints) => 1
  rule productSigns(I, IS) => integerSign(I) *Int productSigns(IS)

  rule contract(.Ints) => none
  rule contract(I, IS)
    => sumMagnitudes(I, IS) *Int productSigns(I, IS)

  // These constants are a readable embedding of solution.mpy.  The loop body
  // is also named so the inductive loop-step claims in spec.k stay compact.
  syntax Stmts ::= "solutionLoopBody" [function]
  rule solutionLoopBody =>
    If(Compare(Name("x"), CmpOp("<", Int(0))),
      Assign(Name("total"), BinOp("-", Name("total"), Name("x")))
      Assign(Name("sign"), UnaryOp("-", Name("sign"))),
      Assign(Name("total"), BinOp("-", Name("total"), Name("x")))
      If(Compare(Name("x"), CmpOp("==", Int(0))),
        Assign(Name("sign"), Int(0)),
        .Stmts))

  syntax Stmts ::= "solutionBody" [function]
  rule solutionBody =>
    If(Compare(Name("arr"), CmpOp("==", ListExpr(.Exprs))),
      Return(NoneVal),
      .Stmts)
    Assign(Name("total"), Int(0))
    Assign(Name("sign"), Int(1))
    Assign(Name("x"), Int(0))
    For(Name("x"), Name("arr"), solutionLoopBody)
    Return(BinOp("*", Name("total"), Name("sign")))

  syntax Pgm ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("prod_signs", Params("arr"), solutionBody))
endmodule
