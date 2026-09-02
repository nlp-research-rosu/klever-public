requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  syntax Int ::= "mathFactorial" "(" Int ")" [function]
               | "mathTriangle" "(" Int ")" [function]
               | "expectedAt" "(" Int ")" [function]
  syntax List ::= "expected" "(" Int ")" [function]
                | "expectedCompletion" "(" Int "," Int "," Int "," Int "," List ")" [function]

  rule mathFactorial(0) => 1
  rule mathFactorial(N) => mathFactorial(N -Int 1) *Int N
    requires N >Int 0

  rule mathTriangle(0) => 0
  rule mathTriangle(N) => mathTriangle(N -Int 1) +Int N
    requires N >Int 0

  rule expectedAt(N) => mathFactorial(N)
    requires N >Int 0 andBool N %Int 2 ==Int 0
  rule expectedAt(N) => mathTriangle(N)
    requires N >Int 0 andBool N %Int 2 =/=Int 0

  // The next four equations are the contract.  F is the product of the
  // indices already visited and T is their sum.  Thus the value appended at
  // an even I is I!, while the value appended at an odd I is 1 + ... + I.
  rule expected(N) => expectedCompletion(1, N, 1, 0, .List)
    requires N >=Int 0

  rule expectedCompletion(I, N, _F, _T, L) => L
    requires I >Int N
  rule expectedCompletion(I, N, F, T, L)
    => expectedCompletion(
         I +Int 1, N, F *Int I, T +Int I,
         L ListItem(F *Int I))
    requires I <=Int N andBool I %Int 2 ==Int 0
  rule expectedCompletion(I, N, F, T, L)
    => expectedCompletion(
         I +Int 1, N, F *Int I, T +Int I,
         L ListItem(T +Int I))
    requires I <=Int N andBool I %Int 2 =/=Int 0

  syntax Program ::= "solution" [macro]
  syntax Stmt ::= "solutionLoop" [macro]

  rule solutionLoop =>
    While(Compare(Name("i"), CmpOp("<=", Name("n"))),
      Assign(
        Name("factorial"),
        BinOp("*", Name("factorial"), Name("i")))
      Assign(Name("total"), BinOp("+", Name("total"), Name("i")))
      If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
        Assign(
          Name("result"),
          BinOp("+", Name("result"), ListExpr(Name("factorial")))),
        Assign(
          Name("result"),
          BinOp("+", Name("result"), ListExpr(Name("total")))))
      Assign(Name("i"), BinOp("+", Name("i"), Int(1))))

  rule solution =>
    Module(
      FuncDef("f", Params("n"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("factorial"), Int(1))
        Assign(Name("total"), Int(0))
        Assign(Name("i"), Int(1))
        solutionLoop
        Return(Name("result"))))
endmodule
