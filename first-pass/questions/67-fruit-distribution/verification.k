// verification.k — fruit_distribution on the UNIFIED semantics, TRAP-FREE
// (P67). solution.py is canonical verbatim (element loop over the real split,
// real .isdigit()/int()/.append(), real sum). The abstract-element
// .isdigit()/int() calls ride the SHARED codesProj echoes (lemmas/builtins.k);
// the sum-fold circularity closes the sum of the built list.

requires "../../reference/src/lemmas.k"

module FRUIT-DISTRIBUTION-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // the append-builder fold: ints of the digit tokens. Guards spell the
  // SHAPED executed atoms of the shared isdigit echo; the kept value is the
  // shared int() echo's intDigAcc
  syntax ValSeq ::= dFilt(ValSeq, ValSeq) [function, total]
  rule dFilt(.ValSeq, ACC:ValSeq) => ACC [simplification]
  rule dFilt(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => dFilt(R, valSeqConcat(ACC, vCons(intDigAcc(codesProj(V), 0), .ValSeq)))
    requires notBool (isLen(codesProj(V)) ==Int 0) andBool dgN(codesProj(V)) ==Int 1
    [simplification]
  rule dFilt(vCons(V:Val, R:ValSeq), ACC:ValSeq) => dFilt(R, ACC)
    requires notBool (notBool (isLen(codesProj(V)) ==Int 0) andBool dgN(codesProj(V)) ==Int 1)
    [simplification]

  // sum summary (the sum-fold test's shape, problem-local)
  syntax Int ::= sumOf(ValSeq, Int) [function, total]
  rule sumOf(.ValSeq, ACC:Int) => ACC [simplification]
  rule sumOf(vCons(V:Val, R:ValSeq), ACC:Int) => sumOf(R, ACC +Int intOf(V))
    requires isInt(V) orBool isBool(V) [simplification]

  // dFilt only appends intTok terms (Ints): allInt preservation echo
  rule allInt(dFilt(_:ValSeq, ACC:ValSeq)) => allInt(ACC) [simplification]

  // splitSep always yields at least one token (both its rules produce vCons)
  rule vsLen(splitSep(_:IntSeq, _:Int, _:IntSeq)) >Int 0 => true [simplification]
  rule 0 <Int vsLen(splitSep(_:IntSeq, _:Int, _:IntSeq)) => true [simplification]

  // the result
  syntax Int ::= fdRes(IntSeq, Int) [function]
  rule fdRes(CS:IntSeq, N:Int)
    => N -Int sumOf(dFilt(splitSep(CS, 32, .IntSeq), .ValSeq), 0)
    [simplification]
endmodule
