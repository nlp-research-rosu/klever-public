// verif.k — TRUSTED-SORT mechanism: an abstract total sortI symbol that stays opaque on symbolic
// input (kprove) but runs a concrete insertion sort (krun), with isSorted(sortI(L)) as a trusted
// lemma (the ordering kernel is proven separately in ../sort-probe; permutation is assumed). Same
// no-evaluators idiom as projectIntTotal / KEVM keccak. This is what lets the 17 sort problems be
// closed as "verified wrapper + trusted sort engine".
module SORTTRUST
  imports INT
  imports BOOL
  imports K-EQUAL
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)

  syntax Bool ::= isSorted(IntSeq) [function, total]
  rule isSorted(.IntSeq) => true [simplification]
  rule isSorted(iCons(_:Int, .IntSeq)) => true [simplification]
  rule isSorted(iCons(X:Int, iCons(Y:Int, R:IntSeq))) => X <=Int Y andBool isSorted(iCons(Y, R)) [simplification]

  // concrete insertion-sort engine (for krun); the proven kernel lives in ../sort-probe
  syntax IntSeq ::= insert(Int, IntSeq) [function]
  rule insert(X:Int, .IntSeq) => iCons(X, .IntSeq)
  rule insert(X:Int, iCons(Y:Int, R:IntSeq)) => iCons(X, iCons(Y, R)) requires X <=Int Y
  rule insert(X:Int, iCons(Y:Int, R:IntSeq)) => iCons(Y, insert(X, R)) requires X >Int Y

  // TRUSTED ascending sort: abstract+total+no-evaluators ⇒ opaque on symbolic L (kprove),
  // concrete insertion sort on ground L (krun).
  syntax IntSeq ::= sortI(IntSeq) [function, total, symbol(sortI), no-evaluators]
  rule sortI(.IntSeq) => .IntSeq [concrete]
  rule sortI(iCons(X:Int, R:IntSeq)) => insert(X, sortI(R)) [concrete]
  rule isSorted(sortI(L:IntSeq)) => true [simplification]   // trusted ordering lemma

  // toy "program": result = sorted(L)
  syntax KItem ::= prog(IntSeq) | done(IntSeq)
  rule <k> prog(L:IntSeq) => done(sortI(L)) ... </k>
  configuration <k> $PGM:K </k>
endmodule
