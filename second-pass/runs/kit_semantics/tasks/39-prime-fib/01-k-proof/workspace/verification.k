requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  // Syntactic abbreviations only: these macros expand to the translated
  // solution.py body before execution or proof.
  syntax Stmt  ::= "primeFibInner" [macro]
                 | "primeFibOuter" [macro]
  syntax Stmts ::= "primeFibBody"  [macro]
  syntax KItem ::= "primeFibInnerCore" [macro]
                 | "primeFibOuterCore" [macro]

  // Mathematical summaries used by the loop invariants.
  syntax Bool ::= primeScan(Int, Int, Bool) [function]
  syntax Int  ::= primeFibSearch(Int, Int, Int, Int) [function]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  rule primeFibInner
    => While(
         Compare(
           BinOp("*", Name("divisor"), Name("divisor")),
           CmpOp("<=", Name("a"))),
         If(
           Compare(
             BinOp("%", Name("a"), Name("divisor")),
             CmpOp("==", Int(0))),
           Assign(Name("is_prime"), Bool(false))
           .Stmts,
           .Stmts)
         Assign(
           Name("divisor"),
           BinOp("+", Name("divisor"), Int(1)))
         .Stmts)

  rule primeFibInnerCore
    => #while(
         Compare(
           BinOp("*", Name("divisor"), Name("divisor")),
           CmpOp("<=", Name("a"))),
         If(
           Compare(
             BinOp("%", Name("a"), Name("divisor")),
             CmpOp("==", Int(0))),
           Assign(Name("is_prime"), Bool(false))
           .Stmts,
           .Stmts)
         Assign(
           Name("divisor"),
           BinOp("+", Name("divisor"), Int(1)))
         .Stmts)

  rule primeFibOuter
    => While(
         Compare(Name("count"), CmpOp("<", Name("n"))),
         Assign(
           Name("next_value"),
           BinOp("+", Name("a"), Name("b")))
         Assign(Name("a"), Name("b"))
         Assign(Name("b"), Name("next_value"))
         Assign(Name("divisor"), Int(2))
         Assign(
           Name("is_prime"),
           Compare(Name("a"), CmpOp(">=", Int(2))))
         primeFibInner
         Assign(
           Name("count"),
           BinOp("+", Name("count"), Name("is_prime")))
         .Stmts)

  rule primeFibOuterCore
    => #while(
         Compare(Name("count"), CmpOp("<", Name("n"))),
         Assign(
           Name("next_value"),
           BinOp("+", Name("a"), Name("b")))
         Assign(Name("a"), Name("b"))
         Assign(Name("b"), Name("next_value"))
         Assign(Name("divisor"), Int(2))
         Assign(
           Name("is_prime"),
           Compare(Name("a"), CmpOp(">=", Int(2))))
         primeFibInner
         Assign(
           Name("count"),
           BinOp("+", Name("count"), Name("is_prime")))
         .Stmts)

  rule primeFibBody
    => Assign(Name("a"), Int(0))
       Assign(Name("b"), Int(1))
       Assign(Name("count"), Int(0))
       Assign(Name("next_value"), Int(0))
       Assign(Name("divisor"), Int(2))
       Assign(Name("is_prime"), Bool(false))
       primeFibOuter
       Return(Name("a"))
       .Stmts

  // primeScan(A,D,P) is the flag left after trial-dividing A by every
  // integer from D through floor(sqrt(A)), starting with flag P.
  rule primeScan(A, D, P) => P
    requires D >=Int 2 andBool D *Int D >Int A
    [simplification]
  rule primeScan(A, D, _P) => false
    requires D >=Int 2
     andBool D *Int D <=Int A
     andBool pyMod(A, D) ==Int 0
    [simplification]
  rule primeScan(A, D +Int 1, P) => primeScan(A, D, P)
    requires D >=Int 2
     andBool D *Int D <=Int A
     andBool pyMod(A, D) =/=Int 0
    [simplification]

  // Once a divisor has cleared the flag, later iterations cannot restore it.
  rule primeScan(_A, D, false) => false
    requires D >=Int 2
    [simplification]

  // Remaining-search summary for the outer loop.  A and B are consecutive
  // Fibonacci-state values, and C prime Fibonacci values have been seen.
  rule primeFibSearch(N, C, A, _B) => A
    requires C >=Int N
    [simplification]
  rule primeFibSearch(N, C, _A, B) => B
    requires N >=Int 1
     andBool C <Int N
     andBool notBool (
       C +Int #if primeScan(B, 2, B >=Int 2) #then 1 #else 0 #fi
       <Int N)
     andBool B >=Int 1
    [simplification]
  rule primeFibSearch(
         N,
         C +Int #if primeScan(B, 2, B >=Int 2) #then 1 #else 0 #fi,
         B,
         A +Int B)
    => primeFibSearch(N, C, A, B)
    requires N >=Int 1
     andBool C <Int N
     andBool A >=Int 0
     andBool B >=Int 1
    [simplification]
endmodule
