// notes/iter-probe/verif-partial.k — the [total] hypothesis.
// Same shape as verif-fn.k, but f is over a bare ValSeq (both constructors
// covered => genuinely [total]) and marked [function]. Question: does
// totality make kprove narrow the symbolic VS that plain [function] would not?

module ITER-PARTIAL
  imports INT
  imports BOOL

  syntax ValSeq ::= ".ValSeq" | vCons(Int, ValSeq)

  syntax IStep ::= "iDone" | iYield(Int, ValSeq)
  syntax IStep ::= f(ValSeq) [function]
  rule f(.ValSeq)                => iDone
  rule f(vCons(X:Int, R:ValSeq)) => iYield(X, R)

  syntax KItem ::= #drive(ValSeq) | #step(IStep)
  rule <k> #drive(VS:ValSeq)               => #step(f(VS)) ... </k>
  rule <k> #step(iDone)                     => .K ... </k>
  rule <k> #step(iYield(_X:Int, R:ValSeq))  => #drive(R) ... </k>

  configuration <k> $PGM:KItem </k>
endmodule
