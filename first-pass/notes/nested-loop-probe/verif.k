// Probe (v2): NESTED range-loop invariant, inner loop run in the <k> HEAD (so its circularity fires),
// with a continuation. outer i in [0,N), inner j in [0,N), count += 1. Claim: count ends C + N*N.
module NEST
  imports INT
  imports BOOL
  syntax Int ::= innerAcc(Int, Int, Int) [function, total]
  rule innerAcc(J:Int, HI:Int, C:Int) => C requires J >=Int HI [simplification]
  rule innerAcc(J:Int, HI:Int, C:Int) => innerAcc(J +Int 1, HI, C +Int 1) requires J <Int HI [simplification]
  syntax Int ::= outerAcc(Int, Int, Int) [function, total]
  rule outerAcc(I:Int, HI:Int, C:Int) => C requires I >=Int HI [simplification]
  rule outerAcc(I:Int, HI:Int, C:Int) => outerAcc(I +Int 1, HI, innerAcc(0, HI, C)) requires I <Int HI [simplification]

  syntax KItem ::= innerLoop(Int, Int, Int) | outerLoop(Int, Int, Int) | #afterInner(Int, Int)
  rule <k> innerLoop(J:Int, HI:Int, C:Int) => C ... </k> requires J >=Int HI
  rule <k> innerLoop(J:Int, HI:Int, C:Int) => innerLoop(J +Int 1, HI, C +Int 1) ... </k> requires J <Int HI
  // outer: run the inner loop in the HEAD, then continue via the continuation
  rule <k> outerLoop(I:Int, HI:Int, C:Int) => C ... </k> requires I >=Int HI
  rule <k> outerLoop(I:Int, HI:Int, C:Int) => innerLoop(0, HI, C) ~> #afterInner(I, HI) ... </k> requires I <Int HI
  rule <k> CV:Int ~> #afterInner(I:Int, HI:Int) => outerLoop(I +Int 1, HI, CV) ... </k>
  configuration <k> $PGM:K </k>
endmodule
