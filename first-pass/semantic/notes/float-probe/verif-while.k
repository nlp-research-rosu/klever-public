// Probe: can a WHILE loop with an OPAQUE-FLOAT guard do partial correctness? (32's bisection guard
// is `end - begin > 1e-10` on symbolic floats.) If the guard can't split, the loop can't execute.
module FPW
  imports FLOAT
  imports INT
  imports BOOL
  syntax Float ::= step(Float) [function, total, no-evaluators]     // opaque float update
  syntax Bool  ::= guard(Float) [function, total, no-evaluators]    // opaque float guard
  syntax Float ::= wsum(Float, Float) [function, total]             // summary (partial)
  syntax KItem ::= wloop(Float, Float)
  rule <k> wloop(B:Float, ACC:Float) => ACC ... </k> requires notBool guard(B)
  rule <k> wloop(B:Float, ACC:Float) => wloop(step(B), ACC) ... </k> requires guard(B)
  configuration <k> $PGM:K </k>
endmodule
