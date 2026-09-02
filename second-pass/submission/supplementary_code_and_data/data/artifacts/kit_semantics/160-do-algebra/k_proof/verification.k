requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  syntax Bool ::= definedProjectInt(Val) [function, total]
                | definedProjectStr(Val) [function, total]
                | allowedOperator(Val)   [function, total]
                | validAlgebraLists(ValSeq, ValSeq) [function, total]
                | validAlgebraRest(ValSeq, ValSeq, Val) [function, total]

  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]
  syntax Str ::= projectStrTotal(Val)
    [function, total, symbol(projectStrTotal), no-evaluators]

  syntax IntSeq ::= codesOf(Str) [function, total]
                  | codesProject(Val) [function, total]
                  | runPairCodes(IntSeq, ValSeq, ValSeq) [function, total]
  syntax Val ::= lastPairValue(ValSeq, ValSeq) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY

  // Guarded total twins of the built-in partial subsort casts.  They let the
  // symbolic backend retain the value of a dynamically sorted list head once
  // validAlgebraLists has established its concrete Python value class.
  rule definedProjectInt(V:Val) => isInt(V)
  rule definedProjectStr(V:Val) => isStrV(V)

  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]
  rule #Ceil({@V:Val}:>Str)
    => ({ definedProjectStr(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectIntTotal(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Int => projectIntTotal(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectIntTotal(I:Int) => I [simplification]

  rule projectStrTotal(V:Val) => {V}:>Str
    requires definedProjectStr(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Str => projectStrTotal(V)
    requires definedProjectStr(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectStrTotal(S:Str) => S [simplification]

  rule codesOf(str(CS:IntSeq)) => CS
  rule codesProject(V:Val) => codesOf(projectStrTotal(V))

  // These are guarded dispatch twins of fixed MPY rules:
  //   str(I:Int) and str(A) + str(B).
  // They do not add behavior; the projections above connect each dynamic head
  // to the same partial cast selected by the fixed rule's static subsort.
  rule applyBuiltin("str", V:Val, .Vals)
    => str(strToCodes(Int2String(projectIntTotal(V))))
    requires definedProjectInt(V)
    [simplification]

  rule applyBin("+", str(A:IntSeq), V:Val)
    => str(seqConcat(A, codesProject(V)))
    requires definedProjectStr(V)
    [simplification]

  rule allowedOperator(V:Val)
    => V ==K str(iCons(43, .IntSeq))
       orBool V ==K str(iCons(45, .IntSeq))
       orBool V ==K str(iCons(42, .IntSeq))
       orBool V ==K str(iCons(47, iCons(47, .IntSeq)))
       orBool V ==K str(iCons(42, iCons(42, .IntSeq)))

  // The second list is the operator list after solution.py has appended "".
  // Validate the current pair before inspecting the tails; this exposes the
  // dynamic Int/Str guards as soon as #iterNext reveals one pair.
  rule validAlgebraLists(
         vCons(V:Val, NR:ValSeq),
         vCons(W:Val, OR:ValSeq))
    => definedProjectInt(V)
       andBool projectIntTotal(V) >=Int 0
       andBool definedProjectStr(W)
       andBool validAlgebraRest(NR, OR, W)

  rule validAlgebraLists(_:ValSeq, _:ValSeq) => false [owise]

  // The final pair has two empty tails and requires the appended empty string.
  // A non-final pair requires one of the five prompt operators, then recurses.
  rule validAlgebraRest(.ValSeq, OR:ValSeq, W:Val)
    => OR ==K .ValSeq andBool W ==K str(.IntSeq)
  rule validAlgebraRest(
         vCons(V:Val, NR:ValSeq),
         OR:ValSeq,
         CURRENT:Val)
    => allowedOperator(CURRENT)
       andBool validAlgebraLists(
                   vCons(V, NR),
                   OR)
  rule validAlgebraRest(_:ValSeq, _:ValSeq, _:Val) => false [owise]

  // Exact recurrence of expression += str(oprn) + oprt.
  rule runPairCodes(ACC:IntSeq, .ValSeq, _:ValSeq) => ACC
  rule runPairCodes(
         ACC:IntSeq,
         vCons(_:Val, _:ValSeq),
         .ValSeq)
    => ACC
  rule runPairCodes(
         ACC:IntSeq,
         vCons(V:Val, NR:ValSeq),
         vCons(W:Val, OR:ValSeq))
    => runPairCodes(
         seqConcat(
           ACC,
           seqConcat(
             strToCodes(Int2String(projectIntTotal(V))),
             codesProject(W))),
         NR,
         OR)

  rule lastPairValue(
         vCons(V:Val, .ValSeq),
         _:ValSeq)
    => V
  rule lastPairValue(
         vCons(_:Val, NR:ValSeq),
         vCons(_:Val, OR:ValSeq))
    => lastPairValue(NR, OR)
    requires validAlgebraLists(NR, OR)
    [simplification]
  rule lastPairValue(_:ValSeq, _:ValSeq) => noneV [owise]
endmodule
