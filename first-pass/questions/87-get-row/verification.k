// verification.k — get_row on the UNIFIED semantics. A GENERAL (jagged) INT-grid 2D scan proof via LOOP
// INVARIANTS (not an entry-unroll). Ports the old inner+outer fold structure to unified ValSeq, and
// IMPLEMENTS the features a nested `lst[i][j]` on a symbolic row needs:
//
//   * rowProj (Q115 / two-d-grid-rung): project a row Val to its ValSeq.
//   * NESTED-SUBSCRIPT bridge: `lst[i]` = valSeqAt(VS,i) is a SYMBOLIC list Val (isListV, not
//     syntactically list(..)), so `applyIndex`/`seqLen` on it are stuck — bridge through rowProj.
//     isListV of an opaque row is derived from allList(VS) by an echo.
//   * DE-ESCAPED cell compare: under the allIntGrid domain the shared subscript lemma casts the
//     cell and `cell == x` reduces to a REAL atomic Int equality (case-split by #branch) — the
//     scan structure, coord order, AND the per-cell equality are all verified. No opaque symbols.
//
// Domain: allList(VS) (a list of lists), jagged OK. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module GETROW-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- 2D features: row projection + list predicate + the per-row echo.
  syntax ValSeq ::= rowProj(Val) [function, total, symbol(rowProj), no-evaluators]
  rule rowProj(list(RS:ValSeq)) => RS [simplification]

  syntax Bool ::= isListV(Val) [function]
  rule isListV(list(_:ValSeq)) => true [simplification]
  // an opaque row valSeqAt(VS,I) is a list when the whole grid is (allList) and I is in range.
  rule isListV(valSeqAt(VS:ValSeq, I:Int)) => true
    requires allList(VS) andBool 0 <=Int I andBool I <Int vsLen(VS) [simplification]

  syntax Bool ::= allList(ValSeq) [function, total]
  rule allList(.ValSeq) => true [simplification]
  rule allList(vCons(V:Val, R:ValSeq)) => isListV(V) andBool allList(R) [simplification]

  // the deref narrower junk-branches a row lst[i] into {valSeqAt(VS,I) #Equals ref(_)}; the shared
  // killers only carry allInt, so under the grid domain the ref branch survives and the row-subscript
  // grinds. allIntGrid twins refute it (a row of an int-grid is a list, never a ref).
  rule { ref(_:Int) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom
    requires allIntGrid(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals ref(_:Int) } => #Bottom
    requires allIntGrid(VS) [simplification]
  // the narrower also floats a dictV / tuple / str case for the row; a grid row is a list, refute all
  rule { dictV(_:ValSeq, _:ValSeq) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom
    requires allIntGrid(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals dictV(_:ValSeq, _:ValSeq) } => #Bottom
    requires allIntGrid(VS) [simplification]
  rule { tuple(_:ValSeq) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom
    requires allIntGrid(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals tuple(_:ValSeq) } => #Bottom
    requires allIntGrid(VS) [simplification]
  rule { str(_:IntSeq) #Equals valSeqAt(VS:ValSeq, _:Int) } => #Bottom
    requires allIntGrid(VS) [simplification]
  rule { valSeqAt(VS:ValSeq, _:Int) #Equals str(_:IntSeq) } => #Bottom
    requires allIntGrid(VS) [simplification]

  // ---- DE-ESCAPED domain: an INT grid (each row a list of ints) — faithful to the problem
  // statement ("find integers x"); the opaque cellEqV never meant anything on non-Int cells anyway.
  syntax Bool ::= allIntGrid(ValSeq) [function, total]
  rule allIntGrid(.ValSeq) => true [simplification]
  rule allIntGrid(vCons(V:Val, R:ValSeq))
    => isListV(V) andBool allInt(rowProj(V)) andBool allIntGrid(R) [simplification]
  // per-row echoes under the grid domain (mirror the allList/isListV echo shape).
  rule isListV(valSeqAt(VS:ValSeq, I:Int)) => true
    requires allIntGrid(VS) andBool 0 <=Int I andBool I <Int vsLen(VS) [simplification]
  rule allInt(rowProj(valSeqAt(VS:ValSeq, I:Int))) => true
    requires allIntGrid(VS) andBool 0 <=Int I andBool I <Int vsLen(VS) [simplification]

  // ---- nested-subscript / len bridges for a symbolic row Val (isListV).
  rule applyIndex(V:Val, I:Int) => valSeqAt(rowProj(V), I) requires isListV(V) andBool I >=Int 0 [simplification]
  rule seqLen(V:Val) => vsLen(rowProj(V))                  requires isListV(V) [simplification]

  // ---- the cell compare is now REAL: under allInt(RVS) the SHARED subscript lemma
  // (lemmas/subscript.k) casts the cell and applyCmp reduces to the atomic Int equality
  // projectIntTotal(valSeqAt(RVS, j)) ==Int x, which #branch case-splits. No opaque remains.

  // innerFold/outerFold are structurally total (base + step cover all indices); the [function]
  // declaration leaves #Ceil(fold) sticking when the fold lands in a heap-cell post (claim 2's
  // outerFold(..innerFold..)). Discharge it — the folds are always defined.
  rule #Ceil(innerFold(_:Int, _:Int, _:Int, _:ValSeq, _:Int, _:ValSeq)) => #Top [simplification]
  rule #Ceil(outerFold(_:Int, _:Int, _:ValSeq, _:Int, _:ValSeq)) => #Top [simplification]

  // ---- inner fold: jj in [JJ, K); column j = K-1-jj (descending); append tuple(i,j) when cell==x.
  syntax ValSeq ::= innerFold(Int, Int, Int, ValSeq, Int, ValSeq) [function]
  rule innerFold(JJ:Int, K:Int, _I:Int, _RVS:ValSeq, _X:Int, ACC:ValSeq) => ACC
    requires JJ >=Int K [simplification]
  rule innerFold(JJ:Int, K:Int, I:Int, RVS:ValSeq, X:Int, ACC:ValSeq)
    => innerFold(JJ +Int 1, K, I, RVS, X,
         valSeqConcat(ACC, vCons(tuple(vCons(I, vCons(K -Int 1 -Int JJ, .ValSeq))), .ValSeq)))
    requires JJ <Int K andBool projectIntTotal(valSeqAt(RVS, K -Int 1 -Int JJ)) ==Int X          [simplification]
  rule innerFold(JJ:Int, K:Int, I:Int, RVS:ValSeq, X:Int, ACC:ValSeq)
    => innerFold(JJ +Int 1, K, I, RVS, X, ACC)
    requires JJ <Int K andBool notBool (projectIntTotal(valSeqAt(RVS, K -Int 1 -Int JJ)) ==Int X) [simplification]

  // ---- outer fold: i in [I, M); each runs the inner fold over row i = rowProj(valSeqAt(VS,i)).
  syntax ValSeq ::= outerFold(Int, Int, ValSeq, Int, ValSeq) [function]
  rule outerFold(I:Int, M:Int, _VS:ValSeq, _X:Int, ACC:ValSeq) => ACC
    requires I >=Int M [simplification]
  rule outerFold(I:Int, M:Int, VS:ValSeq, X:Int, ACC:ValSeq)
    => outerFold(I +Int 1, M, VS, X,
         innerFold(0, vsLen(rowProj(valSeqAt(VS, I))), I, rowProj(valSeqAt(VS, I)), X, ACC))
    requires I <Int M [simplification]

endmodule
