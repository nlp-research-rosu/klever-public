// verification.k — words_in_sentence on the UNIFIED semantics, TRAP-FREE
// (P143). solution.py is canonical verbatim: element loop over the real
// no-arg split, inline length-primality scan (sticky flg, no break), append
// builder, and the real " ".join. Builtin bridges: len on abstract elements
// (shared seqLen echo).

requires "../../reference/src/lemmas.k"

module WORDS-IN-SENTENCE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // len on an abstract str element reduces via the SHARED seqLen echo
  // (lemmas/builtins.k: seqLen(V) => isLen(codesProj(V)) requires isStr(V));
  // the claims carry isStr/allStr premises for the word tokens

  // split only appends str tokens (flushTok), so its all-str status is its
  // accumulator's
  rule allStr(splitWS(_CS:IntSeq, _CUR:IntSeq, ACC:ValSeq)) => allStr(ACC) [simplification]

  // sticky divisor flag over i in [I, HI): 1 if any divisor of N
  syntax Int ::= divFlg(Int, Int, Int, Int) [function, total]
  rule divFlg(_N:Int, I:Int, HI:Int, F:Int) => F requires I >=Int HI [simplification]
  rule divFlg(N:Int, I:Int, HI:Int, _F:Int) => divFlg(N, I +Int 1, HI, 1)
    requires I <Int HI andBool pyMod(N, I) ==Int 0 [simplification]
  rule divFlg(N:Int, I:Int, HI:Int, F:Int) => divFlg(N, I +Int 1, HI, F)
    requires I <Int HI andBool notBool (pyMod(N, I) ==Int 0) [simplification]
  // 1 absorbs (sticky flag never resets)
  rule divFlg(_N:Int, _I:Int, _HI:Int, 1) => 1 [simplification]

  // per-word keep decision + the filter fold
  syntax ValSeq ::= wordFilt(ValSeq, ValSeq) [function, total]
  rule wordFilt(.ValSeq, ACC:ValSeq) => ACC [simplification]
  // len == 1: flg=1, never kept (1 != 0 and len != 2)
  rule wordFilt(vCons(V:Val, R:ValSeq), ACC:ValSeq) => wordFilt(R, ACC)
    requires isLen(codesProj(V)) ==Int 1 [simplification]
  rule wordFilt(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => wordFilt(R, valSeqConcat(ACC, vCons(V, .ValSeq)))
    requires notBool (isLen(codesProj(V)) ==Int 1)
     andBool (divFlg(isLen(codesProj(V)), 2, isLen(codesProj(V)), 0) ==Int 0 orBool isLen(codesProj(V)) ==Int 2)
    [simplification]
  rule wordFilt(vCons(V:Val, R:ValSeq), ACC:ValSeq) => wordFilt(R, ACC)
    requires notBool (isLen(codesProj(V)) ==Int 1)
     andBool notBool (divFlg(isLen(codesProj(V)), 2, isLen(codesProj(V)), 0) ==Int 0 orBool isLen(codesProj(V)) ==Int 2)
    [simplification]

  // the result: join with the single-space separator
  syntax Val ::= wisRes(IntSeq) [function]
  rule wisRes(CS:IntSeq)
    => str(joinCodes(iCons(32, .IntSeq), wordFilt(splitWS(CS, .IntSeq, .ValSeq), .ValSeq)))
    [simplification]
endmodule
