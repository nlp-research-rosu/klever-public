requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A named copy of the exact constructor tree emitted in solution.mpy.
  // Keeping it here lets the path-partition claims share one source term.
  syntax Program ::= "solutionProgram" [function, total]
  rule solutionProgram
    => Module(
         FuncDef("is_simple_power", Params("x", "n"),
           If(Compare(Name("x"), CmpOp("==", Int(1))),
             Return(Bool(true)),
             .Stmts)
           If(Compare(Name("x"), CmpOp("<", Int(1))),
             Return(Bool(false)),
             .Stmts)
           If(Compare(Name("n"), CmpOp("<", Int(2))),
             Return(Bool(false)),
             .Stmts)
           Assign(Name("power"), Name("n"))
           While(Compare(Name("power"), CmpOp("<", Name("x"))),
             Assign(Name("power"), BinOp("*", Name("power"), Name("n"))))
           Return(Compare(Name("power"), CmpOp("==", Name("x"))))))

  // For P > 0 and N >= 2, this is the first member of
  // P, P*N, P*N*N, ... that is greater than or equal to X.
  syntax Int ::= powerCeiling(Int, Int, Int) [function, total]
  rule powerCeiling(P, X, N) => powerCeiling(P *Int N, X, N)
    requires P <Int X
  rule powerCeiling(P, X, _N) => P
    requires X <=Int P

  // The contract over integers.  The exponent may be zero, so 1 is a
  // simple power of every base.  Nontrivial powers use bases at least 2.
  syntax Bool ::= simplePowerSpec(Int, Int) [function, total]
  rule simplePowerSpec(X, N)
    => (X ==Int 1)
       orBool (1 <Int X
               andBool 2 <=Int N
               andBool powerCeiling(N, X, N) ==Int X)

endmodule
