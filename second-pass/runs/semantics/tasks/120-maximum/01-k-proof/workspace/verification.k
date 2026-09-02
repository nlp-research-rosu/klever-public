requires "reference-semantics/semantics.k"

module MAXIMUM-VERIFICATION
  imports MPY

  // The generated body of solution.mpy, named once so the proof claims use
  // exactly the program that concrete execution parses.
  syntax Stmts ::= "maximumBody" [macro]
  rule maximumBody
    => If(Compare(Name("k"), CmpOp("==", Int(0))),
          Return(ListExpr(.Exprs)) .Stmts,
          .Stmts)
       Return(
         Subscript(
           Call(Name("sorted"), Name("arr"), .Exprs),
           Slice(UnaryOp("-", Name("k")), NoBound, NoBound)))
       .Stmts

  // sorted() is the supplied trusted ascending permutation.  Its symbolic
  // constructor is opaque, so expose the one extensional fact needed to
  // normalize Python's negative slice bound.
  rule vsLen(sortVS(VS:ValSeq)) => vsLen(VS) [simplification]
endmodule
