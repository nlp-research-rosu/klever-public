// verification.k — count_nums on the UNIFIED semantics, TRAP-FREE (P108).
// solution.py is canonical verbatim: nested digits_sum def (sign tuple-assign,
// digit comprehension over the REAL str(n), n[0] subscript-assign, real sum),
// ds builder comprehension CALLING digits_sum per element, positive filter
// comprehension, len. No interceptions: str(symbolic int) rides the SHARED
// digitCodes bridge; int(single-char) the shared constructor rule; the sum is
// the REAL #sumAcc fold; compares ride the shared k-cell/cast lemmas.

requires "../../reference/src/lemmas.k"

module COUNT-NUMS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ---- the digit comprehension fold: R ++ [c - 48 for each code c] --------
  syntax ValSeq ::= intFold(IntSeq, ValSeq) [function, total]
  rule intFold(.IntSeq, R:ValSeq) => R [simplification]
  rule intFold(iCons(C:Int, T:IntSeq), R:ValSeq)
    => intFold(T, valSeqConcat(R, vCons(C -Int 48, .ValSeq)))
    [simplification]
  // it appends Ints only
  rule allInt(intFold(_:IntSeq, R:ValSeq)) => allInt(R) [simplification]

  // a one-slot write of an Int keeps the all-int discipline
  rule allInt(setVSAt(VS:ValSeq, _:Int, V:Val)) => allInt(VS)
    requires isInt(V) [simplification]

  // ---- the real sum fold's value (the P67 shape) ---------------------------
  syntax Int ::= sumI(ValSeq, Int) [function, total]
  rule sumI(.ValSeq, A:Int) => A [simplification]
  rule sumI(vCons(V:Val, R:ValSeq), A:Int) => sumI(R, A +Int intOf(V))
    requires isInt(V) orBool isBool(V) [simplification]

  // ---- the total element accessor (the atI idiom for ValSeq): valSeqAt is
  // partial, and a partial inside an atom blocks lifting and churns #Ceil;
  // the bridge rewrites in-range occurrences (problem-local)
  syntax Val ::= atV(ValSeq, Int) [function, total]
  rule atV(.ValSeq, _:Int) => noneV [simplification]
  rule atV(vCons(V:Val, _:ValSeq), I:Int) => V requires I <=Int 0 [simplification]
  rule atV(vCons(_:Val, S:ValSeq), I:Int) => atV(S, I -Int 1)
    requires I >Int 0 [simplification]
  rule valSeqAt(VS:ValSeq, I:Int) => atV(VS, I)
    requires 0 <=Int I andBool I <Int vsLen(VS) [simplification]

  // ref-disjointness killers for atV (the P26 class): the deref narrowers
  // split a value-position atV term into ref/cellRef junk branches
  rule { ref(_:Int) #Equals atV(VS:ValSeq, _:Int) } => #Bottom
    requires allInt(VS) [simplification]
  rule { atV(VS:ValSeq, _:Int) #Equals ref(_:Int) } => #Bottom
    requires allInt(VS) [simplification]
  rule { cellRef(_:Int) #Equals atV(VS:ValSeq, _:Int) } => #Bottom
    requires allInt(VS) [simplification]
  rule { atV(VS:ValSeq, _:Int) #Equals cellRef(_:Int) } => #Bottom
    requires allInt(VS) [simplification]
  rule { list(_:ValSeq) #Equals atV(VS:ValSeq, _:Int) } => #Bottom
    requires allInt(VS) [simplification]
  rule { atV(VS:ValSeq, _:Int) #Equals list(_:ValSeq) } => #Bottom
    requires allInt(VS) [simplification]

  // length facts making the slot-0 bounds decide
  rule vsLen(intFold(CS:IntSeq, R:ValSeq)) => isLen(CS) +Int vsLen(R) [simplification]
  rule isLen(digitCodes(N:Int)) >Int 0 => true requires N >=Int 0 [simplification]
  rule 0 <Int isLen(digitCodes(N:Int)) => true requires N >=Int 0 [simplification]

  // ---- digits_sum's return value, per sign branch --------------------------
  // (the executed spellings verbatim: digitCodes via the shared str bridge,
  // the comp fold, the slot-0 product write, then the sum of the whole)
  syntax Int ::= dsRes(Int) [function, total]
  rule dsRes(N:Int)
    => sumI(setVSAt(intFold(digitCodes(N), .ValSeq), 0,
              projectIntTotal(atV(intFold(digitCodes(N), .ValSeq), 0))), 0)
    requires N >=Int 0 [simplification]
  rule dsRes(N:Int)
    => sumI(setVSAt(intFold(digitCodes(-1 *Int N), .ValSeq), 0,
              projectIntTotal(atV(intFold(digitCodes(-1 *Int N), .ValSeq), 0)) *Int -1), 0)
    requires N <Int 0 [simplification]

  // ---- the ds builder fold (one digits_sum call per element) ---------------
  syntax ValSeq ::= dsFold(ValSeq, ValSeq) [function, total]
  rule dsFold(.ValSeq, R:ValSeq) => R [simplification]
  rule dsFold(vCons(V:Val, T:ValSeq), R:ValSeq)
    => dsFold(T, valSeqConcat(R, vCons(dsRes(projectIntTotal(V)), .ValSeq)))
    requires isInt(V) [simplification]
  rule allInt(dsFold(VS:ValSeq, R:ValSeq)) => allInt(R)
    requires allInt(VS) [simplification]

  // ---- the positive filter fold (the P30 spellings) ------------------------
  syntax ValSeq ::= posFilt(ValSeq, ValSeq) [function, total]
  rule posFilt(.ValSeq, R:ValSeq) => R [simplification]
  rule posFilt(vCons(V:Val, T:ValSeq), R:ValSeq)
    => posFilt(T, valSeqConcat(R, vCons(V, .ValSeq)))
    requires isInt(V) andBool {V}:>Int >Int 0 [simplification]
  rule posFilt(vCons(V:Val, T:ValSeq), R:ValSeq) => posFilt(T, R)
    requires isInt(V) andBool {V}:>Int <=Int 0 [simplification]

  // ---- the whole result -----------------------------------------------------
  syntax Int ::= cnRes(ValSeq) [function]
  rule cnRes(VS:ValSeq) => vsLen(posFilt(dsFold(VS, .ValSeq), .ValSeq))
    [simplification]
endmodule
