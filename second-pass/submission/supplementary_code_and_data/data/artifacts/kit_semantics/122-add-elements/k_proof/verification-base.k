requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // The source contract restricts every list element to Python integers.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool allInts(REST)

  // A totalized projection lets the Haskell backend use the information
  // isInt(V) without changing the represented value.  Every operational use
  // below is guarded by isInt.
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

  // Guarded dispatch twins of the supplied MPY-INT equations.  These do not
  // skip a program construct; they expose the existing Int behavior after
  // the dynamic Val-to-Int sort fact has been established.
  rule applyCmp(OP:String, V:Val, I:Int)
    => applyCmp(OP, projectIntTotal(V), I)
    requires isInt(V) andBool isEqOrdOp(OP)
    [simplification]

  rule applyBin("+", I:Int, V:Val)
    => I +Int projectIntTotal(V)
    requires isInt(V)
    [simplification]

  // Mathematical specification: retain an integer exactly when its absolute
  // decimal representation has at most two digits, i.e. -99 <= I <= 99.
  syntax Int ::= qualifyingValue(Int) [function, total]
  rule qualifyingValue(I:Int)
    => #if I >=Int -99 andBool I <=Int 99 #then I #else 0 #fi
    [simplification]

  syntax Int ::= qualifyingVal(Val) [function, total]
  rule qualifyingVal(V:Val) => qualifyingValue(projectIntTotal(V))
    requires isInt(V)
    [simplification]
  rule qualifyingVal(V:Val) => 0
    requires notBool isInt(V)
    [simplification]

  // Sum the qualifying values in the first N positions.  The equations are
  // total: nonpositive N and an exhausted sequence both contribute zero.
  syntax Int ::= qualifyingPrefix(ValSeq, Int) [function, total]
  rule qualifyingPrefix(_:ValSeq, N:Int) => 0
    requires N <=Int 0
    [simplification]
  rule qualifyingPrefix(.ValSeq, N:Int) => 0
    requires N >Int 0
    [simplification]
  rule qualifyingPrefix(vCons(V:Val, REST:ValSeq), N:Int)
    => qualifyingVal(V) +Int qualifyingPrefix(REST, N -Int 1)
    requires N >Int 0
    [simplification]
endmodule
