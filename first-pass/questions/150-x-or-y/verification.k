// verification.k — x_or_y on the UNIFIED semantics: reuses the is_prime divisor scan
// (primeAcc, from #31) over range(2, n), then selects x/y. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module X-OR-Y-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // sel: the `if prime: x else: y` select.
  syntax Int ::= sel(Bool, Int, Int) [function, total]
  rule sel(B:Bool, X:Int, _Y:Int) => X requires B [simplification]
  rule sel(B:Bool, _X:Int, Y:Int) => Y requires notBool B [simplification]

  // primeAcc (from #31): P starts (n != 1 for x_or_y); cleared by any divisor in [I, HI).
  syntax Bool ::= primeAcc(Int, Int, Int, Bool) [function, total]
  rule primeAcc(_N:Int, I:Int, HI:Int, P:Bool) => P requires I >=Int HI [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, _P:Bool) => primeAcc(N, I +Int 1, HI, false)
       requires I <Int HI andBool N modInt I ==Int 0 [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, P:Bool) => primeAcc(N, I +Int 1, HI, P)
       requires I <Int HI andBool N modInt I =/=Int 0 [simplification]
endmodule
