// Probe v3: nested loop threading an OPAQUE accumulator (stepI has no rules on symbolic input),
// simulating 20's min-tracking triple. Tests: does the opaque accumulator survive the inner->outer
// boundary capture (CV:Int ~> #afterInner) through nesting?
module NESTOP
  imports INT
  imports BOOL
  syntax Int ::= stepI(Int, Int) [function, total, no-evaluators]   // opaque update (like closestStep)
  syntax Int ::= innerAcc(Int, Int, Int) [function, total]
  rule innerAcc(J:Int, HI:Int, A:Int) => A requires J >=Int HI [simplification]
  rule innerAcc(J:Int, HI:Int, A:Int) => innerAcc(J +Int 1, HI, stepI(A, J)) requires J <Int HI [simplification]
  syntax Int ::= outerAcc(Int, Int, Int) [function, total]
  rule outerAcc(I:Int, HI:Int, A:Int) => A requires I >=Int HI [simplification]
  rule outerAcc(I:Int, HI:Int, A:Int) => outerAcc(I +Int 1, HI, innerAcc(0, HI, A)) requires I <Int HI [simplification]

  syntax KItem ::= innerLoop(Int, Int, Int) | outerLoop(Int, Int, Int) | #afterInner(Int, Int)
  rule <k> innerLoop(J:Int, HI:Int, A:Int) => A ... </k> requires J >=Int HI
  rule <k> innerLoop(J:Int, HI:Int, A:Int) => innerLoop(J +Int 1, HI, stepI(A, J)) ... </k> requires J <Int HI
  rule <k> outerLoop(I:Int, HI:Int, A:Int) => A ... </k> requires I >=Int HI
  rule <k> outerLoop(I:Int, HI:Int, A:Int) => innerLoop(0, HI, A) ~> #afterInner(I, HI) ... </k> requires I <Int HI
  rule <k> CV:Int ~> #afterInner(I:Int, HI:Int) => outerLoop(I +Int 1, HI, CV) ... </k>
  configuration <k> $PGM:K </k>
endmodule
