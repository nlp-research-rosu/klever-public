requires "reference-semantics/semantics.k"

module MAX-FILL-SUMMARY
  imports MPY

  // Guarded total projections for the dynamic Val supersort. Their values are
  // used only under the matching sort/constructor guards below.
  syntax Bool ::= definedProjectInt(Val) [function, total]
  rule definedProjectInt(V) => isInt(V)

  syntax Int ::= projectInt(Val)
    [function, total, symbol(maxFillProjectInt), no-evaluators]

  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]
  rule projectInt(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Int => projectInt(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectInt(I:Int) => I [simplification]

  syntax ValSeq ::= rowVals(Val)
    [function, total, symbol(maxFillRowVals), no-evaluators]
  rule rowVals(list(VS)) => VS [simplification]

  syntax Bool ::= isListVal(Val) [function, total]
  rule isListVal(V) => V ==K list(rowVals(V))

  // Domain predicates. allRows permits any finite number and length of rows,
  // but every element must be an integer 0 or 1.
  syntax Bool ::= allBinary(ValSeq) [function, total]
                | allRows(ValSeq)   [function, total]

  rule allBinary(.ValSeq) => true
  rule allBinary(vCons(V, VS))
    => isInt(V)
       andBool (V ==K projectInt(V))
       andBool (projectInt(V) ==Int 0 orBool projectInt(V) ==Int 1)
       andBool allBinary(VS)

  rule allRows(.ValSeq) => true
  rule allRows(vCons(V, VS))
    => isListVal(V) andBool allBinary(rowVals(V)) andBool allRows(VS)

  // Exact value summaries. rowSum deliberately uses MPY-BUILTINS' intOf:
  // on allBinary rows that is exactly the transition performed by #sumAcc.
  syntax Int ::= rowSum(ValSeq)          [function, total]
               | bucketCost(ValSeq, Int) [function, total]
               | gridCost(ValSeq, Int)   [function, total]

  rule rowSum(.ValSeq)       => 0
  rule rowSum(vCons(V, VS))  => intOf(V) +Int rowSum(VS)

  // This is MPY-INT's exact positive-divisor // equation, after the numerator
  // expression in solution.py has evaluated.
  rule bucketCost(VS, C)
    => ((rowSum(VS) +Int C -Int 1)
          -Int pyMod(rowSum(VS) +Int C -Int 1, C)) /Int C
    requires C >Int 0
  rule bucketCost(_VS, C) => 0
    requires C <=Int 0

  rule gridCost(.ValSeq, _C)      => 0
  rule gridCost(vCons(V, VS), C)  => bucketCost(rowVals(V), C) +Int gridCost(VS, C)

  // The for target is initialized before the loop. This helper records the
  // exact value left in it after consuming an arbitrary suffix.
  syntax Val ::= finalRow(ValSeq, Val) [function, total]
  rule finalRow(.ValSeq, PREV)       => PREV
  rule finalRow(vCons(V, VS), _PREV) => finalRow(VS, V)

endmodule

module MAX-FILL-VERIFICATION
  imports MAX-FILL-SUMMARY

  // Guarded static-dispatch twin of MPY-BUILTINS' intOf(I:Int) => I.
  rule intOf(V:Val) => projectInt(V)
    requires isInt(V)
    [simplification]

  // Guarded dispatch twin for the existing MPY-CALL sum rule. isListVal(V)
  // is definitionally V ==K list(rowVals(V)), so the RHS is exactly the fixed
  // rule's #sumAcc(V, 0). No continuation or state cell is changed.
  rule <k> #applyK(toCall(builtinV("sum")), (V:Val, .Vals))
        => #sumAcc(list(rowVals(V)), 0) ... </k>
    requires isListVal(V)
    [priority(40)]
endmodule
