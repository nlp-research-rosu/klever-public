requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  syntax Bool ::= numericVal(Val) [function, total]
  rule numericVal(V:Val)
    => isInt(V) orBool isBool(V) orBool isFloat(V)

  syntax Bool ::= numericSeq(ValSeq) [function, total]
  rule numericSeq(.ValSeq) => true
  rule numericSeq(vCons(V:Val, REST:ValSeq))
    => numericVal(V) andBool numericSeq(REST)

  // Total comparison summary. The first three equations are exactly the
  // corresponding fixed-semantics applyCmp("<", _, Int) cases.
  syntax Bool ::= numericLt(Val, Int) [function, total]
  rule numericLt(I:Int, T:Int)   => I <Int T
  rule numericLt(B:Bool, T:Int)  => boolAsInt(B) <Int T
  rule numericLt(F:Float, T:Int) => ltFI(F, T)
  rule numericLt(_:Val, _:Int)   => false [owise]

  syntax Bool ::= allBelow(ValSeq, Int) [function, total]
  rule allBelow(.ValSeq, _:Int) => true
  rule allBelow(vCons(V:Val, REST:ValSeq), T:Int)
    => numericLt(V, T) andBool allBelow(REST, T)

  // Exact final value of the source-level loop variable. This state summary is
  // needed because MPY represents frame deletion as a symbolic map update.
  syntax Val ::= lastVisited(ValSeq, Val, Int) [function, total]
  rule lastVisited(.ValSeq, OLD:Val, _:Int) => OLD
  rule lastVisited(vCons(V:Val, REST:ValSeq), _:Val, T:Int)
    => #if numericLt(V, T)
       #then lastVisited(REST, V, T)
       #else V
       #fi
endmodule
