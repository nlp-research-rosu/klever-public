requires "reference-semantics/semantics.k"

module MAXIMUM-BODY-MUTATED
  imports MPY

  // Deliberately wrong submitted-body mutation: the positive branch now
  // returns [] instead of sorted(arr)[-k:].
  syntax Stmts ::= "mutatedMaximumBody" [macro]
  rule mutatedMaximumBody
    => If(Compare(Name("k"), CmpOp("==", Int(0))),
          Return(ListExpr(.Exprs)) .Stmts,
          .Stmts)
       Return(ListExpr(.Exprs))
       .Stmts

  rule vsLen(sortVS(VS:ValSeq)) => vsLen(VS) [simplification]
endmodule
