// verification.k — intersection on the UNIFIED semantics: is_prime of the interval-overlap
// length (reuses #31's primeAcc), returned as "YES"/"NO". See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module INTERSECTION-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // primeAcc (from #31): P starts (length>=2); cleared by any divisor of the length in [I, HI).
  syntax Bool ::= primeAcc(Int, Int, Int, Bool) [function, total]
  rule primeAcc(_N:Int, I:Int, HI:Int, P:Bool) => P requires I >=Int HI [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, _P:Bool) => primeAcc(N, I +Int 1, HI, false)
       requires I <Int HI andBool N modInt I ==Int 0 [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, P:Bool) => primeAcc(N, I +Int 1, HI, P)
       requires I <Int HI andBool N modInt I =/=Int 0 [simplification]

  // ires(LEN) = "YES" if LEN>0 and is_prime(LEN), else "NO". Guarded so the path discharges it.
  syntax Val ::= ires(Int) [function, total]
  rule ires(LEN:Int) => str(strToCodes("YES"))
       requires LEN >Int 0 andBool primeAcc(LEN, 2, LEN, LEN >=Int 2) [simplification]
  rule ires(LEN:Int) => str(strToCodes("NO"))
       requires notBool (LEN >Int 0 andBool primeAcc(LEN, 2, LEN, LEN >=Int 2)) [simplification]
endmodule
