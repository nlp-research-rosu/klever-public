// verification.k — prime_fib on the UNIFIED semantics, TRAP-FREE (P39).
// is_prime is the no-early-exit trial-division accumulator (P139 shape); its
// REAL call folds via the spec's callee-span claim onto isPrimeV — the Call
// interception is GONE. The search folds via primeFibFold (co-inductive).

requires "../../reference/src/lemmas.k"

module PRIME-FIB-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // the trial scan, matching the body's transitions (no early exit)
  syntax Bool ::= prAcc(Int, Int, Bool) [function, total]
  rule prAcc(P:Int, K:Int, PR:Bool) => PR requires K *Int K >Int P [simplification]
  rule prAcc(P:Int, K:Int, _:Bool) => prAcc(P, K +Int 1, false)
    requires K *Int K <=Int P andBool P modInt K ==Int 0 [simplification]
  rule prAcc(P:Int, K:Int, PR:Bool) => prAcc(P, K +Int 1, PR)
    requires K *Int K <=Int P andBool P modInt K =/=Int 0 [simplification]

  // is_prime's value: the p<2 gate + the scan from k=2, pr=true
  syntax Bool ::= isPrimeV(Int) [function, total, symbol(isPrimeV)]
  rule isPrimeV(P:Int) => false requires P <Int 2 [simplification]
  rule isPrimeV(P:Int) => prAcc(P, 2, true) requires P >=Int 2 [simplification]

  // primeFibFold(A, B, N) = the value of `b` when the search exits. Advances
  // (a,b) -> (b, a+b); decrements N when a+b is prime. Co-inductive; [total]
  // trusts the search terminates (the n-th prime Fibonacci exists).
  syntax Val ::= primeFibFold(Int, Int, Int) [function, total, no-evaluators]
  rule primeFibFold(_:Int, B:Int, N:Int) => B requires N <=Int 0 [simplification]
  rule primeFibFold(A:Int, B:Int, N:Int) => primeFibFold(B, A +Int B, N -Int 1)
    requires N >Int 0 andBool isPrimeV(A +Int B) [simplification]
  rule primeFibFold(A:Int, B:Int, N:Int) => primeFibFold(B, A +Int B, N)
    requires N >Int 0 andBool notBool isPrimeV(A +Int B) [simplification]

  syntax Val ::= primeFibRes(Int) [function, total, no-evaluators]
  rule primeFibRes(N:Int) => primeFibFold(0, 1, N) [simplification]
endmodule
