requires "reference-semantics/semantics.k"

module STRING-SEQUENCE-DOMAIN
  imports MPY

  // Total projection used only to expose the unique code sequence of a string
  // value.  The default makes every non-string unequal to str(stringCodes(V)).
  syntax IntSeq ::= stringCodes(Val) [function, total]
  rule stringCodes(str(S:IntSeq)) => S
  rule stringCodes(_:Val) => .IntSeq [owise]

  syntax Bool ::= isStringVal(Val) [function, total]
  rule isStringVal(V:Val) => V ==K str(stringCodes(V))

  syntax Bool ::= allStrings(ValSeq) [function, total]
  rule allStrings(.ValSeq) => true
  rule allStrings(vCons(V:Val, REST:ValSeq))
    => isStringVal(V) andBool allStrings(REST)
endmodule
