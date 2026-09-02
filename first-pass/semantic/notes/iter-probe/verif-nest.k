// notes/iter-probe/verif-nest.k — the Iterable-sort shape in miniature.
// g is a [total] function over an Iterable sort whose one constructor `wrap`
// wraps the symbolic ValSeq — mirroring iterNext(list(VS)). Question: does
// [total] still narrow when the symbolic part is NESTED under a known ctor?

module ITER-NEST
  imports INT
  imports BOOL

  syntax ValSeq   ::= ".ValSeq" | vCons(Int, ValSeq)
  syntax Iterable ::= wrap(ValSeq)                        // known ctor around the symbolic seq

  syntax IStep ::= "iDone" | iYield(Int, Iterable)
  syntax IStep ::= g(Iterable) [function, total]
  rule g(wrap(.ValSeq))                => iDone
  rule g(wrap(vCons(X:Int, R:ValSeq))) => iYield(X, wrap(R))

  syntax KItem ::= #drive(Iterable) | #step(IStep)
  rule <k> #drive(IT:Iterable)               => #step(g(IT)) ... </k>
  rule <k> #step(iDone)                      => .K ... </k>
  rule <k> #step(iYield(_X:Int, R:Iterable)) => #drive(R) ... </k>

  configuration <k> $PGM:KItem </k>
endmodule
