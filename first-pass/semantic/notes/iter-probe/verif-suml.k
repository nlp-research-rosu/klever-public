// notes/iter-probe/verif-suml.k — sum probe + INVERSION lemmas (can we hand kprove the inversion?)
// Same [total] g over Iterable as `nest`, but the claim asserts an accumulator
// equals a STRUCTURAL summary ssum(VS,_) — the shape of a real loop invariant
// (prefixSum). Tests whether [total]-narrowing gives the structural VS the
// summary needs, or only an opaque g(wrap(VS))=iDone constraint.

module ITER-SUML
  imports INT
  imports BOOL
  imports K-EQUAL

  syntax ValSeq   ::= ".ValSeq" | vCons(Int, ValSeq)
  syntax Iterable ::= wrap(ValSeq)

  syntax IStep ::= "iDone" | iYield(Int, Iterable)
  syntax IStep ::= g(Iterable) [function, total]
  rule g(wrap(.ValSeq))                => iDone
  rule g(wrap(vCons(X:Int, R:ValSeq))) => iYield(X, wrap(R))

  // ssum is [total] to match the real prefixSum — so the residual obligation is the
  // PURE structural one (A == ssum(VS,A)); a partial [function] would add a
  // #Ceil(ssum(VS,A)) definedness conjunct the real (total) summary never has.
  syntax Int ::= ssum(ValSeq, Int) [function, total]
  rule ssum(.ValSeq, A:Int)                => A
  rule ssum(vCons(X:Int, R:ValSeq), A:Int) => ssum(R, A +Int X)

  syntax KItem ::= #drive(Iterable) | #step(IStep)
  configuration <k> $PGM:KItem </k> <acc> 0:Int </acc>
  rule <k> #drive(IT:Iterable)         => #step(g(IT)) ... </k>
  rule <k> #step(iDone)                => .K ... </k>
  rule <k> #step(iYield(X:Int, R:Iterable)) => #drive(R) ... </k> <acc> A:Int => A +Int X </acc>

  // INVERSION lemmas: recover VS's structure from the iterator step's value.
  // (the thing kprove does NOT do on its own for a [total] function)
  rule ssum(VS, A:Int) => A                    requires g(wrap(VS)) ==K iDone           [simplification]
  rule ssum(VS, A:Int) => ssum(R, A +Int X)    requires g(wrap(VS)) ==K iYield(X, wrap(R)) [simplification]
endmodule
