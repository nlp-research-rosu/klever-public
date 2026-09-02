requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTATION
  imports MPY

  // Auditor mutation: preserve the condition but delete the result.append effect.
  syntax Stmts ::= "commonLoopBody" [macro]
  rule commonLoopBody =>
    If(
      BoolOp(
        "and",
        Compare(Name("item"), CmpOp("in", Name("l2"))),
        Compare(Name("item"), CmpOp("not in", Name("result")))
      ),
      .Stmts,
      .Stmts
    )

  syntax Stmts ::= "commonBody" [macro]
  rule commonBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("item"), Int(0))
    For(Name("item"), Name("l1"), commonLoopBody)
    Return(Call(Name("sorted"), Name("result")))

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

  syntax Val ::= lastAfter(ValSeq, Val) [function, total]
  rule lastAfter(.ValSeq, OLD:Val) => OLD
  rule lastAfter(vCons(V:Val, REST:ValSeq), _:Val) =>
    lastAfter(REST, V)
endmodule
