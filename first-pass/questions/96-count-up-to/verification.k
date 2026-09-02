// verification.k — count_up_to on the UNIFIED semantics, TRAP-FREE (P96).
// solution.py is canonical verbatim (nested trial division with break, append
// builder). primeAcc over the pyMod execution atoms (the P59 kit); the outer
// fold appends under the primeAcc case-split.

requires "../../reference/src/lemmas.k"

module COUNT-UP-TO-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  syntax Bool ::= primeAcc(Int, Int, Int, Bool) [function, total]
  rule primeAcc(_N:Int, I:Int, HI:Int, P:Bool) => P
    requires I >=Int HI [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, _P:Bool) => false
    requires I <Int HI andBool pyMod(N, I) ==Int 0 [simplification]
  rule primeAcc(N:Int, I:Int, HI:Int, P:Bool) => primeAcc(N, I +Int 1, HI, P)
    requires I <Int HI andBool notBool (pyMod(N, I) ==Int 0) [simplification]

  syntax ValSeq ::= primesUpTo(Int, Int, ValSeq) [function, total]
  rule primesUpTo(I:Int, HI:Int, ACC:ValSeq) => ACC
    requires I >=Int HI [simplification]
  rule primesUpTo(I:Int, HI:Int, ACC:ValSeq)
    => primesUpTo(I +Int 1, HI, valSeqConcat(ACC, vCons(I, .ValSeq)))
    requires I <Int HI andBool primeAcc(I, 2, I, true) [simplification]
  rule primesUpTo(I:Int, HI:Int, ACC:ValSeq) => primesUpTo(I +Int 1, HI, ACC)
    requires I <Int HI andBool notBool primeAcc(I, 2, I, true) [simplification]
endmodule
