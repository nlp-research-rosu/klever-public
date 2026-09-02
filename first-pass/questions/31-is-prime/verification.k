// verification.k — is_prime summary, on the UNIFIED semantics: a threaded Bool accumulator
// over the divisor scan `for k in range(2, n-1)`. Opens the is_prime rung (range loop +
// Bool accumulator, both already-open unified rungs). See ./PROOF.md and ../NOTES.md.

requires "../../reference/src/lemmas.k"

module IS-PRIME-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // primeAcc(N, I, HI, P): P starts as (n>=2); set to false on ANY divisor of N in [I, HI).
  // = is_prime restricted to the divisor range [I, HI). Pure Int (n and the range var k are
  // ints), no projection needed. Total (bounded counter, exhaustive on I >=Int HI / I <Int HI).
  syntax Bool ::= primeAcc(Int, Int, Int, Bool) [function, total]
  rule primeAcc(_N:Int, I:Int, HI:Int, P:Bool) => P
       requires I >=Int HI [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, _P:Bool) => primeAcc(N, I +Int 1, HI, false)
       requires I <Int HI andBool N modInt I ==Int 0 [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, P:Bool) => primeAcc(N, I +Int 1, HI, P)
       requires I <Int HI andBool N modInt I =/=Int 0 [simplification]
endmodule
