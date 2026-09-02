requires "reference-semantics/semantics.k"

module PROOF-THEORY
  imports MPY

  // Attribute-complete twin of the frozen isStrV discriminator.  The two
  // equations are exhaustive over Val and exactly duplicate its constructor
  // and owise cases; unlike isStrV, this declaration tells the backend it may
  // soundly split a symbolic result.
  syntax Bool ::= isStringKey(Val) [function, total]
  rule isStringKey(str(_:IntSeq)) => true
  rule isStringKey(_:Val) => false [owise]

  // Derived equation between the frozen partial declaration and the
  // attribute-complete twin.  Both sides have the same exhaustive equations.
  rule isStrV(V:Val) => isStringKey(V) [simplification]

  // Observed only when isStringKey(V) is true.  On that complete domain V is
  // str(CS), so the constructor equation uniquely determines the codes.
  syntax IntSeq ::= stringCodes(Val)
                    [function, total, symbol(stringCodes), no-evaluators]
  rule stringCodes(str(CS:IntSeq)) => CS [simplification]

  syntax Bool ::= lowerKeyCodes(IntSeq) [function, total]
                | upperKeyCodes(IntSeq) [function, total]

  rule lowerKeyCodes(CS:IntSeq)
    => hasLower(CS) andBool notBool hasUpper(CS)
  rule upperKeyCodes(CS:IntSeq)
    => hasUpper(CS) andBool notBool hasLower(CS)

  syntax Bool ::= lowerKey(Val) [function, total]
                | upperKey(Val) [function, total]

  rule lowerKey(V:Val) => lowerKeyCodes(stringCodes(V))
    requires isStringKey(V)
    [simplification]
  rule lowerKey(V:Val) => false
    requires notBool isStringKey(V)
    [simplification]

  rule upperKey(V:Val) => upperKeyCodes(stringCodes(V))
    requires isStringKey(V)
    [simplification]
  rule upperKey(V:Val) => false
    requires notBool isStringKey(V)
    [simplification]

  syntax Bool ::= foldLowerKeys(Bool, ValSeq) [function, total]
                | foldUpperKeys(Bool, ValSeq) [function, total]
                | allLowerKeys(ValSeq)        [function, total]
                | allUpperKeys(ValSeq)        [function, total]
                | hasAnyKey(ValSeq)           [function, total]

  rule foldLowerKeys(AL:Bool, .ValSeq) => AL
  rule foldLowerKeys(AL:Bool, vCons(V:Val, REST:ValSeq))
    => foldLowerKeys(AL andBool lowerKey(V), REST)

  rule foldUpperKeys(AU:Bool, .ValSeq) => AU
  rule foldUpperKeys(AU:Bool, vCons(V:Val, REST:ValSeq))
    => foldUpperKeys(AU andBool upperKey(V), REST)

  rule allLowerKeys(KS:ValSeq) => foldLowerKeys(true, KS)
  rule allUpperKeys(KS:ValSeq) => foldUpperKeys(true, KS)

  rule hasAnyKey(.ValSeq) => false
  rule hasAnyKey(vCons(_:Val, _:ValSeq)) => true

  syntax Bool ::= checkCaseSummary(Bool, Bool, Bool, ValSeq)
                  [function, total]
  rule checkCaseSummary(AL:Bool, AU:Bool, SEEN:Bool, KS:ValSeq)
    => (SEEN orBool hasAnyKey(KS))
       andBool
       (foldLowerKeys(AL, KS) orBool foldUpperKeys(AU, KS))
endmodule
