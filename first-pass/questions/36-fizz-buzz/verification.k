// verification.k — fizz_buzz on the UNIFIED semantics, TRAP-FREE (P36).
// solution.py is canonical verbatim: append-filter loop, the real
// join(list(map(str, ns))) composition (all opaque on symbolic data), and the
// bool-int count loop. Domain n >= 1 in the claims (n = 0 runs in the smoke).

requires "../../reference/src/lemmas.k"

module FIZZ-BUZZ-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // filter fold: the multiples of 11 or 13 in [I, HI)
  syntax ValSeq ::= divList(Int, Int, ValSeq) [function, total]
  rule divList(I:Int, HI:Int, ACC:ValSeq) => ACC requires I >=Int HI [simplification]
  rule divList(I:Int, HI:Int, ACC:ValSeq)
    => divList(I +Int 1, HI, valSeqConcat(ACC, vCons(I, .ValSeq)))
    requires I <Int HI andBool (pyMod(I, 11) ==Int 0 orBool pyMod(I, 13) ==Int 0)
    [simplification]
  rule divList(I:Int, HI:Int, ACC:ValSeq) => divList(I +Int 1, HI, ACC)
    requires I <Int HI andBool notBool (pyMod(I, 11) ==Int 0 orBool pyMod(I, 13) ==Int 0)
    [simplification]

  // count of '7' codes (55) in a code seq
  syntax Int ::= count7(IntSeq, Int) [function, total]
  rule count7(.IntSeq, ACC:Int) => ACC [simplification]
  // the step in EXACTLY the execution's bool-int form (the #if never splits)
  rule count7(iCons(C:Int, R:IntSeq), ACC:Int)
    => count7(R, ACC +Int #if C ==Int 55 #then 1 #else 0 #fi) [simplification]

  // the result composition (join/map stay opaque on the symbolic filter)
  syntax Int ::= fbRes(Int) [function]
  rule fbRes(N:Int)
    => count7(joinCodes(.IntSeq, mapStrVS(divList(0, N, .ValSeq))), 0)
    [simplification]
endmodule
