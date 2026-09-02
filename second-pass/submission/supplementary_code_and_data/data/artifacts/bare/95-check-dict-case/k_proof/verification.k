requires "semantic.k"
requires "program.k"

module VERIFICATION
  imports MPY
  imports SOLUTION-PROGRAM

  // Independent, declarative reading of the prompt.  The implementation is
  // correct exactly when its result agrees with contract(INPUT).
  syntax Bool ::= contract(Value) [function]
                | allStringKeys(Values) [function]
                | allLowerKeys(Values) [function]
                | allUpperKeys(Values) [function]
                | lowerKey(Value) [function, total]
                | upperKey(Value) [function, total]

  rule contract(DictVal()) => false
  rule contract(DictVal(KEYS))
    => allStringKeys(KEYS)
       andBool (allLowerKeys(KEYS) orBool allUpperKeys(KEYS))

  rule allStringKeys(V:Value VS:Values)
    => pyIsString(V) andBool allStringKeys(VS)
  rule allStringKeys(V:Value) => pyIsString(V)

  rule allLowerKeys(V:Value VS:Values)
    => lowerKey(V) andBool allLowerKeys(VS)
  rule allLowerKeys(V:Value) => lowerKey(V)

  rule allUpperKeys(V:Value VS:Values)
    => upperKey(V) andBool allUpperKeys(VS)
  rule allUpperKeys(V:Value) => upperKey(V)

  rule lowerKey(StrVal(S)) => pyIsLower(StrVal(S))
  rule lowerKey(IntVal(_)) => false
  rule lowerKey(BoolVal(_)) => false
  rule lowerKey(DictVal(_)) => false
  rule lowerKey(DictVal()) => false
  rule lowerKey(NoneVal) => false

  rule upperKey(StrVal(S)) => pyIsUpper(StrVal(S))
  rule upperKey(IntVal(_)) => false
  rule upperKey(BoolVal(_)) => false
  rule upperKey(DictVal(_)) => false
  rule upperKey(DictVal()) => false
  rule upperKey(NoneVal) => false
endmodule
