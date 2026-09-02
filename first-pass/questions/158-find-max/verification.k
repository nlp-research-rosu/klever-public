// verification.k — find_max on the UNIFIED semantics. A list-of-strings argmax-FIRST reduce with a
// LEX-SMALLEST tie-break on distinct-character count. Elements are symbolic str Vals under allStr;
// each element's codes come via codesProj ([[list-of-strings-proj]]). Two TRUSTED opaque primitives:
// the set cardinality len(set(w)) = isLen(dedupCodes(codesProj(w))) (the reference set model), and
// the string order w < best = lexLt(codesProj(w), codesProj(best)) (K has no str `<`). The argmax
// STRUCTURE (which word wins) is verified; only the two primitives are opaque. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module FIND-MAX-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // set(w) on a symbolic str element bridges through codesProj to the reference set model
  // (setV of the distinct codes); len(setV(DS)) => isLen(DS) is already in mpy-builtins.
  rule applyBuiltin("set", V:Val, .Vals) => setV(dedupCodes(codesProj(V))) requires isStr(V) [simplification]

  // str `<`: the reference strLt (mpy-str.k) — CONCRETE for krun, OPAQUE on symbolic code-seqs
  // (kprove). For a symbolic str ELEMENT (not syntactically str(...)) bridge through codesProj;
  // the concrete-str-form seed str(XC0) is handled by the shared applyCmp("<", str, str) rule
  // (same strLt), so body and summary agree. Threaded through the beats guard, never decided.
  rule applyCmp("<", V:Val, W:Val) => strLt(codesProj(V), codesProj(W))
    requires isStr(V) andBool isStr(W) [simplification]

  // distinct(V) = # of distinct characters = len(set(V)) (matches the body's stored d).
  syntax Int ::= distinct(Val) [function, total]
  rule distinct(V:Val) => isLen(dedupCodes(codesProj(V))) [simplification]

  // beats(W, BEST, BD): does word W beat the running best (word BEST, distinct count BD)? EXACTLY
  // the body's  d > best_d or (d == best_d and w < best)  (strict BoolOp, no folding lemma needed).
  syntax Bool ::= beats(Val, Val, Int) [function, total]
  rule beats(W:Val, BEST:Val, BD:Int)
    => (distinct(W) >Int BD) orBool ((distinct(W) ==Int BD) andBool strLt(codesProj(W), codesProj(BEST)))
    [simplification]

  // findBest(VS, BEST, BD) = the winning word after folding VS. GUARDED case-split on `beats`
  // (the primeAcc pattern) — this ALIGNS with the body's `best = w if beats else best` IfExp split
  // on the UNIFIED semantics (IfExp case-splits truthy(beats); it does not build a K-EQUAL #if).
  syntax Val ::= findBest(ValSeq, Val, Int) [function, total]
  rule findBest(.ValSeq, BEST:Val, _BD:Int) => BEST [simplification]
  rule findBest(vCons(W:Val, VS:ValSeq), BEST:Val, BD:Int) => findBest(VS, W, distinct(W))
    requires beats(W, BEST, BD) [simplification]
  rule findBest(vCons(W:Val, VS:ValSeq), BEST:Val, BD:Int) => findBest(VS, BEST, BD)
    requires notBool beats(W, BEST, BD) [simplification]

  // finalD threads the coupled best_d (needed so the invariant carries best_d through induction).
  syntax Int ::= finalD(ValSeq, Val, Int) [function, total]
  rule finalD(.ValSeq, _BEST:Val, BD:Int) => BD [simplification]
  rule finalD(vCons(W:Val, VS:ValSeq), BEST:Val, BD:Int) => finalD(VS, W, distinct(W))
    requires beats(W, BEST, BD) [simplification]
  rule finalD(vCons(W:Val, VS:ValSeq), BEST:Val, BD:Int) => finalD(VS, BEST, BD)
    requires notBool beats(W, BEST, BD) [simplification]
endmodule
