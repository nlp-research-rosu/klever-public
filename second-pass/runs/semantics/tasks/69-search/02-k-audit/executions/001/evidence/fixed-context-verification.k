requires "reference-semantics/semantics.k"

module FIXED-CONTEXT-VERIFICATION
  imports MPY

  syntax Stmts ::= "#fixedInnerBody" [macro]
  rule #fixedInnerBody
    => If(Compare(Name("item"), CmpOp("==", Name("value"))),
          AugAssign(Name("count"), "+", Int(1)) .Stmts,
          .Stmts) .Stmts

  syntax Stmts ::= "#fixedOuterBody" [macro]
  rule #fixedOuterBody
    => Assign(Name("count"), Int(0))
       For(Name("item"), Name("lst"), #fixedInnerBody)
       If(Compare(Name("count"), CmpOp(">=", Name("value"))),
          If(Compare(Name("value"), CmpOp(">", Name("result"))),
             Assign(Name("result"), Name("value")) .Stmts,
             .Stmts) .Stmts,
          .Stmts) .Stmts
endmodule
