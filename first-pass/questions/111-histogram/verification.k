// verification.k — histogram on the UNIFIED semantics, TRAP-FREE (P111).
// solution.py is canonical verbatim (element iteration, REAL list1.count(i)
// through the heap ref, real split, dict subscript-assign on the value dict).
// NO interceptions; the folds case-split on the shared cntOccVS atoms.

requires "../../reference/src/lemmas.k"

module HISTOGRAM-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // The `i != ""` guard over an abstract split-word V (isStr under allStr): the shared
  // applyCmp("!=", str, str) rule needs both operands syntactically str(_), so it can't fire on
  // the abstract element. Echo it to notBool (V ==K str(.IntSeq)) — the SAME ==K atom the fold
  // guards case-split on, so the short-circuit #branch aligns with maxCnt/buildD's rules.
  rule applyCmp("!=", V:Val, str(EC:IntSeq)) => notBool (V ==K str(EC))
    requires isStr(V) [simplification]

  // loop 1: t := max count among non-empty elements seen so far
  syntax Int ::= maxCnt(ValSeq, ValSeq, Int) [function, total]
  rule maxCnt(.ValSeq, _FULL:ValSeq, T:Int) => T [simplification]
  rule maxCnt(vCons(V:Val, R:ValSeq), FULL:ValSeq, T:Int) => maxCnt(R, FULL, cntOccVS(FULL, V))
    requires cntOccVS(FULL, V) >Int T andBool notBool (V ==K str(.IntSeq))
    [simplification]
  rule maxCnt(vCons(V:Val, R:ValSeq), FULL:ValSeq, T:Int) => maxCnt(R, FULL, T)
    requires notBool (cntOccVS(FULL, V) >Int T andBool notBool (V ==K str(.IntSeq)))
    [simplification]

  // loop 2: collect the elements whose count equals t
  syntax Val ::= buildD(ValSeq, ValSeq, Int, Val) [function, total]
  rule buildD(.ValSeq, _FULL:ValSeq, _T:Int, D:Val) => D [simplification]
  rule buildD(vCons(V:Val, R:ValSeq), FULL:ValSeq, T:Int, D:Val)
    => buildD(R, FULL, T, dictSet(D, V, T))
    requires cntOccVS(FULL, V) ==Int T
    [simplification]
  rule buildD(vCons(V:Val, R:ValSeq), FULL:ValSeq, T:Int, D:Val) => buildD(R, FULL, T, D)
    requires notBool (cntOccVS(FULL, V) ==Int T)
    [simplification]

  // the whole result over the split
  syntax Val ::= histRes(IntSeq) [function]
  rule histRes(CS:IntSeq) => histRes2(splitSep(CS, 32, .IntSeq)) [simplification]
  syntax Val ::= histRes2(ValSeq) [function]
  rule histRes2(VS:ValSeq) => dictV(.ValSeq, .ValSeq)
    requires notBool (maxCnt(VS, VS, 0) >Int 0) [simplification]
  rule histRes2(VS:ValSeq) => buildD(VS, VS, maxCnt(VS, VS, 0), dictV(.ValSeq, .ValSeq))
    requires maxCnt(VS, VS, 0) >Int 0 [simplification]
endmodule
