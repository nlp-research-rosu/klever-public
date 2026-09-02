// verification.k — summary for the words_string proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module WORDS-STRING-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ch in ", " for a 1-char ch == the code is a delimiter (',' 44 or ' ' 32). The unified
  // str `in` is substring (strContains); for a 1-char needle over the concrete 2-char
  // haystack this IS delimiter membership — bridge it to a kprove-splittable predicate.
  syntax Bool ::= isDelim(Int) [function, total]
  rule isDelim(C:Int) => C ==Int 44 orBool C ==Int 32 [simplification]
  rule strContains(iCons(C:Int, .IntSeq), iCons(44, iCons(32, .IntSeq))) => isDelim(C) [simplification]

  // THREE accumulators (result ValSeq of str, current IntSeq, has Bool) threaded over CS.
  // Per char C: delimiter & HAS -> FLUSH str(current) into result and clear; delimiter &
  // not HAS -> no-op; else append C, set has. All land in the scope map, so [total].
  syntax ValSeq ::= wordsRes(IntSeq, ValSeq, IntSeq, Bool) [function, total]
  rule wordsRes(.IntSeq, RESULT:ValSeq, _CUR:IntSeq, _HAS:Bool) => RESULT [simplification]
  rule wordsRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, CUR:IntSeq, HAS:Bool)
    => wordsRes(S, valSeqConcat(RESULT, vCons(str(CUR), .ValSeq)), .IntSeq, false)
    requires isDelim(C) andBool HAS [simplification]
  rule wordsRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, CUR:IntSeq, HAS:Bool)
    => wordsRes(S, RESULT, CUR, HAS)
    requires isDelim(C) andBool notBool HAS [simplification]
  rule wordsRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, CUR:IntSeq, _HAS:Bool)
    => wordsRes(S, RESULT, seqConcat(CUR, iCons(C, .IntSeq)), true)
    requires notBool isDelim(C) [simplification]

  syntax IntSeq ::= wordsCur(IntSeq, IntSeq, Bool) [function, total]
  rule wordsCur(.IntSeq, CUR:IntSeq, _HAS:Bool) => CUR [simplification]
  rule wordsCur(iCons(C:Int, S:IntSeq), _CUR:IntSeq, HAS:Bool) => wordsCur(S, .IntSeq, false)
    requires isDelim(C) andBool HAS [simplification]
  rule wordsCur(iCons(C:Int, S:IntSeq), CUR:IntSeq, HAS:Bool) => wordsCur(S, CUR, HAS)
    requires isDelim(C) andBool notBool HAS [simplification]
  rule wordsCur(iCons(C:Int, S:IntSeq), CUR:IntSeq, _HAS:Bool) => wordsCur(S, seqConcat(CUR, iCons(C, .IntSeq)), true)
    requires notBool isDelim(C) [simplification]

  // has after the loop = "the last char was not a delimiter" (or HAS if CS empty).
  syntax Bool ::= wordsHas(IntSeq, Bool) [function, total]
  rule wordsHas(.IntSeq, HAS:Bool) => HAS [simplification]
  rule wordsHas(iCons(C:Int, S:IntSeq), _HAS:Bool) => wordsHas(S, false) requires isDelim(C) [simplification]
  rule wordsHas(iCons(C:Int, S:IntSeq), _HAS:Bool) => wordsHas(S, true)  requires notBool isDelim(C) [simplification]

  // Left-built accumulator echoes.
endmodule
