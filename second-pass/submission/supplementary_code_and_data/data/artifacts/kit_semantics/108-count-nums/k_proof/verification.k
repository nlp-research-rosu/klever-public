requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // Candidate-domain predicate: every element is an integer.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, R:ValSeq))
    => isInt(V) andBool allInts(R)

  // The Haskell backend does not refine V:Val to Int from an isInt(V) path
  // condition.  This guarded total projection is the standard K cast-boundary
  // idiom; it creates no integer value unless the fixed subsort cast is
  // defined.
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

  // Guarded dispatch twins of the supplied Int equations used after list
  // iteration yields a dynamically sorted Val.
  rule applyCmp("<", V:Val, J:Int)
    => projectIntTotal(V) <Int J
    requires isInt(V)
    [simplification]
  rule applyUn("-", V:Val)
    => 0 -Int projectIntTotal(V)
    requires isInt(V)
    [simplification]

  syntax Int ::= magnitude(Int) [function, total]
  rule magnitude(I:Int) => 0 -Int I requires I <Int 0
  rule magnitude(I:Int) => I        requires I >=Int 0

  // A proof-side name for the code sequence returned by the supplied
  // Int2String/strToCodes primitive.  The concrete rule remains in the fixed
  // semantics; this simplification names its already-produced result.
  syntax IntSeq ::= decimalCodes(Int)
    [function, total, no-evaluators]
  rule strToCodes(Int2String(N:Int)) => decimalCodes(N)
    requires N >=Int 0
    [simplification]

  rule applyBuiltin("str", V:Val, .Vals)
    => str(decimalCodes(projectIntTotal(V)))
    requires isInt(V)
     andBool projectIntTotal(V) >=Int 0
    [simplification]

  syntax Bool ::= allDigitCodes(IntSeq) [function, total]
  rule allDigitCodes(.IntSeq) => true
  rule allDigitCodes(iCons(C:Int, R:IntSeq))
    => (48 <=Int C andBool C <=Int 57) andBool allDigitCodes(R)

  // Contract of the fixed Int2String primitive on non-negative integers.
  // This is the only value-level trust boundary in the proof.
  rule allDigitCodes(decimalCodes(N:Int)) => true
    requires N >=Int 0
    [simplification]

  syntax Int ::= codeDigitSum(IntSeq) [function, total]
  rule codeDigitSum(.IntSeq) => 0
  rule codeDigitSum(iCons(C:Int, R:IntSeq))
    => (C -Int 48) +Int codeDigitSum(R)

  // Result of the source loop's "first nonzero digit seen" accumulator.
  syntax Int ::= chooseFirst(Int, IntSeq) [function, total]
  rule chooseFirst(F:Int, .IntSeq) => F
  rule chooseFirst(0, iCons(C:Int, R:IntSeq))
    => chooseFirst(C -Int 48, R)
  rule chooseFirst(F:Int, iCons(_:Int, R:IntSeq))
    => chooseFirst(F, R)
    requires F =/=Int 0
    [simplification]

  syntax Int ::= lastCode(Int, IntSeq) [function, total]
  rule lastCode(C:Int, .IntSeq) => C
  rule lastCode(_:Int, iCons(C:Int, R:IntSeq)) => lastCode(C, R)

  syntax Int ::= signedDigitSum(Int) [function, total]
  rule signedDigitSum(I:Int)
    => codeDigitSum(decimalCodes(magnitude(I)))
       -Int (2 *Int chooseFirst(0, decimalCodes(magnitude(I))))
    requires I <Int 0
  rule signedDigitSum(I:Int)
    => codeDigitSum(decimalCodes(magnitude(I)))
    requires I >=Int 0

  syntax Int ::= countNumsSpec(ValSeq) [function, total]
  rule countNumsSpec(.ValSeq) => 0
  rule countNumsSpec(vCons(V:Val, R:ValSeq))
    => (#if signedDigitSum(projectIntTotal(V)) >Int 0
         #then 1 #else 0 #fi)
       +Int countNumsSpec(R)
    requires isInt(V)
  rule countNumsSpec(vCons(V:Val, R:ValSeq))
    => countNumsSpec(R)
    requires notBool isInt(V)
endmodule
