// verification.k — check_dict_case on the UNIFIED semantics. Return True iff (nonempty and) all keys
// are strings in one case (all upper OR all lower). The canonical's `else: break` state machine EXITS
// after the second key, so the result depends ONLY on keys[0] and keys[1] in INSERTION ORDER (a known
// dataset bug faithfully reproduced — diff-tested 0/30007). solution.py is the equivalent bounded
// 2-key rewrite (no loop).
//
// The dict is order-preserving `dictV(KS, VS)` (mpy-dict.k); a proof passes `dictV(KS, WS)` symbolic
// and reads `d.keys() = list(KS)`. Each key is a symbolic Val: `isinstance(key, str)` and
// `key.isupper()/islower()` are STUCK on it (owise / a hasUpper fold over symbolic char codes), so they
// are intercepted PROBLEM-LOCALLY to opaque `isStrKeyV`/`isUpperKeyV`/`isLowerKeyV(valSeqAt(KS, i))`,
// keyed on valSeqAt via [simplification] (kprove-only — krun runs the real predicates on concrete keys).
// The result is the bounded summary `checkDictRes(KS)`, a case-split on those opaque key predicates.
// See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module CHECK-DICT-CASE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- opaque per-key predicates on a symbolic dict key valSeqAt(KS, I) (kprove-only).
  syntax Bool ::= isStrKeyV(Val)   [function, total, symbol(isStrKeyV),   no-evaluators]
                | isUpperKeyV(Val) [function, total, symbol(isUpperKeyV), no-evaluators]
                | isLowerKeyV(Val) [function, total, symbol(isLowerKeyV), no-evaluators]

  // junk-narrow legs: a heap ref is not a str key (the deref narrower branches
  // the abstract key toward ref/cellRef; the intended model rejects both)
  rule isStrKeyV(ref(_:Int))     => false [simplification]
  rule isStrKeyV(cellRef(_:Int)) => false [simplification]

  // isinstance(key, str) -> opaque isStrKeyV (interception + the isStrV owise-residue order).
  rule applyBuiltin("isinstance", valSeqAt(KS:ValSeq, I:Int), typeV("str"), .Vals)
    => isStrKeyV(valSeqAt(KS, I)) [simplification]
  rule isStrV(valSeqAt(KS:ValSeq, I:Int)) => isStrKeyV(valSeqAt(KS, I)) [simplification]

  // key.isupper() / key.islower() -> opaque (the real applyMethod folds over symbolic char codes).
  rule applyMethod(valSeqAt(KS:ValSeq, I:Int), "isupper", .Vals) => isUpperKeyV(valSeqAt(KS, I)) [simplification]
  rule applyMethod(valSeqAt(KS:ValSeq, I:Int), "islower", .Vals) => isLowerKeyV(valSeqAt(KS, I)) [simplification]

  // ---- summary: the buggy 2-key result. k0 = valSeqAt(KS,0), k1 = valSeqAt(KS,1). Guards are the
  // EXACT branch path-condition forms (`notBool(vsLen==0)` / `notBool(vsLen==1)`, matching the program's
  // `n==0` / `n==1` case-splits) so kore discharges them without a vsLen>=0 fact.
  //   n==0                                  -> false
  //   k0 not str                            -> false
  //   k0 upper                              -> cdcTail(KS, true)      (first == "upper")
  //   k0 lower (not upper)                  -> cdcTail(KS, false)     (first == "lower")
  //   k0 str but neither upper nor lower    -> false
  syntax Bool ::= checkDictRes(ValSeq) [function, total, no-evaluators]
  rule checkDictRes(KS:ValSeq) => false requires vsLen(KS) ==Int 0 [simplification]
  rule checkDictRes(KS:ValSeq) => false
    requires notBool (vsLen(KS) ==Int 0) andBool notBool isStrKeyV(valSeqAt(KS, 0)) [simplification]
  rule checkDictRes(KS:ValSeq) => cdcTail(KS, true)
    requires notBool (vsLen(KS) ==Int 0) andBool isStrKeyV(valSeqAt(KS, 0)) andBool isUpperKeyV(valSeqAt(KS, 0)) [simplification]
  rule checkDictRes(KS:ValSeq) => cdcTail(KS, false)
    requires notBool (vsLen(KS) ==Int 0) andBool isStrKeyV(valSeqAt(KS, 0))
             andBool notBool isUpperKeyV(valSeqAt(KS, 0)) andBool isLowerKeyV(valSeqAt(KS, 0)) [simplification]
  rule checkDictRes(KS:ValSeq) => false
    requires notBool (vsLen(KS) ==Int 0) andBool isStrKeyV(valSeqAt(KS, 0))
             andBool notBool isUpperKeyV(valSeqAt(KS, 0)) andBool notBool isLowerKeyV(valSeqAt(KS, 0)) [simplification]

  // cdcTail(KS, firstIsUpper): n==1 -> True; n>=2 (notBool(vsLen==1), ambient notBool(vsLen==0)) ->
  // the k1 checks (k1 not str -> False; else its case).
  syntax Bool ::= cdcTail(ValSeq, Bool) [function, total, no-evaluators]
  rule cdcTail(KS:ValSeq, _B:Bool) => true requires vsLen(KS) ==Int 1 [simplification]
  rule cdcTail(KS:ValSeq, _B:Bool) => false
    requires notBool (vsLen(KS) ==Int 1) andBool notBool isStrKeyV(valSeqAt(KS, 1)) [simplification]
  rule cdcTail(KS:ValSeq, true) => isUpperKeyV(valSeqAt(KS, 1))
    requires notBool (vsLen(KS) ==Int 1) andBool isStrKeyV(valSeqAt(KS, 1)) [simplification]
  rule cdcTail(KS:ValSeq, false) => isLowerKeyV(valSeqAt(KS, 1))
    requires notBool (vsLen(KS) ==Int 1) andBool isStrKeyV(valSeqAt(KS, 1)) [simplification]
endmodule
