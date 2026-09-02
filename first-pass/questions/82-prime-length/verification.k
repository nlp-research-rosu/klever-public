// verification.k — prime_length = is_prime(len(string)) on the UNIFIED semantics; reuses
// #31's primeAcc on the symbolic string length isLen(CS). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module PRIME-LENGTH-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // primeAcc (from #31): P starts (l>=2); cleared by any divisor of the length in [I, HI).
  syntax Bool ::= primeAcc(Int, Int, Int, Bool) [function, total]
  rule primeAcc(_N:Int, I:Int, HI:Int, P:Bool) => P requires I >=Int HI [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, _P:Bool) => primeAcc(N, I +Int 1, HI, false)
       requires I <Int HI andBool N modInt I ==Int 0 [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, P:Bool) => primeAcc(N, I +Int 1, HI, P)
       requires I <Int HI andBool N modInt I =/=Int 0 [simplification]
endmodule
