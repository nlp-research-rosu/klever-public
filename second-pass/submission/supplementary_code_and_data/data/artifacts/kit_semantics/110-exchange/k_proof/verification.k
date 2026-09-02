requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Exact syntax abbreviations for solution.mpy.  These are expanded as
  // macros; they do not replace or shortcut any operational execution.
  syntax Stmts ::= "countBody" [macro]
  rule countBody
    => If(
         Compare(BinOp("%", Name("value"), Int(2)), CmpOp("==", Int(0))),
         AugAssign(Name("even_count"), "+", Int(1)),
         .Stmts)

  syntax Stmts ::= "exchangeBody" [macro]
  rule exchangeBody
    => Expr(Str("Return whether exchanges can make every element of lst1 even."))
       Assign(Name("even_count"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("lst1"), countBody)
       For(Name("value"), Name("lst2"), countBody)
       If(
         Compare(
           Name("even_count"),
           CmpOp(">=", Call(Name("len"), Name("lst1"), .Exprs))),
         Return(Str("YES")),
         .Stmts)
       Return(Str("NO"))

  syntax Module ::= "exchangeProgram" [macro]
  rule exchangeProgram
    => Module(FuncDef(
         "exchange",
         Params("lst1", "lst2"),
         exchangeBody))

  // The reference list iterator exposes its head at the dynamic Val sort.
  // These guarded total projections are the standard defined-cast twins used
  // to recover numeric subsorts without manufacturing values.
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

  syntax Bool ::= definedProjectBool(Val) [function, total]
  rule definedProjectBool(V:Val) => isBool(V)

  syntax Bool ::= projectBoolTotal(Val)
    [function, total, symbol(projectBoolTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Bool)
    => ({ definedProjectBool(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectBoolTotal(V:Val) => {V}:>Bool
    requires definedProjectBool(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Bool => projectBoolTotal(V)
    requires definedProjectBool(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectBoolTotal(B:Bool) => B [simplification]
  rule projectBoolTotal(projectBoolTotal(V:Val)) => projectBoolTotal(V)
    [simplification]

  syntax Bool ::= definedProjectFloat(Val) [function, total]
  rule definedProjectFloat(V:Val) => isFloat(V)

  syntax Float ::= projectFloatTotal(Val)
    [function, total, symbol(projectFloatTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Float)
    => ({ definedProjectFloat(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectFloatTotal(V:Val) => {V}:>Float
    requires definedProjectFloat(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Float => projectFloatTotal(V)
    requires definedProjectFloat(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectFloatTotal(F:Float) => F [simplification]
  rule projectFloatTotal(projectFloatTotal(V:Val)) => projectFloatTotal(V)
    [simplification]

  // Python numeric promotion cases missing from the frozen subset.  They are
  // sort-disjoint from every existing MPY applyBin("%", ...) equation.
  syntax Int ::= boolToInt(Bool) [function, total]
  rule boolToInt(false) => 0
  rule boolToInt(true) => 1

  rule applyBin("%", B:Bool, 2) => pyMod(boolToInt(B), 2)
  rule applyBin("%", F:Float, 2) => floatMod(F, 2.0)
  rule applyCmp("==", F:Float, 0) => eqF(F, 0.0) [priority(40)]

  syntax Bool ::= isNumberVal(Val) [function, total]
  rule isNumberVal(V:Val)
    => definedProjectInt(V)
       orBool definedProjectBool(V)
       orBool definedProjectFloat(V)

  // A recursive domain predicate keeps every dynamic list head in the full
  // numeric domain represented by the reference model.
  syntax Bool ::= allNumbers(ValSeq) [function, total]
  rule allNumbers(.ValSeq) => true
  rule allNumbers(vCons(V:Val, VS:ValSeq))
    => isNumberVal(V) andBool allNumbers(VS)

  // Exact parity predicate for each numeric subsort.  The total projections
  // occur only under their matching definedness conjunct.
  syntax Bool ::= numberEven(Val) [function, total]
  rule numberEven(V:Val)
    => (definedProjectInt(V)
        andBool pyMod(projectIntTotal(V), 2) ==Int 0)
       orBool
       (definedProjectBool(V)
        andBool pyMod(boolToInt(projectBoolTotal(V)), 2) ==Int 0)
       orBool
       (definedProjectFloat(V)
        andBool eqF(floatMod(projectFloatTotal(V), 2.0), 0.0))

  // Mathematical count of even numeric values in a Python value sequence.
  syntax Int ::= evenCount(ValSeq) [function, total]
  rule evenCount(.ValSeq) => 0
  rule evenCount(vCons(V:Val, VS:ValSeq)) => 1 +Int evenCount(VS)
    requires numberEven(V)
    [simplification]
  rule evenCount(vCons(V:Val, VS:ValSeq)) => evenCount(VS)
    requires notBool numberEven(V)
    [simplification]

  // The specified answer: exchanges exist exactly when the combined pool
  // contains at least as many even values as the length of lst1.
  syntax Str ::= exchangeResult(ValSeq, ValSeq) [function, total]
  rule exchangeResult(VS1:ValSeq, VS2:ValSeq) => str(strToCodes("YES"))
    requires evenCount(VS1) +Int evenCount(VS2) >=Int vsLen(VS1)
  rule exchangeResult(VS1:ValSeq, VS2:ValSeq) => str(strToCodes("NO"))
    requires evenCount(VS1) +Int evenCount(VS2) <Int vsLen(VS1)
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Name lookup and both literals have already executed when this pure
  // function-composition term is reached.  Its three numeric connection
  // claims are proved bridge-free in connection-spec.k.
  rule applyCmp("==", applyBin("%", V:Val, 2), 0) => numberEven(V)
    requires isNumberVal(V)
    [simplification]
  rule #Ceil(applyBin("%", V:Val, 2)) => #Top
    requires isNumberVal(V)
    [simplification]
endmodule
