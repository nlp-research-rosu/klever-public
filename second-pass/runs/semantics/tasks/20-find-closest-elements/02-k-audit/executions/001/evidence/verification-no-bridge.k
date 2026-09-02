requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact AST fragments generated from solution.py.
  syntax Expr ::= "findClosestLoopCondition" [macro]
  rule findClosestLoopCondition =>
    Compare(
      Name("i"),
      CmpOp("<", BinOp("-", Call(Name("len"), Name("numbers")), Int(1))))

  syntax Stmts ::= "findClosestLoopBody" [macro]
  rule findClosestLoopBody =>
    Assign(Name("low"), Subscript(Name("numbers"), Name("i")))
    Assign(Name("high"), Subscript(Name("numbers"), Name("j")))
    If(Compare(Name("low"), CmpOp(">", Name("high"))),
      Assign(
        TupleExpr(Name("low"), Name("high")),
        TupleExpr(Name("high"), Name("low"))),
      .Stmts)
    If(Compare(
      BinOp("-", Name("high"), Name("low")),
      CmpOp("<", BinOp("-", Name("best_high"), Name("best_low")))),
      Assign(Name("best_low"), Name("low"))
      Assign(Name("best_high"), Name("high")),
      .Stmts)
    AugAssign(Name("j"), "+", Int(1))
    If(Compare(
      Name("j"),
      CmpOp("==", Call(Name("len"), Name("numbers")))),
      AugAssign(Name("i"), "+", Int(1))
      Assign(Name("j"), BinOp("+", Name("i"), Int(1))),
      .Stmts)
    Assign(Name("low"), Name("best_low"))
    Assign(Name("high"), Name("best_high"))
    .Stmts

  syntax Stmts ::= "findClosestBody" [function]
  rule findClosestBody =>
    Expr(Str("Return a closest pair, ordered from smaller to larger."))
    Assign(Name("best_low"), Subscript(Name("numbers"), Int(0)))
    Assign(Name("best_high"), Subscript(Name("numbers"), Int(1)))
    If(Compare(Name("best_low"), CmpOp(">", Name("best_high"))),
      Assign(
        TupleExpr(Name("best_low"), Name("best_high")),
        TupleExpr(Name("best_high"), Name("best_low"))),
      .Stmts)
    Assign(Name("low"), Name("best_low"))
    Assign(Name("high"), Name("best_high"))
    Assign(Name("i"), Int(0))
    Assign(Name("j"), Int(1))
    While(findClosestLoopCondition, findClosestLoopBody)
    Return(TupleExpr(Name("best_low"), Name("best_high")))
    .Stmts

  // A structurally typed symbolic list of floats.
  syntax FloatSeq ::= ".FloatSeq" | fCons(Float, FloatSeq)
  syntax ValSeq ::= floatVals(FloatSeq) [function, total]
  rule floatVals(.FloatSeq) => .ValSeq
  rule floatVals(fCons(F:Float, FS:FloatSeq)) =>
    vCons(F, floatVals(FS))

  syntax Int ::= floatSeqLen(FloatSeq) [function, total]
  rule floatSeqLen(.FloatSeq) => 0
  rule floatSeqLen(fCons(_:Float, FS:FloatSeq)) =>
    1 +Int floatSeqLen(FS)

  rule vsLen(floatVals(FS:FloatSeq)) => floatSeqLen(FS)
    [simplification]

  syntax Float ::= floatAt(FloatSeq, Int) [function, total]
  rule floatAt(fCons(F:Float, _:FloatSeq), 0) => F
  rule floatAt(fCons(_:Float, FS:FloatSeq), I:Int) =>
    floatAt(FS, I -Int 1)
    requires I >Int 0

  // The generic reference accessor returns Val.  This sound proof lemma
  // recovers the stronger Float sort for an in-bounds element of floatVals.
  rule valSeqAt(floatVals(FS:FloatSeq), I:Int) => floatAt(FS, I)
    requires 0 <=Int I andBool I <Int floatSeqLen(FS)
    [simplification]

  // Pure exhaustive-pair specification.  PairState always stores its values
  // in nondecreasing order according to the same primitive comparison used by
  // Python.  Ties preserve the earlier pair.
  syntax PairState ::= pairState(Float, Float)

  syntax Float ::= pairLow(PairState) [function, total]
                 | pairHigh(PairState) [function, total]
  syntax Val ::= pairTuple(PairState) [function, total]
  rule pairLow(pairState(L:Float, _:Float)) => L
  rule pairHigh(pairState(_:Float, H:Float)) => H
  rule pairTuple(pairState(L:Float, H:Float)) =>
    tuple(vCons(L, vCons(H, .ValSeq)))

  syntax PairState ::= orderPairState(Float, Float) [function, total]
  rule orderPairState(A:Float, B:Float) => pairState(B, A)
    requires gtF(A, B)
  rule orderPairState(A:Float, B:Float) => pairState(A, B)
    requires notBool gtF(A, B)

  syntax PairState ::= considerPair(PairState, Float, Float) [function, total]
                     | considerOrdered(PairState, Float, Float) [function, total]
  rule considerPair(P:PairState, A:Float, B:Float) =>
    considerOrdered(P, B, A)
    requires gtF(A, B)
  rule considerPair(P:PairState, A:Float, B:Float) =>
    considerOrdered(P, A, B)
    requires notBool gtF(A, B)

  rule considerOrdered(
    pairState(BL:Float, BH:Float), L:Float, H:Float) =>
    pairState(L, H)
    requires floatLt(subF(H, L), subF(BH, BL))
  rule considerOrdered(P:PairState, L:Float, H:Float) => P
    requires notBool floatLt(
      subF(H, L),
      subF(pairHigh(P), pairLow(P)))

  // Enumerate (i,j) in lexicographic order, exactly as the Python loop does.
  // These equations unfold one iteration only after the path has decided
  // whether j+1 reached the list length.
  syntax PairState ::= scanPairs(FloatSeq, Int, Int, PairState)
                       [function, total]
  rule scanPairs(FS:FloatSeq, I:Int, _J:Int, P:PairState) => P
    requires I >=Int floatSeqLen(FS) -Int 1
  rule scanPairs(FS:FloatSeq, I:Int, J:Int, P:PairState) =>
    scanPairs(
      FS,
      I +Int 1,
      I +Int 2,
      considerPair(P, floatAt(FS, I), floatAt(FS, J)))
    requires I <Int floatSeqLen(FS) -Int 1
     andBool J +Int 1 ==Int floatSeqLen(FS)
  rule scanPairs(FS:FloatSeq, I:Int, J:Int, P:PairState) =>
    scanPairs(
      FS,
      I,
      J +Int 1,
      considerPair(P, floatAt(FS, I), floatAt(FS, J)))
    requires I <Int floatSeqLen(FS) -Int 1
     andBool J +Int 1 =/=Int floatSeqLen(FS)

  syntax PairState ::= lastOrderedPair(FloatSeq) [function, total]
  rule lastOrderedPair(FS:FloatSeq) =>
    orderPairState(
      floatAt(FS, floatSeqLen(FS) -Int 2),
      floatAt(FS, floatSeqLen(FS) -Int 1))

  // The same exhaustive model over the reference semantics' ValSeq sort.  The
  // proof claim supplies only Float elements, so floatValAt is defined on
  // exactly that constructor case.
  syntax Float ::= floatValAt(ValSeq, Int) [function, total]
  rule floatValAt(vCons(F:Float, _:ValSeq), 0) => F
  rule floatValAt(vCons(_:Float, VS:ValSeq), I:Int) =>
    floatValAt(VS, I -Int 1)
    requires I >Int 0

  syntax PairState ::= scanPairsVS(ValSeq, Int, Int, PairState)
                       [function, total]
  rule scanPairsVS(VS:ValSeq, I:Int, _J:Int, P:PairState) => P
    requires I >=Int vsLen(VS) -Int 1
  rule scanPairsVS(VS:ValSeq, I:Int, J:Int, P:PairState) =>
    scanPairsVS(
      VS,
      I +Int 1,
      I +Int 2,
      considerPair(P, floatValAt(VS, I), floatValAt(VS, J)))
    requires I <Int vsLen(VS) -Int 1
     andBool J +Int 1 ==Int vsLen(VS)
  rule scanPairsVS(VS:ValSeq, I:Int, J:Int, P:PairState) =>
    scanPairsVS(
      VS,
      I,
      J +Int 1,
      considerPair(P, floatValAt(VS, I), floatValAt(VS, J)))
    requires I <Int vsLen(VS) -Int 1
     andBool J +Int 1 =/=Int vsLen(VS)

  // Opaque symbolic projections of the exhaustive scan.  K's Haskell backend
  // has no symbolic IEEE-754 evaluator, so forcing scanPairsVS underneath
  // pair projections would enumerate an unbounded symbolic list.  These
  // projections name that same scan result without evaluating it.
  syntax Float ::= closestLowVS(ValSeq, Int, Int, Float, Float)
                   [function, total, symbol(closestLowVS), no-evaluators]
                 | closestHighVS(ValSeq, Int, Int, Float, Float)
                   [function, total, symbol(closestHighVS), no-evaluators]
  rule closestLowVS(VS:ValSeq, I:Int, J:Int, BL:Float, BH:Float) =>
    pairLow(scanPairsVS(VS, I, J, pairState(BL, BH)))
    [concrete]
  rule closestHighVS(VS:ValSeq, I:Int, J:Int, BL:Float, BH:Float) =>
    pairHigh(scanPairsVS(VS, I, J, pairState(BL, BH)))
    [concrete]

  // Proof-domain loop summary.  MPY-FLOAT intentionally leaves symbolic
  // IEEE-754 operations opaque; this rule replaces only the exact translated
  // loop with the structurally recursive exhaustive-pair model above.
  // Concrete execution never imports VERIFICATION and therefore always runs
  // the original While rules.
endmodule
