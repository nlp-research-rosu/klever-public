// verif-subsort.k — verif-plain.k + the Int-refined list declared the "simple" way:
// a plain subsort, NO [overload] tags. Kompiles fine; the rows show what proofs can
// (cannot) do with it, and that even bare-ValSeq claims break once the subsort exists.
//
//   kompile verif-subsort.k --backend haskell --main-module VERIF-SUBSORT --syntax-module VERIF-SUBSORT --output-definition verif-subsort-kompiled
module VERIF-SUBSORT
  imports INT
  imports BOOL
  imports K-EQUAL

  syntax Val    ::= Int | "other" | list(ValSeq)
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
  syntax IntVs  ::= ".IntVs"  | vCons(Int, IntVs)
  syntax ValSeq ::= IntVs

  syntax KItem ::= cloop(Val)
  configuration <k> $PGM:K </k> <acc> 0 </acc>

  rule <k> cloop(list(.ValSeq)) => .K ... </k>
  rule <k> cloop(list(vCons(_:Val, R:ValSeq))) => cloop(list(R)) ... </k>
       <acc> A:Int => A +Int 1 </acc>

  syntax Int ::= lenAcc(ValSeq, Int) [function, total]
  rule lenAcc(.ValSeq, A:Int) => A [simplification]
  rule lenAcc(vCons(_:Val, R:ValSeq), A:Int) => lenAcc(R, A +Int 1) [simplification]

  syntax Int ::= lenI(IntVs, Int) [function, total]
  rule lenI(.IntVs, A:Int) => A [simplification]
  rule lenI(vCons(_:Int, R:IntVs), A:Int) => lenI(R, A +Int 1) [simplification]
endmodule
