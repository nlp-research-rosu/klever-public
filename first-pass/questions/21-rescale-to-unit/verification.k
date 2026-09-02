// verification.k — rescale_to_unit on the UNIFIED semantics, INTERCEPTION-
// FREE (P21, purged). solution.py is canonical verbatim: the REAL min/max
// builtin folds (#minAcc0/#minAccF, #maxAcc0/#maxAccF) run under kprove and
// are proven with claims; minSeed/maxSeed/minF2/maxF2 are the spec-side
// vocabulary in the folds' exact step form. No k-cell rules here.

requires "../../reference/src/lemmas.k"

module RESCALE-TO-UNIT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // the float-list domain predicate: decomposes to the atoms the shared
  // folds' float/int switch guards need (the Q4-rev2 allFloatN pattern)
  syntax Bool ::= allFloatN(ValSeq) [function, total]
  rule allFloatN(.ValSeq) => true
  rule allFloatN(vCons(V:Val, R:ValSeq))
    => isFloat(V) andBool notBool isInt(V) andBool notBool isBool(V)
       andBool allFloatN(R)

  // (minFloat/maxFloat missing-hook workaround rules are SHARED now:
  // lemmas/float.k — any proof whose exploration touches them needs them)

  // spec vocabulary for the REAL min/max folds, in their exact step form
  // (#minContF steps via minFloat(M, {V}:>Float); the seed takes the head)
  syntax Float ::= minF2(ValSeq, Float) [function, total]
  rule minF2(.ValSeq, M:Float) => M [simplification]
  rule minF2(vCons(V:Val, R:ValSeq), M:Float)
    => minF2(R, minFloat(M, {V}:>Float)) [simplification]
  syntax Float ::= maxF2(ValSeq, Float) [function, total]
  rule maxF2(.ValSeq, M:Float) => M [simplification]
  rule maxF2(vCons(V:Val, R:ValSeq), M:Float)
    => maxF2(R, maxFloat(M, {V}:>Float)) [simplification]
  syntax Float ::= minSeed(ValSeq) [function, total]
  rule minSeed(vCons(V:Val, R:ValSeq)) => minF2(R, {V}:>Float) [simplification]
  syntax Float ::= maxSeed(ValSeq) [function, total]
  rule maxSeed(vCons(V:Val, R:ValSeq)) => maxF2(R, {V}:>Float) [simplification]

  // float-subtraction echo on an abstract element (isFloat from allFloat's
  // vCons decomposition in the PC; also kills ref/cellRef narrowing)
  rule applyBin("-", V:Val, F:Float) => subF(projectFloatTotal(V), F)
    requires isFloat(V) [simplification]

  // the comprehension's builder fold: (x - LO) / (HI - LO) per element, in
  // exact execution form (the denominator recomputes per element, as written)
  syntax ValSeq ::= rescSeq(ValSeq, Float, Float, ValSeq) [function, total]
  rule rescSeq(.ValSeq, _:Float, _:Float, ACC:ValSeq) => ACC [simplification]
  rule rescSeq(vCons(V:Val, R:ValSeq), LO:Float, HI:Float, ACC:ValSeq)
    => rescSeq(R, LO, HI,
         valSeqConcat(ACC, vCons(divF(subF(projectFloatTotal(V), LO), subF(HI, LO)), .ValSeq)))
    [simplification]
endmodule
