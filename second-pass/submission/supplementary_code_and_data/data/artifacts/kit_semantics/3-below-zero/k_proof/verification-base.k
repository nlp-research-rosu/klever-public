requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool allInts(REST)

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
  rule projectIntTotal(projectIntTotal(V:Val)) => projectIntTotal(V)
    [simplification]

  syntax Bool ::= belowFrom(Int, ValSeq) [function, total]
  rule belowFrom(_:Int, .ValSeq) => false
  rule belowFrom(BALANCE:Int, vCons(V:Val, REST:ValSeq))
    => #if BALANCE +Int projectIntTotal(V) <Int 0
       #then true
       #else belowFrom(BALANCE +Int projectIntTotal(V), REST)
       #fi
    requires isInt(V)
  rule belowFrom(_:Int, vCons(V:Val, _:ValSeq)) => false
    requires notBool isInt(V)

  rule applyBin("+", I:Int, V:Val) => I +Int projectIntTotal(V)
    requires isInt(V)
    [simplification]

  rule ((L:Int |-> _:Scope) STORE:Map)[L <- undef] => STORE
    requires notBool (L in_keys(STORE))
    [simplification]
endmodule
