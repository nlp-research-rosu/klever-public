requires "reference-semantics/semantics.k"

module UNIQUE-VERIFICATION-BODY-MUTATION
  imports MPY

  syntax Bool ::= memberVS(Val, ValSeq) [function, total]
  rule memberVS(_:Val, .ValSeq) => false [simplification]
  rule memberVS(V:Val, vCons(V, _:ValSeq)) => true [simplification]
  rule memberVS(V:Val, vCons(H:Val, T:ValSeq)) => memberVS(V, T)
    requires notBool (V ==K H)
    [simplification]

  syntax ValSeq ::= addUnique(ValSeq, Val) [function, total]
  rule addUnique(ACC:ValSeq, V:Val) => ACC
    requires memberVS(V, ACC)
  rule addUnique(ACC:ValSeq, V:Val)
    => valSeqConcat(ACC, vCons(V, .ValSeq))
    requires notBool memberVS(V, ACC)

  syntax ValSeq ::= uniqueAcc(ValSeq, ValSeq) [function, total]
  rule uniqueAcc(.ValSeq, ACC:ValSeq) => ACC
  rule uniqueAcc(vCons(V:Val, REST:ValSeq), ACC:ValSeq)
    => uniqueAcc(REST, addUnique(ACC, V))

  syntax Val ::= lastItem(ValSeq, Val) [function, total]
  rule lastItem(.ValSeq, OLD:Val) => OLD
  rule lastItem(vCons(V:Val, REST:ValSeq), _:Val)
    => lastItem(REST, V)

  syntax Stmts ::= "uniqueLoopBody" [function, total]
  rule uniqueLoopBody
    => If(
         Compare(Name("item"), CmpOp("not in", Name("result"))),
         Expr(Call(Attribute(Name("result"), "append"), Name("item"))),
         .Stmts)

  // Deliberate material mutation: omit the call to sorted and return the
  // first-seen accumulator object directly.
  syntax Stmts ::= "uniqueBody" [function, total]
  rule uniqueBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("item"), Name("l"), uniqueLoopBody)
       Return(Name("result"))
endmodule
