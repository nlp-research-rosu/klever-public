// Threaded-accumulator summary (matches the working proofs: primeAcc/lastFold thread the acc).
// stepAcc(n, c) unfolds structurally in LOCKSTEP with the loop -> no additive reassociation.
module PARTIAL3
  imports INT
  imports BOOL
  syntax Int ::= stepAcc(Int, Int) [function, total]
  rule stepAcc(N:Int, C:Int) => C requires N <=Int 1 [simplification]
  rule stepAcc(N:Int, C:Int) => stepAcc(N /Int 2, C +Int 1) requires N >Int 1 [simplification]
  syntax KItem ::= loop(Int, Int)
  rule <k> loop(N:Int, C:Int) => C ... </k> requires N <=Int 1
  rule <k> loop(N:Int, C:Int) => loop(N /Int 2, C +Int 1) ... </k> requires N >Int 1
  configuration <k> $PGM:K </k>
endmodule
