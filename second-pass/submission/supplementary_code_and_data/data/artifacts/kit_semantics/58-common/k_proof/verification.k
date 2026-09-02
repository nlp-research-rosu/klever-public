requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical membership for the fixed semantics' flat ValSeq equality.
  syntax Bool ::= commonMember(Val, ValSeq) [function, total]
  rule commonMember(_:Val, .ValSeq) => false
  rule commonMember(V:Val, vCons(E:Val, R:ValSeq))
    => (E ==K V) orBool commonMember(V, R)

  // Boolean normalization needed by the Haskell backend on the unequal path
  // produced by the fixed semantics' list-membership rule.
  rule ((E:Val ==K V:Val) orBool B:Bool) => B
    requires notBool (E ==K V)
    [simplification]

  // The encounter-order, duplicate-free intersection accumulated by the loop.
  syntax ValSeq ::= commonAcc(ValSeq, ValSeq, ValSeq) [function, total]
  rule commonAcc(.ValSeq, _:ValSeq, ACC:ValSeq) => ACC
  rule commonAcc(vCons(V:Val, R:ValSeq), B:ValSeq, ACC:ValSeq)
    => commonAcc(
         R,
         B,
         #if commonMember(V, B) andBool notBool commonMember(V, ACC)
         #then valSeqConcat(ACC, vCons(V, .ValSeq))
         #else ACC
         #fi)

  // Syntactic abbreviations for the exact translated program fragments.
  syntax Stmts ::= "commonLoopBody" "(" ")" [macro]
  rule commonLoopBody()
    => If(
         BoolOp(
           "and",
           Compare(Name("item"), CmpOp("in", Name("l2"))),
           Compare(Name("item"), CmpOp("not in", Name("result")))
         ),
         Expr(Call(Attribute(Name("result"), "append"), Name("item"))),
         .Stmts
       )

  syntax Stmts ::= "commonBody" "(" ")" [macro]
  rule commonBody()
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("item"), Int(0))
       For(Name("item"), Name("l1"), commonLoopBody())
       Return(Call(Name("sorted"), Name("result")))
endmodule
