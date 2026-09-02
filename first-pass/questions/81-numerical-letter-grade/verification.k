// verification.k — numerical_letter_grade on the UNIFIED semantics,
// INTERCEPTION-FREE (P81, purged). solution.py is canonical verbatim: the
// 13-way elif chain runs inline per element (grade_of + its Call trap GONE;
// eqF81 rehomed to the SHARED eqF). Element compares reduce via
// entailment-gated [simplification] echoes onto the shared eqF/gtF atoms
// (the Q4 applyBin echo class) — no k-cell rules here.

requires "../../reference/src/lemmas.k"

module NUMERICAL-LETTER-GRADE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  rule 0 <Int 1 +Int vsLen(_:ValSeq) => true [simplification]

  rule applyCmp("==", V:Val, F:Float) => eqF(projectFloatTotal(V), F)
    requires isFloat(V) [simplification]
  rule applyCmp(">", V:Val, F:Float) => gtF(projectFloatTotal(V), F)
    requires isFloat(V) [simplification]

  // the per-element 13-way fold, arm guards = the elif chain's PC prefixes
  syntax ValSeq ::= gradeFold(ValSeq, ValSeq) [function, total]
  rule gradeFold(.ValSeq, ACC:ValSeq) => ACC [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(65, iCons(43, .IntSeq))), .ValSeq)))
    requires eqF(projectFloatTotal(V), 4.0) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(65, .IntSeq)), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool gtF(projectFloatTotal(V), 3.7) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(65, iCons(45, .IntSeq))), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool gtF(projectFloatTotal(V), 3.3) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(66, iCons(43, .IntSeq))), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool gtF(projectFloatTotal(V), 3.0) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(66, .IntSeq)), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool gtF(projectFloatTotal(V), 2.7) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(66, iCons(45, .IntSeq))), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool notBool gtF(projectFloatTotal(V), 2.7) andBool gtF(projectFloatTotal(V), 2.3) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(67, iCons(43, .IntSeq))), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool notBool gtF(projectFloatTotal(V), 2.7) andBool notBool gtF(projectFloatTotal(V), 2.3) andBool gtF(projectFloatTotal(V), 2.0) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(67, .IntSeq)), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool notBool gtF(projectFloatTotal(V), 2.7) andBool notBool gtF(projectFloatTotal(V), 2.3) andBool notBool gtF(projectFloatTotal(V), 2.0) andBool gtF(projectFloatTotal(V), 1.7) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(67, iCons(45, .IntSeq))), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool notBool gtF(projectFloatTotal(V), 2.7) andBool notBool gtF(projectFloatTotal(V), 2.3) andBool notBool gtF(projectFloatTotal(V), 2.0) andBool notBool gtF(projectFloatTotal(V), 1.7) andBool gtF(projectFloatTotal(V), 1.3) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(68, iCons(43, .IntSeq))), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool notBool gtF(projectFloatTotal(V), 2.7) andBool notBool gtF(projectFloatTotal(V), 2.3) andBool notBool gtF(projectFloatTotal(V), 2.0) andBool notBool gtF(projectFloatTotal(V), 1.7) andBool notBool gtF(projectFloatTotal(V), 1.3) andBool gtF(projectFloatTotal(V), 1.0) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(68, .IntSeq)), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool notBool gtF(projectFloatTotal(V), 2.7) andBool notBool gtF(projectFloatTotal(V), 2.3) andBool notBool gtF(projectFloatTotal(V), 2.0) andBool notBool gtF(projectFloatTotal(V), 1.7) andBool notBool gtF(projectFloatTotal(V), 1.3) andBool notBool gtF(projectFloatTotal(V), 1.0) andBool gtF(projectFloatTotal(V), 0.7) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(68, iCons(45, .IntSeq))), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool notBool gtF(projectFloatTotal(V), 2.7) andBool notBool gtF(projectFloatTotal(V), 2.3) andBool notBool gtF(projectFloatTotal(V), 2.0) andBool notBool gtF(projectFloatTotal(V), 1.7) andBool notBool gtF(projectFloatTotal(V), 1.3) andBool notBool gtF(projectFloatTotal(V), 1.0) andBool notBool gtF(projectFloatTotal(V), 0.7) andBool gtF(projectFloatTotal(V), 0.0) [simplification]
  rule gradeFold(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => gradeFold(R, valSeqConcat(ACC, vCons(str(iCons(69, .IntSeq)), .ValSeq)))
    requires notBool eqF(projectFloatTotal(V), 4.0) andBool notBool gtF(projectFloatTotal(V), 3.7) andBool notBool gtF(projectFloatTotal(V), 3.3) andBool notBool gtF(projectFloatTotal(V), 3.0) andBool notBool gtF(projectFloatTotal(V), 2.7) andBool notBool gtF(projectFloatTotal(V), 2.3) andBool notBool gtF(projectFloatTotal(V), 2.0) andBool notBool gtF(projectFloatTotal(V), 1.7) andBool notBool gtF(projectFloatTotal(V), 1.3) andBool notBool gtF(projectFloatTotal(V), 1.0) andBool notBool gtF(projectFloatTotal(V), 0.7) andBool notBool gtF(projectFloatTotal(V), 0.0) [simplification]
endmodule
