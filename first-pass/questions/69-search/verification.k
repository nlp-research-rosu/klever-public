// verification.k — search on the UNIFIED semantics. Nested COUNT + MAX. "greatest i such that i
// occurs >= i times" — reformulated (no freq array indexed by symbolic max) as: for each candidate
// v in 1..n, count occurrences of v (inner scan, element==candidate via the mixed isInt echo), and
// keep the largest v with count(v) >= v. Since freq(v) <= n, any valid v <= n, so candidates 1..n
// cover all of them. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module SEARCH-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // inner count over j in [J, N): C + (number of j with lst[j] == V). Guarded case-split.
  syntax Int ::= countFold(Int, Int, Int, ValSeq, Int) [function, total]
  rule countFold(J:Int, N:Int, _V:Int, _VS:ValSeq, C:Int) => C requires J >=Int N [simplification]
  rule countFold(J:Int, N:Int, V:Int, VS:ValSeq, C:Int) => countFold(J +Int 1, N, V, VS, C +Int 1)
    requires J <Int N andBool projectIntTotal(valSeqAt(VS, J)) ==Int V [simplification]
  rule countFold(J:Int, N:Int, V:Int, VS:ValSeq, C:Int) => countFold(J +Int 1, N, V, VS, C)
    requires J <Int N andBool projectIntTotal(valSeqAt(VS, J)) =/=Int V [simplification]

  // outer scan over v in [V, HI): ans := v when countFold(0, N, v, VS, 0) >= v (v increases, so the
  // LAST match is the greatest). Guarded case-split on the count comparison.
  syntax Int ::= searchFold(Int, Int, ValSeq, Int, Int) [function, total]
  rule searchFold(V:Int, HI:Int, _VS:ValSeq, _N:Int, ANS:Int) => ANS requires V >=Int HI [simplification]
  rule searchFold(V:Int, HI:Int, VS:ValSeq, N:Int, _ANS:Int) => searchFold(V +Int 1, HI, VS, N, V)
    requires V <Int HI andBool countFold(0, N, V, VS, 0) >=Int V [simplification]
  rule searchFold(V:Int, HI:Int, VS:ValSeq, N:Int, ANS:Int) => searchFold(V +Int 1, HI, VS, N, ANS)
    requires V <Int HI andBool countFold(0, N, V, VS, 0) <Int V [simplification]

  // result: greatest v in 1..n with count(v) >= v, else -1.
  syntax Val ::= searchRes(ValSeq) [function]
  rule searchRes(VS:ValSeq) => searchFold(1, vsLen(VS) +Int 1, VS, vsLen(VS), -1) [simplification]
endmodule
