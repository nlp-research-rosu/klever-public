requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports BOOL
  imports INT

  // noDivisors(N, D) is true exactly when no integer in [max(2,D), N)
  // divides N.  The D < 2 equation totalizes the mathematical function.
  syntax Bool ::= noDivisors(Int, Int) [function, total]

  // The ascending sequence of prime integers in [C, N), and its [2, N)
  // specialization used by count_up_to.
  syntax ValSeq ::= primesBetween(Int, Int) [function, total]
                  | primesBelow(Int)        [function, total]

  // Exact AST abbreviations copied from solution.mpy.  These are macros only:
  // they neither replace nor accelerate operational execution.
  syntax Stmts ::= "innerBody" [macro]
                 | "outerBody" [macro]
                 | "countBody" [macro]
                 | "countBodyStart3" [macro]

  rule innerBody =>
    If(Compare(BinOp("%", Name("candidate"), Name("divisor")),
               CmpOp("==", Int(0))),
       Assign(Name("prime"), Bool(false)) .Stmts,
       .Stmts)
    Assign(Name("divisor"),
           BinOp("+", Name("divisor"), Int(1))) .Stmts

  rule outerBody =>
    Assign(Name("divisor"), Int(2))
    Assign(Name("prime"), Bool(true))
    While(Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
          innerBody)
    If(Name("prime"),
       Expr(Call(Attribute(Name("primes"), "append"),
                 Name("candidate"))) .Stmts,
       .Stmts)
    Assign(Name("candidate"),
           BinOp("+", Name("candidate"), Int(1))) .Stmts

  rule countBody =>
    If(Compare(Name("n"), CmpOp("<=", Int(2))),
       Return(ListExpr(.Exprs)) .Stmts,
       .Stmts)
    Assign(Name("primes"), ListExpr(.Exprs))
    Assign(Name("candidate"), Int(2))
    Assign(Name("divisor"), Int(2))
    Assign(Name("prime"), Bool(true))
    While(Compare(Name("candidate"), CmpOp("<", Name("n"))),
          outerBody)
    Return(Name("primes")) .Stmts

  // Validation-only material mutation: skips candidate 2.
  rule countBodyStart3 =>
    If(Compare(Name("n"), CmpOp("<=", Int(2))),
       Return(ListExpr(.Exprs)) .Stmts,
       .Stmts)
    Assign(Name("primes"), ListExpr(.Exprs))
    Assign(Name("candidate"), Int(3))
    Assign(Name("divisor"), Int(2))
    Assign(Name("prime"), Bool(true))
    While(Compare(Name("candidate"), CmpOp("<", Name("n"))),
          outerBody)
    Return(Name("primes")) .Stmts
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX
  imports BOOL
  imports INT

  rule noDivisors(N, D) => noDivisors(N, 2)
    requires D <Int 2
  rule noDivisors(N, D) => true
    requires D >=Int 2 andBool D >=Int N
  rule noDivisors(N, D) => false
    requires D >=Int 2 andBool D <Int N
     andBool pyMod(N, D) ==Int 0
  rule noDivisors(N, D) => noDivisors(N, D +Int 1)
    requires D >=Int 2 andBool D <Int N
     andBool pyMod(N, D) =/=Int 0

  rule primesBetween(C, N) => .ValSeq
    requires C >=Int N
  rule primesBetween(C, N)
    => primesBetween(C +Int 1, N)
    requires C <Int N andBool C <Int 2
  rule primesBetween(C, N)
    => vCons(C, primesBetween(C +Int 1, N))
    requires C <Int N andBool C >=Int 2
     andBool noDivisors(C, 2)
  rule primesBetween(C, N)
    => primesBetween(C +Int 1, N)
    requires C <Int N andBool C >=Int 2
     andBool notBool noDivisors(C, 2)

  rule primesBelow(N) => .ValSeq
    requires N <=Int 2
  rule primesBelow(N) => primesBetween(2, N)
    requires N >Int 2

  // Derived by structural induction on A from MPY-LIST's two defining
  // equations for valSeqConcat.  Right association makes the outer-loop
  // accumulator obligation syntactically canonical.
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]
  rule valSeqConcat(A:ValSeq, .ValSeq) => A
    [simplification]
endmodule
