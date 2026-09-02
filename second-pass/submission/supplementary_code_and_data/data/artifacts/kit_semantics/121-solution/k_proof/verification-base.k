requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Exact structural domain predicate for lists whose elements are integers.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool allInts(REST)

  // Guarded total projection, following K's standard partial-cast twin idiom.
  syntax Bool ::= definedProjectInt(Val) [function, total]
  rule definedProjectInt(V:Val) => isInt(V)

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
  rule projectIntTotal(projectIntTotal(V:Val))
    => projectIntTotal(V)
    [simplification]

  // Guarded dynamic-sort twins of the fixed MPY-INT equations.
  rule applyBin("%", V:Val, I:Int)
    => pyMod(projectIntTotal(V), I)
    requires isInt(V)
    [simplification]
  rule applyBin("+", I:Int, V:Val)
    => I +Int projectIntTotal(V)
    requires isInt(V)
    [simplification]

  // Mathematical contribution of one value at a zero-based position.
  syntax Int ::= oddContribution(Int, Int) [function, total]
  rule oddContribution(I:Int, P:Int) => I
    requires pyMod(P, 2) ==Int 0 andBool pyMod(I, 2) =/=Int 0
  rule oddContribution(I:Int, P:Int) => 0
    requires notBool (pyMod(P, 2) ==Int 0 andBool pyMod(I, 2) =/=Int 0)

  // Sum of odd integer elements at even positions, beginning at position P.
  // The non-integer equation totalizes the helper outside the target domain.
  syntax Int ::= oddAtEvenSum(ValSeq, Int) [function, total]
  rule oddAtEvenSum(.ValSeq, _:Int) => 0
  rule oddAtEvenSum(vCons(V:Val, REST:ValSeq), P:Int)
    => oddContribution(projectIntTotal(V), P)
       +Int oddAtEvenSum(REST, P +Int 1)
    requires isInt(V)
  rule oddAtEvenSum(vCons(V:Val, REST:ValSeq), P:Int)
    => oddAtEvenSum(REST, P +Int 1)
    requires notBool isInt(V)

  // Value left in the loop target after consuming a sequence.
  syntax Val ::= lastAfter(ValSeq, Val) [function, total]
  rule lastAfter(.ValSeq, CURRENT:Val) => CURRENT
  rule lastAfter(vCons(V:Val, REST:ValSeq), _:Val)
    => lastAfter(REST, V)
endmodule
