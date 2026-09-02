// verification.k — mean_absolute_deviation on the UNIFIED semantics,
// TRAP-FREE (P4, rev 2: NO #applyK interceptions — the proof runs the REAL
// #sumAcc/#sumAccF float-sum folds and proves them with claims; sumF2 is the
// spec-side fold vocabulary in the folds' exact step form). solution.py is
// canonical verbatim: the genexp reads mean through its closure cell.

requires "../../reference/src/lemmas.k"

module MEAN-ABSOLUTE-DEVIATION-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // kprove-side: the fold's int-to-float seed must not reach the missing
  // Int2Float hook
  rule intToF(0) => 0.0 [simplification]
  rule Int2Float(0, 53, 11) => 0.0 [simplification]

  // the float-list domain predicate, decomposing to EXACTLY the atoms the
  // shared fold's switch guard needs (float.k: "a symbolic proof with
  // isInt(V) in its path condition refutes this branch")
  syntax Bool ::= allFloatN(ValSeq) [function, total]
  rule allFloatN(.ValSeq) => true
  rule allFloatN(vCons(V:Val, R:ValSeq))
    => isFloat(V) andBool notBool isInt(V) andBool notBool isBool(V)
       andBool allFloatN(R)
  // the builder's elements are Floats too
  rule allFloatN(sadSeq(_:ValSeq, _:Float, ACC:ValSeq)) => allFloatN(ACC) [simplification]
  rule allFloatN(valSeqConcat(A:ValSeq, B:ValSeq)) => allFloatN(A) andBool allFloatN(B) [simplification]

  // the real folds' accumulator, in their exact step form
  syntax Float ::= sumF2(ValSeq, Float) [function, total]
  rule sumF2(.ValSeq, ACC:Float) => ACC [simplification]
  rule sumF2(vCons(V:Val, R:ValSeq), ACC:Float)
    => sumF2(R, addF(ACC, {V}:>Float)) [simplification]

  // float-subtraction echo on an abstract element (isFloat from allFloat's
  // vCons decomposition in the PC)
  rule applyBin("-", V:Val, F:Float) => subF(projectFloatTotal(V), F)
    requires isFloat(V) [simplification]

  // the comprehension's builder fold: |x - mean| per element
  syntax ValSeq ::= sadSeq(ValSeq, Float, ValSeq) [function, total]
  rule sadSeq(.ValSeq, _:Float, ACC:ValSeq) => ACC [simplification]
  rule sadSeq(vCons(V:Val, R:ValSeq), MEAN:Float, ACC:ValSeq)
    => sadSeq(R, MEAN, valSeqConcat(ACC, vCons(absF(subF(projectFloatTotal(V), MEAN)), .ValSeq)))
    [simplification]

  // the built elements are Floats, and one is built per input element
  rule allFloat(sadSeq(_:ValSeq, _:Float, ACC:ValSeq)) => allFloat(ACC) [simplification]
  rule vsLen(sadSeq(VS:ValSeq, _:Float, ACC:ValSeq)) => vsLen(VS) +Int vsLen(ACC) [simplification]
endmodule
