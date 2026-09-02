// verification.k — filter_integers on the UNIFIED semantics. Keep the list elements whose runtime
// type is int (order preserved). canonical uses `[x for x in values if isinstance(x, int)]`;
// solution.py rewrites it as an INDEX-based single loop `for i in range(len(values)): if
// isinstance(values[i], int): result += [values[i]]` (behaviorally identical — diff-tested 0/4005 over
// mixed lists of int/float/str/bool/None/list/dict/tuple).
//
// The unified isinstance is a k-cell owise dispatch (`isIntV(V) => false [owise]`) that is STUCK on a
// symbolic Val element — it can't decide the negative. Here isinstance(values[i], int) is intercepted
// PROBLEM-LOCALLY to an opaque isIntElemV(valSeqAt(VS, I)) — keyed on valSeqAt (the loop element) via
// [simplification], so it fires ONLY in kprove and ONLY on the symbolic-index term (krun runs the real
// isinstance on concrete elements — valSeqAt never appears there). The filter STRUCTURE is then
// verified via the Q26 dupFilter list-build fold, case-splitting on the opaque isIntElemV. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module FILTER-INTEGERS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- isinstance(values[i], int) on a symbolic list element -> opaque isIntElemV (case-splittable).
  // Two variants cover both reduction orders (the interception, and the isIntV owise-stuck residue).
  syntax Bool ::= isIntElemV(Val) [function, total, symbol(isIntElemV), no-evaluators]
  rule applyBuiltin("isinstance", valSeqAt(VS:ValSeq, I:Int), typeV("int"), .Vals)
    => isIntElemV(valSeqAt(VS, I)) [simplification]
  rule isIntV(valSeqAt(VS:ValSeq, I:Int)) => isIntElemV(valSeqAt(VS, I)) [simplification]
  // junk-narrow falsity legs (the P90 ghost-class pattern): the deref narrower
  // SUBSTITUTES claim variables, so the refutation must live in the predicate —
  // a heap ref is not an int (isinstance(<list>, int) is False); on a plain
  // Int the test is true
  rule isIntElemV(ref(_:Int))     => false [simplification]
  rule isIntElemV(cellRef(_:Int)) => false [simplification]
  rule isIntElemV(I:Int)          => true  [simplification]

  // FLAT-list domain (user-sanctioned deviation from canonical: no nested
  // containers): every element is a plain value, never a heap ref — the
  // deref-narrowed branches refute via the distribution (the P90 mechanism)
  syntax Bool ::= flatV(Val) [function]
  rule flatV(ref(_:Int))     => false [simplification]
  rule flatV(cellRef(_:Int)) => false [simplification]
  rule flatV(_:Int)          => true  [simplification]
  rule flatV(str(_:IntSeq))  => true  [simplification]
  rule flatV(_:Float)        => true  [simplification]
  rule flatV(_:Bool)         => true  [simplification]
  syntax Bool ::= allFlat(ValSeq) [function, total]
  rule allFlat(.ValSeq) => true [simplification]
  rule allFlat(vCons(V:Val, R:ValSeq)) => flatV(V) andBool allFlat(R) [simplification]

  // the deref narrower junk-branches values[i]=valSeqAt(VS,I) into {valSeqAt(VS,I) #Equals ref(_)};
  // the shared subscript killers only carry allInt/allStr, so under allFlat the ref branch survives
  // and the element read grinds. allFlat twins refute it (a flat-list element is never a heap ref).
  rule { ref(_:Int) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom
    requires allFlat(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals ref(_:Int) } => #Bottom
    requires allFlat(VS) [simplification]

  // ---- filter fold over i in [I, N): append values[i] to the result iff isIntElemV(values[i]).
  // Guarded case-split rules (the Q26 dupFilter / primeAcc pattern) — each branch lines up with the
  // program's `if isinstance(...)`. Builds a ValSeq via valSeqConcat (the list-accumulator shape).
  syntax ValSeq ::= intFilter(Int, Int, ValSeq, ValSeq) [function, total, no-evaluators]
  rule intFilter(I:Int, N:Int, _VS:ValSeq, R:ValSeq) => R requires I >=Int N [simplification]
  rule intFilter(I:Int, N:Int, VS:ValSeq, R:ValSeq)
    => intFilter(I +Int 1, N, VS, valSeqConcat(R, vCons(valSeqAt(VS, I), .ValSeq)))
    requires I <Int N andBool isIntElemV(valSeqAt(VS, I)) [simplification]
  rule intFilter(I:Int, N:Int, VS:ValSeq, R:ValSeq)
    => intFilter(I +Int 1, N, VS, R)
    requires I <Int N andBool notBool isIntElemV(valSeqAt(VS, I)) [simplification]

endmodule
