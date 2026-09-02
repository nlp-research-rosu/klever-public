requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL
  imports MAP
  imports LIST

  // A bijective representation of arbitrary finite Python lists of integers.
  syntax ValSeq ::= intVals(IntSeq) [function, total]
  rule intVals(.IntSeq)                => .ValSeq
  rule intVals(iCons(I:Int, R:IntSeq)) => vCons(I, intVals(R))

  // Inert proof ghost used only to keep the symbolic IntSeq name stable when
  // a circularity rematches the extensionally equal embedded heap value.
  syntax Val ::= intSeqGhost(IntSeq)

  // Total mathematical indexing.  Out-of-bounds cases are totalized to zero;
  // the only connection to source indexing below is guarded in-bounds.
  syntax Int ::= intAt(IntSeq, Int) [function, total, no-evaluators]
  rule intAt(.IntSeq, _:Int) => 0
  rule intAt(iCons(I:Int, _:IntSeq), 0) => I
  rule intAt(iCons(_:Int, R:IntSeq), N:Int) => intAt(R, N -Int 1)
    requires N >Int 0
  rule intAt(iCons(_:Int, _:IntSeq), N:Int) => 0
    requires N <Int 0

  // Derived structural equations connecting that representation to the
  // frozen semantics' length and in-bounds indexing functions.
  rule vsLen(intVals(IS:IntSeq)) => isLen(IS) [simplification]
  rule valSeqAt(intVals(IS:IntSeq), I:Int) => intAt(IS, I)
    requires 0 <=Int I andBool I <Int isLen(IS)
    [simplification]

  // The result specification as three nested bounded existentials over
  // strictly increasing indices.
  syntax Bool ::= thirdFrom(IntSeq, Int, Int, Int) [function, total]
                | pairFrom(IntSeq, Int, Int)       [function, total]
                | tripleFrom(IntSeq, Int)          [function, total]

  rule thirdFrom(IS:IntSeq, I:Int, J:Int, K:Int) => false
    requires I <Int 0
      orBool J <=Int I
      orBool K <=Int J
      orBool I >=Int isLen(IS)
      orBool J >=Int isLen(IS)
  rule thirdFrom(IS:IntSeq, I:Int, J:Int, K:Int) => false
    requires 0 <=Int I
      andBool I <Int J
      andBool J <Int K
      andBool J <Int isLen(IS)
      andBool K >=Int isLen(IS)
  rule thirdFrom(IS:IntSeq, I:Int, J:Int, K:Int)
    => ((intAt(IS, I) +Int intAt(IS, J) +Int intAt(IS, K))
          ==Int 0)
       orBool thirdFrom(IS, I, J, K +Int 1)
    requires 0 <=Int I
      andBool I <Int J
      andBool J <Int K
      andBool K <Int isLen(IS)

  rule pairFrom(IS:IntSeq, I:Int, J:Int) => false
    requires I <Int 0
      orBool J <=Int I
      orBool I >=Int isLen(IS)
  rule pairFrom(IS:IntSeq, I:Int, J:Int) => false
    requires 0 <=Int I
      andBool I <Int J
      andBool J >=Int isLen(IS)
  rule pairFrom(IS:IntSeq, I:Int, J:Int)
    => thirdFrom(IS, I, J, J +Int 1)
       orBool pairFrom(IS, I, J +Int 1)
    requires 0 <=Int I
      andBool I <Int J
      andBool J <Int isLen(IS)

  rule tripleFrom(_:IntSeq, I:Int) => false
    requires I <Int 0
  rule tripleFrom(IS:IntSeq, I:Int) => false
    requires I >=Int isLen(IS)
  rule tripleFrom(IS:IntSeq, I:Int)
    => pairFrom(IS, I, I +Int 1)
       orBool tripleFrom(IS, I +Int 1)
    requires 0 <=Int I andBool I <Int isLen(IS)

  // Exact syntax-level abbreviations for the source loop terms and body.
  syntax Expr ::= innerCond()  [function, total]
                | middleCond() [function, total]
                | outerCond()  [function, total]
  syntax Stmts ::= innerBody()   [function, total]
                 | middleBody()  [function, total]
                 | outerBody()   [function, total]
                 | programBody() [function, total]

  rule innerCond() =>
    Compare(
      Name("k"),
      CmpOp("<", Call(Name("len"), (Name("l"), .Exprs))))

  rule innerBody() =>
    If(
      Compare(
        BinOp(
          "+",
          BinOp(
            "+",
            Subscript(Name("l"), Name("i")),
            Subscript(Name("l"), Name("j"))),
          Subscript(Name("l"), Name("k"))),
        CmpOp("==", Int(0))),
      Assign(Name("found"), Bool(true)) .Stmts,
      .Stmts)
    AugAssign(Name("k"), "+", Int(1))
    .Stmts

  rule middleCond() =>
    Compare(
      Name("j"),
      CmpOp("<", Call(Name("len"), (Name("l"), .Exprs))))

  rule middleBody() =>
    Assign(Name("k"), BinOp("+", Name("j"), Int(1)))
    While(innerCond(), innerBody())
    Assign(Name("k"), Int(0))
    AugAssign(Name("j"), "+", Int(1))
    .Stmts

  rule outerCond() =>
    Compare(
      Name("i"),
      CmpOp("<", Call(Name("len"), (Name("l"), .Exprs))))

  rule outerBody() =>
    Assign(Name("j"), BinOp("+", Name("i"), Int(1)))
    While(middleCond(), middleBody())
    Assign(Name("j"), Int(0))
    AugAssign(Name("i"), "+", Int(1))
    .Stmts

  rule programBody() =>
    Assign(Name("found"), Bool(false))
    Assign(Name("i"), Int(0))
    Assign(Name("j"), Int(0))
    Assign(Name("k"), Int(0))
    While(outerCond(), outerBody())
    Return(Name("found"))
    .Stmts

  syntax Val ::= triplesClosure() [function, total]
  rule triplesClosure() =>
    closureVal(("l", .ParamNames), programBody(), 0)

  syntax Map ::= solutionBindings() [function, total]
  rule solutionBindings() =>
    "triples_sum_to_zero" |-> triplesClosure()
endmodule
