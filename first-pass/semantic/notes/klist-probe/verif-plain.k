// verif-plain.k — BASELINE: heterogeneous cons list, NO Int refinement anywhere.
// The cast-free length loop is the shared test harness of the 3-way differential
// (plain / subsort / overload): it never reads an element, so no cast can be involved.
//
//   kompile verif-plain.k --backend haskell --main-module VERIF-PLAIN --syntax-module VERIF-PLAIN --output-definition verif-plain-kompiled
module VERIF-PLAIN
  imports INT
  imports BOOL
  imports K-EQUAL

  syntax Val    ::= Int | "other" | list(ValSeq)
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)

  syntax KItem ::= cloop(Val)
  configuration <k> $PGM:K </k> <acc> 0 </acc>

  rule <k> cloop(list(.ValSeq)) => .K ... </k>
  rule <k> cloop(list(vCons(_:Val, R:ValSeq))) => cloop(list(R)) ... </k>
       <acc> A:Int => A +Int 1 </acc>

  syntax Int ::= lenAcc(ValSeq, Int) [function, total]
  rule lenAcc(.ValSeq, A:Int) => A [simplification]
  rule lenAcc(vCons(_:Val, R:ValSeq), A:Int) => lenAcc(R, A +Int 1) [simplification]
endmodule
