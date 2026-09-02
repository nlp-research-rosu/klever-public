requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // The material input domain: every element of the finite ValSeq is a string.
  // Writing the recursion over V:Val exposes the head guard to the prover.
  syntax Bool ::= isStringValue(Val) [function, total]
  rule isStringValue(_:Str) => true
  rule isStringValue(_:Val) => false [owise]

  syntax Bool ::= allStrings(ValSeq) [function, total]
  rule allStrings(.ValSeq) => true
  rule allStrings(vCons(V:Val, REST:ValSeq))
    => isStringValue(V) andBool allStrings(REST)

  // Guarded total projection (the upstream ceils.k pattern). This only
  // restores the static Str sort already guaranteed by isStringValue; it does
  // not manufacture a concrete string or alter execution state.
  syntax Str ::= projectString(Val)
    [function, total, symbol(projectString), no-evaluators]

  rule #Ceil({@V:Val}:>Str)
    => ({ isStringValue(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectString(V:Val) => {V}:>Str
    requires isStringValue(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Str => projectString(V)
    requires isStringValue(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectString(S:Str) => S [simplification]
  rule projectString(projectString(V:Val)) => projectString(V)
    [simplification]

  // Total static-sort twin of the fixed partial Val operation. Its constructor
  // equation is exactly seqLen(str(CS)) => isLen(CS).
  syntax Int ::= seqLenString(Str)
    [function, total, symbol(seqLenString), no-evaluators]
  rule seqLenString(str(CS:IntSeq)) => isLen(CS) [simplification]

  // A left fold with a strict update: equality keeps the earlier accumulator.
  // The fallback equation only totalizes the function outside the allStrings
  // domain and is unreachable from the target claims.
  syntax Val ::= scanLongest(ValSeq, Val) [function, total]
  rule scanLongest(.ValSeq, ACC:Val) => ACC
  rule scanLongest(vCons(V:Val, REST:ValSeq), ACC:Val)
    => scanLongest(
         REST,
         #if isStringValue(V)
               andBool isStringValue(ACC)
               andBool seqLenString(projectString(V))
                 >Int seqLenString(projectString(ACC))
          #then V
          #else ACC
          #fi
       )

  // Contract value: noneV exactly for empty input; otherwise the fold starts
  // at the first element and therefore keeps that element on a length tie.
  syntax Val ::= longestValue(ValSeq) [function, total]
  rule longestValue(.ValSeq) => noneV
  rule longestValue(vCons(V:Val, REST:ValSeq))
    => scanLongest(vCons(V, REST), V)
    requires isStringValue(V)
  rule longestValue(vCons(V:Val, _:ValSeq)) => noneV
    requires notBool isStringValue(V)
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Guarded dynamic-sort dispatch twin. It restates the fixed string-length
  // equation over precisely the values for which the total projection exists.
  rule seqLen(V:Val) => seqLenString(projectString(V))
    requires isStringValue(V)
    [simplification]
endmodule
