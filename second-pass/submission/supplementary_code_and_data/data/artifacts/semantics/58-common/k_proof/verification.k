requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The exact translated body of solution.py, factored into named syntax so
  // both the loop invariant and the function-level claim use the same term.
  syntax Stmts ::= "commonLoopBody" [macro]
  rule commonLoopBody =>
    If(
      BoolOp(
        "and",
        Compare(Name("item"), CmpOp("in", Name("l2"))),
        Compare(Name("item"), CmpOp("not in", Name("result")))
      ),
      Expr(Call(Attribute(Name("result"), "append"), Name("item"))),
      .Stmts
    )

  syntax Stmts ::= "commonBody" [macro]
  rule commonBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("item"), Int(0))
    For(Name("item"), Name("l1"), commonLoopBody)
    Return(Call(Name("sorted"), Name("result")))

  syntax Stmt ::= "commonDefinition" [macro]
  rule commonDefinition =>
    FuncDef("common", Params("l1", "l2"), commonBody)

  // Mathematical membership.  spec.k proves separately that this recursive
  // function is exactly the supplied #memberAcc operational fold.
  syntax Bool ::= memberVS(Val, ValSeq) [function, total]
  rule memberVS(_:Val, .ValSeq) => false [simplification]
  rule memberVS(V:Val, vCons(E:Val, _:ValSeq)) => true
    requires V ==K E
    [simplification]
  rule memberVS(V:Val, vCons(E:Val, REST:ValSeq)) =>
    memberVS(V, REST)
    requires notBool (V ==K E)
    [simplification]

  syntax Bool ::= shouldAdd(Val, ValSeq, ValSeq) [function, total]
  rule shouldAdd(V:Val, SECOND:ValSeq, ACC:ValSeq) =>
    memberVS(V, SECOND) andBool notBool memberVS(V, ACC)

  // commonAcc scans FIRST from left to right, retains precisely the elements
  // that occur in SECOND, and suppresses later duplicates using ACC.
  syntax ValSeq ::= commonAcc(ValSeq, ValSeq, ValSeq) [function, total]
  rule commonAcc(.ValSeq, _:ValSeq, ACC:ValSeq) => ACC
  rule commonAcc(vCons(V:Val, REST:ValSeq), SECOND:ValSeq, ACC:ValSeq) =>
    #if shouldAdd(V, SECOND, ACC)
    #then
      commonAcc(
        REST,
        SECOND,
        valSeqConcat(ACC, vCons(V, .ValSeq))
      )
    #else commonAcc(REST, SECOND, ACC)
    #fi

  syntax ValSeq ::= commonSpec(ValSeq, ValSeq) [function, total]
  rule commonSpec(FIRST:ValSeq, SECOND:ValSeq) =>
    commonAcc(FIRST, SECOND, .ValSeq)

  // The loop writes each yielded element to `item`; this helper describes that
  // otherwise irrelevant final local binding and makes the invariant exact.
  syntax Val ::= lastAfter(ValSeq, Val) [function, total]
  rule lastAfter(.ValSeq, OLD:Val) => OLD
  rule lastAfter(vCons(V:Val, REST:ValSeq), _:Val) =>
    lastAfter(REST, V)
endmodule
