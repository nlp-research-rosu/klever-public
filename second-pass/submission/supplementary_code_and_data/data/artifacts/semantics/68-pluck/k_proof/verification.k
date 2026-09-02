requires "reference-semantics/semantics.k"

module PLUCK-VERIFICATION
  imports MPY

  syntax Int ::= asInt(Val) [function, total]
  rule asInt(I:Int) => I

  // Derived specialization of MPY-LIST's iterator rule.  Its higher priority
  // exposes the contract's integer element sort to symbolic execution; for
  // concrete integer lists it has exactly the same right-hand side as MPY.
  rule <k> #iterNext(list(vCons(V:Val, REST:ValSeq)))
        => #iterYield(asInt(V), list(REST)) ... </k>
       requires isInt(V)
       [priority(40)]

  // The predicate exactly captures when the implementation replaces its
  // current candidate.  B == -1 represents "no even value seen yet".
  syntax Bool ::= pluckTake(Int, Int) [function, total]
  rule pluckTake(V:Int, B:Int)
    => pyMod(V, 2) ==Int 0
       andBool (B ==Int -1 orBool V <Int B)

  syntax Int ::= nextBest(Int, Int) [function, total]
               | nextBestIndex(Int, Int, Int, Int) [function, total]
  rule nextBest(V:Int, B:Int) => V
    requires pyMod(V, 2) ==Int 0 andBool B ==Int -1
  rule nextBest(V:Int, B:Int) => V
    requires pyMod(V, 2) ==Int 0
     andBool B =/=Int -1 andBool V <Int B
  rule nextBest(V:Int, B:Int) => B
    requires pyMod(V, 2) =/=Int 0
  rule nextBest(V:Int, B:Int) => B
    requires pyMod(V, 2) ==Int 0
     andBool B =/=Int -1 andBool V >=Int B
  rule nextBestIndex(V:Int, B:Int, _:Int, I:Int) => I
    requires pyMod(V, 2) ==Int 0 andBool B ==Int -1
  rule nextBestIndex(V:Int, B:Int, _:Int, I:Int) => I
    requires pyMod(V, 2) ==Int 0
     andBool B =/=Int -1 andBool V <Int B
  rule nextBestIndex(V:Int, _B:Int, BI:Int, _:Int) => BI
    requires pyMod(V, 2) =/=Int 0
  rule nextBestIndex(V:Int, B:Int, BI:Int, _:Int) => BI
    requires pyMod(V, 2) ==Int 0
     andBool B =/=Int -1 andBool V >=Int B

  // Functional reference fold used by the invariant and final contract.
  syntax PluckState ::= pstate(Int, Int, Int, Int)
  syntax PluckState ::= scanPluck(ValSeq, Int, Int, Int, Int)
                        [function, total]
  rule scanPluck(.ValSeq, B:Int, BI:Int, I:Int, LAST:Int)
    => pstate(B, BI, I, LAST)
  rule scanPluck(vCons(V:Val, REST:ValSeq),
                 B:Int, BI:Int, I:Int, _:Int)
    => scanPluck(
         REST,
         nextBest(asInt(V), B),
         nextBestIndex(asInt(V), B, BI, I),
         I +Int 1,
         asInt(V))

  syntax Int ::= stateBest(PluckState) [function, total]
               | stateBestIndex(PluckState) [function, total]
               | stateIndex(PluckState) [function, total]
               | stateLast(PluckState) [function, total]
  rule stateBest(pstate(B:Int, _:Int, _:Int, _:Int)) => B
  rule stateBestIndex(pstate(_:Int, BI:Int, _:Int, _:Int)) => BI
  rule stateIndex(pstate(_:Int, _:Int, I:Int, _:Int)) => I
  rule stateLast(pstate(_:Int, _:Int, _:Int, LAST:Int)) => LAST

  syntax ValSeq ::= pluckResult(ValSeq) [function, total]
  rule pluckResult(VS:ValSeq)
    => .ValSeq
    requires stateBest(scanPluck(VS, -1, -1, 0, 0)) ==Int -1
  rule pluckResult(VS:ValSeq)
    => vCons(
         stateBest(scanPluck(VS, -1, -1, 0, 0)),
         vCons(
           stateBestIndex(scanPluck(VS, -1, -1, 0, 0)),
           .ValSeq))
    requires stateBest(scanPluck(VS, -1, -1, 0, 0)) =/=Int -1

  // The HumanEval precondition: every node is non-negative.
  syntax Bool ::= allNonNegative(ValSeq) [function, total]
  rule allNonNegative(.ValSeq) => true
  rule allNonNegative(vCons(V:Val, REST:ValSeq))
    => isInt(V)
       andBool asInt(V) >=Int 0
       andBool allNonNegative(REST)
endmodule
