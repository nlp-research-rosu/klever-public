// verification.k — summary for the select_words proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module SELECT-WORDS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ch not in "aeiouAEIOU" -> not a vowel. Bridge the unified substring membership for a
  // 1-char needle over the concrete 10-char vowel haystack to a splittable predicate.
  syntax Bool ::= isVowelC(Int) [function, total]
  rule isVowelC(C:Int) => C ==Int 97 orBool C ==Int 101 orBool C ==Int 105 orBool C ==Int 111 orBool C ==Int 117
                   orBool C ==Int 65 orBool C ==Int 69 orBool C ==Int 73 orBool C ==Int 79 orBool C ==Int 85 [simplification]
  rule strContains(iCons(C:Int, .IntSeq), iCons(97, iCons(101, iCons(105, iCons(111, iCons(117, iCons(65, iCons(69, iCons(73, iCons(79, iCons(85, .IntSeq))))))))))) => isVowelC(C) [simplification]

  // FOUR accumulators (result ValSeq of str, current IntSeq, cnt Int, has Bool) threaded
  // over CS with fixed input N. Five branch cases per char C:
  //   1. C==32 & HAS & CNT==N  : flush str(current) into result; reset
  //   2. C==32 & HAS & CNT!=N  : drop current;                   reset
  //   3. C==32 & !HAS          : no-op
  //   4. C!=32 & vowel         : append C; cnt unchanged
  //   5. C!=32 & consonant     : append C; cnt+1
  // All four summaries share these five cases; all [total] (scope-map values).

  syntax ValSeq ::= selRes(IntSeq, ValSeq, IntSeq, Int, Bool, Int) [function, total]
  rule selRes(.IntSeq, RESULT:ValSeq, _CUR:IntSeq, _CNT:Int, _HAS:Bool, _N:Int) => RESULT [simplification]
  rule selRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, CUR:IntSeq, CNT:Int, HAS:Bool, N:Int)
    => selRes(S, valSeqConcat(RESULT, vCons(str(CUR), .ValSeq)), .IntSeq, 0, false, N)
    requires C ==Int 32 andBool HAS andBool CNT ==Int N [simplification]
  rule selRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, _CUR:IntSeq, CNT:Int, HAS:Bool, N:Int)
    => selRes(S, RESULT, .IntSeq, 0, false, N)
    requires C ==Int 32 andBool HAS andBool CNT =/=Int N [simplification]
  rule selRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, CUR:IntSeq, CNT:Int, HAS:Bool, N:Int)
    => selRes(S, RESULT, CUR, CNT, HAS, N)
    requires C ==Int 32 andBool notBool HAS [simplification]
  rule selRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, CUR:IntSeq, CNT:Int, _HAS:Bool, N:Int)
    => selRes(S, RESULT, seqConcat(CUR, iCons(C, .IntSeq)), CNT, true, N)
    requires C =/=Int 32 andBool isVowelC(C) [simplification]
  rule selRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, CUR:IntSeq, CNT:Int, _HAS:Bool, N:Int)
    => selRes(S, RESULT, seqConcat(CUR, iCons(C, .IntSeq)), CNT +Int 1, true, N)
    requires C =/=Int 32 andBool notBool isVowelC(C) [simplification]

  syntax IntSeq ::= selCur(IntSeq, IntSeq, Int, Bool, Int) [function, total]
  rule selCur(.IntSeq, CUR:IntSeq, _CNT:Int, _HAS:Bool, _N:Int) => CUR [simplification]
  rule selCur(iCons(C:Int, S:IntSeq), _CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selCur(S, .IntSeq, 0, false, N)
    requires C ==Int 32 andBool HAS andBool CNT ==Int N [simplification]
  rule selCur(iCons(C:Int, S:IntSeq), _CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selCur(S, .IntSeq, 0, false, N)
    requires C ==Int 32 andBool HAS andBool CNT =/=Int N [simplification]
  rule selCur(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selCur(S, CUR, CNT, HAS, N)
    requires C ==Int 32 andBool notBool HAS [simplification]
  rule selCur(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, _HAS:Bool, N:Int) => selCur(S, seqConcat(CUR, iCons(C, .IntSeq)), CNT, true, N)
    requires C =/=Int 32 andBool isVowelC(C) [simplification]
  rule selCur(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, _HAS:Bool, N:Int) => selCur(S, seqConcat(CUR, iCons(C, .IntSeq)), CNT +Int 1, true, N)
    requires C =/=Int 32 andBool notBool isVowelC(C) [simplification]

  syntax Int ::= selCnt(IntSeq, IntSeq, Int, Bool, Int) [function, total]
  rule selCnt(.IntSeq, _CUR:IntSeq, CNT:Int, _HAS:Bool, _N:Int) => CNT [simplification]
  rule selCnt(iCons(C:Int, S:IntSeq), _CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selCnt(S, .IntSeq, 0, false, N)
    requires C ==Int 32 andBool HAS andBool CNT ==Int N [simplification]
  rule selCnt(iCons(C:Int, S:IntSeq), _CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selCnt(S, .IntSeq, 0, false, N)
    requires C ==Int 32 andBool HAS andBool CNT =/=Int N [simplification]
  rule selCnt(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selCnt(S, CUR, CNT, HAS, N)
    requires C ==Int 32 andBool notBool HAS [simplification]
  rule selCnt(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, _HAS:Bool, N:Int) => selCnt(S, seqConcat(CUR, iCons(C, .IntSeq)), CNT, true, N)
    requires C =/=Int 32 andBool isVowelC(C) [simplification]
  rule selCnt(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, _HAS:Bool, N:Int) => selCnt(S, seqConcat(CUR, iCons(C, .IntSeq)), CNT +Int 1, true, N)
    requires C =/=Int 32 andBool notBool isVowelC(C) [simplification]

  syntax Bool ::= selHas(IntSeq, IntSeq, Int, Bool, Int) [function, total]
  rule selHas(.IntSeq, _CUR:IntSeq, _CNT:Int, HAS:Bool, _N:Int) => HAS [simplification]
  rule selHas(iCons(C:Int, S:IntSeq), _CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selHas(S, .IntSeq, 0, false, N)
    requires C ==Int 32 andBool HAS andBool CNT ==Int N [simplification]
  rule selHas(iCons(C:Int, S:IntSeq), _CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selHas(S, .IntSeq, 0, false, N)
    requires C ==Int 32 andBool HAS andBool CNT =/=Int N [simplification]
  rule selHas(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, HAS:Bool, N:Int) => selHas(S, CUR, CNT, HAS, N)
    requires C ==Int 32 andBool notBool HAS [simplification]
  rule selHas(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, _HAS:Bool, N:Int) => selHas(S, seqConcat(CUR, iCons(C, .IntSeq)), CNT, true, N)
    requires C =/=Int 32 andBool isVowelC(C) [simplification]
  rule selHas(iCons(C:Int, S:IntSeq), CUR:IntSeq, CNT:Int, _HAS:Bool, N:Int) => selHas(S, seqConcat(CUR, iCons(C, .IntSeq)), CNT +Int 1, true, N)
    requires C =/=Int 32 andBool notBool isVowelC(C) [simplification]

endmodule
