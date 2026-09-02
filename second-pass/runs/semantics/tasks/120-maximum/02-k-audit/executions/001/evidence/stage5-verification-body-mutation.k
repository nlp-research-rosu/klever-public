requires "reference-semantics/semantics.k"

module MAXIMUM-VERIFICATION
  imports MPY

  // Reviewer body-sensitivity mutation: the k>0 return is deliberately wrong.
  syntax Stmts ::= "maximumBody" [macro]
  rule maximumBody
    => If(Compare(Name("k"), CmpOp("==", Int(0))),
          Return(ListExpr(.Exprs)) .Stmts,
          .Stmts)
       Return(ListExpr(.Exprs))
       .Stmts

  rule vsLen(sortVS(VS:ValSeq)) => vsLen(VS) [simplification]
endmodule
