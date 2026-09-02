// verification.k — max_fill on the UNIFIED semantics. A grid is a LIST OF INT LISTS
// list(vCons(list(row0), ...)); the outer loop sums, per row, the integer-ceil
// (sum(row)+cap-1)//cap. This opens the 2D-grid rung: each row is a symbolic list Val, projected to
// its ValSeq by rowProj (the codesProj analog, one level up) under an allList precondition; sum(row)
// is intercepted at #applyK to the actual sum sumVS(rowProj(row)) (the #sumAcc fold is stuck on a
// symbolic row). The per-row sum is VERIFIED (the real sum), not trusted. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module MAX-FILL-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- list-of-lists: project a row (a list Val) to its ValSeq; allList precondition. isListV is
  // a custom predicate (list is a constructor, not a sort, so there is no builtin isList).
  syntax ValSeq ::= rowProj(Val) [function, total, symbol(rowProj), no-evaluators]
  rule rowProj(list(RS:ValSeq)) => RS [simplification]

  syntax Bool ::= isListV(Val) [function]
  rule isListV(list(_:ValSeq)) => true [simplification]

  syntax Bool ::= allList(ValSeq) [function, total]
  rule allList(.ValSeq) => true [simplification]
  rule allList(vCons(V:Val, R:ValSeq)) => isListV(V) andBool allList(R) [simplification]

  // NOTE (de-escape rework): the former #applyK sum interception is REMOVED (the
  // pattern this rework eliminates). The shared builtin now sums a symbolic int
  // list (sumIntVS in semantics/builtins.k); this proof is rebuilt on it at P115.

  syntax Int ::= sumVS(ValSeq) [function, total]
  rule sumVS(.ValSeq) => 0 [simplification]
  rule sumVS(vCons(V:Val, S:ValSeq)) => projectIntTotal(V) +Int sumVS(S) [simplification]

  // Python floored // (pyMod-based; matches applyBin("//", ...)).
  syntax Int ::= fdiv(Int, Int) [function]
  rule fdiv(A:Int, B:Int) => (A -Int pyMod(A, B)) /Int B requires B =/=Int 0

  // outer fold: total += (sum(row)+cap-1)//cap over the grid rows.
  syntax Int ::= fillFrom(Int, ValSeq, Int) [function, total]
  rule fillFrom(ACC:Int, .ValSeq, _CAP:Int) => ACC [simplification]
  rule fillFrom(ACC:Int, vCons(V:Val, REST:ValSeq), CAP:Int)
    => fillFrom(ACC +Int fdiv(sumVS(rowProj(V)) +Int CAP -Int 1, CAP), REST, CAP)
    requires CAP =/=Int 0 [simplification]
endmodule
