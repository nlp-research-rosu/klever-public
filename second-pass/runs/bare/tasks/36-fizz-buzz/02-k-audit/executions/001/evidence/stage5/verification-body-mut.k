requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  syntax Int ::= digitSevens(Int) [function, total]
               | fizzContribution(Int) [function, total]
               | fizzFrom(Int, Int) [function, total]
               | fizzEnd(Int) [function, total]

  rule fizzEnd(N) => 0
    requires N <Int 0
  rule fizzEnd(N) => N
    requires N >=Int 0

  rule digitSevens(X) => 0
    requires X <=Int 0
  rule digitSevens(X) => 1 +Int digitSevens(X /Int 10)
    requires X >Int 0 andBool X %Int 10 ==Int 7
  rule digitSevens(X) => digitSevens(X /Int 10)
    requires X >Int 0 andBool X %Int 10 =/=Int 7

  rule fizzContribution(I) => digitSevens(I)
    requires I %Int 11 ==Int 0
  rule fizzContribution(I) => digitSevens(I)
    requires I %Int 11 =/=Int 0 andBool I %Int 13 ==Int 0
  rule fizzContribution(I) => 0
    requires I %Int 11 =/=Int 0 andBool I %Int 13 =/=Int 0

  rule fizzFrom(I, N) => 0
    requires I >=Int N
  rule fizzFrom(I, N) => fizzContribution(I) +Int fizzFrom(I +Int 1, N)
    requires I <Int N

  rule (A +Int B) +Int C => A +Int (B +Int C) [simplification]

  syntax Stmt ::= "INNER-LOOP" [macro]
  rule INNER-LOOP =>
    While(Compare(Name("x"), CmpOp(">", Int(0))),
      If(Compare(BinOp("%", Name("x"), Int(10)), CmpOp("==", Int(7))),
        Assign(Name("count"), BinOp("+", Name("count"), Int(2))),
        .Stmts)
      Assign(Name("x"), BinOp("//", Name("x"), Int(10))))

  syntax Stmt ::= "OUTER-LOOP" [macro]
  rule OUTER-LOOP =>
    While(Compare(Name("i"), CmpOp("<", Name("n"))),
      If(BoolOp("or",
          Compare(BinOp("%", Name("i"), Int(11)), CmpOp("==", Int(0))),
          Compare(BinOp("%", Name("i"), Int(13)), CmpOp("==", Int(0)))),
        Assign(Name("x"), Name("i"))
        INNER-LOOP,
        .Stmts)
      Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
endmodule

