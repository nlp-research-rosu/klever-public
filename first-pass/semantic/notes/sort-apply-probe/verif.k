// Probe: can a program LOOP over the (opaque) trusted sort output? Model sortI (opaque symbolic),
// then a driver that sums the sorted list. If the loop can't consume sortI(L), the sort-output
// problems (33/37/105) are blocked mid-execution regardless of the correctness framework.
module APPLY
  imports INT
  imports BOOL
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  syntax IntSeq ::= sortI(IntSeq) [function, total, symbol(sortI), no-evaluators]
  // (no concrete rules needed for the probe; opaque on symbolic input)
  syntax Int ::= sumOf(IntSeq) [function, total]
  rule sumOf(.IntSeq) => 0 [simplification]
  rule sumOf(iCons(X:Int, R:IntSeq)) => X +Int sumOf(R) [simplification]
  // driver: sum a list by consuming it in the <k> cell
  syntax KItem ::= sumLoop(IntSeq, Int)
  rule <k> sumLoop(.IntSeq, A:Int) => A ... </k>
  rule <k> sumLoop(iCons(X:Int, R:IntSeq), A:Int) => sumLoop(R, A +Int X) ... </k>
  configuration <k> $PGM:K </k>
endmodule
