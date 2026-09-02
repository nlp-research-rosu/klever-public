requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // The source contract's input domain.
  syntax Bool ::= nonNegativeVals(ValSeq) [function, total]
  rule nonNegativeVals(.ValSeq) => true
  rule nonNegativeVals(vCons(I:Int, R:ValSeq))
    => I >=Int 0 andBool nonNegativeVals(R)
  rule nonNegativeVals(vCons(_V:Val, _R:ValSeq)) => false [owise]

  // State transformers for the loop.  These are definitional summaries: they
  // describe final scalar state but never rewrite an MPY program computation.
  syntax Int ::= nextRepeated(Val, Int, Val) [function, total]
  rule nextRepeated(P:Val, C:Int, V:Val) => C +Int 1
    requires V ==K P
  rule nextRepeated(P:Val, _C:Int, V:Val) => 1
    requires notBool (V ==K P)

  syntax Val ::= scanPrevious(Val, ValSeq) [function, total]
  rule scanPrevious(P:Val, .ValSeq) => P
  rule scanPrevious(_P:Val, vCons(V:Val, R:ValSeq))
    => scanPrevious(V, R)

  syntax Int ::= scanRepeated(Val, Int, ValSeq) [function, total]
  rule scanRepeated(_P:Val, C:Int, .ValSeq) => C
  rule scanRepeated(P:Val, C:Int, vCons(V:Val, R:ValSeq))
    => scanRepeated(V, nextRepeated(P, C, V), R)

  syntax Val ::= scanValue(Val, ValSeq) [function, total]
  rule scanValue(V:Val, .ValSeq) => V
  rule scanValue(_V:Val, vCons(V:Val, R:ValSeq))
    => scanValue(V, R)

  syntax Bool ::= duplicateOK(Val, Int, ValSeq) [function, total]
  rule duplicateOK(_P:Val, _C:Int, .ValSeq) => true
  rule duplicateOK(P:Val, C:Int, vCons(V:Val, R:ValSeq))
    => notBool (nextRepeated(P, C, V) >Int 2)
       andBool duplicateOK(V, nextRepeated(P, C, V), R)

  syntax Bool ::= scanDuplicates(Val, Int, Bool, ValSeq)
                  [function, total]
  rule scanDuplicates(P:Val, C:Int, B:Bool, VS:ValSeq)
    => B andBool duplicateOK(P, C, VS)

  // Human-facing contract predicate.  sortVS is the supplied semantics'
  // explicitly trusted ascending-permutation primitive.  The second conjunct
  // says that every input value occurs at most twice.
  syntax Bool ::= sortedWithAtMostTwo(ValSeq) [function]
  rule sortedWithAtMostTwo(VS:ValSeq)
    => (VS ==K sortVS(VS))
       andBool scanDuplicates(-1, 0, true, VS)
    requires nonNegativeVals(VS)
endmodule
