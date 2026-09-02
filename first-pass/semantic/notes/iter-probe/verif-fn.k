// notes/iter-probe/verif-fn.k — iterNext as a [FUNCTION] (the FAILING wiring).
// Minimal model of the loop dispatch: a list of ints, an iterator step, and a
// driver that walks the whole list. The ONLY thing under test is how iterNext
// is wired; everything else is identical to verif-rw.k.

module ITER-FN
  imports INT
  imports BOOL

  syntax ValSeq ::= ".ValSeq" | vCons(Int, ValSeq)
  syntax Val    ::= list(ValSeq)

  // the iterator step, as a FUNCTION — evaluated by MATCHING only.
  syntax IStep ::= "iDone" | iYield(Int, Val)
  syntax IStep ::= iterNext(Val) [function]
  rule iterNext(list(.ValSeq))                => iDone
  rule iterNext(list(vCons(X:Int, R:ValSeq))) => iYield(X, list(R))

  // driver: consume the whole iterable one element at a time.
  // NOTE: iterNext(V) is passed as an ARGUMENT to #step — it must reduce as a
  // function before any #step rule can match.
  syntax KItem ::= #drive(Val) | #step(IStep)
  rule <k> #drive(V:Val)                   => #step(iterNext(V)) ... </k>
  rule <k> #step(iDone)                    => .K ... </k>
  rule <k> #step(iYield(_X:Int, REST:Val)) => #drive(REST) ... </k>

  configuration <k> $PGM:KItem </k>
endmodule
