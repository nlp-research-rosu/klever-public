requires "semantic.k"

module VERIFICATION
  imports MPY

  // Mathematical contract: every element is strictly below the threshold.
  syntax Bool ::= allBelow(IntSeq, Int) [function, total]
  rule allBelow(nil, _T) => true
  rule allBelow(cons(I, XS), T)
    => (I <Int T) andBool allBelow(XS, T)

  // One canonical spelling of the exact translated solution, shared by claims.
  syntax Pgm ::= "solutionProgram" [macro]
  rule solutionProgram
    => Module(
         FuncDef("below_threshold", Params("l", "t"),
           For(Name("x"), Name("l"),
             If(Compare(Name("x"), CmpOp(">=", Name("t"))),
               Return(Bool(false)),
               .Stmts))
           Return(Bool(true))))
endmodule
