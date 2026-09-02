requires "reference-semantics/semantics.k"

module SEARCH-FIXED-GHOST
  imports MPY

  syntax Stmts ::= "#innerBody" [macro]
  rule #innerBody
    => If(Compare(Name("item"), CmpOp("==", Name("value"))),
          AugAssign(Name("count"), "+", Int(1)) .Stmts,
          .Stmts) .Stmts

  syntax Stmts ::= "#outerBody" [macro]
  rule #outerBody
    => Assign(Name("count"), Int(0))
       For(Name("item"), Name("lst"), #innerBody)
       If(Compare(Name("count"), CmpOp(">=", Name("value"))),
          If(Compare(Name("value"), CmpOp(">", Name("result"))),
             Assign(Name("result"), Name("value")) .Stmts,
             .Stmts) .Stmts,
          .Stmts) .Stmts

  syntax Stmts ::= "#searchBody" [macro]
  rule #searchBody
    => Assign(Name("result"), UnaryOp("-", Int(1)))
       For(Name("value"), Name("lst"), #outerBody)
       Return(Name("result")) .Stmts

  syntax IntValSeq ::= ".ValSeq" | vCons(Int, IntValSeq)
  syntax ValSeq ::= IntValSeq
  syntax IntValSeq ::= "oneSeq" [macro]
  rule oneSeq => vCons(1, .ValSeq)
endmodule
