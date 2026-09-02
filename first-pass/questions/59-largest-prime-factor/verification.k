// verification.k — largest_prime_factor on the UNIFIED semantics, TRAP-FREE
// (P59). solution.py is canonical verbatim (NESTED is_prime via closure cells,
// early returns, and-short-circuit, max()). NO interceptions: the callee-span
// claim folds is_prime's real loop (with its early Return) to primeAcc; the
// outer invariant runs the REAL call per iteration (Probe A shape).

requires "../../reference/src/lemmas.k"

module LARGEST-PRIME-FACTOR-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // primeAcc over the EXACT execution atoms (pyMod — applyBin's % form)
  syntax Bool ::= primeAcc(Int, Int, Int, Bool) [function, total]
  rule primeAcc(_N:Int, I:Int, HI:Int, P:Bool) => P
    requires I >=Int HI [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, _P:Bool) => false
    requires I <Int HI andBool pyMod(N, I) ==Int 0 [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, P:Bool) => primeAcc(N, I +Int 1, HI, P)
    requires I <Int HI andBool notBool (pyMod(N, I) ==Int 0) [simplification]

  // the sticky-max collection fold over j in [J, HI)
  syntax Int ::= lpfAcc(Int, Int, Int, Int) [function, total]
  rule lpfAcc(J:Int, HI:Int, _N:Int, ACC:Int) => ACC
    requires J >=Int HI [simplification]
  rule lpfAcc(J:Int, HI:Int, N:Int, ACC:Int) => lpfAcc(J +Int 1, HI, N, maxInt(ACC, J))
    requires J <Int HI andBool pyMod(N, J) ==Int 0 andBool primeAcc(J, 2, J -Int 1, true)
    [simplification]
  rule lpfAcc(J:Int, HI:Int, N:Int, ACC:Int) => lpfAcc(J +Int 1, HI, N, ACC)
    requires J <Int HI
     andBool notBool (pyMod(N, J) ==Int 0 andBool primeAcc(J, 2, J -Int 1, true))
    [simplification]
endmodule
