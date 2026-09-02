// The REAL test: Collatz loop (3n+1 branch), which is NOT known to terminate. Threaded accumulator.
// If [all-path] + circularity closes this, kprove gives PARTIAL correctness with NO termination proof.
module PARTIAL4
  imports INT
  imports BOOL
  syntax Int ::= cAcc(Int, Int) [function, total]
  rule cAcc(N:Int, C:Int) => C requires N <=Int 1 [simplification]
  rule cAcc(N:Int, C:Int) => cAcc(N /Int 2, C +Int 1)        requires N >Int 1 andBool N %Int 2 ==Int 0 [simplification]
  rule cAcc(N:Int, C:Int) => cAcc(3 *Int N +Int 1, C +Int 1) requires N >Int 1 andBool N %Int 2 =/=Int 0 [simplification]
  syntax KItem ::= loop(Int, Int)
  rule <k> loop(N:Int, C:Int) => C ... </k> requires N <=Int 1
  rule <k> loop(N:Int, C:Int) => loop(N /Int 2, C +Int 1) ... </k>        requires N >Int 1 andBool N %Int 2 ==Int 0
  rule <k> loop(N:Int, C:Int) => loop(3 *Int N +Int 1, C +Int 1) ... </k> requires N >Int 1 andBool N %Int 2 =/=Int 0
  configuration <k> $PGM:K </k>
endmodule
