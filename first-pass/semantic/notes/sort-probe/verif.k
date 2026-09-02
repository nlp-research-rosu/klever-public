// verif3.k — insert preserves sortedness, proven by execution-driven circularity that carries a
// LOWER BOUND through the recursion (mirrors K's insertion-sort-spec: requires sorted(prefix) +
// the head bound, ensures sorted(result)). The list splits in the <k> open; the bound resolves the
// "head of the opaque recursive insert" obligation that a bare isSorted(insert(X,L)) cannot close.
module SORT
  imports INT
  imports BOOL
  imports K-EQUAL
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)

  syntax Bool ::= isSorted(IntSeq) [function, total]
  rule isSorted(.IntSeq) => true [simplification]
  rule isSorted(iCons(_:Int, .IntSeq)) => true [simplification]
  rule isSorted(iCons(X:Int, iCons(Y:Int, R:IntSeq))) => X <=Int Y andBool isSorted(iCons(Y, R)) [simplification]

  syntax IntSeq ::= insert(Int, IntSeq) [function, total]
  rule insert(X:Int, .IntSeq) => iCons(X, .IntSeq) [simplification]
  rule insert(X:Int, iCons(Y:Int, R:IntSeq)) => iCons(X, iCons(Y, R)) requires X <=Int Y [simplification]
  rule insert(X:Int, iCons(Y:Int, R:IntSeq)) => iCons(Y, insert(X, R)) requires X >Int Y [simplification]

  // head of insert (non-inductive: determined by X vs the first element only)
  syntax Int ::= ihead(IntSeq) [function]
  rule ihead(iCons(X:Int, _:IntSeq)) => X [simplification]
  rule ihead(insert(X:Int, .IntSeq)) => X [simplification]
  rule ihead(insert(X:Int, iCons(Y:Int, _R:IntSeq))) => minInt(X, Y) [simplification]

  // BRIDGE: isSorted of a cons onto the opaque recursive insert term (insert is always nonempty,
  // head = ihead(insert(...))). Lets isSorted see past the unreduced insert(X,R).
  rule isSorted(iCons(B:Int, insert(X:Int, R:IntSeq)))
    => B <=Int ihead(insert(X, R)) andBool isSorted(insert(X, R)) [simplification]

  // head lower bound of the input (B bounds the head; with isSorted ⇒ B bounds all elements)
  syntax Bool ::= lbHead(Int, IntSeq) [function, total]
  rule lbHead(_:Int, .IntSeq) => true [simplification]
  rule lbHead(B:Int, iCons(Y:Int, _R:IntSeq)) => B <=Int Y [simplification]

  // driver: splits L in the <k> open, recurses on the tail with the new bound = circularity
  syntax KItem ::= ind(Int, Int, IntSeq)
  rule <k> ind(_B:Int, _X:Int, .IntSeq) => .K ... </k>
  rule <k> ind(_B:Int, X:Int, iCons(Y:Int, _R:IntSeq)) => .K ... </k> requires X <=Int Y
  rule <k> ind(_B:Int, X:Int, iCons(Y:Int, R:IntSeq)) => ind(Y, X, R) ... </k> requires X >Int Y

  // ==== PERMUTATION half: insert(X,L) is a permutation of X::L =================================
  // multiset via occurrence count.  count(Y, iCons(Z, M)) reduces for ANY M (the outer cons is
  // visible), so count sees past the opaque recursive insert(X,R) — no bound needed here.
  syntax Int ::= count(Int, IntSeq) [function, total]
  rule count(_Y:Int, .IntSeq) => 0 [simplification]
  // peel the cons UNCONDITIONALLY (Z ==Int Y stays symbolic) so count reduces without deciding the
  // witness — the outer cons is always visible, so this sees past the opaque recursive insert(X,R).
  rule count(Y:Int, iCons(Z:Int, R:IntSeq)) => (#if Z ==Int Y #then 1 #else 0 #fi) +Int count(Y, R) [simplification]

  // driver: splits L in the <k> open, recurses on the tail = circularity
  syntax KItem ::= permInd(Int, Int, IntSeq)   // (Y witness, X inserted, L)
  rule <k> permInd(_Y:Int, _X:Int, .IntSeq) => .K ... </k>
  rule <k> permInd(_Y:Int, X:Int, iCons(Z:Int, _R:IntSeq)) => .K ... </k> requires X <=Int Z
  rule <k> permInd(Y:Int, X:Int, iCons(Z:Int, R:IntSeq)) => permInd(Y, X, R) ... </k> requires X >Int Z

  syntax KItem ::= run(Bool)
  rule <k> run(B:Bool) => B ... </k>
  configuration <k> $PGM:K </k>
endmodule
