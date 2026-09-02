requires "semantic.k"

module VERIFICATION-BODY-MUT
  imports SEMANTIC

  syntax Int ::= lpfSpec(Int, Int) [function]
  rule lpfSpec(N, F) => N
    requires F *Int F >Int N
  rule lpfSpec(N, F) => lpfSpec(N /Int F, F)
    requires F *Int F <=Int N andBool N %Int F ==Int 0
  rule lpfSpec(N, F) => lpfSpec(N, F +Int 1)
    requires F *Int F <=Int N andBool N %Int F =/=Int 0

  syntax Stmt ::= "factorLoop" [macro]
  rule factorLoop
    => While(
         Compare(BinOp("*", Name("factor"), Name("factor")),
                 CmpOp("<=", Name("n"))),
         If(Compare(BinOp("%", Name("n"), Name("factor")),
                    CmpOp("==", Int(0))),
            Assign(Name("n"), BinOp("//", Name("n"), Name("factor"))),
            Assign(Name("factor"), BinOp("+", Name("factor"), Int(2)))))

  syntax PyModule ::= "solutionModule" [macro]
  rule solutionModule
    => Module(
         FuncDef("largest_prime_factor", Params("n"),
           Assign(Name("factor"), Int(2))
           factorLoop
           Return(Name("n"))))
endmodule
