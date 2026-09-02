requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // Guarded dynamic-to-static Int refinement. The projection has no evaluator
  // outside its guard; on actual Int values it is the identity.
  syntax Bool ::= isIntVal(Val) [function, total]
  rule isIntVal(_:Int) => true
  rule isIntVal(_:Val) => false [owise]

  syntax Bool ::= definedProjectInt(Val) [function, total]
  rule definedProjectInt(V:Val) => isIntVal(V)

  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectIntTotal(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]

  rule {V:Val}:>Int => projectIntTotal(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]

  rule projectIntTotal(I:Int) => I [simplification]
  rule projectIntTotal(projectIntTotal(V:Val)) => projectIntTotal(V)
    [simplification]

  // Guarded dispatch twins of the frozen MPY-INT equations. They do not add
  // behavior: they expose the same integer operations when operands have the
  // dynamic Val sort but the path condition establishes both are Int values.
  rule applyCmp("==", V:Val, W:Val)
    => projectIntTotal(V) ==Int projectIntTotal(W)
    requires isIntVal(V) andBool isIntVal(W)
    [simplification]

  rule applyCmp(">=", V:Val, W:Val)
    => projectIntTotal(V) >=Int projectIntTotal(W)
    requires isIntVal(V) andBool isIntVal(W)
    [simplification]

  rule applyCmp(">", V:Val, W:Val)
    => projectIntTotal(V) >Int projectIntTotal(W)
    requires isIntVal(V) andBool isIntVal(W)
    [simplification]

  rule applyBin("+", V:Val, W:Val)
    => projectIntTotal(V) +Int projectIntTotal(W)
    requires isIntVal(V) andBool isIntVal(W)
    [simplification]

  // The HumanEval precondition: every input element is a positive integer.
  syntax Bool ::= allPositive(ValSeq) [function, total]
  rule allPositive(.ValSeq) => true
  rule allPositive(vCons(V:Val, VS:ValSeq))
    => isIntVal(V)
       andBool projectIntTotal(V) >Int 0
       andBool allPositive(VS)

  // Exact frequency of X in a finite integer sequence.
  syntax Int ::= frequencyOf(Int, ValSeq) [function, total]
  rule frequencyOf(_:Int, .ValSeq) => 0
  rule frequencyOf(X:Int, vCons(V:Val, VS:ValSeq))
    => (#if X ==Int projectIntTotal(V) #then 1 #else 0 #fi)
       +Int frequencyOf(X, VS)
    requires isIntVal(V)
  rule frequencyOf(X:Int, vCons(V:Val, VS:ValSeq))
    => frequencyOf(X, VS)
    requires notBool isIntVal(V)

  // One outer-loop update.
  syntax Int ::= updateAnswer(Int, Int, Int) [function, total]
  rule updateAnswer(A:Int, X:Int, N:Int) => X
    requires N >=Int X andBool X >Int A
  rule updateAnswer(A:Int, X:Int, N:Int) => A
    requires N <Int X
  rule updateAnswer(A:Int, X:Int, N:Int) => A
    requires N >=Int X andBool X <=Int A

  // Exact fold performed by the outer loop over the remaining candidates.
  syntax Int ::= searchSummary(ValSeq, ValSeq, Int) [function, total]
  rule searchSummary(.ValSeq, _:ValSeq, A:Int) => A
  rule searchSummary(
         vCons(V:Val, REST:ValSeq),
         FULL:ValSeq,
         A:Int)
    => searchSummary(
         REST,
         FULL,
         updateAnswer(
           A,
           projectIntTotal(V),
           frequencyOf(projectIntTotal(V), FULL)))
    requires isIntVal(V)
  rule searchSummary(
         vCons(V:Val, REST:ValSeq),
         FULL:ValSeq,
         A:Int)
    => searchSummary(REST, FULL, A)
    requires notBool isIntVal(V)
endmodule
