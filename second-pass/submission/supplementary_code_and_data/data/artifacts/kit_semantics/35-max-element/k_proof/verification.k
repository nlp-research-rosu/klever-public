requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // A guarded total twin of Val's partial projection to Int.
  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]
  rule #Ceil({@V:Val}:>Int)
    => ({ isInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]
  rule projectIntTotal(V:Val) => {V}:>Int
    requires isInt(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Int => projectIntTotal(V)
    requires isInt(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectIntTotal(I:Int) => I [simplification]

  // Dispatch twin needed by the symbolic backend.  It restates the equation
  // already enforced by MPY's static Int rule.
  rule applyCmp(">", V:Val, M:Int)
    => projectIntTotal(V) >Int M
    requires isInt(V)
    [simplification]

  // ---- Full fixed-semantics max domain -----------------------------------

  syntax Bool ::= isNumericV(Val) [function, total]
  rule isNumericV(V:Val)
    => isInt(V) orBool isBool(V) orBool isFloat(V)

  syntax Bool ::= allNumericVS(ValSeq) [function, total]
  rule allNumericVS(.ValSeq) => true
  rule allNumericVS(vCons(V:Val, REST:ValSeq))
    => isNumericV(V) andBool allNumericVS(REST)

  syntax Bool ::= allStrVS(ValSeq) [function, total]
  rule allStrVS(.ValSeq) => true
  rule allStrVS(vCons(V:Val, REST:ValSeq))
    => isStr(V) andBool allStrVS(REST)

  // Guarded total projections for the other three orderable value sorts.
  syntax Float ::= projectFloatTotal(Val)
    [function, total, symbol(projectFloatTotal), no-evaluators]
  rule #Ceil({@V:Val}:>Float)
    => ({ isFloat(@V) #Equals true } #And #Ceil(@V))
    [simplification]
  rule projectFloatTotal(V:Val) => {V}:>Float
    requires isFloat(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Float => projectFloatTotal(V)
    requires isFloat(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectFloatTotal(F:Float) => F [simplification]

  // Haskell has no FLOAT.max hook.  Symbolic proofs keep this fixed primitive
  // opaque and thread its Float result; LLVM ground execution still evaluates
  // the real hook through the concrete equation.
  syntax Float ::= maxFOpaque(Float, Float)
    [function, total, symbol(maxFOpaque), no-evaluators]
  rule maxFOpaque(F1:Float, F2:Float) => maxFloat(F1, F2) [concrete]
  rule maxFloat(F1:Float, F2:Float) => maxFOpaque(F1, F2)
    [symbolic(F1, F2), simplification]

  syntax Bool ::= projectBoolTotal(Val)
    [function, total, symbol(projectBoolTotal), no-evaluators]
  rule #Ceil({@V:Val}:>Bool)
    => ({ isBool(@V) #Equals true } #And #Ceil(@V))
    [simplification]
  rule projectBoolTotal(V:Val) => {V}:>Bool
    requires isBool(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Bool => projectBoolTotal(V)
    requires isBool(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectBoolTotal(B:Bool) => B [simplification]

  syntax Str ::= projectStrTotal(Val)
    [function, total, symbol(projectStrTotal), no-evaluators]
  rule #Ceil({@V:Val}:>Str)
    => ({ isStr(@V) #Equals true } #And #Ceil(@V))
    [simplification]
  rule projectStrTotal(V:Val) => {V}:>Str
    requires isStr(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Str => projectStrTotal(V)
    requires isStr(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectStrTotal(S:Str) => S [simplification]

  syntax IntSeq ::= codesOf(Str) [function, total]
  rule codesOf(str(CS:IntSeq)) => CS

  // A total tagged view of Val.  Its four disjoint guards cover every Val;
  // only the first three cases are admitted by allNumericVS.
  syntax NumericView ::= nInt(Int)
                       | nBool(Bool)
                       | nFloat(Float)
                       | nOther(Val)
  syntax NumericView ::= numericView(Val) [function, total]
  rule numericView(V:Val) => nInt(projectIntTotal(V))
    requires isInt(V)
  rule numericView(V:Val) => nBool(projectBoolTotal(V))
    requires isBool(V)
  rule numericView(V:Val) => nFloat(projectFloatTotal(V))
    requires isFloat(V)
  rule numericView(V:Val) => nOther(V)
    requires notBool isNumericV(V)

  // Exhaustive comparison table.  Every numeric equation is the RHS of MPY's
  // existing static applyCmp dispatch for the corresponding pair of sorts.
  syntax Bool ::= numericGt(NumericView, NumericView) [function, total]
  rule numericGt(nInt(I:Int), nInt(J:Int)) => I >Int J
  rule numericGt(nInt(I:Int), nBool(B:Bool))
    => I >Int boolAsInt(B)
  rule numericGt(nBool(B:Bool), nInt(I:Int))
    => boolAsInt(B) >Int I
  rule numericGt(nBool(B1:Bool), nBool(B2:Bool))
    => boolAsInt(B1) >Int boolAsInt(B2)
  rule numericGt(nFloat(F1:Float), nFloat(F2:Float)) => gtF(F1, F2)
  rule numericGt(nInt(I:Int), nFloat(F:Float)) => ltFI(F, I)
  rule numericGt(nFloat(F:Float), nInt(I:Int)) => ltIF(I, F)
  rule numericGt(nBool(B:Bool), nFloat(F:Float))
    => ltFI(F, boolAsInt(B))
  rule numericGt(nFloat(F:Float), nBool(B:Bool))
    => ltIF(boolAsInt(B), F)
  rule numericGt(nOther(_:Val), _:NumericView) => false
  rule numericGt(_:NumericView, nOther(_:Val)) => false

  // Dynamic dispatch twins for the two orderable domains.
  rule applyCmp(">", V:Val, M:Val)
    => numericGt(numericView(V), numericView(M))
    requires isNumericV(V) andBool isNumericV(M)
    [simplification]
  rule applyCmp(">", V:Val, M:Val)
    => strLt(codesOf(projectStrTotal(M)), codesOf(projectStrTotal(V)))
    requires isStr(V) andBool isStr(M)
    [simplification]

  // The three value-sort predicates are mutually exclusive in K even though
  // the symbolic backend does not infer that fact from a Boolean guard.
  rule isFloat(V:Val) orBool isBool(V) => false
    requires isInt(V)
    [simplification]
  rule isInt(V:Val) orBool isBool(V) => false
    requires isFloat(V)
    [simplification]
  rule isInt(V:Val) orBool isFloat(V) => false
    requires isBool(V)
    [simplification]

  // General strict-comparison folds.  They keep the first element on ties,
  // matching MPY's #maxAccV continuation.
  syntax Val ::= maxNumericGeneralVS(Val, ValSeq) [function]
  rule maxNumericGeneralVS(M:Val, .ValSeq) => M
  rule maxNumericGeneralVS(M:Val, vCons(V:Val, REST:ValSeq))
    => maxNumericGeneralVS(
         #if numericGt(numericView(V), numericView(M))
         #then V
         #else M
         #fi,
         REST
       )

  syntax Val ::= maxStrGeneralVS(Val, ValSeq) [function]
  rule maxStrGeneralVS(M:Val, .ValSeq) => M
  rule maxStrGeneralVS(M:Val, vCons(V:Val, REST:ValSeq))
    => maxStrGeneralVS(
         #if strLt(
               codesOf(projectStrTotal(M)),
               codesOf(projectStrTotal(V))
             )
         #then V
         #else M
         #fi,
         REST
       )

  // State-specific summaries mirror MPY's specialized accumulator and the
  // exact point where a mixed numeric value hands execution to #maxAccV.
  syntax Val ::= maxIntNumericVS(Int, ValSeq) [function]
  rule maxIntNumericVS(M:Int, .ValSeq) => M
  rule maxIntNumericVS(M:Int, vCons(V:Val, REST:ValSeq))
    => maxIntNumericVS(maxInt(M, projectIntTotal(V)), REST)
    requires isInt(V)
    [simplification]
  rule maxIntNumericVS(M:Int, vCons(V:Val, REST:ValSeq))
    => maxNumericGeneralVS(M, vCons(V, REST))
    requires isFloat(V) orBool isBool(V)
    [simplification]

  syntax Val ::= maxFloatNumericVS(Float, ValSeq) [function]
  rule maxFloatNumericVS(M:Float, .ValSeq) => M
  rule maxFloatNumericVS(M:Float, vCons(V:Val, REST:ValSeq))
    => maxFloatNumericVS(
         maxFloat(M, projectFloatTotal(V)),
         REST
       )
    requires isFloat(V)
    [simplification]
  rule maxFloatNumericVS(M:Float, vCons(V:Val, REST:ValSeq))
    => maxNumericGeneralVS(M, vCons(V, REST))
    requires isInt(V) orBool isBool(V)
    [simplification]
endmodule
